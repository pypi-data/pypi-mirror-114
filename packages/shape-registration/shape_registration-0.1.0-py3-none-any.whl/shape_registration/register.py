from functools import partial
from shape_registration.cropping import (
    crop_to_bounding_box,
    extract_nonzero_bounding_box,
)
from shape_registration.transformation import (
    AffineTransformation,
    DiffermorphicDemonTransformation,
    Transformation,
)
from typing import Callable, Optional
from shape_registration.lightning_registration import LightningRegistration
import torch
from shape_registration.utils import Dice, denormalize_points, snap_to_contour


__all__ = [
    "transfer_points_on_segmentations",
    "register_affine",
    "register_diffeomorphic",
]


def _register(
    source_image,
    target_image,
    is_mask,
    gpus,
    verbose: bool,
    return_metrics,
    **registration_kwargs
):
    metrics = {}

    if is_mask:
        metrics["dice"] = Dice()
    else:
        metrics["l1"] = torch.nn.L1Loss()

    reg_kwargs = {"metrics": metrics}
    reg_kwargs.update(registration_kwargs)

    task = LightningRegistration(**reg_kwargs)
    if gpus is None:
        if torch.cuda.is_available():
            gpus = torch.cuda.device_count()

    task.fit(
        source_image,
        target_image,
        gpus=gpus,
        precision=16 + 16 * (1 - int(bool(gpus))),
        weights_summary=None,
        progress_bar_refresh_rate=None if verbose else 0,
    )

    if return_metrics:
        return task.transform, task.trainer.callback_metrics
    return task.transform


def register_affine(
    source_image: torch.Tensor,
    target_image: torch.Tensor,
    is_mask: bool = True,
    gpus: Optional[int] = None,
    verbose: bool = True,
    return_metrics: bool = False,
    **registration_kwargs
) -> AffineTransformation:
    """
    Register a dataset using an affine transform.

    Args:
        source_image: the source image (Cx(D)xHxW)
        target_image: the target image (Cx(D)xHxW)
        is_mask: whether the images are masks
        gpus: the number of gpus to use, if None, will use all available
        verbose: whether to print progress
        return_metrics: whether to return metrics
        registration_kwargs: the keyword arguments for the registration function

    Returns:
        the registration transform
    """
    affine_reg_kwargs = {
        "transform_type": "affine",
        "shrink_factors": [8, 4, 2, 1],
        "num_iters": [100, 50, 25, 10],
        "sigmas": None,
        "lr": [1e-1, 1e-2, 1e-2, 1e-2],
    }

    affine_reg_kwargs.update(registration_kwargs)
    return _register(
        source_image,
        target_image,
        is_mask,
        gpus,
        verbose,
        return_metrics,
        **affine_reg_kwargs
    )


def register_diffeomorphic(
    source_image: torch.Tensor,
    target_image: torch.Tensor,
    is_mask: bool = True,
    gpus: Optional[int] = None,
    verbose: bool = True,
    return_metrics: bool = False,
    **registration_kwargs
) -> DiffermorphicDemonTransformation:
    """
    Register a dataset using a diffeomorphic demons transform.

    Args:
        source_image: the source image (Cx(D)xHxW)
        target_image: the target image (Cx(D)xHxW)
        is_mask: whether the images are masks
        gpus: the number of gpus to use, if None, will use all available
        verbose: whether to print progress
        return_metrics: whether to return metrics
        registration_kwargs: the keyword arguments for the registration function

    Returns:
        the registration transform
    """
    diffeomorphic_reg_kwargs = {
        "transform_type": "diffeomorphic_demons",
        "shrink_factors": [4, 2, 1],
        "num_iters": [50, 50, 25],
        "sigmas": 2,
        "lr": [1e-1, 1e-2, 1e-2],
    }

    diffeomorphic_reg_kwargs.update(registration_kwargs)

    return _register(
        source_image,
        target_image,
        is_mask,
        gpus,
        verbose,
        return_metrics,
        **diffeomorphic_reg_kwargs
    )


def transfer_points_on_segmentations(
    source_points: torch.Tensor,
    source_image: torch.Tensor,
    target_image: torch.Tensor,
    include_preregistration: bool = True,
    crop_to_segmentation: bool = True,
    crop_boundary_proportion: float = 0.1,
    contour_snap: bool = False,
    prereg_fn: Optional[Callable[[torch.Tensor, torch.Tensor], Transformation]] = None,
    reg_fn: Optional[Callable[[torch.Tensor, torch.Tensor], Transformation]] = None,
    verbose: bool = False,
    gpus: Optional[int] = None,
    return_trafo: bool = False,
) -> torch.Tensor:
    """
    Transfer points from one image to another.

    Args:
        source_points: the points to transfer ((Z,)Y,X)
        source_image: the source image (Cx(D)xHxW)
        target_image: the target image (Cx(D)xHxW)
        include_preregistration: whether to include the (affine) pre-registration
        crop_to_segmentation: whether to crop to the actual segmentation (crops away only background)
        crop_boundary_proportion: the proportion of the boundary to crop
        contour_snap: whether to snap the transferred points to the closest contour point of the target image
        prereg_fn: a function to determine a pre-registration transform (typically affine)
        reg_fn: a function to determine a registration transform (typically diffeomorphic demons)
        verbose: whether to print progress

    Returns:
        the transferred points
    """
    # crop to segmentation since registration may collapse if to much background included
    if crop_to_segmentation:
        centers_source, ranges_source = extract_nonzero_bounding_box(source_image[None])
        ranges_source = (ranges_source * (1 + crop_boundary_proportion)).long()
        source_image = crop_to_bounding_box(
            source_image[None], centers_source, ranges_source
        )[0]

        mins_source = (centers_source - ranges_source / 2.0).long()[0]

        centers_target, ranges_target = extract_nonzero_bounding_box(target_image[None])
        ranges_target = (ranges_target * (1 + crop_boundary_proportion)).long()
        target_image = crop_to_bounding_box(
            target_image[None], centers_target, ranges_target
        )[0]

        mins_target = (centers_target - ranges_target / 2.0).long()[0]
        # also adjust crops to cropped domain
        source_points = source_points - mins_source

    # (affine) pre-registration
    if include_preregistration:
        if prereg_fn is None:
            prereg_fn = partial(register_affine, verbose=verbose, gpus=gpus)

        # explicitly register the inverse way, since displacement fields are implemented as a
        # lookup for the target domain and not necessarily bijective
        prereg_transformation = prereg_fn(target_image, source_image)
        with torch.no_grad():
            # apply transform to image to get intermediate. Don't use it as an initialization since
            # that way it's only regarded on the lowest resolution of the following registration
            prereg_image = prereg_transformation(target_image)[0]
    else:
        prereg_image = target_image
        # identity transform
        prereg_transformation = Transformation(target_image.shape[1:])

    # (diffeomorphic) registration
    if reg_fn is None:
        reg_fn = partial(
            register_diffeomorphic,
            verbose=verbose,
            gpus=gpus,
        )

    # explicitly register the inverse way, since displacement fields are implemented as a
    # lookup for the target domain and not necessarily bijective
    reg_transformation = reg_fn(prereg_image, source_image)

    # point transformation; just lookup + denormalization due to inverse registration
    with torch.no_grad():
        total_trafo = prereg_transformation + reg_transformation

        displacement = (
            total_trafo.compute_complete_transform_displacement() + total_trafo.grid
        )
        result_points = []
        for p in source_points.unbind():
            result_points.append(displacement[tuple([0] + p.tolist())])

        result_points = torch.flip(torch.stack(result_points), (-1,))

        transformed_points = denormalize_points(
            result_points, torch.tensor(target_image.shape[1:]).to(result_points)
        )

        if contour_snap:
            transformed_points = snap_to_contour(transformed_points, target_image)

        if crop_to_bounding_box:
            transformed_points = transformed_points + mins_target

    if return_trafo:
        return transformed_points, total_trafo
    return transformed_points
