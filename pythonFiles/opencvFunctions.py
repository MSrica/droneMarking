# -*- coding: utf-8 -*-
"""
@author: srica
"""

# libraries
import math
import cv2 as cv
import numpy as np

# files
import constants
import calculations

# mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        if constants.measuringMarkerInsideLimits == False: return
        elif len(constants.routePoints) == 0:
            constants.routePoints.append([(int(x/constants.SHRINK), int(y/constants.SHRINK))])
        elif calculations.getDistanceBetweenTwoPoints(constants.routePoints[-1][0], [x/constants.SHRINK, y/constants.SHRINK]) * constants.centimeterToPixelRatio >= constants.TELLO_MINIMUM_DISTANCE and calculations.getDistanceBetweenTwoPoints(constants.routePoints[0][0], [x/constants.SHRINK, y/constants.SHRINK]) * constants.centimeterToPixelRatio >= constants.TELLO_MINIMUM_DISTANCE: 
            constants.routePoints.append([(int(x/constants.SHRINK), int(y/constants.SHRINK))])
        else:
            print(f'Distance between points shorter than {constants.TELLO_MINIMUM_DISTANCE} cm')
    elif event == cv.EVENT_RBUTTONDBLCLK:
        constants.dronePoints = []
        if len(constants.routePoints) == 0: return
        constants.routePoints.pop()
    elif event == cv.EVENT_MBUTTONDBLCLK:
        if len(constants.dronePoints) in (0, 1):
            constants.dronePoints.append([(int(x/constants.SHRINK), int(y/constants.SHRINK))])

# opening communication with camera
def communicateWithCamera():
    cap = cv.VideoCapture(constants.CAMERA_SOURCE)
    cv.namedWindow('Marker detection')
    cv.setMouseCallback('Marker detection', mouse_callback)
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

def drawCenterMeasuringCircle(frame):
	circleCenterX, circleCenterY, radius = calculations.getWindowCenterCircleCoordinates(frame)
	cv.circle(frame, (circleCenterX, circleCenterY), radius, constants.RED, constants.BORDER_CIRCLE_WIDTH)

# showing window and checking for exit
def showWindow(frame, followingPoints):
    #if len(followingPoints) > 0: frame = drawFollowingPoints(frame, followingPoints)
    
    if len(constants.routePoints) > 0:
        frame = drawRoutePoints(frame)

    if len(constants.dronePoints) > 0:
        frame = drawDronePoints(frame)    

    if len(constants.dronePoints) > 0:
        frame = drawDronePoints(frame)   

    frameSmall = cv.resize(frame, (0, 0), fx=constants.SHRINK, fy=constants.SHRINK)
    cv.imshow('Marker detection', frameSmall)
    wait = cv.waitKey(30)

    if wait in (ord('q'), ord('Q')):
        return False
    elif wait in (ord('s'), ord('S')):
        showNext()
    elif wait in (ord('m'), ord('M')):
        move()

    return True

# drawing marker center and axes
def drawMarker(image, id, aMarker, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, corners):   
    # drawing marker center
    cv.circle(image, (aMarker[4]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)
    
    # drawing orientation axes of a marker
    #cv.aruco.drawAxis(image, cameraMatrix, cameraDistortionCoefficients, rotationVector, translationVector, constants.MARKER_ORIENTATION_LENGTH)

    # line below replaces manual drawing
    #cv.aruco.drawDetectedMarkers(image, corners) 
    #cv.line(image, aMarker[3], aMarker[0], constants.GREEN, constants.LINE_WIDTH)
    #cv.line(image, aMarker[0], aMarker[1], constants.GREEN, constants.LINE_WIDTH)
    #cv.line(image, aMarker[1], aMarker[2], constants.GREEN, constants.LINE_WIDTH)
    #cv.line(image, aMarker[2], aMarker[3], constants.GREEN, constants.LINE_WIDTH)

    lineVector = [aMarker[0][0] - aMarker[1][0], aMarker[0][1] - aMarker[1][1]]
    lineLength = math.sqrt(lineVector[0]*lineVector[0] + lineVector[1]*lineVector[1])
    lineVector[0] = lineVector[0] / lineLength
    lineVector[1] = lineVector[1] / lineLength
    midDistance = calculations.getDistanceBetweenTwoPoints(aMarker[0], aMarker[1])/2
    midPoint = [int(aMarker[1][0] + lineVector[0] * midDistance), int(aMarker[1][1] + lineVector[1] * midDistance)]
    cv.circle(image, (midPoint[0], midPoint[1]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)

    #cv.putText(image, str(id), (aMarker[0][0], aMarker[0][1] - 10), constants.FONT, constants.FONT_SCALE, constants.RED, constants.LINE_WIDTH)
    constants.markerPoints = []
    constants.markerPoints.append([aMarker[4][0], aMarker[4][1]])
    constants.markerPoints.append(midPoint)

    showNextMarker()

    if len(constants.markerPoints) > 2:
        cv.line(image, constants.markerPoints[0], constants.markerPoints[2], constants.GREEN, constants.LINE_WIDTH)

def drawFollowingPoints(frame, followingPoints):
    #return cv.drawContours(frame, [np.array(followingPoints)], constants.CLOSED_CIRCUIT, constants.WHITE, constants.LINE_WIDTH)
    formatedFollowingPoints = np.array(followingPoints)
    formatedFollowingPoints = formatedFollowingPoints.reshape((-1, 1, 2))
    return cv.polylines(frame, [formatedFollowingPoints], constants.CLOSED_CIRCUIT, constants.WHITE, constants.LINE_WIDTH)

def drawRoutePoints(frame):
    formatedRoutePoints = np.array(constants.routePoints)
    formatedRoutePoints = formatedRoutePoints.reshape((-1, 1, 2))
    for point in formatedRoutePoints:
        cv.circle(frame, (point[0][0], point[0][1]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)

    return cv.polylines(frame, [formatedRoutePoints], constants.CLOSED_CIRCUIT, constants.WHITE, constants.LINE_WIDTH)

def drawDronePoints(frame):
    formatedDronePoints = np.array(constants.dronePoints)
    formatedDronePoints = formatedDronePoints.reshape((-1, 1, 2))
    cv.circle(frame, (formatedDronePoints[0][0][0], formatedDronePoints[0][0][1]), constants.CIRCLE_RADIUS, constants.BLUE, constants.CIRCLE_WIDTH)
    if len(formatedDronePoints) >= 2:
        cv.line(frame, (formatedDronePoints[0][0][0], formatedDronePoints[0][0][1]), (formatedDronePoints[1][0][0], formatedDronePoints[1][0][1]), constants.BLUE, constants.LINE_WIDTH)
        cv.circle(frame, (formatedDronePoints[1][0][0], formatedDronePoints[1][0][1]), constants.CIRCLE_RADIUS, constants.BLUE, constants.CIRCLE_WIDTH)
        if len(formatedDronePoints) >= 3:
            cv.line(frame, (formatedDronePoints[0][0][0], formatedDronePoints[0][0][1]), (formatedDronePoints[2][0][0], formatedDronePoints[2][0][1]), constants.BLUE, constants.LINE_WIDTH)
            
            angle = 0
            radius = int(calculations.getDistanceBetweenTwoPoints([constants.dronePoints[1][0][0], constants.dronePoints[1][0][1]], [constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]]))
            axesLength = (radius, radius)
            startAngle = 180 * np.arctan2(constants.dronePoints[1][0][1] - constants.dronePoints[0][0][1], constants.dronePoints[1][0][0] - constants.dronePoints[0][0][0]) / np.pi
            endAngle = 180 * np.arctan2(constants.dronePoints[2][0][1] - constants.dronePoints[0][0][1], constants.dronePoints[2][0][0] - constants.dronePoints[0][0][0]) / np.pi 
            
            if startAngle < 0: startAngle += 360
            if endAngle < 0: endAngle += 360

            if(startAngle-endAngle > endAngle-startAngle):
                tmp = startAngle
                startAngle = endAngle
                endAngle = tmp

            cv.ellipse(frame, (constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]), axesLength, angle, startAngle, endAngle, constants.BLUE, constants.LINE_WIDTH)

            if len(formatedDronePoints) >= 4:
                cv.circle(frame, (formatedDronePoints[3][0][0], formatedDronePoints[3][0][1]), constants.CIRCLE_RADIUS, constants.RED, constants.CIRCLE_WIDTH)

    return frame

def showNext():
    minimumDistance = 99999.
    closestPoint = None

    if len(constants.routePoints) <= 1:
        print('No route')
        return
    
    if len(constants.dronePoints) <= 1:
        print('No drone')
        return
    
    for point in constants.routePoints:
        currentDistance = calculations.getDistanceBetweenTwoPoints([point[0][0], point[0][1]], [constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]])
        if currentDistance < minimumDistance and currentDistance*constants.centimeterToPixelRatio >= constants.TELLO_MINIMUM_DISTANCE:
            minimumDistance = currentDistance
            closestPoint = point
        if currentDistance <= constants.MINIMUM_DISTANCE_POINT:
            minimumDistance = 0
            closestPoint = point
            break

    if len(constants.dronePoints) == 3:
        constants.dronePoints.pop()

    if len(constants.dronePoints) == 2:
        if minimumDistance == 0:
            for index, point in enumerate(constants.routePoints):
                if closestPoint == point:
                    if index == len(constants.routePoints)-1:
                        index = -1
                    
                        constants.dronePoints.append(constants.routePoints[index+1][0])
        else:
            constants.dronePoints.append(closestPoint)

    ang = math.degrees(math.atan2(constants.dronePoints[2][0][1]-constants.dronePoints[0][0][1], constants.dronePoints[2][0][0]-constants.dronePoints[0][0][1]) - math.atan2(constants.dronePoints[1][0][1]-constants.dronePoints[0][0][1], constants.dronePoints[1][0][0]-constants.dronePoints[0][0][0]))
    if ang < 0: 
        ang += 360

    lineVector = [constants.dronePoints[2][0][0] - constants.dronePoints[0][0][0], constants.dronePoints[2][0][1] - constants.dronePoints[0][0][1]]
    lineLength = math.sqrt(lineVector[0]*lineVector[0] + lineVector[1]*lineVector[1])
    lineVector[0] = lineVector[0] / lineLength
    lineVector[1] = lineVector[1] / lineLength

    droneDistance = calculations.getDistanceBetweenTwoPoints([constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]], [constants.dronePoints[1][0][0], constants.dronePoints[1][0][1]])
    constants.dronePoints.append([(int(constants.dronePoints[0][0][0] + lineVector[0] * droneDistance), int(constants.dronePoints[0][0][1] + lineVector[1] * droneDistance))])
    
    newDistance = calculations.getDistanceBetweenTwoPoints([constants.dronePoints[2][0][0], constants.dronePoints[2][0][1]], [constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]])
    print(f'Angle and distance to next point: {ang:.3f} degrees, {newDistance*constants.centimeterToPixelRatio:.3f} cm')

def move():
    if len(constants.routePoints) <= 1:
        print('No route')
        return
    
    if len(constants.dronePoints) <= 1:
        print('No drone')
        return

    if len(constants.dronePoints) <= 3:
        print('No drone direction')
        return

    lineVector = [constants.dronePoints[2][0][0] - constants.dronePoints[0][0][0], constants.dronePoints[2][0][1] - constants.dronePoints[0][0][1]]
    lineLength = math.sqrt(lineVector[0]*lineVector[0] + lineVector[1]*lineVector[1])
    lineVector[0] = lineVector[0] / lineLength
    lineVector[1] = lineVector[1] / lineLength

    droneDistance = calculations.getDistanceBetweenTwoPoints([constants.dronePoints[0][0][0], constants.dronePoints[0][0][1]], [constants.dronePoints[1][0][0], constants.dronePoints[1][0][1]])
    nextPointX = constants.dronePoints[2][0][0]
    nextPointY = constants.dronePoints[2][0][1]
    constants.dronePoints = []
    constants.dronePoints = [[(int(nextPointX), int(nextPointY))]]
    constants.dronePoints.append([(int(nextPointX + lineVector[0] * droneDistance), int(nextPointY + lineVector[1] * droneDistance))])

def showNextMarker():
    minimumDistance = 99999.
    closestPoint = None

    if len(constants.routePoints) <= 1:
        print('No route')
        return
    
    if len(constants.markerPoints) <= 1:
        print('No drone')
        return
    
    for point in constants.routePoints:
        currentDistance = calculations.getDistanceBetweenTwoPoints([point[0][0], point[0][1]], [constants.markerPoints[0][0], constants.markerPoints[0][1]])
        if currentDistance < minimumDistance and currentDistance*constants.centimeterToPixelRatio >= constants.TELLO_MINIMUM_DISTANCE:
            minimumDistance = currentDistance
            closestPoint = point
        if currentDistance <= constants.MINIMUM_DISTANCE_POINT:
            minimumDistance = 0
            closestPoint = point
            break

    if len(constants.markerPoints) == 3:
        constants.markerPoints.pop()

    if closestPoint == None: return

    if len(constants.markerPoints) == 2:
        if minimumDistance == 0:
            for index, point in enumerate(constants.routePoints):
                if closestPoint == point:
                    if index == len(constants.routePoints)-1:
                        index = -1
                        constants.markerPoints.append([constants.routePoints[index+1][0][0], constants.routePoints[index+1][0][1]])
        else:
            constants.markerPoints.append([closestPoint[0][0], closestPoint[0][1]])

    ang = math.degrees(math.atan2(constants.markerPoints[2][1]-constants.markerPoints[0][1], constants.markerPoints[2][0]-constants.markerPoints[0][1]) - math.atan2(constants.markerPoints[1][1]-constants.markerPoints[0][1], constants.markerPoints[1][0]-constants.markerPoints[0][0]))
    if ang < 0: ang += 360

    lineVector = [constants.markerPoints[2][0] - constants.markerPoints[0][0], constants.markerPoints[2][1] - constants.markerPoints[0][1]]
    lineLength = math.sqrt(lineVector[0]*lineVector[0] + lineVector[1]*lineVector[1])
    lineVector[0] = lineVector[0] / lineLength
    lineVector[1] = lineVector[1] / lineLength

    droneDistance = calculations.getDistanceBetweenTwoPoints([constants.markerPoints[0][0], constants.markerPoints[0][1]], [constants.markerPoints[1][0], constants.markerPoints[1][1]])
    constants.markerPoints.append([int(constants.markerPoints[0][0] + lineVector[0] * droneDistance), int(constants.markerPoints[0][1] + lineVector[1] * droneDistance)])
    
    newDistance = calculations.getDistanceBetweenTwoPoints([constants.markerPoints[2][0], constants.markerPoints[2][1]], [constants.markerPoints[0][0], constants.markerPoints[0][1]])
    print(f'Angle and distance to next point: {ang:.3f} degrees, {newDistance*constants.centimeterToPixelRatio:.3f} cm')