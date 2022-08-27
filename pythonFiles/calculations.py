# -*- coding: utf-8 -*-
"""
@author: srica
"""

def getMarkerCoordinates(aCorner):
    topLeft, topRight, bottomRight, bottomLeft = aCorner
    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    centerX = int((topLeft[0] + bottomRight[0]) / 2.0)
    centerY = int((topLeft[1] + bottomRight[1]) / 2.0)

    return topLeft, topRight, bottomRight, bottomLeft, centerX, centerY


def sortMarkers(aCorner, ids, rotationVectors, translationVectors):
    ids = ids.flatten()     # ([[1,2], [3,4]]) -> ([1, 2, 3, 4])
    zipped = zip(aCorner, ids, rotationVectors, translationVectors)
    zipped = list(zipped)
    zippedSorted = sorted(zipped, key = lambda x: x[1])

    return zippedSorted