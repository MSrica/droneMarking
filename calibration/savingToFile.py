# -*- coding: utf-8 -*-
"""
@author: srica
"""

import numpy as np
import os

import constants

def saveToFile(mtx, dist, rvecs, tvecs):
    if not os.path.exists(constants.VALUES_FOLDER):
      os.makedirs(constants.VALUES_FOLDER)
    
    # to txt   
    with open(constants.CAMERA_MATRIX_FILE, 'w+') as f:
        for line in mtx:
            np.savetxt(f, line, fmt='%.2f')
            
    with open(constants.DISTORTION_MATRIX_FILE, 'w+') as f:
        for line in dist:
            np.savetxt(f, line, fmt='%.2f')
            
    with open(constants.ROTATION_VECTORS_FILE, 'w+') as f:
        for line in rvecs:
            np.savetxt(f, line, fmt='%.2f')
            
    with open(constants.TRANSLATION_VECTORS_FILE, 'w+') as f:
        for line in tvecs:
            np.savetxt(f, line, fmt='%.2f')
            
    
# =============================================================================
#     # to csv
#     import pandas as pd
#     df = pd.DataFrame(data=mtx.astype(float))
#     df.to_csv(constants.CAMERA_MATRIX_FILE, sep=' ', header=False, float_format='%.2f', index=False)
#     
#     df = pd.DataFrame(data=dist.astype(float))
#     df.to_csv(constants.DISTORTION_MATRIX_FILE, sep=' ', header=False, float_format='%.2f', index=False)
#     
#     df = pd.DataFrame(data=rvecs.astype(float))
#     df.to_csv(constants.ROTATION_VECTORS_FILE, sep=' ', header=False, float_format='%.2f', index=False)
#     
#     df = pd.DataFrame(data=tvecs.astype(float))
#     df.to_csv(constants.TRANSLATION_VECTORS_FILE, sep=' ', header=False, float_format='%.2f', index=False)
# =============================================================================
