#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Purpose: Creating MTRasym images
# Created: May 14, 2021, by Or Perlman (or@ieee.org)
"""

import numpy as np
import matplotlib.pyplot as plt
from csaps import csaps
import scipy.io as sio
from Conventional_CEST_Utils import b0_correction, load_arrange_zspec_im, mtr_asym

# User input #
# >>>
FieldStrength = 9.4  # Tesla
Maximum_Ppm_Offset_Non_wassr = 7  # (ppm)
Offset_Interval_Non_Wassr = 0.25  # (ppm)
Pre_Folder_Path = '/media/paul/4d19f9fe-4896-4ccb-8ace-e3d1d12cad65/PostDoc/Data/CEST/Phantoms/L_arg/' \
                  'AutoCEST_Mar_2021/20210319_082635_Larg_Phantom_pH5_5p5_6_a_1_1/'
Scan_Folder_Num = 14
Im_Dim = 64  # e.g 64 for a 64x64 image
# <<<

# Load and arrange Z-spectrm images
MainFieldMHz = np.round(FieldStrength * 42.5764)  # (MHz)
W_PPM, Z_Ims_Plus_to_Minus = load_arrange_zspec_im(Maximum_Ppm_Offset_Non_wassr, Offset_Interval_Non_Wassr,
                                                   Pre_Folder_Path, Scan_Folder_Num,
                                                   Im_Dim)
# B0 correction
B0_Map = sio.loadmat('Wasser_B0.mat')['Wasser_B0']
W_Hz = W_PPM * FieldStrength * 42.5764
B0_Corrected_Imgs = b0_correction(B0_Map, Z_Ims_Plus_to_Minus, W_Hz)

#  single pixel MTRasym calculation
# >>>
W_PPM = W_PPM[:, 0]  # converting to 0d vector for csaps
MTR_asym_percent_positive_side, MTR_asym_percent_positive_side_csaps, Freq_offsets_positive_side, \
Freq_offsets_positive_side_csaps = mtr_asym(frequency_offsets=W_PPM,
                                            si=B0_Corrected_Imgs[40, 40, :], s0=1)

# Plotting
mtr_fig = plt.figure()
mtr_ax = mtr_fig.add_subplot(1, 2, 1)
plt.plot(Freq_offsets_positive_side, MTR_asym_percent_positive_side, '-xr')
plt.gca().invert_xaxis()
mtr_ax.set_xlabel('w (ppm)')
mtr_ax.yaxis.tick_right()
mtr_ax.yaxis.set_label_position("right")
mtr_ax.set_ylabel('MTR$_{asym}$ (%)')

mtr_csaps_ax = mtr_fig.add_subplot(1, 2, 2)
plt.plot(Freq_offsets_positive_side_csaps, MTR_asym_percent_positive_side_csaps, '-ob')
plt.gca().invert_xaxis()
mtr_csaps_ax.set_xlabel('w (ppm)')
mtr_csaps_ax.yaxis.tick_right()
mtr_csaps_ax.yaxis.set_label_position("right")
mtr_csaps_ax.set_ylabel('MTR$_{asym}$ after csaps (%)')

# <<<

# Full image MTRasym
# >>>
mtr_asym_per_pixel = np.zeros((Im_Dim, Im_Dim, np.int((B0_Corrected_Imgs.shape[2] + 1) / 2)))   # e.g 64 x 64 x 29
for r_ind in range(Im_Dim):
    for c_ind in range(Im_Dim):
        mtr_asym_per_pixel[r_ind, c_ind, :], _, _, _ = mtr_asym(frequency_offsets=W_PPM,
                                                                si=B0_Corrected_Imgs[r_ind, c_ind, :], s0=1)


# Plotting
mtr_im_fig = plt.figure()
mtr_im_ax = mtr_im_fig.add_subplot(1, 1, 1)
plt.imshow(mtr_asym_per_pixel[:, :, np.int(np.nonzero(Freq_offsets_positive_side == 3)[0])], cmap='viridis',
           clim=[20, 50])
plt.title('MTR_{asym} (%)')
plt.colorbar()
plt.show()
