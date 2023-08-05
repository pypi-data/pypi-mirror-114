from typing import Tuple

import torch

__all__ = ["inverse_procrustes", "procrustes", "points2point_procrustes"]


def inverse_procrustes(
    moving_landmarks: torch.Tensor,
    norm: float,
    rotation_mtx: torch.Tensor,
    scale: float,
    mean: torch.Tensor,
) -> torch.Tensor:
    """
    Do the inverse procrustes operation: Used, because data is in trace(data1)=1 space - very small.
    Inverse procrustes transforms the data back in the normal image space according to norm, R, s, mean

    Args:
        moving_landmarks: Nxd landmarks to transform
        norm: 1x1 normalisation
        rotation_mtx: dxd rotation matrix
        scale: 1x1 scale
        mean: dx1 translation

    Returns:
        torch.Tensor: inversed procrustes data
    """
    data = moving_landmarks.clone().double()
    data = torch.dot(data / scale.double(), rotation_mtx.double())

    data *= norm
    data += mean
    return data


def procrustes(
    fixed_landmarks: torch.Tensor, moving_landmarks: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, list]:
    """
    Modified version of scipy.spatial.procrustes returning transformation parameters to make inverse operation possible

    Args:
        fixed_landmarks: n rows represent points in k (columns) space, reference data
        moving_landmarks: n rows of data in k space to be fit to fixed_landmarks

    Returns:
        torch.Tensor: mtx_fixed (standardized version of fixed_landmarks)
        torch.Tensor: mtx_moving (orientation of moving_landmarks that best fits fixed_landmarks)
        torch.Tensor: disparity (remaining difference between mtx_fixed and mtx_moving)
        list: list of applied transforms needed for inverse operation
    """
    mtx_fixed = fixed_landmarks.clone().double()
    mtx_moving = moving_landmarks.clone().double()

    if mtx_fixed.ndim != 2 or mtx_moving.ndim != 2:
        raise ValueError("Input matrices must be two-dimensional")
    if mtx_fixed.shape != mtx_moving.shape:
        raise ValueError("Input matrices must be of same shape")
    if mtx_fixed.size == 0:
        raise ValueError("Input matrices must be >0 rows and >0 cols")

    # translate all the data to the origin
    mean1 = torch.mean(mtx_fixed, 0)
    mean2 = torch.mean(mtx_moving, 0)

    mtx_fixed -= torch.mean(mtx_fixed, 0)
    mtx_moving -= torch.mean(mtx_moving, 0)

    norm1 = torch.linalg.norm(mtx_fixed)
    norm2 = torch.linalg.norm(mtx_moving)

    if norm1 == 0 or norm2 == 0:
        raise ValueError("Input matrices must contain >1 unique points")

    # change scaling of data (in rows) such that trace(mtx*mtx') = 1
    mtx_fixed /= norm1
    mtx_moving /= norm2

    # transform mtx_moving to minimize disparity
    if mtx_fixed.ndim != 2:
        raise ValueError("expected ndim to be 2, but observed %s" % mtx_fixed.ndim)
    if mtx_fixed.shape != mtx_moving.shape:
        raise ValueError(
            "the shapes of fixed and moving differ (%s vs %s)"
            % (mtx_fixed.shape, mtx_moving.shape)
        )

    # Be clever with transposes, with the intention to save memory.
    u, w, v = torch.svd(mtx_moving.T.dot(mtx_fixed).T)
    vt = v.transpose(-2, -1)
    rotation_mtx = u.dot(vt)
    scale = w.sum()
    mtx_moving = torch.dot(mtx_moving, rotation_mtx.T) * scale

    # measure the dissimilarity between the two datasets
    disparity = torch.sum(torch.square(mtx_fixed - mtx_moving))

    return (
        mtx_fixed,
        mtx_moving,
        disparity,
        [mean1, norm1, mean2, norm2, rotation_mtx, scale],
    )


def points2point_procrustes(
    fixed_landmarks: torch.Tensor, moving_landmarks: torch.Tensor
) -> Tuple[torch.Tensor, list]:
    """
    Procrustes Registration from points to points. Applies procrustes between moving and fixed landmarks
    and then registeres the moving landmarks using the transformation parameters from the procrustes algorithm
    (-> inverse procrustes of mtx_moving with transformation parameters)

    Args:
        fixed_landmarks: reference points
        moving_landmarks: points to be fit to fixed_landmarks

    Returns:
        torch.Tensor: registered landmarks
        list: transformation parameters
    """
    (
        _,
        mtx_moving,
        _,
        [translation1, norm1, translation2, norm2, rotation, scaling],
    ) = procrustes(fixed_landmarks, moving_landmarks)
    registered_landmarks = inverse_procrustes(
        mtx_moving, norm1, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], scaling, translation1
    )

    return (
        registered_landmarks,
        [translation1, norm1, translation2, norm2, rotation, scaling],
    )
