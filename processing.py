import numpy as np

# from cuml.cluster import DBSCAN
from sklearn.cluster import DBSCAN

import ransac

from constants import *


def processing(point_cloud: np.ndarray) -> np.ndarray:
    """
    Remove the floor (RANSAC) and cluster the remaining
    points (DBSCAN) to compute the cones centroid.

    Args:
        point_cloud (np.ndarray): 3D coordinates in LiDAR frame.

    Returns:
        np.ndarray: 3D coordinates of cone's centroid in LiDAR frame.
    """

    no_floor = ransac.remove_floor(point_cloud)

    # Run cluster algorithm
    cluster = DBSCAN(eps=MAX_DISTANCE, min_samples=MIN_SAMPLES)

    labels = cluster.fit(no_floor).labels_

    del cluster

    centroids = []
    for label in labels:
        centroids.append(
            np.mean(no_floor[labels == label], axis=0)
        )

    
    return np.asarray(centroids)
