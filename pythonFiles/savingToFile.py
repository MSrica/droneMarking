# -*- coding: utf-8 -*-
"""
@author: srica
"""

import numpy as np
import os

import constants

def writeArrayToFile(fileName, values):
  with open(fileName, 'w+') as f:
      for line in values:
          np.savetxt(f, line, fmt='%.2f')

def writeValueToFile(fileName, value):
  with open(fileName, 'w+') as f:
    f.write(str(value))

def saveToFiles(mtx, dist, rvecs, tvecs, reprojectionError):
  if not os.path.exists(constants.VALUES_FOLDER):
    os.makedirs(constants.VALUES_FOLDER)
  
  writeArrayToFile(constants.CAMERA_MATRIX_FILE, mtx)  
  writeArrayToFile(constants.DISTORTION_MATRIX_FILE, dist)  
  writeArrayToFile(constants.ROTATION_VECTORS_FILE, rvecs)  
  writeArrayToFile(constants.TRANSLATION_VECTORS_FILE, tvecs)  
  writeValueToFile(constants.REPROJECTION_ERROR_FILE, reprojectionError)