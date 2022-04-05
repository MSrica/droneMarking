# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2

import constants

# finding markers in image
def findArucoMarkers(image, cameraMatrix, cameraDistortionCoefficients):
	arucoDictionary = cv2.aruco.Dictionary_get(constants.ARUCO_TYPE)
	arucoParameters = cv2.aruco.DetectorParameters_create()
	(markerCorners, ids, _) = cv2.aruco.detectMarkers(image, arucoDictionary, parameters=arucoParameters)
	rotationVectors, translationVectors, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, constants.MARKER_SIDE_LENGTH, cameraMatrix, cameraDistortionCoefficients)
	return markerCorners, ids, rotationVectors, translationVectors