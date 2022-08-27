# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import cv2

# files
import constants

# finding markers in image
def findArucoMarkers(image, cameraMatrix, cameraDistortionCoefficients):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	arucoDictionary = cv2.aruco.Dictionary_get(constants.ARUCO_TYPE)
	arucoParameters = cv2.aruco.DetectorParameters_create()
	markerCorners, ids, _ = cv2.aruco.detectMarkers(gray, arucoDictionary, parameters=arucoParameters, cameraMatrix=cameraMatrix, distCoeff=cameraDistortionCoefficients)
	rotationVectors, translationVectors, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, constants.MARKER_SIDE_LENGTH, cameraMatrix, cameraDistortionCoefficients)
	
	return markerCorners, ids, rotationVectors, translationVectors