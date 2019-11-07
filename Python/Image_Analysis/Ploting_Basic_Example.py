#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: matplotlib image "ploting" example/template
Created: Nov 7, 2019
Author: Or Perlman (or@ieee.org)
"""

import numpy as np
import matplotlib.pyplot as plt

# General unified ploting parameters
Unified_Font_Size = 25
Unified_Colorbar_Label_Size = 10

# General data folder path
Data_Folder_Path = '...'

fig = plt.figure(figsize=(40, 20))

# Ploting T1/T2 images
for Slice_Ind in np.arange(np.shape(T2map)[1]):
	Slice_Ind = 50
	plt.suptitle('Slice = '+str(Slice_Ind))
	T1_ax = fig.add_subplot(1, 2, 1)
	T1_plot = plt.imshow(T1map[:, Slice_Ind, :], cmap='jet')
	T1_plot.set_clim(0.0, 2500.0)
	T1_ax.set_title('T1 (ms)', fontsize=Unified_Font_Size)
	cb = plt.colorbar(ticks=np.arange(0.0, 2500+500, 500), orientation='vertical', fraction=0.046, pad=0.04)
	cb.ax.tick_params(labelsize=Unified_Colorbar_Label_Size)

	T2_ax = fig.add_subplot(1, 2, 2)
	T2_plot = plt.imshow(T2map[:, Slice_Ind, :], cmap='jet')
	T2_plot.set_clim(0.0, 120.0)
	T2_ax.set_title('T2 (ms)', fontsize=Unified_Font_Size)
	cb = plt.colorbar(ticks=np.arange(0.0, 120+40, 40), orientation='vertical', fraction=0.046, pad=0.04)
	cb.ax.tick_params(labelsize=Unified_Colorbar_Label_Size)
	plt.pause(180)
	fig.canvas.draw() 

