# !/usr/bin/env python3
# -*- coding: utf-8 -*-


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
