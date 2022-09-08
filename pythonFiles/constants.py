# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import os
import cv2
import math
import glob
import random

# needed when better camera is connected (intel camera)
# camera and window resolution
# USB 2.1 						    USB 3.0
#CAMERA_CAPTURE_RESOLUTION_X = 1280	# 1920
#CAMERA_CAPTURE_RESOLUTION_Y = 720	# 1080
#CAMERA_CAPTURE_FPS = 15 			# 30
#WINDOW_WIDTH = 800

#CAMERA_SOURCE = 0
CAMERA_SOURCE = 'http://192.168.5.13:8080/video'

# marker types, lengths and values
ARUCO_TYPE = cv2.aruco.DICT_4X4_1000
MARKER_SIDE_LENGTH = 0.03
MARKER_DIAGONAL_LENGTH = math.sqrt((MARKER_SIDE_LENGTH ** 2) * 2) * 100
MARKER_ORIENTATION_LENGTH = MARKER_SIDE_LENGTH / 2

MEASURING_MARKER_ID = 0
CLOSED_CIRCUIT = False
PIXEL_DIFFERENCE = 5

# drawing values
SHRINK = 0.5
LINE_WIDTH = 2
CIRCLE_WIDTH = -1
CIRCLE_RADIUS = 4
BORDER_CIRCLE_WIDTH = 2
BORDER_CIRCLE_RADIUS = 5
CENTER_CIRCLE_RADIUS = 40
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)

# directory settings
#CURRENT_DIRECTORY = os.path.dirname(os.getcwd())
CURRENT_DIRECTORY = os.getcwd()
DEVICE_NAME = 'A52S'
SAMPLE_IMAGES = CURRENT_DIRECTORY + '\\samples\\' + DEVICE_NAME + '\\'
NR_OF_IMAGES = random.randint(1, 19)

# termination criteria
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners, size of one square in m
NX = 6
NY = 8
SQUARE_SIZE = 0.03

# shrink image coefficient 
SHRINK = 0.5

# directory of images
IMAGES = glob.glob(SAMPLE_IMAGES + '*.jpg')
EXAMPLE_IMAGE = SAMPLE_IMAGES + str(NR_OF_IMAGES) + '.jpg'

# files
VALUES_FOLDER = CURRENT_DIRECTORY + '\\cameraValues\\' + DEVICE_NAME + '\\'
FILE_EXTENSION = '.txt'

CAMERA_MATRIX_FILE = VALUES_FOLDER + 'cameraMatrix' + FILE_EXTENSION
DISTORTION_MATRIX_FILE = VALUES_FOLDER + 'distortionMatrix' + FILE_EXTENSION
ROTATION_VECTORS_FILE = VALUES_FOLDER + 'rotationVectors' + FILE_EXTENSION
TRANSLATION_VECTORS_FILE = VALUES_FOLDER + 'translationVectors' + FILE_EXTENSION
REPROJECTION_ERROR_FILE = VALUES_FOLDER + 'reprojectionError' + FILE_EXTENSION