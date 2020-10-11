#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Image registration using pyelastix (https://github.com/almarklein/pyelastix)
Based on example.py in https://github.com/almarklein/pyelastix
Modified by Or Perlman (or@ieee.org) on Oct. 10, 2020
"""

import pyelastix
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

# Load T1/dataToMatch maps
t1 = np.array(sio.loadmat('T1_map.mat')['T1_map']).astype('float32', order='C')
dataToMatch = np.array(sio.loadmat('dataToMatch.mat')['dataToMatch']).astype('float32', order='C')
dataToMatch = dataToMatch[15, :, :]

# Get default params and adjust
params = pyelastix.get_default_params()
params.NumberOfResolutions = 2
params.FixedInternalImagePixelType = "float"
params.FMovingInternalImagePixelType = "float"
params.UseDirectionCosines = "true"
params.Registration = "MultiResolutionRegistration"
params.Interpolator = "BSplineInterpolator"
params.ResampleInterpolator = "FinalBSplineInterpolator"
params.RResampler = "DefaultResampler"
params.FixedImagePyramid = "FixedRecursiveImagePyramid"
params.MovingImagePyramid = "MovingRecursiveImagePyramid"
params.Optimizer = "AdaptiveStochasticGradientDescent"
params.Transform = "EulerTransform"
params.Metric = "AdvancedMattesMutualInformation"
params.AutomaticScalesEstimation = "true"
params.AutomaticTransformInitialization = "true"
params.HowToCombineTransforms = "Compose"
params.NumberOfHistogramBins = 16
params.ErodeMask = "false"
params.MaximumNumberOfIterations = 200
params.NumberOfSpatialSamples = 4000
params.NewSamplesEveryIteration = "true"
params.ImageSampler = "Random"
params.FinalBSplineInterpolationOrder = 3
# print(params)

# >>> Register >>>
# Perform the registration of dataToMatch to t1
# field is a tuple with arrays describing the deformation for each dimension (x-y-z order, in world units)
reg_dataToMatch, field = pyelastix.register(dataToMatch, t1, params)
# <<< Register <<<

# build an RGB image with the unregistered sequence
combined_im = np.zeros((128, 128, 3))
combined_im[..., 0] = reg_dataToMatch/np.max(reg_dataToMatch)
combined_im[..., 1] = t1/np.max(t1)
combined_im[..., 2] = t1/np.max(t1)

# Visualize the result
fig = plt.figure(1)
plt.clf()
plt.subplot(231)
plt.imshow(t1, clim=(800, 3000))
plt.title('Original fixed image')
plt.subplot(232)
plt.imshow(dataToMatch)
plt.title('Original image to register')
plt.subplot(233)
plt.imshow(reg_dataToMatch)
plt.title('Registered image')
plt.subplot(234)
plt.imshow(combined_im)
plt.title('Combined image (to show differences)')
plt.subplot(235)
plt.imshow(field[0])
plt.title('Field[0]')
plt.subplot(236)
plt.imshow(field[1])
plt.title('Field[1]')
plt.show()
