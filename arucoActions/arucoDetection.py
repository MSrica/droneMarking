# -*- coding: utf-8 -*-
"""
@source: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
@author: srica
"""

import cv2 as cv
import numpy as np

import markerDetection
import constants


looping = True



# TODO when branch is merged with calibration, hardcoded for now
def getCameraValues():
    return np.array(constants.A52S_CAMERA_MATRIX), np.array(constants.A52S_DISTORTION_MATRIX)

def showWindow(frame):
    cv.imshow('Marker detection', frame)

    if cv.waitKey(30) == ord('q'):
        return False

    return True

def drawMarker(image, markerID, aMarker):   
    cv.circle(image, (aMarker[4], aMarker[5]), constants.CIRCLE_RADIUS, (0, 0, 255), constants.CIRCLE_WIDTH)

def getMarkerCoordinates(aCorner):
    (topLeft, topRight, bottomRight, bottomLeft) = aCorner
    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    centerX = int((topLeft[0] + bottomRight[0]) / 2.0)
    centerY = int((topLeft[1] + bottomRight[1]) / 2.0)

    return topLeft, topRight, bottomRight, bottomLeft, centerX, centerY

def mainLoop():
    global looping

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    while looping:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break
        
        # image processing
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        cameraMatrix, cameraDistortionCoefficients = getCameraValues()
        aCorner, ids, rotationVectors, translationVectors = markerDetection.findArucoMarkers(frame, cameraMatrix, cameraDistortionCoefficients)
        
        # if no corners found, loop back
        if not len(aCorner):
            looping = showWindow(frame)
            continue

        ids = ids.flatten()     # ([[1,2], [3,4]]) -> ([1, 2, 3, 4])

        zipped = zip(aCorner, ids, rotationVectors, translationVectors)
        zipped = list(zipped)
        zippedSorted = sorted(zipped, key = lambda x: x[1])

        # passing trough all markers
        for (markerCorner, markerID, rotationVector, translationVector) in zippedSorted:
            aCorner = markerCorner.reshape((4, 2))   # matrix to 4 pairs
            aMarker = getMarkerCoordinates(aCorner)  # all points of marker - topLeft, topRight, bottomRight, bottomLeft, centerX, centerY
            
            drawMarker(frame, markerID, aMarker)     # drawing centers of all markers
            cv.aruco.drawAxis(frame, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, constants.MARKER_ORIENTATION_LENGTH)

        looping = showWindow(frame)
        
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    mainLoop()