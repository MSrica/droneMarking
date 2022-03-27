# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 14:12:59 2022

@author: srica

@source: https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
"""

import numpy as np
import cv2 as cv
import glob


# termination criteria
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# number of corners
NX = NY = 7

# shrinking coefficient 
SHRINK = 0.5


objp = np.zeros((NX*NY, 3), np.float32)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# TODO change to real data (mm)
objp[:, :2] = np.mgrid[0:NX, 0:NY].T.reshape(-1, 2)

images = glob.glob('a52s/*.jpg')

# objpoints - 3d point in real world space
# imgpoints - 2d points in image plane
# mtx       - camera matrix
# dist      - distortion matrix
# rvecs     - rotation vectors
# tvecs     - translation vectors
objpoints, imgpoints, mtx, dist, rvecs, tvecs = ([] for i in range(6))


for imgName in images:
    img = cv.imread(imgName)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (NX, NY), None)
    
    #iIf found add object points, image points
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        cornersFound = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
        
        # draw the corners and show image
        cv.drawChessboardCorners(img, (NX, NY), cornersFound, True)
        img = cv.resize(img, (0, 0), fx = SHRINK, fy = SHRINK)
        cv.imshow(imgName, img)
    else:
        print(imgName, ret, corners)
        
# q or esc to exit all windows
cv.waitKey()
cv.destroyAllWindows()

     
# if at least 1 image is considered   
if objpoints:
    # get camera intrinsic and extrinsic parameters
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # TODO probs mtx is wrong (small values)
    #print(mtx)
    
    img = cv.imread('a52s/viber_image_2022-03-27_19-11-37-526.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # undistort first method
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    
    # undistort second method
    #mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    #dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
    
    # crop the image
    #x, y, w, h = roi
    #dst = dst[y:y+h, x:x+w]
    
    # shrink to desired size
    dstSmall = cv.resize(dst, (0, 0), fx = SHRINK, fy = SHRINK)
    imgSmall = cv.resize(img, (0, 0), fx = SHRINK, fy = SHRINK)
    
    cv.imshow('Calibration result for viber_image_2022-03-27_19-11-37-526.jpg', dstSmall)
    cv.imshow('OG viber_image_2022-03-27_19-11-37-526.jpg', imgSmall)
    cv.waitKey()
    cv.destroyAllWindows()
        
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "Total error: {}".format(mean_error/len(objpoints)) )