# -*- coding: utf-8 -*-
"""
@source: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
@author: srica
"""

# libraries
import cv2 as cv

# files
import calculations
import opencvFunctions
import markerDetection
import cameraCalibration

# global variables
looping = True

# main program
def mainLoop():
    # program looping or not
    global looping

    # opening communication with camera
    cap, ret = opencvFunctions.communicateWithCamera()
    if not ret: return False
        
    # main part of program
    while looping:
        # getting frame from camera
        looping, frame = cap.read()
        if not looping:
            print("Can't receive frame. Exiting ...")
            return False
        
        # getting camera values
        cameraMatrix, cameraDistortionCoefficients = opencvFunctions.getCameraValues()
        # finding all markers in image
        corners, ids, rotationVectors, translationVectors = markerDetection.findArucoMarkers(frame, cameraMatrix, cameraDistortionCoefficients)
        
        # if no corners found, loop back
        if not len(corners):
            looping = opencvFunctions.showWindow(frame)
            continue
        
        # sorting data from all markers
        zippedSorted = calculations.sortMarkers(corners, ids, rotationVectors, translationVectors)
        
        # passing trough all markers
        for (markerCorner, id, rotationVector, translationVector) in zippedSorted:
            # getting all coordinates of a marker - topLeft, topRight, bottomRight, bottomLeft, centerX, centerY
            aCorner = markerCorner.reshape((4, 2))
            aMarker = calculations.getMarkerCoordinates(aCorner)
            
            # drawing out markers
            opencvFunctions.drawMarker(frame, id, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, corners)

        # showing screen and checking for looping conditional
        looping = opencvFunctions.showWindow(frame)
        
    # when everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    return True


if __name__ == '__main__':
    ret = True
    if input('Type y for calibration ') == 'y':
        ret = cameraCalibration.mainLoop()
    if not ret: exit

    ret = mainLoop()
    if not ret: exit