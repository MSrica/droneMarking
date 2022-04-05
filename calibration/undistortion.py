# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2 as cv

import constants


def undistort(mtx, dist):
    # get random image
    img = cv.imread('a52s/viber_image_2022-03-27_19-11-37-526.jpg')
    h,  w = img.shape[:2]
    
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # undistort first method
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    
    # undistort second method
    #mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    #dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
    
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    
    # shrink to desired size
    dstSmall = cv.resize(dst, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
    imgSmall = cv.resize(img, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
    
    # show comparison between original and calibrated
    cv.imshow('Calibration result for viber_image_2022-03-27_19-11-37-526.jpg', dstSmall)
    cv.imshow('OG viber_image_2022-03-27_19-11-37-526.jpg', imgSmall)
    cv.waitKey()
    cv.destroyAllWindows()
        
def getError(objpoints, imgpoints, mtx, dist, rvecs, tvecs):
    # show error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
    print("Total error: {}".format(mean_error/len(objpoints)))