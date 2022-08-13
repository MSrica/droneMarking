# -*- coding: utf-8 -*-
"""
@source: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
@author: srica
"""

# libraries
import cv2 as cv

# files
import opencvFunctions
import markerDetection
import calculations

# global variables
looping = True

# main program
def mainLoop():
    # program looping or not
    global looping

    # opening communication with camera
    cap, ret = opencvFunctions.communicateWithCamera()
    if not ret: exit()
        
    # main part of program
    while looping:
        # getting frame from camera
        looping, frame = cap.read()
        if not looping:
            print("Can't receive frame. Exiting ...")
            break
        
        # getting camera values
        cameraMatrix, cameraDistortionCoefficients = opencvFunctions.getCameraValues()
        # finding all markers in image
        aCorner, ids, rotationVectors, translationVectors = markerDetection.findArucoMarkers(frame, cameraMatrix, cameraDistortionCoefficients)
        
        # if no corners found, loop back
        if not len(aCorner):
            looping = opencvFunctions.showWindow(frame)
            continue
        
        # sorting data from all markers
        zippedSorted = calculations.sortMarkers(aCorner, ids, rotationVectors, translationVectors)
        
        # passing trough all markers
        for (markerCorner, _, rotationVector, translationVector) in zippedSorted:
            # getting all coordinates of a marker - topLeft, topRight, bottomRight, bottomLeft, centerX, centerY
            aCorner = markerCorner.reshape((4, 2))
            aMarker = calculations.getMarkerCoordinates(aCorner)
            
            # drawing out markers
            opencvFunctions.drawMarker(frame, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector)

        # showing screen and checking for looping conditional
        looping = opencvFunctions.showWindow(frame)
        
    # when everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

# cal mainLoop when file is run
if __name__ == '__main__':
    mainLoop()