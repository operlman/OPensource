#!/usr/bin/env python3
# Automatic masking of image borders using Otsu thresholding and hole filling
# Created on June 29, 2020 by Or Perlman (or@ieee.org)
# Note that some 3rd party codes was used as specified throughout the script
# -*- coding: utf-8 -*-

import numpy as np
from scipy import misc, ndimage
import matplotlib.pyplot as plt
from skimage import filters
from skimage.morphology import reconstruction


def fill_binary_im_holes(binary_im):
    # Filling holes in binary image
    # https://stackoverflow.com/questions/36294025/python-equivalent-to-matlab-funciton-imfill-for-grayscale

    seed = np.ones(np.shape(binary_im))
    binary_im[:, 0] = 0
    binary_im[:, -1] = 0
    binary_im[0, :] = 0
    binary_im[-1, :] = 0
    seed[:, 0] = 0
    seed[:, -1] = 0
    seed[0, :] = 0
    seed[-1, :] = 0
    filled_binary_im = reconstruction(seed, binary_im, method='erosion')

    return filled_binary_im


def mask_background(orig_image, plot_flag):
    """
    :param orig_image: original image (ndarray of any type)
    :param plot_flag: (logical)
    :return: background_mask (logical, background=True)
    :return: masked_im (masked image)
    """

    # Converting rgb2gray if required
    if len(orig_image.shape) == 3:  # if rgb or rgba image it has a 3rd dimension
        gray_im = np.dot(orig_image[..., :3], [0.299, 0.587, 0.114])
    else:
        gray_im = np.copy(orig_image)

    # Otsu thresholding
    otsu_threshold = filters.threshold_otsu(gray_im)
    mask_with_holes = gray_im < otsu_threshold

    # Fill holes
    background_mask = fill_binary_im_holes(mask_with_holes * 1)  # * 1 for casting logical to int

    # Masking the input image
    if len(np.shape(orig_image)) > 2:  # Adding a dimension to the mask for broadcasting a color image
        masked_im = orig_image * background_mask[..., np.newaxis]
    else:
        masked_im = orig_image * background_mask

    if orig_image.dtype == 'uint8':
        masked_im = np.uint8(masked_im)

    if plot_flag:
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 3, 1)
        plt.title('Original Image')
        ax1.imshow(orig_image)

        ax2 = fig.add_subplot(1, 3, 2)
        ax2.imshow(background_mask, cmap='gray')
        plt.title('Background Mask')

        ax4 = fig.add_subplot(1, 3, 3)
        ax4.imshow(masked_im, cmap='viridis')
        plt.title('Masked Image')
        plt.show()

    return background_mask, masked_im
