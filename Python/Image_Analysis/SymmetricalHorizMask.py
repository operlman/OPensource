#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Creating an horizontally symetrical mask
Created on Tue Sep 24 13:57:40 2019
%------------------------input variables-------------------------------------%
% Im - the original image on which the mask was created
% Mask - original mask
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% SymmetHorMask - a horizontally symmetrical logica mask (for the input one)
% Symmet_verts - the vertices of the horiztonal symmetrical mask borders
%----------------------------------------------------------------------------%

@author: Or Perlman (or@ieee.org; operlman@mgh.harvard.edu)
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_erosion

def SymmetricalHorizMask(Im, Mask):

    #Ploting the input image and the Mask on it
    
    Im_With_Mask_Zeroed = np.copy(Im)
    Im_With_Mask_Zeroed[Mask] = 0
    fig=plt.figure(figsize=(40, 20))
    Im_ax = fig.add_subplot(1, 1, 1)
    plt.imshow(Im_With_Mask_Zeroed, cmap = 'hot')
    Im_ax.set_title('Input image with mask as 0', fontsize=10)
    Im_ax.set_axis_off()


    #Delineating the center of symmetry
    print('Please mark the center of symmetry...')
    Coordinates = plt.ginput(1)
    col_center = Coordinates[0][0]

    col_center=np.round(col_center); #rounding (pixel location)
    print('Thank you')
    
    #Initizalizing new mask
    SymmetHorMask=np.zeros((Mask.shape[0],Mask.shape[1]),dtype = bool);
    
    #Coordinates of mask pixels
    FoundIndices = np.where(Mask)
    row_orig = FoundIndices[0]
    col_orig = FoundIndices[1]

    #Creating horizontally mirrored mask
    for ind in range(row_orig.size):
    
        #Calculating horizontal distance between current mask pixel and the
        #   reference center
        CurDist=col_orig[ind]-col_center
    
        #Filling new pixel in the mirrored mask
        SymmetHorMask[row_orig[ind],int(col_center-CurDist)]=True
        
    
    #Getting the boundaries of the mirrored mask
    ###########################################
    #Morphogical erosion of the new mask to get only the inner parts
    ErodedIm = binary_erosion(SymmetHorMask.astype(int), structure = np.ones((3,3))).astype(int)
    BorderIm = SymmetHorMask.astype(int) - ErodedIm
    
    Symmet_verts = np.where(BorderIm)

    Im_With_Mask_Zeroed[SymmetHorMask==True] = 0
    plt.imshow(Im_With_Mask_Zeroed, cmap = 'hot')
    Im_ax.set_title('Mask and its reflection zeroed', fontsize=10)
    Im_ax.set_axis_off()


    return SymmetHorMask, Symmet_verts
    
