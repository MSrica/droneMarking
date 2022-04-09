# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2 as cv
import glob


# termination criteria
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners, size of square
NX = NY = 7
SQUARE_SIZE = 0.015

# shrink image coefficient 
SHRINK = 0.5

# directory of images
IMAGES = glob.glob('ideapad_lenovo_gaming/*.jpg')

# files
VALUES_FOLDER = 'cameraValues'
FILE_EXTENSION = '.txt'

CAMERA_MATRIX_FILE = 'cameraValues/cameraMatrix' + FILE_EXTENSION
DISTORTION_MATRIX_FILE = 'cameraValues/distorionMatrix' + FILE_EXTENSION
ROTATION_VECTORS_FILE = 'cameraValues/rotationVectors' + FILE_EXTENSION
TRANSLATION_VECTORS_FILE = 'cameraValues/translationVectors' + FILE_EXTENSION