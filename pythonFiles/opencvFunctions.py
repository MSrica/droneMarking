# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import os
import cv2 as cv
import numpy as np

# files
import constants

# opening communication with camera
def communicateWithCamera():
    cap = cv.VideoCapture(constants.CAMERA_SOURCE)
    if not cap.isOpened():
        print("Cannot open camera")
        return cap, False

    return cap, True

# getting camera matrix and distortion
def getCameraValues():
    cameraFile = open(constants.CAMERA_MATRIX_FILE, 'r')
    cameraLines = cameraFile.readlines()
    cameraMatrix = np.array([[float(cameraLines[0][:-2]), float(cameraLines[1][:-2]), float(cameraLines[2][:-2])], [float(cameraLines[3][:-2]), float(cameraLines[4][:-2]), float(cameraLines[5][:-2])], [float(cameraLines[6][:-2]), float(cameraLines[7][:-2]), float(cameraLines[8][:-2])]])

    distortionFile = open(constants.DISTORTION_MATRIX_FILE, 'r')
    distortionLines = distortionFile.readlines()
    distortionMatrix = np.array([[float(distortionLines[0][:-2]), float(distortionLines[1][:-2]), float(distortionLines[2][:-2]), float(distortionLines[3][:-2]), float(distortionLines[4][:-2])]])

    return cameraMatrix, distortionMatrix

# showing window and checking for exit
def showWindow(frame):
    frameSmall = cv.resize(frame, (0, 0), fx=constants.SHRINK, fy=constants.SHRINK)
    cv.imshow('Marker detection', frameSmall)

    if cv.waitKey(10) == ord('q'):
        return False

    return True

# drawing marker center and axes
def drawMarker(image, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector):   
    # drawing marker center
    cv.circle(image, (aMarker[4], aMarker[5]), constants.CIRCLE_RADIUS, (0, 0, 255), constants.CIRCLE_WIDTH)
    # drawing orientation axes of a marker
    cv.aruco.drawAxis(image, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, constants.MARKER_ORIENTATION_LENGTH)