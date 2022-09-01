# -*- coding: utf-8 -*-
"""
@author: srica
"""

import constants

def getMarkerCoordinates(aCorner):
    topLeft, topRight, bottomRight, bottomLeft = aCorner

    centerX = int((topLeft[0] + topRight[0] + bottomRight[0] + bottomLeft[0])/4)
    centerY = int((topLeft[1] + topRight[1] + bottomRight[1] + bottomLeft[1])/4)
    center = (centerX, centerY)
    
    #centerX = traslationVector[0][0]
    #centerY = traslationVector[0][1]
    
    #centerX = int((topLeft[0] + bottomRight[0]) / 2.0)
    #centerY = int((topLeft[1] + bottomRight[1]) / 2.0)

    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    return topLeft, topRight, bottomRight, bottomLeft, center

def getWindowCenterCircleCoordinates(frame):
	circleCenterX = (int)((frame.shape[1]-1) / 2)
	circleCenterY = (int)((frame.shape[0]-1) / 2)

	return circleCenterX, circleCenterY, constants.CENTER_CIRCLE_RADIUS

def checkMeasuringMarkerPosition(frame, center):
    circleCenterX, circleCenterY, radius = getWindowCenterCircleCoordinates(frame)
    if (circleCenterX < center[0] + radius and circleCenterX > center[0] - radius) and (circleCenterY < center[1] + radius and circleCenterY > center[1] - radius): 
        return True
    return False

def sortMarkers(aCorner, ids, rotationVectors, translationVectors):
    ids = ids.flatten()     # ([[1,2], [3,4]]) -> ([1, 2, 3, 4])
    zipped = zip(aCorner, ids, rotationVectors, translationVectors)
    zipped = list(zipped)
    zippedSorted = sorted(zipped, key = lambda x: x[1])

    return zippedSorted