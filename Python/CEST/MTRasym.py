#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Purpose: calculating MTRasym for CEST data
# Created: Sep. 4, 2020 by Or Perlman (or@ieee.org; operlman@mgh.harvard.edu)
# Changes log:
"""

import numpy as np
import matplotlib.pyplot as plt
from csaps import csaps
import scipy.io as sio


# Utils function - calculating MTR-asymmetry
def mtr_asym(frequency_offsets, si, s0):
    """
    
    :param frequency_offsets: saturation frequency offsets (ppm), e.g.: np.linspace(7, -7, 57)
    :param si: corresonding measured signal intensities (raw)
    :param s0: raw signal intesity with no saturation
    :return: mtr_asym_percent_positive_side - MTR-asymmetry at the positive spectrum side (%)
    :return: mtr_asym_percent_positive_side_csaps - MTR-asymmetry at the positive spectrum side (%)
             after cubic spline approximation interpolation
    :return: freq_offsets_positive_side (ppm)
    :return: freq_offsets_positive_side_csaps (ppm) - interpolated to 5 times number of original points
    """

    z_spectrum = si / s0
    mtr_asym_percent = 100 * (np.flipud(z_spectrum) - z_spectrum)
    mtr_asym_percent_positive_side = mtr_asym_percent[:int((mtr_asym_percent.size - 1) / 2 + 1)]
    freq_offsets_positive_side = frequency_offsets[:int((mtr_asym_percent.size - 1) / 2 + 1)]

    # cubic spline approximation with automaic smoothing parameter
    freq_offsets_positive_side_csaps = np.linspace(freq_offsets_positive_side[0],
                                                   freq_offsets_positive_side[-1],
                                                   5 * np.size(freq_offsets_positive_side))
    y_interpolated_flipped, smooth = \
        csaps(np.flipud(freq_offsets_positive_side),
              np.flipud(mtr_asym_percent_positive_side),
              np.flipud(freq_offsets_positive_side_csaps))  # flipud for rising range
    mtr_asym_percent_positive_side_csaps = np.flipud(y_interpolated_flipped)

    return mtr_asym_percent_positive_side, mtr_asym_percent_positive_side_csaps, freq_offsets_positive_side, \
           freq_offsets_positive_side_csaps



# User input #
##############
subject_code = ''

# Loading input data #
######################
#  b0_corrected_z_images - B0 corrected images(e.g., 64 x 64 x 57) without csaps
#  w_ppm: saturation frequency offsets(ppm)
input_data = sio.loadmat(subject_code + '.mat')
b0_corrected_z_images = input_data['B0_Corrected_Z_Images']
w_ppm = input_data['W_PPM'][:, 0]  # converting to 0d vector for csaps
del input_data

# Calculating MTRasym
MTR_asym_percent_positive_side, MTR_asym_percent_positive_side_csaps, Freq_offsets_positive_side, \
           Freq_offsets_positive_side_csaps = mtr_asym(frequency_offsets=w_ppm,
                                                       si=b0_corrected_z_images[22, 15, :], s0=1)

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

plt.show()
