#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: calculating statistics in ROI
Created on Thu Sep 12 14:10:08 2019
@author: Or Perlman (or@ieee.org)
Args: Im - image
      ROI_Mask - as a binary mask with the same shape as Im
      Print_Flag (Binary for printing mean and std)
Returns: mean, std, min, max, ROI_Values_Flattened for the given ROI
"""
import numpy as np

def Calc_Stat_in_ROI(Im, ROI_Mask, Print_Flag = True):
    
    ROI_mean = np.mean(Im[ROI_Mask])
    ROI_std = np.std(Im[ROI_Mask])
    ROI_min = np.amin(Im[ROI_Mask])
    ROI_max = np.amax(Im[ROI_Mask])
    ROI_Values_Flattened = Im[ROI_Mask].flatten('F') # F -> fortran-like (columns order)
    
    if Print_Flag:
        print("ROI mean\u00B1std: %.1f\u00B1%.1f" %(ROI_mean, ROI_std)) # \u00B1 = (plus-minus sign)
        
    return ROI_mean, ROI_std, ROI_min, ROI_max, ROI_Values_Flattened
