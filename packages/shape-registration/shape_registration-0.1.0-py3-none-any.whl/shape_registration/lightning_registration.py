from copy import deepcopy
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple, Union

import pytorch_lightning as pl
import torch
from torch.nn import functional as F
from torch.nn.modules import loss
from torch.optim.optimizer import Optimizer
from torch.utils.data.dataloader import DataLoader

from shape_registration.losses import MeanSquaredError
from shape_registration.regularizer import GaussianRegularizer
from shape_registration.transformation import (
    AffineTransformation,
    DiffermorphicDemonTransformation,
    Transformation
)
from shape_registration.utils import convolution, gaussian_kernel


class LightningRegistration(pl.LightningModule):
    transform: Transformation

    def __init__(
        self,
        transform_type: str,
        loss_fn: Optional[Callable] = None,
        shrink_factors: Union[int, Sequence[int], Sequence[Sequence[int]]] = (),
        sigmas: Optional[Union[int, Sequence[int], Sequence[Sequence[int]]]] = 2,
        num_iters: Union[int, Sequence[int]] = 100,
        lr: Union[float, Sequence[float]] = 1e-1,
        displacement_upsampling: str = "linear",
        previous_transform: Optional[Transformation] = None,
        metrics: Optional[Union[Mapping, Sequence, pl.metrics.Metric]] = None,
        transform_kwargs: Optional[dict] = None,
        **kwargs
    ):
        super().__init__()
        self.save_hyperparameters()

        self.metrics = torch.nn.ModuleDict(metrics)

        if loss_fn is None:
            loss_fn = MeanSquaredError()

        if transform_kwargs is None:
            transform_kwargs = {}

        self.regularizer: Optional[GaussianRegularizer] = None
        self._pseudo_dataset: torch.utils.data.Dataset

        self._current_resolution_stage = None

        # don't register them as buffers to alwauys keep them on cpu
        self._orig_fixed = None
        self._orig_moving = None
        self._previous_displacement = None

        if isinstance(shrink_factors, Sequence):
            num_resolution_levels = len(shrink_factors)
        elif isinstance(sigmas, Sequence):
            num_resolution_levels = len(sigmas)
        elif isinstance(num_iters, Sequence):
            num_resolution_levels = len(num_iters)
        else:
            num_resolution_levels = 1

        self._num_resolution_levels = num_resolution_levels

        if isinstance(shrink_factors, int):
            shrink_factors = [shrink_factors] * self._num_resolution_levels

        if len(shrink_factors) != self._num_resolution_levels:
            raise AssertionError

        if isinstance(sigmas, int):
            sigmas = [sigmas] * self._num_resolution_levels

        if not (sigmas is None or len(sigmas) == self._num_resolution_levels):
            raise AssertionError

        if sigmas is not None and transform_type != 'diffeomorphic_demons':
            raise ValueError('sigmas for regularization are only supported for diffeomorphic demons!')

        if isinstance(num_iters, int):
            num_iters = [num_iters] * self._num_resolution_levels

        if len(num_iters) != self._num_resolution_levels:
            raise AssertionError

        if isinstance(lr, float):
            lr = [lr] * self._num_resolution_levels

        if len(lr) != self._num_resolution_levels:
            raise AssertionError

        self._transformation_type: str = transform_type
        self.loss_fn: Callable = loss_fn
        self._shrink_factors: Sequence[int] = shrink_factors
        self._sigmas: Sequence[int] = sigmas
        self._num_iters: Sequence[int] = num_iters
        self._lr: Sequence[float] = lr
        self._displacement_upsampling: str = displacement_upsampling
        self._transform_kwargs = transform_kwargs
        self.transform = previous_transform

    def training_step(self, batch: Any, batch_idx: int) -> Any:
        moving_image, fixed_image = batch["data"], batch["label"]

        result = self.transform(moving_image)

        loss = self.loss_fn(
            warped_image=result,
            moving_image=moving_image,
            fixed_image=fixed_image,
            displacement=self.transform.compute_complete_transform_displacement() + self.transform.grid,
        )

        for k, v in self.metrics.items():
            self.log(
                k, v(result, fixed_image), on_step=True, on_epoch=False, prog_bar=True
            )

        return loss

    def on_before_zero_grad(self, optimizer: Optimizer) -> None:
        if self.global_step > 1 and self.regularizer is not None:
            self.regularizer(self.transform.parameters())
        return super().on_before_zero_grad(optimizer)

    def prepare_next_resolution(self):
        if self._current_resolution_stage is None:
            self._current_resolution_stage = 0
        else:
            self._current_resolution_stage += 1

        curr_moving, curr_fixed = self.build_resolution_images(
            moving_image=self._orig_moving,
            fixed_image=self._orig_fixed,
            resolution_index=self._current_resolution_stage,
        )

        self._pseudo_dataset = PseudoRegistrationDataset(
            moving=curr_moving,
            fixed=curr_fixed,
            length=self._num_iters[self._current_resolution_stage],
        )

        # if hasattr(self, 'transform'):
        # self.transform.to('cpu')
        # del self.transform
        torch.cuda.empty_cache()

        transformation = self.create_transformation(
            moving_image=curr_moving, fixed_image=curr_fixed
        )

        regularizer = None

        if self._sigmas is not None:
            regularizer = GaussianRegularizer(
                self._sigmas[self._current_resolution_stage], dim=curr_moving.ndim - 1
            )

        self.learning_rate = self._lr[self._current_resolution_stage]

        self.regularizer = regularizer
        self.transform = transformation
        # reset optimizers, must do it like this to ensure types are correct
        self.trainer.accelerator.setup_optimizers(self.trainer)
        self.transform.to(self.device, self.dtype)

        if self.regularizer is not None:
            self.regularizer.to(self.device, self.dtype)

    def build_resolution_images(
        self,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        resolution_index: int,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """resamples the images for the current stage of the resolution pyramid

        Args:
            moving_image: the moving image before resampling
            fixed_image: the fixed image before resampling
            resolution_index: the index of the current resolution stage

        Raises:
            ValueError: Invalid dimensionality

        Returns:
            torch.Tensor: the resampled moving image
            torch.Tensor: the resampled fixed image
        """
        level = torch.tensor(
            self._shrink_factors[resolution_index],
            device="cpu",
            dtype=self.dtype,
        )

        sigma = level / 2

        kernel = gaussian_kernel(sigma, dim=moving_image.ndim - 1)

        padding = (
            ((torch.tensor(kernel.size(), dtype=torch.float, device="cpu") - 1) / 2)
            .to(torch.int)
            .tolist()
        )
        kernel = kernel.unsqueeze(0).unsqueeze(0)
        kernel = kernel.repeat(
            moving_image.size(0), moving_image.size(0), *([1] * (moving_image.ndim - 1))
        )
        kernel = kernel.to(dtype=self.dtype)

        

        level_list = level.long().tolist()

        new_moving = convolution(
            moving_image[None],
            kernel,
            stride=level_list,
            padding=padding,
        )[0]
        new_fixed = convolution(
            fixed_image[None],
            kernel,
            stride=level_list,
            padding=padding,
        )[0]

        return new_moving, new_fixed

    def create_transformation(
        self, moving_image: torch.Tensor, fixed_image: torch.Tensor
    ) -> Transformation:
        """Creates the transformation for the current resolution level

        Args:
            moving_image: the moving image of the current resolution stage
            fixed_image: the fixed image of the current resolution stage

        Raises:
            ValueError: invalid transformation type

        Returns:
            Transformation: the created transformation for the current resolution level
        """
        # TODO: make the transformation type an independent value for each resolution
        if self._transformation_type == "affine":
            transformation_cls = AffineTransformation
        elif self._transformation_type == "diffeomorphic_demons":
            transformation_cls = DiffermorphicDemonTransformation
        else:
            raise ValueError

        transformation_kwargs = deepcopy(self._transform_kwargs)

        return transformation_cls(
            fixed_image.shape[1:],
            previous_trafo=self.transform,
            **transformation_kwargs
        )

    @torch.no_grad()
    def predict(self, x: torch.Tensor, *args, **kwargs) -> torch.Tensor:
        return self(x)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.transform(x)

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self._pseudo_dataset, batch_size=1, pin_memory=torch.cuda.is_available()
        )

    def setup(self, stage) -> None:
        
        self.prepare_next_resolution()
        return super().setup(stage=stage)

    def on_epoch_end(self) -> None:

        # don't do it in last epoch
        if self.current_epoch < self._num_resolution_levels - 1:
            self.trainer._lightning_optimizers = None
            self.prepare_next_resolution()

        return super().on_epoch_end()

    def fit(self, moving_image: torch.Tensor, fixed_image: torch.Tensor, **kwargs):
        self._orig_moving = moving_image.cpu()
        self._orig_fixed = fixed_image.cpu()

        kwargs["max_epochs"] = self._num_resolution_levels
        kwargs["checkpoint_callback"] = kwargs.get("checkpoint_callback", False)
        kwargs["logger"] = kwargs.get("logger", None)

        if self.trainer is None:
            trainer = pl.Trainer(reload_dataloaders_every_epoch=True, **kwargs)
            trainer.fit(self)
        else:
            self.trainer.fit(self)

        self._orig_moving = None
        self._orig_fixed = None

        return self

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)


class PseudoRegistrationDataset(torch.utils.data.Dataset):
    def __init__(self, moving: torch.Tensor, fixed: torch.Tensor, length: int):
        super().__init__()
        self.moving = moving
        self.fixed = fixed
        self.length = length

    def __getitem__(self, index):
        return {"data": self.moving, "label": self.fixed}

    def __len__(self):
        return self.length
