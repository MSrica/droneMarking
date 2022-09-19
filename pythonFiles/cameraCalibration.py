# -*- coding: utf-8 -*-
"""
@author: srica
@source: https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
"""

# libraries
import imageAnalyzing
import savingToFile


# 2e+2 -> 200
import numpy as np
np.set_printoptions(suppress=True)


def mainLoop():
    ret, objpoints, imgpoints = imageAnalyzing.getPoints()  # objpoints - 3d point in real world space, imgpoints - 2d points in image plane
    if not ret: return False
    
    ret, mtx, dist, rvecs, tvecs, reprojectionError = imageAnalyzing.getCameraValues(objpoints, imgpoints)  # mtx - camera matrix, dist - distortion matrix, rvecs - rotation vectors, tvecs - translation vectors
    if not ret: return False

    savingToFile.saveToFiles(mtx, dist, rvecs, tvecs, reprojectionError)
    print('Successfully calibrated and saved camera values')
    print(f'Reprojection error: {reprojectionError:.3f}')
    return True
    
    
if __name__ == '__main__':
    mainLoop()