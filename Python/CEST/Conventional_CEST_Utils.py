#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Purpose: conventional CEST functions Utils file, including:
    1) load_arrange_zspec_im
    2) b0_correction
    3) mtr_asym
# Created: May 14, 2021, by Or Perlman (or@ieee.org)
"""

import numpy as np
import matplotlib.pyplot as plt
from csaps import csaps
import scipy.io as sio
import pydicom as dcm
import scipy.interpolate as interpolate


def load_arrange_zspec_im(maximum_ppm_offset_non_wassr, offset_interval_non_wassr, pre_folder_path, scan_folder_num,
                          im_dim):
    """
    :param maximum_ppm_offset_non_wassr:  maximum z-spectrum frequency offset (e.g. 7 ppm)
    :param offset_interval_non_wassr:  offset interval - e.g. 0.25 ppm
    :param pre_folder_path: folder to data (excluding protocol number) (str)
    :param scan_folder_num: scan folder number (int)
    :param im_dim: dimension in pixels of the squared image (e.g. 64)
    :return: w_ppm - saturation frequency offset (e.g. 7, 6.75, ..., 0, -0.25, ... -7)
             z_ims_plus_to_minus - z-spectrum images that correspont to w_x ~[0, 1], e.g. shape (64, 64, 57)
    """

    # Orgainizing a few variables and info
    num_offsets_non_wassr = np.size(np.arange(-maximum_ppm_offset_non_wassr, maximum_ppm_offset_non_wassr +
                                              offset_interval_non_wassr, offset_interval_non_wassr))
    additional_dicom_path = '/pdata/1/dicom/'  # Standard dicom path suffix
    full_path = pre_folder_path + str(scan_folder_num) + additional_dicom_path

    # Loading raw z-spectrum data
    # Arranging the images from -X ppm to X ppm (e.g. X=7)
    raw_im = np.zeros((num_offsets_non_wassr + 1, im_dim, im_dim))

    for ind in range(num_offsets_non_wassr + 1):  # + 1 due to  M0 im
        if ind + 1 < 10:
            raw_im[ind, :, :] = np.float64(dcm.dcmread(full_path + 'MRIm0' + np.str(ind + 1) + '.dcm').pixel_array)
        else:
            raw_im[ind, :, :] = np.float64(dcm.dcmread(full_path + 'MRIm' + np.str(ind + 1) + '.dcm').pixel_array)

    #  Not using first scanned image (very far offset saturaion - 5000 ppm)
    normalization_im = np.copy(raw_im[0, :, :])

    # Z imagesc (normalized by M0)
    z_imgs = np.copy(raw_im[1:, :, :]) / normalization_im

    # 1-dim offsetlist (ppm)
    pos_w_x = np.arange(maximum_ppm_offset_non_wassr, 0 - offset_interval_non_wassr,
                        -offset_interval_non_wassr).reshape(-1,
                                                            1)  # maximum_ppm_offset_non_wassr
    # :-offset_interval_non_wassr:0

    neg_w_x = -pos_w_x[0:-1].reshape(-1, 1)  # -pos_w_x(1:end-1);%0 offset was scanned once, hence the end-1
    w_ppm = np.vstack((pos_w_x, np.flipud(neg_w_x)))  # [pos_w_x.';flipud(neg_w_x.')];% (5, 4.75,...0,-0.25,....-5)

    #  Re-ordering Z_ims to correspond to w_x from -5 to 5 ppm
    z_ims_plus_to_minus = np.zeros((im_dim, im_dim, num_offsets_non_wassr))  # e.g. 64 x 64 x 57
    three_d_mat_ind = 0
    for orig_ind in np.arange(0, num_offsets_non_wassr, 2):
        z_ims_plus_to_minus[:, :, three_d_mat_ind] = z_imgs[orig_ind, :, :]
        three_d_mat_ind = three_d_mat_ind + 1

    for orig_ind in np.arange(num_offsets_non_wassr - 2, 1 - 2, -2):  # flipping cell order for negative side
        z_ims_plus_to_minus[:, :, three_d_mat_ind] = z_imgs[orig_ind, :, :]
        three_d_mat_ind = three_d_mat_ind + 1

    return w_ppm, z_ims_plus_to_minus


# # User input #
# # >>>
# FieldStrength = 9.4  # Tesla
# Maximum_Ppm_Offset_Non_wassr = 7  # (ppm)
# Offset_Interval_Non_Wassr = 0.25  # (ppm)
# Pre_Folder_Path = '/media/paul/4d19f9fe-4896-4ccb-8ace-e3d1d12cad65/PostDoc/Data/CEST/Phantoms/L_arg/' \
#                   'AutoCEST_Mar_2021/20210319_082635_Larg_Phantom_pH5_5p5_6_a_1_1/'
# Scan_Folder_Num = 14
# Im_Dim = 64  # e.g 64 for a 64x64 image
# # <<<
#
# # Example run
# MainFieldMHz = np.round(FieldStrength * 42.5764)  # (MHz)
# W_X, Z_Ims_Plus_to_Minus = load_arrange_zspec_im(Maximum_Ppm_Offset_Non_wassr, Offset_Interval_Non_Wassr,
#                                                  Pre_Folder_Path, Scan_Folder_Num,
#                                                  Im_Dim)


def b0_correction(b0_map, original_images, w_hz):
    """
    :param b0_map: (Hz), optimally from a WASSR scan
    :param original_images (3D array, row x col x num_images)
    :param w_hz: saturation frequency offsets (Hz)
    :return: b0_corrected_images (3D array, row x col x num_images)
    """

    # Initialization
    b0_corrected_images = np.zeros(np.shape(original_images))

    for r_ind in np.arange(original_images.shape[0]):
        for c_ind in range(original_images.shape[1]):

            # Current pixel original z-spectrum
            cur_pixel_orig_z_vec = original_images[r_ind, c_ind, :].reshape(-1, 1)

            # Current pixel B0 shift (Hz)
            cur_pixel_b0 = b0_map[r_ind, c_ind]

            # Correcting current pixel if B0 shift is not zero
            if cur_pixel_b0 != 0:
                # Cubic spline interpolation (initially flipping for splrep compatibility)
                tck = interpolate.splrep(np.flipud(w_hz - cur_pixel_b0), np.flipud(cur_pixel_orig_z_vec), s=0)
                b0_corrected_images[r_ind, c_ind, :] = np.squeeze(interpolate.splev(w_hz, tck, der=0))

    return b0_corrected_images


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

# # User input #
# ##############
# subject_code = ''
#
# # Loading input data #
# ######################
# #  b0_corrected_z_images - B0 corrected images(e.g., 64 x 64 x 57) without csaps
# #  w_ppm: saturation frequency offsets(ppm)
# input_data = sio.loadmat(subject_code + '.mat')
# b0_corrected_z_images = input_data['B0_Corrected_Z_Images']
# w_ppm = input_data['W_PPM'][:, 0]  # converting to 0d vector for csaps
# del input_data
#
# # Calculating MTRasym
# MTR_asym_percent_positive_side, MTR_asym_percent_positive_side_csaps, Freq_offsets_positive_side, \
#            Freq_offsets_positive_side_csaps = mtr_asym(frequency_offsets=w_ppm,
#                                                        si=b0_corrected_z_images[22, 15, :], s0=1)
#
# # Plotting
# mtr_fig = plt.figure()
# mtr_ax = mtr_fig.add_subplot(1, 2, 1)
# plt.plot(Freq_offsets_positive_side, MTR_asym_percent_positive_side, '-xr')
# plt.gca().invert_xaxis()
# mtr_ax.set_xlabel('w (ppm)')
# mtr_ax.yaxis.tick_right()
# mtr_ax.yaxis.set_label_position("right")
# mtr_ax.set_ylabel('MTR$_{asym}$ (%)')
#
# mtr_csaps_ax = mtr_fig.add_subplot(1, 2, 2)
# plt.plot(Freq_offsets_positive_side_csaps, MTR_asym_percent_positive_side_csaps, '-ob')
# plt.gca().invert_xaxis()
# mtr_csaps_ax.set_xlabel('w (ppm)')
# mtr_csaps_ax.yaxis.tick_right()
# mtr_csaps_ax.yaxis.set_label_position("right")
# mtr_csaps_ax.set_ylabel('MTR$_{asym}$ after csaps (%)')
#
# plt.show()
