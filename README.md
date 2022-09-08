# Drone marking
Python project which aims to incorporate live video feed of a drone in order to guide the second drone along the wanted path using only previously mentioned video fered, no other sensors. Drones that are used are DJI Phantom 4 Pro V2 and DJI Tello.

## Camera calibration and ArUco markers
A checkerboard pattern is used for camera calibration in order to extract intrinsic values of a camera for improved accuracy.
When the camera is calibrated, ArUco markers are used for tracking the drone. Position vales are saved inside a local database (simple file system).

## Navigation
Programmatically navigating the Phantom was not necessary, but navigating the Tello was. For that job, Python was also used in order to maintain the simplicity of use.

## Marking