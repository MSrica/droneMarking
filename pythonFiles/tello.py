# -*- coding: utf-8 -*-
"""
@author: srica
"""

# https://djitellopy.readthedocs.io/en/latest/tello/
# https://tello.oneoffcoder.com/python.html

from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(20)
tello.rotate_counter_clockwise(180)
tello.move_forward(20)
tello.rotate_clockwise(180)
tello.move_forward(20)

# go_xyz_speed

tello.land()