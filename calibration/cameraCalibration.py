# -*- coding: utf-8 -*-
"""
@author: srica

@source: https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
"""

# TODO myb NX has to be diff from NY

# libraries
import numpy as np

import imageAnalyzing
import undistortion
import savingToFile


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
    #undistortion.undistort(mtx, dist)
    undistortion.getError(objpoints, imgpoints, mtx, dist, rvecs, tvecs)
    savingToFile.saveToFile(mtx, dist, rvecs, tvecs)
    
    
if __name__ == '__main__':
    mainLoop()