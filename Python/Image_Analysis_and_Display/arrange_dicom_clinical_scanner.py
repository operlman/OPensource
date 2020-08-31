#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Arranging dicom data from a clinical scanneer
@author: Or Perlman (or@ieee.org)
"""

import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
from os import listdir
import time
import scipy.io as sio

# #################################  Input parameters #################################################
# Number of characters in each dicom filename, excluding the different "minute/sec/ms/..." time-stamp
Last_Im_Indx_Character = 41

im_folder_path = ''

PlotFlag = True
######################################################################################################

long_file_names = listdir(im_folder_path)
num_imgs = len(long_file_names)

# Initialize short names list as a copy of the long one
short_file_names = long_file_names.copy()

# Remove the irrelevant end of the string in each file from Siemens scanner's output
for ind in range(len(long_file_names)):
    short_file_names[ind] = long_file_names[ind][Last_Im_Indx_Character:-4]  # -4 helps when len is not fixed

# Sorting the file names according to rising image numbers
sorted_short_file_names = sorted(short_file_names)

# Creating a new list of sorted long file names (to be used for loading images at the correct order)
final_long_sorted_file_names = sorted_short_file_names.copy()
for ind1 in range(num_imgs):
    for ind2 in range(num_imgs):
        if final_long_sorted_file_names[ind1] == long_file_names[ind2][Last_Im_Indx_Character:-4]:
            final_long_sorted_file_names[ind1] = long_file_names[ind2]

# Reading first image to get its dimensions
raw_data = dicom.dcmread(im_folder_path + '/' + final_long_sorted_file_names[0])
im_1 = np.asarray(raw_data.pixel_array, dtype=float)  # returns a float NumPy array

# Creating a 3D numpy array to hold all sorted images
dataToMatch = np.zeros((num_imgs, im_1.shape[0], im_1.shape[1]))

# Reading all Dicom images into a numpy array and displaying them
Unified_Font_Size = 15
Unified_Colorbar_Label_Size = 15
fig = plt.figure()

im_ind = 0
for cur_file_name in final_long_sorted_file_names:
    DICOM_data = dicom.dcmread(im_folder_path + '/' + cur_file_name)
    dataToMatch[im_ind, :, :] = np.asarray(DICOM_data.pixel_array, dtype=float)  # returns a float NumPy array

    if PlotFlag:
        ax = fig.add_subplot(np.ceil(num_imgs/7), 7, im_ind + 1)
        NRF_plot = plt.imshow(dataToMatch[im_ind, :, :] / np.max(dataToMatch), cmap='gray')
        NRF_plot.set_clim(0.0, 1.0)
        ax.set_title(im_ind, fontsize=Unified_Font_Size)
        ax.set_axis_off()
        ax.set_title(im_ind + 1)
        fig.canvas.draw()

    im_ind = im_ind + 1

if PlotFlag:
    plt.pause(20)

# Saving the images set as .mat for convenient compatibility with both Python and Matlab
sio.savemat('dataToMatch.mat', {'dataToMatch': dataToMatch})
disp('dataset was saved as dataToMatch.mat (format: float)')
