# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import cv2 as cv
import numpy as np

import constants

def getPoints():
    objpoints, imgpoints = ([] for _ in range(2))

    objp = np.zeros((constants.NX*constants.NY, 3), np.float32)
    objp[:, :2] = np.mgrid[0:constants.NX, 0:constants.NY].T.reshape(-1, 2)
    objp = objp * constants.SQUARE_SIZE
    
    for imgName in constants.IMAGES:
        img = cv.imread(imgName)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        #ret, corners = cv.findChessboardCorners(gray, (constants.NX, constants.NY), cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
        ret, corners = cv.findChessboardCorners(gray, (constants.NX, constants.NY), None)
        if not ret:
            print("No pattern found on " + imgName)
            continue

        cornersBetter = cv.cornerSubPix(gray, corners, (20, 20),(-1, -1), constants.CRITERIA)
        #cornersBetter = cv.cornerSubPix(gray, corners, (11, 11),(-1, -1), constants.CRITERIA)
        objpoints.append(objp)
        imgpoints.append(cornersBetter)
        
        """cv.drawChessboardCorners(img, (constants.NX, constants.NY), cornersBetter, ret)
        imgShow = cv.resize(img, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
        cv.imshow(imgName, imgShow)
        cv.waitKey(0)
        cv.destroyAllWindows()"""
    
    ret = True
    if not objpoints:
        print("No images taken in cosideration")
        ret = False

    return ret, objpoints, imgpoints

def getCameraValues(objpoints, imgpoints):
    reprojectionError = 0 
    img = cv.imread(constants.EXAMPLE_IMAGE)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    ret, oldMtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    if not ret:
        print("Camera calibration not successful")
        return ret, oldMtx, dist, rvecs, tvecs, reprojectionError

    h,  w = img.shape[:2]
    mtx, roi = cv.getOptimalNewCameraMatrix(oldMtx, dist, (w, h), 1, (w, h))
    dst = cv.undistort(img, oldMtx, dist, None, mtx)

    # idk
    #x, y, w, h = roi
    #dst = dst[y:y + h, x:x + w]
    #img = img[y:y + h, x:x + w]
    
    """imgSmall = cv.resize(img, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
    dstSmall = cv.resize(dst, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
    
    cv.imshow('Original image ' + constants.EXAMPLE_IMAGE, imgSmall)
    cv.imshow('Calibration result for ' + constants.EXAMPLE_IMAGE, dstSmall)
    cv.waitKey(0)
    cv.destroyAllWindows()"""

    meanError = 0
    for i in range(len(objpoints)):
        imgpointsNew, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpointsNew, cv.NORM_L2)/len(imgpointsNew)
        meanError += error
    reprojectionError = meanError/len(objpoints)
    
    return ret, mtx, dist, rvecs, tvecs, reprojectionError