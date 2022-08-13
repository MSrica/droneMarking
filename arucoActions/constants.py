# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import cv2
import math

# needed when better camera is connected (intel camera)
# camera and window resolution
# USB 2.1 						    USB 3.0
#CAMERA_CAPTURE_RESOLUTION_X = 1280	# 1920
#CAMERA_CAPTURE_RESOLUTION_Y = 720	# 1080
#CAMERA_CAPTURE_FPS = 15 			# 30
#WINDOW_WIDTH = 800

# marker types, lengths and values
ARUCO_TYPE = cv2.aruco.DICT_4X4_1000
MARKER_SIDE_LENGTH = 0.098
MARKER_DIAGONAL_LENGTH = math.sqrt((MARKER_SIDE_LENGTH ** 2) * 2) * 100
MARKER_ORIENTATION_LENGTH = MARKER_SIDE_LENGTH / 2

MEASURING_MARKER_ID = 0

# drawing values
SHRINK = 0.5
LINE_WIDTH = 2
CIRCLE_WIDTH = -1
CIRCLE_RADIUS = 4
BORDER_CIRCLE_WIDTH = 2
BORDER_CIRCLE_RADIUS = 5

# camera matrices
CAMERA_MATRIX_FILE = 'calibration/cameraValues/cameraMatrix.txt'
DISTORTION_MATRIX_FILE = 'calibration/cameraValues/distortionMatrix.txt'