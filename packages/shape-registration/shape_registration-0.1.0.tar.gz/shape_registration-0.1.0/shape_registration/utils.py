import math
from typing import Optional, Sequence, Union
import torch
from torch.nn import functional as F
from scipy.spatial.distance import dice as dice_dissimilarity

# TODO: Also check for duplicated code (separate utils package?)

__all__ = [
    "gaussian_kernel",
    "interpolate_displacement",
    "create_grid_2d",
    "create_grid_3d",
    "create_grid",
]

def gaussian_kernel(
    sigma: Union[torch.Tensor, int, Sequence],
    dim: Optional[int] = None,
    device: Optional[Union[str, torch.device]] = None,
    kernel_size: Optional[int] = None
):
    """creates a Nd gaussian

    Args:
        sigma: the std
        dim: the dimensionality. If not given, try to determine it by sigma. Defaults to None.
        device: the device. Defaults to None.

    Returns:
        torch.Tensor: Nd gaussian kernel
    """
    if dim is None and isinstance(sigma, Sequence) and len(sigma) > 1:
        dim = len(sigma)

    if isinstance(sigma, Sequence):
        sigma = torch.tensor(sigma, device=device)

    if isinstance(sigma, int):
        sigma = torch.tensor([sigma] * dim, device=device)

    if isinstance(sigma, torch.Tensor) and sigma.numel() == 1:
        sigma = sigma.view((1,)).repeat(dim)

    if kernel_size is None:
        kernel_size = (2 * torch.ceil(sigma.float() / 2) + 1).long()
    if isinstance(kernel_size, int):
        kernel_size = [kernel_size] * dim


    # The gaussian kernel is the product of the
    # gaussian function of each dimension.
    kernel = 1
    meshgrids = torch.meshgrid(
        [
            torch.arange(size, dtype=torch.float32)
            for size in kernel_size
        ]
    )
    for size, std, mgrid in zip(kernel_size, sigma, meshgrids):
        mean = (size - 1) / 2
        kernel *= 1 / (std * math.sqrt(2 * math.pi)) * \
                    torch.exp(-((mgrid - mean) / std) ** 2 / 2)

    # Make sure sum of values in gaussian kernel equals 1.
    kernel = kernel / torch.sum(kernel)

    return kernel.to(device)

def convolution(input: torch.Tensor, kernel: torch.Tensor, **kwargs):
    if kernel.ndim == 4:
        return F.conv2d(input, kernel, **kwargs)
    elif kernel.ndim == 5:
        return F.conv3d(input, kernel, **kwargs)
    raise NotImplementedError("Kernel dimensionality not supported")


def interpolate_displacement(
    displacement: torch.Tensor, new_size: Sequence, interpolation: str = "linear"
) -> torch.Tensor:
    """interpolates the displacement field to fit for a new target size

    Args:
        displacement: the displacement field to interpolate
        new_size: the new image size
        interpolation: the interpolation type. Defaults to "linear".

    Returns:
        torch.Tensor: the interpolated displacement field
    """
    dim = displacement.size(-1)
    if dim == 2:
        displacement = displacement.permute(0, 3, 1, 2)
        if interpolation == "linear":
            interpolation = "bilinear"
        else:
            interpolation = "nearest"
    elif dim == 3:
        displacement = displacement.permute(0, 4, 1, 2, 3)
        if interpolation == "linear":
            interpolation = "trilinear"
        else:
            interpolation = "nearest"

    interpolated_displacement = F.interpolate(
        displacement, size=new_size, mode=interpolation, align_corners=False
    )

    if dim == 2:
        interpolated_displacement = interpolated_displacement.permute(0, 2, 3, 1)
    elif dim == 3:
        interpolated_displacement = interpolated_displacement.permute(0, 2, 3, 4, 1)

    return interpolated_displacement


def create_grid_2d(
    image_size: Sequence,
    dtype: Optional[Union[str, torch.dtype]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> torch.Tensor:
    """creates a 2d grid for a certain image size

    Args:
        image_size: the size of the target image
        dtype: the dtype of the resulting grid. Defaults to None.
        device: [the device the resulting grid should lie on. Defaults to None.

    Returns:
        torch.Tensor: the created grid
    """
    nx = image_size[0]
    ny = image_size[1]

    x = torch.linspace(-1, 1, steps=ny, dtype=dtype, device=device)
    y = torch.linspace(-1, 1, steps=nx, dtype=dtype, device=device)

    x = x.expand(nx, -1)
    y = y.expand(ny, -1).transpose(0, 1)

    x.unsqueeze_(0).unsqueeze_(3)
    y.unsqueeze_(0).unsqueeze_(3)

    return torch.cat((x, y), 3).to(dtype=dtype, device=device)


def create_grid_3d(
    image_size: Sequence,
    dtype: Optional[Union[str, torch.dtype]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> torch.Tensor:
    """creates a 3d grid for a certain image size

    Args:
        image_size: the size of the target image
        dtype: the dtype of the resulting grid. Defaults to None.
        device: [the device the resulting grid should lie on. Defaults to None.

    Returns:
        torch.Tensor: the created grid
    """
    nz = image_size[0]
    ny = image_size[1]
    nx = image_size[2]

    x = torch.linspace(-1, 1, steps=nx, dtype=dtype, device=device)
    y = torch.linspace(-1, 1, steps=ny, dtype=dtype, device=device)
    z = torch.linspace(-1, 1, steps=nz, dtype=dtype, device=device)

    x = x.expand(ny, -1).expand(nz, -1, -1)
    y = y.expand(nx, -1).expand(nz, -1, -1).transpose(1, 2)
    z = z.expand(nx, -1).transpose(0, 1).expand(ny, -1, -1).transpose(0, 1)

    x.unsqueeze_(0).unsqueeze_(4)
    y.unsqueeze_(0).unsqueeze_(4)
    z.unsqueeze_(0).unsqueeze_(4)
    return torch.cat((x, y, z), 4).to(dtype=dtype, device=device)


def create_grid(
    image_size: Sequence,
    dtype: Optional[Union[str, torch.dtype]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> torch.Tensor:
    """creates a Nd grid for a certain image size

    Args:
        image_size: the size of the target image
        dtype: the dtype of the resulting grid. Defaults to None.
        device: [the device the resulting grid should lie on. Defaults to None.

    Raises:
        ValueError: Invalid dimensionality

    Returns:
        torch.Tensor: the created grid
    """
    dim = len(image_size)

    if dim == 2:
        return create_grid_2d(image_size=image_size, dtype=dtype, device=device)

    if dim == 3:
        return create_grid_3d(image_size=image_size, dtype=dtype, device=device)
    raise ValueError("Error " + str(dim) + " is not a valid grid type")


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / torch.norm(vector)


def angle_between(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'::

    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return torch.acos(torch.clamp(torch.dot(v1_u, v2_u), -1.0, 1.0))


def tri_angle_between(pt1, pt2, pt3):
    return angle_between(pt1 - pt2, pt3 - pt2)

def normalize_points(points: torch.Tensor, img_size: torch.Tensor):
    assert len(img_size) == points.size(-1)

    img_size = img_size.view(*([1] * (points.ndim -1)), points.size(-1))
    return points * 2.0 / img_size - 1


def denormalize_points(points: torch.Tensor, img_size: torch.Tensor):
    img_size = img_size.view(*([1] * (points.ndim -1)), points.size(-1))
    return (points + 1) * img_size / 2.0

def dice_similarity(img1: torch.Tensor, img2: torch.Tensor) -> torch.Tensor:
    img1_npy = img1.detach().cpu().numpy()
    img2_npy = img2.detach().cpu().numpy()

    return torch.tensor(
        1 - dice_dissimilarity(img1_npy.reshape(-1), img2_npy.reshape(-1)),
        device=img1.device,
    )

class Dice(torch.nn.Module):
    @staticmethod
    def forward(*args, **kwargs):
        return dice_similarity(*args, **kwargs)

def snap_to_contour(points, mask: torch.Tensor):
    from scipy.ndimage.morphology import binary_erosion

    mask = mask.squeeze()

    eroded_mask = torch.from_numpy(binary_erosion(mask.detach().cpu().numpy(), iterations=1)).to(mask)
    contour = mask - eroded_mask
    contour_points = contour.nonzero()
    
    distances = (contour_points.unsqueeze(0) - points.unsqueeze(1)).pow(2).sum(-1)

    arg_mins = torch.argmin(distances, dim=1)
    return contour_points[arg_mins]
    