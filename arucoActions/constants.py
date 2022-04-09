# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2
import math

# camera and window resolution
# USB 2.1 						USB 3.0
CAMERA_CAPTURE_RESOLUTION_X = 1280	# 1920
CAMERA_CAPTURE_RESOLUTION_Y = 720	# 1080
CAMERA_CAPTURE_FPS = 15 			# 30
WINDOW_WIDTH = 800

# marker types, lengths and values
ARUCO_TYPE = cv2.aruco.DICT_4X4_1000 # not working for me in spyder
MARKER_SIDE_LENGTH = 0.097
MARKER_DIAGONAL_LENGTH = math.sqrt((MARKER_SIDE_LENGTH ** 2) * 2) * 100
MARKER_ORIENTATION_LENGTH = 0.1

MEASURING_MARKER_ID = 0

# drawing values
LINE_WIDTH = 2
CIRCLE_WIDTH = -1
CIRCLE_RADIUS = 4
BORDER_CIRCLE_WIDTH = 2
BORDER_CIRCLE_RADIUS = 5

# camera matrices, temporary until merge
A52S_CAMERA_MATRIX = [[1208.15, 0.00, 805.49], [0.00, 1197.12, 577.64], [0.00, 0.00, 1.00]]
A52S_DISTORTION_MATRIX = [[0.31, -2.38, 0.01, 0.00, 6.30]]