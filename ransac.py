import numpy as np

from constants import *


def crop_rectangle(point_cloud: np.ndarray) -> np.ndarray:
    """
    Filter initially the point cloud by cropping just a rectangle.

    Args:
        point_cloud (np.ndarray): 3D coordinates in LiDAR frame.

    Returns:
        np.ndarray: filtered point cloud.
    """

    mask_x = (MINIMUM_X < point_cloud[:, 0]) & (point_cloud[:, 0] < MAXIMUM_X)
    mask_y = (MINIMUM_Y < point_cloud[:, 1]) & (point_cloud[:, 1] < MAXIMUM_Y)

    return point_cloud[mask_x & mask_y]


def compute_planes(random_points: np.ndarray) -> np.ndarray:
    """
    At every three points, compute the respective plane. The plane equation
    is ax + by + cz + d = 0 and the coefficients are a, b, c, and d.

    Args:
        random_points (np.ndarray): of downsample with 3D coordinates in rows.

    Returns:
        np.ndarray: normalized normals and respective d values of
            each plane with coefficients a, b, c, and d in rows.
    """

    reshaped = np.reshape(random_points, (NUM_PLANES, 3, 3))

    vectors = reshaped[:, 1:] - reshaped[:, :1]
    normals = np.cross(vectors[:, 0], vectors[:, 1])

    norms = np.sqrt(
        np.einsum("ij,ij->i", normals, normals)
    )

    mask = norms > 0   # Remove collinear points
    normals = normals[mask] / norms[mask, np.newaxis]

    d_values = -np.einsum("ij,ij->i", normals, reshaped[mask, 0])

    return np.concatenate((normals, d_values[:, np.newaxis]), axis=1)


def find_best_plane(downsample: np.ndarray, planes: np.ndarray) -> np.ndarray:
    """
    Find the plane between the computed with the most inlier points.

    Args:
        downsample (np.ndarray): just the first rows of the point cloud.

        planes (np.ndarray): normalized normals and respective d values
            of each plane with coefficients a, b, c, and d in rows.

    Returns:
        np.ndarray: normalized normal and respective d value of best plane.
    """

    distances = np.abs(
        np.matmul(planes[:, :3], downsample.T) + planes[:, 3:]
    )

    mask = distances < DIST2PLANE_THRESHOLD
    inliers_quantity = np.sum(mask, axis=1)

    return planes[np.argmax(inliers_quantity)]


def remove_floor(point_cloud: np.ndarray) -> np.ndarray:
    """
    Find the best plane and remove the inliers which represent the floor.

    Args:
        point_cloud (np.ndarray): 3D coordinates in LiDAR frame.

    Returns:
        np.ndarray: filtered (no floor) point cloud.
    """

    point_cloud = crop_rectangle(point_cloud)
    downsample = point_cloud[:DOWNSAMPLE_SIZE]

    random_points = downsample[
        np.random.randint(DOWNSAMPLE_SIZE, size=3 * NUM_PLANES)
    ]

    planes = compute_planes(random_points)
    best_plane = find_best_plane(downsample, planes)

    distances = np.abs(
        np.matmul(best_plane[:3], point_cloud.T) + best_plane[3]
    )

    return point_cloud[distances > DIST2PLANE_THRESHOLD]
