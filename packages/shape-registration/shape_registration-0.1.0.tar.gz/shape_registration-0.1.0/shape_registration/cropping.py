# TODO: Duplicated here for current separation of code
from typing import Optional, Tuple, Union

import torch
from torch.nn import functional as F


def extract_nonzero_bounding_box(
    tensor: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:

    # create empty ranges
    ranges = torch.zeros(
        tensor.size(0),
        tensor.ndim - 2,
        dtype=torch.long,
        device=tensor.device,
    )
    # create empty centers
    centers = torch.zeros(
        tensor.size(0),
        tensor.ndim - 2,
        dtype=torch.long,
        device=tensor.device,
    )
    for idx, _tensor in enumerate(tensor):
        bounds = torch.tensor(
            [(tmp.min(), tmp.max()) for tmp in _tensor.nonzero(as_tuple=True)],
            device=tensor.device,
        )
        # ensure this is an even number
        ranges[idx, :] = (
            torch.ceil((bounds[:, 1] - bounds[:, 0]).float() / 2) * 2
        ).long()[
            1:
        ]  # extract max range of all channels
        centers[idx, :] = bounds[1:, 0] + ranges[idx] // 2

    return centers, ranges


def crop_to_bounding_box(
    tensor: torch.Tensor,
    centers: torch.Tensor,
    ranges: torch.Tensor,
    additional_tensor: Optional[torch.Tensor] = None,
    **padding_kwargs
) -> Union[Tuple[torch.Tensor, torch.Tensor], torch.Tensor]:
    max_range = ranges.max(0)[0]
    out = torch.zeros(
        tensor.size(0),
        tensor.size(1),
        *max_range.tolist(),
        device=tensor.device,
        dtype=tensor.dtype,
    )

    if additional_tensor is not None:
        additional_out = torch.zeros(
            additional_tensor.size(0),
            additional_tensor.size(1),
            *max_range.tolist(),
            device=additional_tensor.device,
            dtype=additional_tensor.dtype,
        )

    # calciulate the absolute minimum range
    abs_min_range = (centers - max_range / 2.0).min(0)[0]

    # calculate padding on the first side per dim
    first_paddings = torch.where(
        abs_min_range < 0, abs_min_range.abs(), torch.zeros_like(abs_min_range)
    )

    # calculate padding on the last side per dim
    last_paddings = torch.clamp(
        (centers + max_range / 2.0).max(0)[0]
        - torch.tensor(tensor.shape[2:], device=centers.device, dtype=centers.dtype),
        0,
    )

    # combine paddings
    total_paddings = []

    for idx in range(len(first_paddings)):
        total_paddings += [first_paddings[idx], last_paddings[idx]]

    total_paddings = torch.stack(total_paddings).long().tolist()

    # add padding offset to centers
    centers = centers + first_paddings[None]

    # pad tensor
    tensor = F.pad(tensor, total_paddings, **padding_kwargs)

    # pad additional tensor if given
    if additional_tensor is not None:
        additional_tensor = F.pad(additional_tensor, total_paddings, **padding_kwargs)

    # re-assign tensors
    for idx in range(out.size(0)):
        mins = (centers[idx] - max_range / 2.0).long()
        maxs = (centers[idx] + max_range / 2.0).long()
        if len(mins) == 2:
            out[idx] = tensor[idx][..., mins[0] : maxs[0], mins[1] : maxs[1]]
            if additional_tensor is not None:
                additional_out[idx] = additional_tensor[idx][
                    ..., mins[0] : maxs[0], mins[1] : maxs[1]
                ]
        elif len(mins) == 3:
            out[idx] = tensor[idx][
                ..., mins[0] : maxs[0], mins[1] : maxs[1], mins[2] : maxs[2]
            ]
            if additional_tensor is not None:
                additional_out[idx] = additional_tensor[idx][
                    ..., mins[0] : maxs[0], mins[1] : maxs[1], mins[2] : maxs[2]
                ]
    # remove channel dim for mask_out if mask had no channel dim
    if additional_tensor is not None and additional_tensor.ndim == tensor.ndim - 1:
        additional_out = additional_out[:, 0]

    if additional_tensor is None:
        return out
    return out, additional_out


def crop_to_nonzero(
    tensor: torch.Tensor,
    additional_tensor: Optional[torch.Tensor] = None,
    **padding_kwargs
) -> Union[Tuple[torch.Tensor, torch.Tensor], torch.Tensor]:
    """
    crops tensor to non-zero and additional tensor to the same part of the
    tensor if given
    Args:
        tensor: the tensor to crop
        additional_tensor: an additional tensor to crop to the same region
            as :attr`tensor`
        **padding_kwargs: keyword arguments to controll the necessary padding
    Returns:
        torch.Tensor: the cropped tensor
        Optional[torch.Tensor]: the cropped additional tensor,
            only returned if passed
    """
    centers, ranges = extract_nonzero_bounding_box(tensor)

    return crop_to_bounding_box(
        tensor,
        centers=centers,
        ranges=ranges,
        additional_tensor=additional_tensor,
        **padding_kwargs,
    )

