# -*- coding: utf-8 -*-

#--------------------------------------------------------------------#
#                                                                    #
# Copyright (C) 2018 HOLOEYE Photonics AG. All rights reserved.      #
# Contact: https://holoeye.com/contact/                              #
#                                                                    #
# This file is part of HOLOEYE SLM Display SDK.                      #
#                                                                    #
# You may use this file under the terms and conditions of the        #
# "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
#                                                                    #
#--------------------------------------------------------------------#


# Calculates a lens using numpy and show it on the SLM.

import sys, time, math

# Import the SLM Display SDK:
import detect_heds_module_path
from holoeye import slmdisplaysdk

if not slmdisplaysdk.supportNumPy:
    print("Please install numpy to make this example work on your system.")
    sys.exit()

# Import numpy for matrix multiplication:
import numpy as np

# Make some enumerations available locally to avoid too much code:
ErrorCode = slmdisplaysdk.SLMDisplay.ErrorCode
ShowFlags = slmdisplaysdk.SLMDisplay.ShowFlags

# Detect SLMs and open a window on the selected SLM:
slm = slmdisplaysdk.SLMDisplay()

# Open the SLM preview window (might have an impact on performance):
slm.utilsSLMPreviewShow()

# Configure the lens properties:
innerRadius = slm.height_px / 3
centerX = 0
centerY = 0

# Calculate the phase values of a lens in a pixel-wise matrix:

pixel_size = slm.pixelsize_um

# pre-calc. helper variables:
phaseModulation = 2*math.pi
n_x =  slm.width_px
n_y = slm.height_px

size_x = n_x*pixel_size
size_y = n_y*pixel_size




x = np.linspace(-size_x/2., size_x/2, n_x)
y = np.linspace(-size_y/2., size_y/2, n_y)

X, Y = np.meshgrid(x, y, indexing='ij')

#focal length in microns
f = 200000

#wavelength in microns
wavelength = 0.633

lens_phase = 2*np.pi/wavelength*np.sqrt(X**2+Y**2+f**2) % (2*np.pi)


phaseData = slmdisplaysdk.createFieldSingle(n_x, n_y)

for y in range(n_y):
    row = phaseData[y]
    for x in range(n_x):
        row[x] = lens_phase[x, y]


error = slm.showPhasevalues(phaseData)

assert error == ErrorCode.NoError, slm.errorString(error)

# If your IDE terminates the python interpreter process after the script is finished, the SLM content
# will be lost as soon as the script finishes.

# You may insert further code here.

# Wait a few seconds:
time.sleep(4)

# Unloading the SDK may or may not be required depending on your IDE:
slm.release()
