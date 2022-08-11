# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2 as cv
import glob
import random


# termination criteria
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners, size of one square in m
NX = 6
NY = 8
SQUARE_SIZE = 0.03

# shrink image coefficient 
SHRINK = 0.5

# directory of images
IMAGES = glob.glob('calibration/a52sSamples/*.jpg')
EXAMPLE_IMAGE = f'calibration/a52sSamples/{random.randint(1, 19)}.jpg'

# files
VALUES_FOLDER = 'cameraValues/'
FILE_EXTENSION = '.txt'

CAMERA_MATRIX_FILE = VALUES_FOLDER + 'cameraMatrix' + FILE_EXTENSION
DISTORTION_MATRIX_FILE = VALUES_FOLDER + 'distorionMatrix' + FILE_EXTENSION
ROTATION_VECTORS_FILE = VALUES_FOLDER + 'rotationVectors' + FILE_EXTENSION
TRANSLATION_VECTORS_FILE = VALUES_FOLDER + 'translationVectors' + FILE_EXTENSION
REPROJECTION_ERROR_FILE = VALUES_FOLDER + 'reprojectionError' + FILE_EXTENSION