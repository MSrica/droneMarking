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
def showWindow(frame, followingPoints):
    if len(followingPoints) > 0:
        frame = drawFollowingPoints(frame, followingPoints)

    frameSmall = cv.resize(frame, (0, 0), fx=constants.SHRINK, fy=constants.SHRINK)
    cv.imshow('Marker detection', frameSmall)


    if cv.waitKey(10) == ord('q'):
        return False

    return True

# drawing marker center and axes
def drawMarker(image, id, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, corners):   
    # drawing marker center
    cv.circle(image, (aMarker[4]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)
    
    # drawing orientation axes of a marker
    cv.aruco.drawAxis(image, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, constants.MARKER_ORIENTATION_LENGTH)

    # line below replaces manual drawing
    #cv.aruco.drawDetectedMarkers(image, corners) 
    cv.line(image, aMarker[3], aMarker[0], constants.GREEN, constants.LINE_WIDTH)
    cv.line(image, aMarker[0], aMarker[1], constants.GREEN, constants.LINE_WIDTH)
    cv.line(image, aMarker[1], aMarker[2], constants.GREEN, constants.LINE_WIDTH)
    cv.line(image, aMarker[2], aMarker[3], constants.GREEN, constants.LINE_WIDTH)

    cv.circle(image, (aMarker[0][0], aMarker[0][1]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)

    cv.putText(image, str(id), (aMarker[0][0], aMarker[0][1] - 10), constants.FONT, constants.FONT_SCALE, constants.RED, constants.LINE_WIDTH)

def drawFollowingPoints(frame, followingPoints):
    formatedFollowingPoints = np.array(followingPoints)
    formatedFollowingPoints = formatedFollowingPoints.reshape((-1, 1, 2))
    return cv.polylines(frame, [formatedFollowingPoints], constants.CLOSED_CIRCUIT, constants.WHITE, constants.LINE_WIDTH)

    #return cv.drawContours(frame, [np.array(followingPoints)], 0, (255,255,255), 2)