import json

import numpy as np

from constants import MAX_DISTANCE_TO_SCAN


def load_track(filename: str = "track.json") -> dict:
    """
    Load track from JSON file.

    Args:
        filename (str, optional): name of the JSON file
            that will be read. Defaults to "track.json".

    Returns:
        dict: that represents the track {"cones", "center_line"}.
    """

    track = {"cones": None, "center_line": None}

    with open(filename) as file:
        content = json.load(file)

        track["cones"] = np.concatenate(
            (np.asarray(content["mark_cones"]),
             np.asarray(content["blue_cones"]),
             np.asarray(content["yellow_cones"])), axis=0
        )

        track["center_line"] = np.asarray(content["center_line"])

    return track


def get_vehicle_pose(track: dict, index: int) -> np.ndarray:
    """
    Get vehicle pose from some position in the track.

    Args:
        track (dict): dict that represents the track {"cones", "center_line"}.
        index (int): index that represents the vehicle position in the track.

    Returns:
        np.ndarray: vehicle pose in global frame [x, y, z, yaw].
    """

    pose = np.zeros(4)

    direction = (
        track["center_line"][index+1] - track["center_line"][index]
    )

    pose[:2] = track["center_line"][index]
    pose[3] = np.arctan2(direction[1], direction[0])

    return pose


def get_closest_cones(pose: np.ndarray, cones: np.ndarray) -> np.ndarray:
    """
    Get only the cones that are close enough to be detected.

    Args:
        pose (np.ndarray): vehicle pose in global frame [x, y, z, yaw].
        cones (np.ndarray): all cones with 3D coordinates in rows.

    Returns:
        np.ndarray: only visible cones with 3D coordinates in rows.
    """

    vectors = cones - pose[:2]

    mask = np.einsum("ij,ij->i", vectors, vectors) < MAX_DISTANCE_TO_SCAN**2

    return cones[mask]
