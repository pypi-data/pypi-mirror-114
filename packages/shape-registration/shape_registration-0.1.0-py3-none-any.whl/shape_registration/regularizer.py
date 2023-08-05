from typing import Iterable, Optional, Sequence, Union

import torch
from torch.nn import functional as F

from shape_registration.utils import gaussian_kernel

__all__ = ["GaussianRegularizer"]


class GaussianRegularizer(torch.nn.Module):
    """Gaussian Regularizer"""

    def __init__(
        self, sigma: Union[torch.Tensor, int, Sequence], dim: Optional[int] = None
    ):
        """

        Args:
            sigma: std values for building the gaussian kernel
            dim: the kernel dimensionality. If not given, will try to estimate it. Defaults to None.

        Raises:
            ValueError: Invalid kernel dimensionality
        """
        super().__init__()

        if dim is None and isinstance(sigma, Sequence) and len(sigma) > 1:
            dim = len(sigma)

        if dim is None:
            raise AssertionError
        if isinstance(sigma, int) or len(sigma) != len(sigma):
            sigma = [sigma] * dim

        self.register_buffer("kernel", gaussian_kernel(sigma, dim))
        self.kernel = self.kernel[None, None]

        self.kernel = self.kernel.expand(
            dim, *(torch.ones(dim + 1, dtype=torch.int, device="cpu") * -1).tolist()
        )

        if dim == 1:
            self.conv_fn = F.conv1d
        elif dim == 2:
            self.conv_fn = F.conv2d
        elif dim == 3:
            self.conv_fn = F.conv3d
        else:
            raise ValueError

        self.padding = (
            (
                (
                    torch.tensor(self.kernel.shape[2:], dtype=torch.float, device="cpu")
                    - 1
                )
                / 2
            )
            .to(torch.int)
            .tolist()
        )
        self.dim = dim

    def forward(self, parameters: Iterable[torch.Tensor]):
        """The actual regularization

        Args:
            parameters: the parameters to regularize
        """
        with torch.no_grad():
            for param in parameters:
                param = self.conv_fn(
                    param[None], self.kernel, padding=self.padding, groups=self.dim
                ).squeeze()
