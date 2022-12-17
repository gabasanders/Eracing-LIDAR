import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from constantspcl import SCAN_FIELD_WIDTH, MAX_DISTANCE_TO_SCAN


POINT_COLOR = "#0065D9"

LIDAR_FOV_ALPHA = 0.3
LIDAR_FOV_COLOR = "#8F00C7"


def draw2D(point_cloud: np.ndarray) -> None:
    """
    Draw a point cloud using matplotlib in a 2D top view.

    Args:
        point_cloud (np.ndarray): simulated LiDAR measurement.
    """

    ax = plt.axes()

    ax.axis("off")
    ax.set_aspect("equal")

    ax.scatter(
        point_cloud[:, 0],
        point_cloud[:, 1],
        color=POINT_COLOR
    )

    plt.tight_layout()
    plt.show()


def draw3D(point_cloud: np.ndarray) -> None:
    """
    Draw a point cloud using matplotlib in a 3D environment.

    Args:
        point_cloud (np.ndarray): simulated LiDAR measurement.
    """

    ax = plt.axes(projection="3d")

    ax.axis("off")
    ax.set_box_aspect(
        (np.ptp(point_cloud[:, 0]),
         np.ptp(point_cloud[:, 1]),
         np.ptp(point_cloud[:, 2]))
    )

    ax.scatter3D(
        point_cloud[:, 0],
        point_cloud[:, 1],
        point_cloud[:, 2],
        color=POINT_COLOR
    )

    plt.tight_layout()
    plt.show()


def draw_lidar_view(track: dict, pose: np.ndarray) -> None:
    """
    Draw the track top view marking the LiDAR field of view.

    Args:
        track (dict): dict that represents the track {"cones", "center_line"}.
        pose (np.ndarray): vehicle pose in global frame [x, y, z, yaw].
    """

    ax = plt.axes()

    ax.axis("off")
    ax.set_aspect("equal")

    direction = np.array([np.cos(pose[3]), np.sin(pose[3])])

    cos = np.cos(0.5 * SCAN_FIELD_WIDTH)
    sin = np.sin(0.5 * SCAN_FIELD_WIDTH)

    rotmat = np.array(
        [[ cos, -sin],
         [ sin,  cos]]
    )

    fov_point_A = direction @ rotmat
    fov_point_B = direction @ rotmat.T

    theta_A = np.arctan2(fov_point_A[1], fov_point_A[0])
    theta_B = np.arctan2(fov_point_B[1], fov_point_B[0])

    # Convert the angles to first cycle
    theta_A += 2 * np.pi if theta_A < 0.0 else 0.0
    theta_B += 2 * np.pi if theta_B < 0.0 else 0.0

    # Make sure that theta_A < theta_B
    theta_B += 2 * np.pi if theta_A > theta_B else 0.0

    angle = np.linspace(theta_A, theta_B, 48)[:, np.newaxis]
    vectors = np.concatenate((np.cos(angle), np.sin(angle)), axis=1)

    fov = pose[:2] + MAX_DISTANCE_TO_SCAN * vectors
    fov = np.concatenate(
        (pose[:2].reshape((1, 2)), fov, pose[:2].reshape((1, 2))), axis=0
    )

    ax.fill(
        fov[:, 0],
        fov[:, 1],
        color=LIDAR_FOV_COLOR,
        alpha=LIDAR_FOV_ALPHA,
        zorder=0
    )

    ax.scatter(
        track["cones"][:, 0],
        track["cones"][:, 1],
        color=POINT_COLOR,
        zorder=1
    )

    plt.tight_layout()
    plt.show()


def read_point_cloud(filename: str) -> np.ndarray:
    """
    Read point cloud coordinates from a CSV file.

    Args:
        filename (str): name of the CSV file that will be read.

    Returns:
        np.ndarray: 3D coordinates in LiDAR frame.
    """

    df = pd.read_csv(filename)

    return df.to_numpy()


def write_point_cloud(filename: str, point_cloud: np.ndarray) -> None:
    """
    Generate a CSV file by point cloud coordinates.

    Args:
        filename (str): name of the CSV file that will be created.
        point_cloud (np.ndarray): 3D coordinates in LiDAR frame.
    """

    df = pd.DataFrame(point_cloud, columns=["x", "y", "z"])

    df.to_csv(f"{filename}.csv", index=False)

