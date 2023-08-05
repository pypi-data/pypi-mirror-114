
from typing import Optional, Sequence, Union

import torch
from pytorch_lightning.utilities.device_dtype_mixin import DeviceDtypeModuleMixin
from rising.transforms.functional.affine import parametrize_matrix

from torch.nn import functional as F

from shape_registration.utils import (
    convolution,
    create_grid,
    interpolate_displacement,
    normalize_points,
)
from shape_registration.delaunay import (
    interpolate_normalized_point as interpolate_normalized_point_delaunay,
)


__all__ = [
    "Transformation",
    "AffineTransformation",
    "SimilarityTransformation",
    "RigidTransformation",
]


class Transformation(DeviceDtypeModuleMixin, torch.nn.Module):
    """Class representing arbitrary transformations."""

    def __init__(
        self,
        image_size: Sequence,
        previous_trafo: Optional[Union[torch.Tensor, "Transformation"]] = None,
        interpolation: str = "bilinear",
    ):
        """

        Args:
            image_size: the size of the target image
            previous_trafo: the previous transformation.
                If given it will always be added to the current transformation. Defaults to None.
        """
        super().__init__()

        while image_size[0] == 1:
            image_size = image_size[1:]

        image_size = [
            i.item() if isinstance(i, torch.Tensor) else i for i in image_size
        ]

        self.dim = len(image_size)
        self.register_buffer("image_size", torch.tensor(image_size))
        self.register_buffer(
            "grid", create_grid(self.image_size, dtype=self.dtype, device=self.device)
        )

        if isinstance(previous_trafo, Transformation):
            self.previous_trafo = previous_trafo
            self.previous_trafo.adapt_to_size(self.image_size)

        elif isinstance(previous_trafo, torch.Tensor):
            previous_trafo = previous_trafo.detach()

            # resample previous transform if necessary
            if previous_trafo.shape[1:-1] != image_size:
                previous_trafo = interpolate_displacement(
                    previous_trafo, new_size=image_size
                )
            self.register_buffer("previous_trafo", previous_trafo)
        else:
            self.previous_trafo = None

        self.interpolation = interpolation

    def outside_mask(self, moving: torch.Tensor) -> torch.Tensor:
        """returns a mask specifying which pixels are transformed outside the image domain

        Args:
            moving: the moving image

        Returns:
            torch.Tensor: the mask
        """
        mask = torch.zeros_like(self.image_size, dtype=torch.uint8, device=self.device)

        # exclude points which are transformed outside the image domain
        for dim in range(self.displacement.size()[-1]):
            mask += self.displacement[..., dim].gt(1) + self.displacement[..., dim].lt(
                -1
            )

        mask = mask == 0

        return mask

    def compute_displacement(self) -> torch.Tensor:
        """Returns the displacement flow of the current transform

        Returns:
            torch.Tensor: the displacement flow
        """
        return torch.zeros_like(self.grid)

    def forward(self, moving_image: torch.Tensor) -> torch.Tensor:
        """Applies the current transform to the given image

        Args:
            moving_image: the image to transform

        Returns:
            torch.Tensor: the transformed image
        """

        while moving_image.ndim < self.dim + 2:
            moving_image = moving_image.unsqueeze(0)

        displacement = self.compute_complete_transform_displacement() + self.grid

        warped_moving = F.grid_sample(
            moving_image,
            displacement.repeat(moving_image.size(0), *([1] * (self.dim + 1))),
            mode=self.interpolation,
        )

        # for _ in range(added_dims):
        #     warped_moving = warped_moving.squeeze(0)
        return warped_moving

    def compute_complete_transform_displacement(self) -> torch.Tensor:
        """Computes the complete displacement field (including the previous transform)

        Returns:
            torch.Tensor: the complete displacement field
        """
        displacement = self.compute_displacement()
        if self.previous_trafo is not None:
            if isinstance(self.previous_trafo, torch.Tensor):
                previous_trafo = self.previous_trafo
            else:
                previous_trafo = (
                    self.previous_trafo.compute_complete_transform_displacement()
                )

            displacement = previous_trafo + displacement

        return displacement

    def adapt_to_size(self, image_size: Sequence):
        """Adapts the transformation to the given image size

        Args:
            image_size: the new image size
        """
        self.image_size = torch.tensor(image_size)
        self.grid = create_grid(self.image_size, dtype=self.dtype, device=self.device)
        if isinstance(self.previous_trafo, torch.Tensor):
            self.previous_trafo = interpolate_displacement(
                self.previous_trafo,
                new_size=[
                    i.item() if isinstance(i, torch.Tensor) else i for i in image_size
                ],
            )
        elif isinstance(self.previous_trafo, Transformation):
            self.previous_trafo.adapt_to_size(image_size)

    def __add__(self, other):
        if isinstance(other, Transformation):
            other_image_size = other.image_size.tolist()
            other_displacement = other.compute_complete_transform_displacement()
        elif isinstance(other, torch.Tensor):
            other_image_size = other.shape[2:-1]
            other_displacement = other
        elif other is None:
            return self
        else:
            raise NotImplementedError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

        own_image_size = self.image_size.tolist()
        own_displacement = self.compute_complete_transform_displacement()
        max_size = [max(a, b) for a, b in zip(own_image_size, other_image_size)]

        if max_size != list(other_image_size):
            other_displacement = interpolate_displacement(
                other_displacement, new_size=max_size
            )

        if max_size != own_image_size:
            own_displacement = interpolate_displacement(
                own_displacement, new_size=max_size
            )

        return Transformation(
            image_size=max_size, previous_trafo=own_displacement + other_displacement
        )

    def __radd__(self, other):
        return self + other

    # TODO: Add code for delaunay-based point trafo

class AffineTransformation(Transformation):
    """Affine transformation"""

    def __init__(
        self,
        image_size: Sequence,
        previous_trafo: Optional[Transformation] = None,
        interpolation: str = "bilinear",
    ):
        """

        Args:
            image_size: the size of the target image
            previous_trafo: the previous transformation.
                If given it will always be added to the current transformation. Defaults to None.
        """

        if isinstance(previous_trafo, AffineTransformation):
            scale = previous_trafo.scale
            translation = previous_trafo.translation
            rotation = previous_trafo.rotation

            previous_trafo = None
        else:
            scale = None
            translation = None
            rotation = None
        super().__init__(
            image_size=image_size,
            previous_trafo=previous_trafo,
            interpolation=interpolation,
        )

        if scale is None:
            scale = torch.ones(self.dim, device=self.device, dtype=self.dtype)

        if translation is None:
            translation = torch.zeros(self.dim, device=self.device, dtype=self.dtype)

        if rotation is None:
            rotation = torch.zeros(self.dim, device=self.device, dtype=self.dtype)

        self.scale = torch.nn.Parameter(
            scale.to(device=self.device, dtype=self.dtype), requires_grad=True
        )
        self.translation = torch.nn.Parameter(
            translation.to(device=self.device, dtype=self.dtype), requires_grad=True
        )
        self.rotation = torch.nn.Parameter(
            rotation.to(device=self.device, dtype=self.dtype), requires_grad=True
        )

    def build_affine(self):
        """returns the affine transformation as a matrix"""
        return parametrize_matrix(
            scale=self.scale,
            rotation=self.rotation,
            translation=self.translation,
            batchsize=1,
            ndim=self.dim,
            device=self.device,
            dtype=self.dtype,
        )

    def compute_displacement(self) -> torch.Tensor:
        """Returns the displacement flow of the current transform

        Returns:
            torch.Tensor: the displacement flow
        """
        return (
            F.affine_grid(self.build_affine(), size=(1, 1, *self.image_size))
            - self.grid
        )

class DiffermorphicDemonTransformation(Transformation):
    """Diffeomorphic Demons"""

    def __init__(
        self,
        image_size: Sequence,
        scaling: Optional[int] = None,
        previous_trafo: Optional[Transformation] = None,
        interpolation: str = "bilinear",
    ):
        """

        Args:
            image_size: the size of the target image
            scaling: number of scaling iterations. Defaults to None.
            previous_trafo: the previous transformation.
                If given it will always be added to the current transformation. Defaults to None.
        """
        super().__init__(
            image_size=image_size,
            previous_trafo=previous_trafo,
            interpolation=interpolation,
        )

        self.scaling = scaling
        self.init_scaling = 8
        self.displacement_field = torch.nn.Parameter(
            torch.zeros(self.dim, *self.image_size)
        )

    def adapt_to_size(self, image_size: Sequence):
        super().adapt_to_size(image_size)
        self.displacement_field = torch.nn.Parameter(
            interpolate_displacement(
                self.displacement_field.permute(*range(1, self.dim + 1), 0)[None],
                new_size=[
                    i.item() if isinstance(i, torch.Tensor) else i for i in image_size
                ],
            )[0].permute(-1, *range(self.dim))
        )

    def forward(self, *args, **kwargs):

        return super().forward(*args, **kwargs)

    def compute_scaling(self, displacement: torch.Tensor) -> int:
        """If scaling is not provided, it will be derived from the displacement field norm

        Args:
            displacement: the displacement field

        Returns:
            int: the scaling value
        """
        with torch.no_grad():
            scaling = self.init_scaling

            norm = torch.norm(displacement / (2 ** scaling))

            while norm > 0.5:
                scaling += 1
                norm = torch.norm(displacement / (2 ** scaling))

            return scaling

    def diffeomorphic_2d(self, displacement: torch.Tensor) -> torch.Tensor:
        """Compute displacement field in 2d

        Args:
            displacement: the current displacement

        Returns:
            torch.Tensor: the resulting displacement field
        """
        if self.scaling is None:
            scaling = self.compute_scaling(displacement)

        else:
            scaling = self.scaling

        displacement = displacement / (2 ** scaling)

        displacement = displacement.unsqueeze(0)

        for i in range(scaling):
            # channels last
            displacement = displacement + F.grid_sample(
                displacement, displacement.permute(0, 2, 3, 1) + self.grid
            )

        # channels front
        return displacement.permute(0, 2, 3, 1)

    def diffeomorphic_3d(self, displacement: torch.Tensor) -> torch.Tensor:
        """Compute displacement field in 3d

        Args:
            displacement: the current displacement

        Returns:
            torch.Tensor: the resulting displacement field
        """
        if self.scaling is None:
            scaling = self.compute_scaling(displacement)

        else:
            scaling = self.scaling

        displacement = displacement / (2 ** scaling)
        displacement = displacement.unsqueeze(0)

        for i in range(scaling):
            # channels last
            displacement = displacement + F.grid_sample(
                displacement, displacement.permute(0, 2, 3, 4, 1) + self.grid
            )

        # channels front
        return displacement.permute(0, 2, 3, 4, 1)

    def diffeomorphic(self, displacement_field: torch.Tensor):
        if self.dim == 2:
            # channels last
            return self.diffeomorphic_2d(displacement_field)
        if self.dim == 3:
            # channels last
            return self.diffeomorphic_3d(displacement_field)
        raise ValueError

    def compute_displacement(self) -> torch.Tensor:
        """Computes the transform's displacement field

        Raises:
            ValueError: invalid dimensionality

        Returns:
            torch.Tensor: the displacement field
        """
        displacement = self.displacement_field
        return self.diffeomorphic(displacement)