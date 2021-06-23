#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Purpose: Converting mosaic image data into 3D
# Created: June 23, 2021, by Or Perlman (or@ieee.org)
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


def convert_mosaic_to_3d(mosaic_data, iterations=10, num_images_per_mosaic_dim=10, plot_flag=True):
    """
    # Converting mosaic data into 3d
    :param mosaic_data: image mosaic with shape (iterations, mosaic_dim, mosaic_dim) -> (e.g., 81 x 1160 x 1160)
    :param iterations: number of temporal iterations of the data (e.g. points on z-spectra, MRF raw iterations, etc.
    :param num_images_per_mosaic_dim: int (e.g. 10)
    :param plot_flag
    :return: organized_4d_stack (e.g. of shape 81 x 100 x 116 x 116
    """
    mosaic_dim = np.shape(mosaic_data)[1]  # e.g. 1160

    # Single organized image size
    single_dim_organized_size = mosaic_dim / num_images_per_mosaic_dim  # e.g. 1160 / 10 = 116
    assert (np.round(single_dim_organized_size) == single_dim_organized_size)
    single_dim_organized_size = int(single_dim_organized_size)

    organized_4d_stack = np.zeros((iterations, num_images_per_mosaic_dim ** 2, single_dim_organized_size,
                                   single_dim_organized_size))
    print('size of organized_4d_stack = ' + str(np.shape(organized_4d_stack)))

    for iter_ind in range(iterations):
        im_ind = 0
        for new_r_ind in range(num_images_per_mosaic_dim):
            for new_c_ind in range(num_images_per_mosaic_dim):
                cur_im = mosaic_data[iter_ind, new_r_ind * single_dim_organized_size: new_r_ind *
                                                                                      single_dim_organized_size +
                                                                single_dim_organized_size, new_c_ind *
                                                                                            single_dim_organized_size:
                                                                                            new_c_ind *
                                                                                            single_dim_organized_size
                                                                                            + single_dim_organized_size]

                organized_4d_stack[iter_ind, im_ind, :, :] = np.copy(cur_im)
                im_ind = im_ind + 1

    if plot_flag:
        fig = plt.figure()
        for ind in range(np.shape(organized_4d_stack)[2]):
            plt.imshow(organized_4d_stack[0, :, ind, :])
            plt.title(str(ind))
            plt.pause(0.3)
            fig.canvas.draw()
    return organized_4d_stack
