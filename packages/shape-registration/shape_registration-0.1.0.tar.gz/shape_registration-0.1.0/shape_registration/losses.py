import math
from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

import torch
from torch.nn import functional as F

try:
    from pytorch_lightning.metrics.functional.reduction import reduce
except ImportError:
    from torchmetrics.utilities.distributed import reduce

from pytorch_lightning.utilities.device_dtype_mixin import \
    DeviceDtypeModuleMixin

from shape_registration.utils import gaussian_kernel


def get_mask(displacement: torch.Tensor) -> torch.Tensor:
    """Computes a mask of points inside the image domain

    Args:
        displacement: the displacement field

    Returns:
        torch.Tensor: mask to be inside the image domain
    """
    mask = (displacement.gt(1).long() + displacement.lt(-1).long()).sum(-1)

    mask = mask == 0

    if not mask.any():
        mask = torch.ones_like(mask)

    return mask


def mean_squared_error(
    warped_image: torch.Tensor,
    fixed_image: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    reduction: str = "elementwise_mean",
) -> torch.Tensor:
    r"""The mean square error loss is a simple and fast to compute point-wise measure
    which is well suited for monomodal image registration.

    .. math::
        \mathcal{S}_{\text{MSE}} := \frac{1}{\vert \mathcal{X} \vert}\sum_{x\in\mathcal{X}}
          \Big(I_M\big(x+f(x)\big) - I_F\big(x\big)\Big)^2
    Args:
        warped_image: the warped moving image
        fixed_image: the fixed target image
        mask: the mask specifying points inside the image domain. Defaults to None.
        reduction: the reduction type. Defaults to "elementwise_mean".

    Returns:
        torch.Tensor: the loss value
    """
    value = (warped_image - fixed_image).pow(2)

    if mask is not None:
        value = torch.masked_select(value, mask)

    return reduce(value, reduction=reduction)


def normalized_cross_correlation(
    warped_image: torch.Tensor,
    fixed_image: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    eps: float = 1e-10,
    reduction: str = "elementwise_mean",
) -> torch.Tensor:
    r"""The normalized cross correlation loss is a measure for image pairs with a linear
    intensity relation.

    .. math::
        \mathcal{S}_{\text{NCC}} := \frac{\sum I_F\cdot (I_M\circ f)
                - \sum\text{E}(I_F)\text{E}(I_M\circ f)}
                {\vert\mathcal{X}\vert\cdot\sum\text{Var}(I_F)\text{Var}(I_M\circ f)}

    Args:
        warped_image: the warped moving image
        fixed_image: the fixed target image
        mask: the mask specifying points inside the image domain. Defaults to None.
        eps: the (small) epsilon to avoid zero division
        reduction: the reduction type. Defaults to "elementwise_mean".

    Returns:
        torch.Tensor: the loss value
    """
    if mask is not None:
        fixed_image = torch.masked_select(fixed_image, mask)
        warped_image = torch.masked_select(warped_image, mask)

    value = (
        -1.0
        * torch.sum(
            (fixed_image - torch.mean(fixed_image))
            * (warped_image - torch.mean(warped_image))
        )
        / torch.sqrt(
            torch.sum((fixed_image - torch.mean(fixed_image)) ** 2)
            * torch.sum((warped_image - torch.mean(warped_image)) ** 2)
            + eps
        )
    )

    return reduce(value, reduction=reduction)


def local_normalized_cross_correlation(
    warped_image: torch.Tensor,
    moving_image: torch.Tensor,
    fixed_image: torch.Tensor,
    kernel: torch.Tensor,
    mask: torch.Tensor,
    eps: float = 1e-10,
    reduction: str = "elementwise_mean",
) -> torch.Tensor:
    """The local normalized cross correlation.

    Args:
        warped_image: the warped moving image
        moving_image: the moving image
        fixed_image: the fixed target image
        kernel: the convolutional kernel
        mask: the mask specifying points inside the image domain. Defaults to None.
        eps: the (small) epsilon to avoid zero division
        reduction: the reduction type. Defaults to "elementwise_mean".

    Returns:
        torch.Tensor: the loss value
    """
    if moving_image.ndim == 2:
        conv_fn = F.conv2d
    elif moving_image.ndim == 3:
        conv_fn = F.conv3d
    else:
        raise ValueError

    mean_moving = conv_fn(warped_image[None, None], kernel)
    variance_moving = conv_fn(warped_image[None, None] ** 2, kernel) - mean_moving ** 2

    mean_fixed = conv_fn(fixed_image[None, None], kernel)
    variance_fixed = conv_fn(fixed_image[None, None] ** 2, kernel) - mean_fixed ** 2

    mean_fixed_moving = conv_fn((fixed_image * warped_image)[None, None], kernel)
    cc = (mean_fixed_moving - mean_moving * mean_fixed) ** 2 / (
        variance_moving * variance_fixed + eps
    )

    if mask is not None:
        mask = conv_fn(mask[None].to(warped_image.dtype), kernel) == 0

        value = torch.masked_select(cc, mask)

    else:
        value = cc

    return -reduce(value, reduction=reduction)


def compute_marginal_entropy(values, bins, sigma, eps: float = 1e-10):
    """Computes the marginal entropy

    Args:
        values: values for marginal entropy
        bins: the bins for the exponential term
        sigma: standard deviation
        eps: the epsilon to avoid zero division. Defaults to 1e-10.

    Returns:
        torch.Tensor: the loss value
    """
    normalizer = math.sqrt(2.0 * math.pi) * sigma

    p = torch.exp(-((values - bins).pow(2).div(sigma))).div(normalizer)
    p_n = p.mean(dim=1)
    p_n = p_n / (torch.sum(p_n) + eps)

    return -(p_n * torch.log2(p_n + eps)).sum(), p


def mutual_information(
    warped_image: torch.Tensor,
    fixed_image: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    bins: int = 64,
    sigma: int = 3,
    spatial_samples: float = 0.1,
    background: Optional[Union[str, int, float]] = None,
):
    r"""Implementation of the Mutual Information image loss.

    .. math::
        \mathcal{S}_{\text{MI}} := H(F, M) - H(F|M) - H(M|F)

    Args:
        warped_image: the warped moving image
        fixed_image: the fixed target image
        mask: mask of pixels inside image domain. Defaults to None.
        bins: number of bins for intensity distribution. Defaults to 64.
        sigma: kernel sigma. Defaults to 3.
        spatial_samples: percentage of pixels. Defaults to 0.1.
        background: how to handle background. Defaults to None.

    Returns:
        torch.Tensor: the loss value
    """
    if mask is not None:
        warped_image = torch.masked_select(warped_image, mask)
        fixed_image = torch.masked_select(fixed_image, mask)

    number_of_pixel = warped_image.numel()

    sample = (
        torch.zeros(
            number_of_pixel, device=fixed_image.device, dtype=fixed_image.dtype
        ).uniform_()
        < spatial_samples
    )

    if background is None:
        background_fixed = torch.min(fixed_image)
        background_warped = torch.min(warped_image)
    elif background == "mean":
        background_fixed = torch.mean(fixed_image)
        background_warped = torch.mean(warped_image)
    else:
        background_fixed = background
        background_warped = background

    max_f = torch.max(fixed_image)
    max_m = torch.max(warped_image)

    if isinstance(background_fixed, torch.Tensor):
        background_fixed = background_fixed.item()

    if isinstance(background_warped, torch.Tensor):
        background_warped = background_warped.item()

    if isinstance(max_f, torch.Tensor):
        max_f = max_f.item()

    if isinstance(max_m, torch.Tensor):
        max_m = max_m.item()

    bins_fixed_image = torch.linspace(
        background_fixed,
        max_f,
        bins,
        device=fixed_image.device,
        dtype=fixed_image.dtype,
    ).unsqueeze(1)

    bins_warped_image = torch.linspace(
        background_warped,
        max_m,
        bins,
        device=fixed_image.device,
        dtype=fixed_image.dtype,
    ).unsqueeze(1)

    # compute marginal entropy fixed image
    image_samples_fixed = torch.masked_select(fixed_image.view(-1), sample)

    ent_fixed_image, p_f = compute_marginal_entropy(
        image_samples_fixed, bins_fixed_image, sigma
    )

    # compute marginal entropy warped image
    image_samples_warped = torch.masked_select(warped_image.view(-1), sample)

    ent_warped_image, p_w = compute_marginal_entropy(
        image_samples_warped, bins_warped_image, sigma
    )

    p_joint = torch.mm(p_f, p_w.transpose(0, 1)).div(2.0 * math.pi * sigma ** 2)
    p_joint = p_joint / (torch.sum(p_joint) + 1e-10)

    ent_joint = -(p_joint * torch.log2(p_joint + 1e-10)).sum()

    return -(ent_fixed_image + ent_warped_image - ent_joint)


def normalized_gradient_fields(
    warped_image: torch.Tensor,
    fixed_image: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    spacing: Optional[torch.Tensor] = None,
    eps: Optional[float] = 1e-5,
    reduction: str = "elementwise_mean",
):

    if spacing is None:
        spacing = [1.0] * warped_image.ndim

    if warped_image.ndim == 2:
        dy_fixed = (fixed_image[..., 1:, 1:] - fixed_image[..., :-1, 1:]) * spacing[0]
        dx_fixed = (fixed_image[..., 1:, 1:] - fixed_image[..., 1:, :-1]) * spacing[1]

        if eps is None:
            with torch.no_grad():
                eps = torch.mean(dy_fixed.abs() + dx_fixed.abs())

        norm_fixed = torch.sqrt(dx_fixed ** 2 + dy_fixed ** 2 + eps ** 2)

        ng_fixed = F.pad(
            torch.stack((dy_fixed, dx_fixed), dim=0).unsqueeze(0) / norm_fixed,
            [0, 1, 0, 1],
        )

        dy_warped = (warped_image[..., 1:, 1:] - warped_image[..., :-1, 1:]) * spacing[
            0
        ]
        dx_warped = (warped_image[..., 1:, 1:] - warped_image[..., 1:, :-1]) * spacing[
            1
        ]

        norm_warped = torch.sqrt(dx_warped ** 2 + dy_warped ** 2 + eps ** 2)

        ng_warped = F.pad(
            torch.stack((dy_warped, dx_warped), dim=0).unsqueeze(0) / norm_warped,
            [0, 1, 0, 1],
        )

    elif warped_image.ndim == 3:
        dz_fixed = (
            fixed_image[..., 1:, 1:, 1:] - fixed_image[..., :-1, 1:, 1:]
        ) * spacing[0]
        dy_fixed = (
            fixed_image[..., 1:, 1:, 1:] - fixed_image[..., 1:, :-1, 1:]
        ) * spacing[1]
        dx_fixed = (
            fixed_image[..., 1:, 1:, 1:] - fixed_image[..., 1:, 1:, :-1]
        ) * spacing[2]

        if eps is None:
            with torch.no_grad():
                eps = torch.mean(dz_fixed.abs() + dy_fixed().abs() + dx_fixed.abs())

        norm_fixed = torch.sqrt(
            dx_fixed ** 2 + dy_fixed ** 2 + dz_fixed ** 2 + eps ** 2
        )

        ng_fixed = F.pad(
            torch.stack((dz_fixed, dy_fixed, dx_fixed), dim=0).unsqueeze(0)
            / norm_fixed,
            [0, 1, 0, 1, 0, 1],
        )

        dz_warped = (
            warped_image[..., 1:, 1:, 1:] - warped_image[..., :-1, 1:, 1:]
        ) * spacing[0]
        dy_warped = (
            warped_image[..., 1:, 1:, 1:] - warped_image[..., 1:, :-1, 1:]
        ) * spacing[1]
        dx_warped = (
            warped_image[..., 1:, 1:, 1:] - warped_image[..., 1:, 1:, :-1]
        ) * spacing[2]

        norm_warped = torch.sqrt(
            dx_warped ** 2 + dy_warped ** 2 + dz_warped ** 2 + eps ** 2
        )

        ng_warped = F.pad(
            torch.stack((dz_warped, dy_warped, dx_warped), dim=0).unsqueeze(0)
            / norm_warped,
            [0, 1, 0, 1, 0, 1],
        )

    else:
        raise ValueError

    value = (ng_warped * ng_fixed).sum(1)

    value = -(value ** 2)

    if mask is not None:
        value = torch.masked_select(value, mask)

    return reduce(value, reduction=reduction)


def structual_similarity(
    warped_image: torch.Tensor,
    fixed_image: torch.Tensor,
    kernel: torch.Tensor,
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 1.0,
    c1: float = 1e-5,
    c2: float = 1e-5,
    c3: float = 1e-5,
    mask: Optional[torch.Tensor] = None,
    reduction: str = "elementwise_mean",
):

    if warped_image.ndim == 2:
        conv_fn = F.conv2d
    elif warped_image.ndim == 3:
        conv_fn = F.conv3d
    else:
        raise ValueError

    if mask is not None:
        mask = ~mask

        mask = mask.to(warped_image.dtype)

        mask = conv_fn(mask[None], kernel)
        mask = mask == 0

    mean_warped_image = conv_fn(warped_image[None, None], kernel)

    variance_warped_image = conv_fn(warped_image.pow(2)[None, None], kernel) - (
        mean_warped_image.pow(2)
    )

    mean_fixed_image = conv_fn(fixed_image[None, None], kernel)

    variance_fixed_image = conv_fn(fixed_image.pow(2)[None, None], kernel) - (
        mean_fixed_image.pow(2)
    )

    mean_fixed_moving_image = conv_fn((fixed_image * warped_image)[None, None], kernel)

    covariance_fixed_moving = (
        mean_fixed_moving_image - mean_warped_image * mean_fixed_image
    )

    luminance = (2 * mean_fixed_image * mean_warped_image + c1) / (
        mean_fixed_image.pow(2) + mean_warped_image.pow(2) + c1
    )

    contrast = (
        2
        * torch.sqrt(variance_fixed_image + 1e-10)
        * torch.sqrt(variance_warped_image + 1e-10)
        + c2
    ) / (variance_fixed_image + variance_warped_image + c2)

    structure = (covariance_fixed_moving + c3) / (
        torch.sqrt(variance_fixed_image + 1e-10)
        * torch.sqrt(variance_warped_image + 1e-10)
        + c3
    )

    sim = luminance.pow(alpha) * contrast.pow(beta) * structure.pow(gamma)

    if mask is not None:
        value = torch.masked_select(sim, mask)
    else:
        value = sim

    value = -value

    return reduce(value, reduction=reduction)


class AbstractRegistrationLoss(DeviceDtypeModuleMixin, torch.nn.Module, ABC):
    @abstractmethod
    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:
        raise NotImplementedError


class MeanSquaredError(AbstractRegistrationLoss):
    def __init__(self, reduction: str = "elementwise_mean") -> None:
        super().__init__()

        self.reduction = reduction

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:
        mask = get_mask(displacement=displacement)
        return mean_squared_error(
            warped_image=warped_image,
            fixed_image=fixed_image,
            mask=mask,
            reduction=self.reduction,
        )


class NormalizedCrossCorrelation(AbstractRegistrationLoss):
    def __init__(self, reduction: str = "elementwise_mean", eps: float = 1e-10) -> None:
        super().__init__()

        self.reduction = reduction
        self.eps = eps

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:
        mask = get_mask(displacement=displacement)

        return normalized_cross_correlation(
            warped_image=warped_image,
            fixed_image=fixed_image,
            mask=mask,
            eps=self.eps,
            reduction=self.reduction,
        )


class LocalNormalizedCrossCorrelation(AbstractRegistrationLoss):
    def __init__(
        self,
        dim: int,
        kernel_type: str = "box",
        sigma: Union[int, Sequence] = 3,
        reduction: str = "elementwise_mean",
        eps: float = 1e-10,
    ) -> None:
        super().__init__()

        self.reduction = reduction
        self.eps = eps

        if not isinstance(sigma, Sequence):
            sigma = [sigma] * dim

        if len(sigma) != dim:
            raise AssertionError
        sigma = torch.tensor(sigma)

        if kernel_type == "box":
            kernel_size = sigma * 2 + 1
            kernel = torch.ones(
                *kernel_size.tolist(), dtype=self.dtype, device=self.device
            ) / float((torch.prod(kernel_size) ** 2).item())

        elif kernel_type == "gaussian":
            kernel = gaussian_kernel(sigma=sigma, dim=dim, device=self.device)

        else:
            raise ValueError

        self.register_buffer("kernel", kernel[None, None])

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:
        mask = get_mask(displacement=displacement)

        return local_normalized_cross_correlation(
            warped_image=warped_image,
            moving_image=moving_image,
            fixed_image=fixed_image,
            kernel=self.kernel,
            mask=mask,
            eps=self.eps,
            reduction=self.reduction,
        )


class MutualInformation(AbstractRegistrationLoss):
    def __init__(
        self,
        bins: int = 64,
        sigma: int = 3,
        spatial_samples: float = 0.1,
        background: Optional[Union[str, int, float]] = None,
    ):
        super().__init__()

        self.bins = bins
        self.sigma = sigma
        self.spatial_samples = spatial_samples
        self.background = background

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:

        mask = get_mask(displacement)

        return mutual_information(
            warped_image=warped_image,
            fixed_image=fixed_image,
            mask=mask,
            bins=self.bins,
            sigma=self.sigma,
            spatial_samples=self.spatial_samples,
            background=self.background,
        )


class NormalizedGradientFields(AbstractRegistrationLoss):
    def __init__(
        self,
        spacing: Optional[torch.Tensor] = None,
        eps: Optional[float] = 1e-5,
        reduction: str = "elementwise_mean",
    ) -> None:
        super().__init__()

        self.spacing = spacing
        self.eps = eps
        self.reduction = reduction

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:

        mask = get_mask(displacement=displacement)

        return normalized_gradient_fields(
            warped_image=warped_image,
            fixed_image=fixed_image,
            mask=mask,
            spacing=self.spacing,
            eps=self.eps,
            reduction=self.reduction,
        )


class StructualSimilarity(AbstractRegistrationLoss):
    def __init__(
        self,
        dim: int,
        kernel_type: str = "box",
        sigma: Union[Sequence, int] = 3,
        alpha: float = 1.0,
        beta: float = 1.0,
        gamma: float = 1.0,
        c1: float = 1e-5,
        c2: float = 1e-5,
        c3: float = 1e-5,
        reduction: str = "elementwise_mean",
    ) -> None:
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.reduction = reduction

        if not isinstance(sigma, Sequence):
            sigma = [sigma] * dim

        if len(sigma) != dim:
            raise AssertionError
        sigma = torch.tensor(sigma)

        if kernel_type == "box":
            kernel_size = sigma * 2 + 1
            kernel = torch.ones(
                *kernel_size.tolist(), dtype=self.dtype, device=self.device
            ) / float((torch.prod(kernel_size) ** 2).item())

        elif kernel_type == "gaussian":
            kernel = gaussian_kernel(sigma=sigma, dim=dim, device=self.device)

        else:
            raise ValueError

        self.register_buffer("kernel", kernel[None, None])

    def forward(
        self,
        warped_image: torch.Tensor,
        moving_image: torch.Tensor,
        fixed_image: torch.Tensor,
        displacement: torch.Tensor,
    ) -> torch.Tensor:
        mask = get_mask(displacement=displacement)

        return structual_similarity(
            warped_image=warped_image,
            fixed_image=fixed_image,
            kernel=self.kernel,
            alpha=self.alpha,
            beta=self.beta,
            gamma=self.gamma,
            c1=self.c1,
            c2=self.c2,
            c3=self.c3,
            mask=mask,
            reduction=self.reduction,
        )
