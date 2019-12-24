"""
Created: Dec. 23, 2019
Purpose: Overlaying an image over another with transparency
Notes: Saving to buffer was inspired by https://stackoverflow.com/questions/8598673
Author: Or Perlman (or@ieee.org; operlman@mgh.harvard.edu)
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy
from PIL import Image
import PIL
import io


def im_overlay(back_im, back_cmap, back_clim, front_im, front_cmap,
               front_clim, transparency_percent, mask, trans_background_flag=False):
    """
    :param back_im: background image (2D float np.array)
    :param back_cmap: background image colormap (e.g. 'gray')
    :param back_clim: float tuple (cmap_min, cmap_max)
    :param front_im: image to overlay (2D float np.array)
    :param front_cmap: overlayed image colormap (e.g. 'viridis')
    :param front_clim: float tuple (cmap_min, cmap_max)
    :param transparency_percent: 0-100 % (0 is fully opaque)
    :param mask: 2D float np.array
    :param trans_background_flag: if True, than  backgruond image will be (100-transparency_percent) transparent
    :return: A overlayed_image.png image will be saved in the current directory
    """

    # Ploting the two input images and ROI
    fig = plt.figure(figsize=(20, 40))
    ax_back = fig.add_subplot(1, 3, 1)
    plt.imshow(back_im, clim=back_clim, cmap=back_cmap)
    ax_back.set_title('Background Im')
    plt.colorbar(fraction=0.046, pad=0.04)

    ax_front = fig.add_subplot(1, 3, 2)
    plt.imshow(front_im, clim=front_clim, cmap=front_cmap)
    ax_front.set_title('Front Im')
    plt.colorbar(fraction=0.046, pad=0.04)

    ax_mask = fig.add_subplot(1, 3, 3)
    plt.imshow(mask, cmap='gray')
    ax_mask.set_title('Boolean mask')
    plt.show()

    # converting images to RGBA (RGB with transparency alpha layer)
    # 100% transparent => alpha set to 0, fully opaque => alpha = 255
    # Ploting is only performed for the sake of data conversion without showing
    # RGBA background image
    fig = plt.figure(frameon=False)
    fig.set_size_inches(20, 20)  # Modify this if required
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(back_im, clim=back_clim, cmap=back_cmap)
    buf = io.BytesIO()  # For saving to buffer (https://stackoverflow.com/questions/8598673)
    plt.savefig(buf, bbox_inchs='tight', format='png')
    buf.seek(0)
    rgb_back_im = Image.open(buf)
    rgba_back_im = rgb_back_im.copy()
    rgba_back_im.putalpha(int(255))  # Adding alpha layer, but image is still fully opaque
    buf.close()

    # RGBA front image
    fig = plt.figure(frameon=False)
    fig.set_size_inches(20, 20)  # Modify this if required
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(front_im, clim=front_clim, cmap=front_cmap)
    buf = io.BytesIO()  # For saving to buffer (https://stackoverflow.com/questions/8598673)
    plt.savefig(buf, bbox_inchs='tight', format='png')
    buf.seek(0)
    rgb_front_im = Image.open(buf)
    rgba_front_im = rgb_front_im.copy()
    rgba_front_im.putalpha(int(255))  # Adding alpha layer, but image is still fully opaque
    buf.close()

    # Converting the mask to the same size as other images
    fig = plt.figure(frameon=False)
    fig.set_size_inches(20, 20)  # Modify this if required
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(mask, cmap='gray')
    buf = io.BytesIO()  # For saving to buffer (https://stackoverflow.com/questions/8598673)
    plt.savefig(buf, bbox_inchs='tight', format='png')
    buf.seek(0)
    rgb_mask = Image.open(buf)
    rgb_mask = np.array(rgb_mask)  # Converting to numpy (still rgb shape) array
    mask_gray = np.dot(rgb_mask[..., :3], [0.299, 0.587, 0.114])  # Converting to gray
    mask_2d_correct_shape_boolean = mask_gray > 0

    buf.close()

    # Setting desired transparency for ROI in background image (opposite of the front transparancy)
    transparent_back_im = np.array(rgba_back_im)

    if trans_background_flag:
        helper = transparent_back_im[mask_2d_correct_shape_boolean]  # finding the 4D pixels that belong to the mask
        helper[:, 3] = int(transparency_percent / 100 * 255)  # 100% transparent => alpha set to 0, fully opaque => 255
        transparent_back_im[mask_2d_correct_shape_boolean] = helper

    # Setting desired transparency for ROI in front image
    transparent_front_im = np.array(rgba_front_im)
    helper = transparent_front_im[mask_2d_correct_shape_boolean]  # finding the 4D image pixels that belong to the mask
    helper[:, 3] = int((100 - transparency_percent) / 100 * 255)  # 100% transparent alpha 0, fully opaque alpha = 255
    transparent_front_im[mask_2d_correct_shape_boolean] = helper

    # Setting all non-ROI pixels to fully transparent in the front image
    helper = transparent_front_im[~mask_2d_correct_shape_boolean]  # finding the 4D image pixels that belong to the mask
    helper[:, 3] = 0  # 100% transparent => alpha set to 0, fully opaque => alpha = 255
    transparent_front_im[~mask_2d_correct_shape_boolean] = helper

    # Re-converting the transparent front and back images to PIL Image type
    transparent_back_im = PIL.Image.fromarray(transparent_back_im)
    transparent_front_im = PIL.Image.fromarray(transparent_front_im)

    overlayed_image = PIL.Image.alpha_composite(transparent_back_im, transparent_front_im)
    # overlayed_image.show()
    overlayed_image.save('overlayed_image.png')
    print('\noverlayed_image.png was successfully saved')

    return 0


# Example run
# Background image (T2 map)
T2_im = sio.loadmat('B1L1T2/Ground_Truth_Maps.mat')['GT_T2']  # shape = 64, 64
T2_cmap = 'gray'
T2_clim = (0, 110)

# Front im (MTR assymetry at 3.5 uT)
MTR_im = sio.loadmat('B1L1T2/MTRasym_per_B1Batch1_LRP_1_day_18')['MTRasym_per_B1'][:, :, 1]  # MTR for 3.5 uT B1
MTR_cmap = 'inferno'
MTR_clim = (0, 4)

# ROI mask
# ROI_mask = sio.loadmat('B1L1T2/ROI_Mask.mat')['ROI_Mask']
ROI_mask = sio.loadmat('B1L1T2/Brain_Mask.mat')['Brain_Mask']

ROI_mask = ROI_mask > 0  # converting to boolean

im_overlay(back_im=T2_im, back_cmap=T2_cmap, back_clim=T2_clim, front_im=MTR_im, front_cmap=MTR_cmap,
           front_clim=MTR_clim, transparency_percent=80, mask=ROI_mask, trans_background_flag=False)
