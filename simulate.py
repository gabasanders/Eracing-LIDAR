from constantspcl import *
import numpy as np


def compute_distance(delta_pos: np.ndarray, direction: np.ndarray) -> float:
    """
    The distance will be the appropriate root of equation ax² + 2bx + c = 0.

    Args:
        delta_pos (np.ndarray): difference between vehicle pos and cone pos.
        direction (np.ndarray): direction of laser beam firing in 3D space.

    Returns:
        float: appropriate distance if the laser beam hit the cone or None otherwise.
    """

    a = direction @ A @ direction.T
    b = delta_pos @ A @ direction.T
    c = delta_pos @ A @ delta_pos.T

    if a == 0:
        return None if b == 0 else -0.5 * c / b

    delta = (b/a)**2 - (c/a)

    if delta < 0:
        return None

    distance_1 = -b/a + np.sqrt(delta)
    distance_2 = -b/a - np.sqrt(delta)

    if distance_1 >= 0 and distance_2 >= 0:
        return min(distance_1, distance_2)
    if distance_1 >= 0 and distance_2 < 0:
        return distance_1
    if distance_1 < 0 and distance_2 >= 0:
        return distance_2

    return None


def scan_channel(pose: np.ndarray, cones: np.ndarray, channel_angle: float) -> np.ndarray:
    """
    Scan the given channel and compute the respective partial point cloud.

    Args:
        pose (np.ndarray): LiDAR pose in global frame [x, y, z, yaw].
        cones (np.ndarray): all visible cones with 3D coordinates in rows.

        channel_angle (float): angle in radians of a channel concerning
            the horizontal plane. Only negative angles must be passed.

    Returns:
        np.ndarray: points identified by LiDAR for the given channel.
    """

    num_points = round(2 * np.pi / ANGULAR_RESOLUTION)

    angles = np.linspace(
        SCAN_FIELD_CENTER_ANGLE - 0.5 * SCAN_FIELD_WIDTH,
        SCAN_FIELD_CENTER_ANGLE + 0.5 * SCAN_FIELD_WIDTH,
        num_points
    )

    points = np.zeros((num_points, 3))

    for (index, angle) in enumerate(angles):
        direction = np.array(
            [np.cos(channel_angle) * np.cos(angle + pose[3]),
             np.cos(channel_angle) * np.sin(angle + pose[3]),
             np.sin(channel_angle)]
        )

        distances = []
        for cone in cones:
            distance = compute_distance(pose[:3] - cone, direction)

            if distance is not None:
                distances.append(distance)

        if len(distances) > 0:
            distance = np.random.normal(
                min(distances), DISTANCE_UNCERTAINTY
            )

            points[index] = pose[:3] + distance * direction

            if 0 < points[index, 2] and points[index, 2] < CONE_EFFECTIVE_HEIGHT:
                continue

        distance = np.random.normal(
            -pose[2] / direction[2], DISTANCE_UNCERTAINTY
        )

        points[index] = pose[:3] + distance * direction

    return points


def generate_point_cloud(pose: np.ndarray, cones: np.ndarray) -> np.ndarray:
    """
    Generate the complete LiDAR point cloud.

    Args:
        pose (np.ndarray): vehicle pose in global frame [x, y, z, yaw].
        cones (np.ndarray): all visible cones with 2D coordinates in rows.

    Returns:
        np.ndarray: point cloud in LiDAR frame.
    """

    point_cloud = np.zeros((0, 3))

    new_coord = np.array([CONE_HEIGHT] * len(cones))[:, np.newaxis]

    cones = np.concatenate((cones, new_coord), axis=1)

    pose[3] += LIDAR_ORIENTATION
    pose[:3] += LIDAR_DISPLACEMENT

    for channel in CHANNEL_ANGLE_IN_RAD:
        point_cloud = np.append(
            point_cloud, scan_channel(pose, cones, channel), axis=0
        )

    cos = np.cos(pose[3])
    sin = np.sin(pose[3])

    rotmat = np.array(
        [[cos, -sin, 0],
         [sin,  cos, 0],
         [  0,    0, 1]]
    )

    return (point_cloud - pose[:3]) @ rotmat
