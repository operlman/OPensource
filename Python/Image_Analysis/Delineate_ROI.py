#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: delineating a mask 
Created on Fri Aug  9 12:42:47 2019
@author: Or Perlman (or@ieee.org)
            Some sub-functions taken from open-source code 
            found online (mentioned when relevant in the script)
Args: Im - input image
      Input_ax - ax of required image to delineate
      Selector_Type - 'Lasso', 'Polygon', 'Circle'
      Pause_Time - maximum time (s) required for image pause (delineation during that time)
      PlotFlag (True / False)
Returns: ROI.npz: ROI['Mask'] -binary mask
                  ROI['verts'] - vertices of ROI (for Polygon or Lasso selector), 
                                                     or
                  ROI['verts_as_mask_border'] (for Circle selector)
"""
from matplotlib.widgets import LassoSelector, PolygonSelector
#, EllipseSelector, RectangleSelector
from pylab import ginput
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage import draw


def Delineate_ROI(Im, Selector_Type = 'Circle', Pause_Time = 10, PlotFlag = True):

    #Getting and saving the vertices of the delineated ROI boundaries 
    def Onselect_Lasso_or_Polygon(verts):
        verts = np.array(verts)
        np.save('ROI',verts)
        print('Please wait until '+str(Pause_Time)+'s are over')
        
    #poly2mask adapted from: https://github.com/scikit-image/scikit-image/issues/1103#issuecomment-52378754
    def poly2mask(vertex_row_coords, vertex_col_coords, shape):
        fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
        mask = np.zeros(shape, dtype=np.bool)
        mask[fill_row_coords, fill_col_coords] = True
        return mask

    #Ploting the raw input image on which the ROI will be delineated
    fig = plt.figure()
    Input_ax = fig.add_subplot(1,1,1)
    Input_plot = plt.imshow(Im, cmap = 'magma')
    Input_plot.set_clim(0,1400)
    plt.colorbar(orientation = 'vertical', fraction = 0.046, pad = 0.04)
    Input_ax.set_title('Input Image')
    
    
    
    #Delineate ROIs using the desired selector type
    if Selector_Type == 'Lasso':
        _tmp = LassoSelector(Input_ax, Onselect_Lasso_or_Polygon)
        plt.pause(Pause_Time) #pause is required for keeping the image available for delination
        
    elif Selector_Type == 'Polygon':
        _tmp = PolygonSelector(Input_ax, Onselect_Lasso_or_Polygon)
        plt.pause(Pause_Time) #pause is required for keeping the image available for delination

    # Inspired by https://stackoverflow.com/questions/44865023/circular-masking-an-image-in-python-using-numpy-arrays
    elif Selector_Type == 'Circle':
        print('Please mark the circle center...')
        Center = np.array(ginput(1))
        Radius = int(input('Thank you. What is the required radius?'))
        Im_H = Im.shape[0]#Image height [pixels]
        Im_W = Im.shape[1]#Image width [pixels]
        Y, X = np.ogrid[:Im_H, :Im_W]
        Dist_from_Center = np.sqrt((X - Center[0][0])**2 + (Y-Center[0][1])**2)
        Mask = Dist_from_Center <= Radius
        verts_as_mask_border = np.round(Dist_from_Center) == Radius
        np.savez('ROI',verts_as_mask_border = verts_as_mask_border,Mask = Mask)
        print('ROI.npy (verts and Mask) saved successfully')
        
    else:
        print('Invalid Selector_Type!')  
        
        
    ######## Arranging saved file if not using circle ROI
    if  Selector_Type!='Circle' : 
        verts = np.load("ROI.npy")
        Mask = poly2mask(verts[:,1], verts[:,0], Im.shape)
        np.savez('ROI',verts = verts,Mask = Mask)
        os.remove('ROI.npy') #removing redundant file
        print('ROI.npy (verts and Mask) saved successfully')
    ##########################################################
    
    if PlotFlag:
        if  Selector_Type=='Circle' : 
            fig = plt.figure()
            Im_ax = fig.add_subplot(1,2,1)
            Im_zero_in_circle = np.copy(Im)
            Im_zero_in_circle[verts_as_mask_border]=0
            Implt = plt.imshow(Im_zero_in_circle,cmap = 'viridis')
            Implt.set_clim(np.min(Im_zero_in_circle),np.max(Im_zero_in_circle))
            plt.colorbar(orientation = 'vertical', fraction = 0.046, pad = 0.04)
            Im_ax.set_title('Im with mask verts')
            
            Masked_Im_ax = fig.add_subplot(1,2,2)
            Masked_Im = np.copy(Im)
            Masked_Im[~Mask]=0
            Masked_plt = plt.imshow(Masked_Im,cmap = 'viridis')
            Masked_plt.set_clim(np.min(Im_zero_in_circle),np.max(Im_zero_in_circle))
            plt.colorbar(orientation = 'vertical', fraction = 0.046, pad = 0.04)
            Masked_Im_ax.set_title('Masked Im')
            plt.show()

        else: #Polygon or lasso has their verts as points instead of masks
            fig = plt.figure()
            Im_ax = fig.add_subplot(1,2,1)
            Implt = plt.imshow(Im,cmap = 'viridis')
            Im_ax.plot(verts[:,0],verts[:,1],color = 'r')
            
            #Connecting last and first points with a line
            Im_ax.plot([verts[-1,0],verts[0,0]],[verts[-1,1],verts[0,1]],color = 'r') 

            Implt.set_clim(np.min(Im),np.max(Im))
            plt.colorbar(orientation = 'vertical', fraction = 0.046, pad = 0.04)
            Im_ax.set_title('Im with mask verts')
            
            Masked_Im_ax = fig.add_subplot(1,2,2)
            Masked_Im = np.copy(Im)
            Masked_Im[~Mask]=0
            Masked_plt = plt.imshow(Masked_Im,cmap = 'viridis')
            Masked_plt.set_clim(np.min(Im),np.max(Im))
            plt.colorbar(orientation = 'vertical', fraction = 0.046, pad = 0.04)
            Masked_Im_ax.set_title('Masked Im')
            plt.show()