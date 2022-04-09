# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import cv2 as cv
import numpy as np

# files
import constants

# opening communication with camera
def communicateWithCamera():
    # TODO define source better - 0 -> ?
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return cap, False

    return cap, True

# getting camera matrix and distortion
def getCameraValues():
    # TODO dynamic when branch is merged with cameraCalibration, hardcoded for now
    return np.array(constants.LIG_CAMERA_MATRIX), np.array(constants.LIG_DISTORTION_MATRIX)

# showing window and checking for exit
def showWindow(frame):
    cv.imshow('Marker detection', frame)

    if cv.waitKey(30) == ord('q'):
        return False

    return True

# drawing marker center and axes
def drawMarker(image, markerID, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector):   
    # drawing marker center
    cv.circle(image, (aMarker[4], aMarker[5]), constants.CIRCLE_RADIUS, (0, 0, 255), constants.CIRCLE_WIDTH)
    # drawing orientation axes of a marker
    cv.aruco.drawAxis(image, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, constants.MARKER_ORIENTATION_LENGTH)