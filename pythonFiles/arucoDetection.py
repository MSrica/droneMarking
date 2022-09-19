# -*- coding: utf-8 -*-
"""
@source: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
@author: srica
"""

# draw drone and orientation (line)

# libraries
import cv2 as cv
import numpy as np

# files
import constants
import calculations
import opencvFunctions
import markerDetection
import cameraCalibration


# main program
def mainLoop():
    followingPoints = []
    looping = True

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

        if not constants.measuringMarkerInsideLimits: opencvFunctions.drawCenterMeasuringCircle(frame)
            
        # getting camera values
        cameraMatrix, cameraDistortionCoefficients = opencvFunctions.getCameraValues()
        # finding all markers in image
        corners, ids, rotationVectors, translationVectors = markerDetection.findArucoMarkers(frame, cameraMatrix, cameraDistortionCoefficients)
        
        # if no corners found, loop back
        if not len(corners):
            looping = opencvFunctions.showWindow(frame, followingPoints)
            continue
        
        # sorting data from all markers
        zippedSorted = calculations.sortMarkers(corners, ids, rotationVectors, translationVectors)
        
        # passing trough all markers
        for (markerCorner, id, rotationVector, translationVector) in zippedSorted:
            #print(rotationVector[0])
            #print(cv.Rodrigues(rotationVector))
            if id != constants.MEASURING_MARKER_ID:# and not measuringMarkerInsideLimits: continue
                continue

            # getting all coordinates of a marker - topLeft, topRight, bottomRight, bottomLeft, centerX, centerY
            aCorner = markerCorner.reshape((4, 2))
            aMarker = calculations.getMarkerCoordinates(aCorner)

            # drawing out markers
            opencvFunctions.drawMarker(frame, id, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, corners)

            if not constants.measuringMarkerInsideLimits:
                constants.measuringMarkerInsideLimits = calculations.checkMeasuringMarkerPosition(frame, aMarker[4])
                if not constants.measuringMarkerInsideLimits: break

            if constants.centimeterToPixelRatio == 0:
                calibrationMarkerDiagonalPixels = calculations.getDistanceBetweenTwoPoints(aMarker[0], aMarker[2])
                constants.centimeterToPixelRatio = constants.MARKER_DIAGONAL_LENGTH / calibrationMarkerDiagonalPixels

            if id == 0 and (len(followingPoints) == 0 or (abs(aMarker[4][0] - followingPoints[-1][0][0]) > constants.PIXEL_DIFFERENCE or abs(aMarker[4][1] - followingPoints[-1][0][1]) > constants.PIXEL_DIFFERENCE)):
                followingPoints.append([aMarker[4]]) # polylines
                #followingPoints.append((aMarker[4], aMarker[5])) # contours

        # showing screen and checking for looping conditional
        looping = opencvFunctions.showWindow(frame, followingPoints)
        
    # when everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    return True


if __name__ == '__main__':
    ret = True
    #if input('Type y for calibration ') == 'y':
    #    ret = cameraCalibration.mainLoop()
    if not ret: exit

    ret = mainLoop()
    if not ret: exit