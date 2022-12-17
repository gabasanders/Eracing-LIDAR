import numpy as np


#===============================================#
#                                               #
#                Cone parameters                #
#                                               #
#===============================================#

CONE_RADIUS = 0.076
CONE_HEIGHT = 0.440

# Auxiliary matrix to compute the LiDAR distance to each point
A = np.diag([CONE_HEIGHT**2, CONE_HEIGHT**2, -CONE_RADIUS**2])

CONE_EFFECTIVE_HEIGHT = 0.325


#===============================================#
#                                               #
#               LiDAR parameters                #
#                                               #
#===============================================#

LIDAR_ORIENTATION = np.deg2rad(0.0)
LIDAR_DISPLACEMENT = np.array([0.0, 0.0, 1.1])

SCAN_FIELD_WIDTH = np.deg2rad(200.0)
SCAN_FIELD_CENTER_ANGLE = np.deg2rad(0.0)

ANGULAR_RESOLUTION = np.deg2rad(0.018)

CHANNEL_ANGLE_IN_RAD = np.array(
    [-0.0557982, -0.111003, -0.165195, -0.218009, -0.269200, -0.318505]
)

DISTANCE_UNCERTAINTY = 0.0003   #0.03


#===============================================#
#                                               #
#           Optimize scan parameters            #
#                                               #
#===============================================#

MIN_TAN_VALUE = np.abs(np.tan(CHANNEL_ANGLE_IN_RAD[0]))

MAX_DISTANCE_TO_SCAN = (
    CONE_RADIUS + LIDAR_DISPLACEMENT[2] / MIN_TAN_VALUE
)
