import random

import numpy as np
from skimage.segmentation import find_boundaries

__all__ = ["sample_landmarks"]


def sample_landmarks(
    mask_image: np.ndarray, number_of_points: int = 2000
) -> np.ndarray:
    """
    Performs a random sampling of points on the mask surface

    Args:
        mask_image: 3D numpy array
        number of points: number of landmarks we want to sample

    Returns:
        np.ndarray: array containing coordinates of the selected landmarks

    """
    mask_image_copy = mask_image
    # Get array with the same shape as mask_image. True where points on boundary, false otherwise
    boundary = find_boundaries(mask_image_copy, mode="outer")
    possible_points = np.asarray(np.where(boundary))
    # each entry in the list will be an array containing the coordinates of a boundary point
    possible_points_numpy_list = []

    for idx in range(possible_points.shape[1]):
        possible_points_numpy_list.append(
            np.double(
                [
                    possible_points[2, idx],
                    possible_points[1, idx],
                    possible_points[0, idx],
                ]
            )
        )

    out_points = random.sample(possible_points_numpy_list, number_of_points)

    return np.asarray(out_points)
