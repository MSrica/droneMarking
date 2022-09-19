# -*- coding: utf-8 -*-
"""
@author: srica
"""

# https://djitellopy.readthedocs.io/en/latest/tello/
# https://tello.oneoffcoder.com/python.html

import time
from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()
time.sleep(2)

tello.move_forward(20)
time.sleep(2)   

tello.rotate_clockwise(180)
time.sleep(2)

tello.move_forward(20)
time.sleep(2)

tello.land()