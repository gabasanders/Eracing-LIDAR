import os
import json

import numpy as np

import handlerpcl as handlerpcl
import simulate

from constantspcl import MAX_DISTANCE_TO_SCAN


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


def main(ini_index: int, fin_index: int, directory: str) -> None:
    """
    Generate some point clouds from a possible trajectory of the vehicle on the track.

    Args:
        ini_index (int): initial index of the track center line.
        fin_index (int):  final  index of the track center line.

        directory (str): path and name of the directory
            where the point clouds will be stored.
    """

    track = load_track()

    if not os.path.exists(directory):
        os.mkdir(directory)

    if fin_index < ini_index:
        fin_index = len(track["center_line"])
    else:
        fin_index += 1

    for index in range(ini_index, fin_index):
        pose = get_vehicle_pose(track, index)
        nearby = get_closest_cones(pose, track["cones"])

        point_cloud = simulate.generate_point_cloud(pose, nearby)
        np.random.shuffle(point_cloud)

        handlerpcl.write_point_cloud(f"{directory}//pcl_{index}", point_cloud)

        # handler.draw2D(point_cloud)
        # handler.draw3D(point_cloud)
        # handler.draw_lidar_view(track, pose)


if __name__ == "__main__":
    main(0, 5, "pcls")

