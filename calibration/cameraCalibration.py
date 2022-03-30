# -*- coding: utf-8 -*-
"""
@author: srica

@source: https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
"""

# TODO probs mtx is wrong
# TODO myb NX has to be diff from NY

# libraries
import numpy as np
import cv2 as cv
import glob

import imageAnalyzing
import undistortion


# termination criteria
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners, size of square
NX = NY = 7
SQUARE_SIZE = 0.015


# shrink image coefficient 
SHRINK = 0.5


# directory of images
IMAGES = glob.glob('a52s/*.jpg')


# can be commented, simply does 2e+2 -> 200
np.set_printoptions(suppress=True)

    

def mainLoop():
    # objpoints - 3d point in real world space
    # imgpoints - 2d points in image plane
    # mtx       - camera matrix
    # dist      - distortion matrix
    # rvecs     - rotation vectors
    # tvecs     - translation vectors
    
    objpoints, imgpoints = imageAnalyzing.getPoints()
    mtx, dist, rvecs, tvecs = imageAnalyzing.getCameraVlaues(objpoints, imgpoints)
    undistortion.undistort(mtx, dist)
    undistortion.getError(objpoints, imgpoints, mtx, dist, rvecs, tvecs)
    
    
    
if __name__ == '__main__':
    mainLoop()