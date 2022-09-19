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

#CAMERA_SOURCE = 0
CAMERA_SOURCE = 'http://192.168.5.20:8080/video'

# marker types, lengths and values
ARUCO_TYPE = cv2.aruco.DICT_4X4_1000
MARKER_SIDE_LENGTH = 0.03 # cm
MARKER_DIAGONAL_LENGTH = math.sqrt((MARKER_SIDE_LENGTH ** 2) * 2) * 100
MARKER_ORIENTATION_LENGTH = MARKER_SIDE_LENGTH / 2
TELLO_MINIMUM_DISTANCE = 20 # cm
MINIMUM_DISTANCE_POINT = 2 # cm

MEASURING_MARKER_ID = 0
CLOSED_CIRCUIT = True
PIXEL_DIFFERENCE = 5

# drawing values
SHRINK = 0.7
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
CURRENT_DIRECTORY = os.path.dirname(os.getcwd())
#CURRENT_DIRECTORY = os.getcwd()
DEVICE_NAME = 'A52S'
SAMPLE_IMAGES = CURRENT_DIRECTORY + '\\samples\\' + DEVICE_NAME + '\\'
NR_OF_IMAGES = len([entry for entry in os.listdir(SAMPLE_IMAGES) if os.path.isfile(os.path.join(SAMPLE_IMAGES, entry))])
RANDOM_IMAGE = random.randint(1, NR_OF_IMAGES)

# termination criteria
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners
NX = 6
NY = 8
SQUARE_SIZE = 0.03 # m

# directory of images
IMAGES = glob.glob(SAMPLE_IMAGES + '*.jpg')
EXAMPLE_IMAGE = SAMPLE_IMAGES + str(RANDOM_IMAGE) + '.jpg'

# files
VALUES_FOLDER = CURRENT_DIRECTORY + '\\cameraValues\\' + DEVICE_NAME + '\\'
FILE_EXTENSION = '.txt'

CAMERA_MATRIX_FILE = VALUES_FOLDER + 'cameraMatrix' + FILE_EXTENSION
DISTORTION_MATRIX_FILE = VALUES_FOLDER + 'distortionMatrix' + FILE_EXTENSION
ROTATION_VECTORS_FILE = VALUES_FOLDER + 'rotationVectors' + FILE_EXTENSION
TRANSLATION_VECTORS_FILE = VALUES_FOLDER + 'translationVectors' + FILE_EXTENSION
REPROJECTION_ERROR_FILE = VALUES_FOLDER + 'reprojectionError' + FILE_EXTENSION

# global variables
dronePoints = []
routePoints = []
markerPoints = []
centimeterToPixelRatio = 0.
measuringMarkerInsideLimits = False