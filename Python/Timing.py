#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 09:54:48 2019
Purpose: Timing some script in python
@author: Or Perlman (or@ieee.org)
"""
import time

#Storing the training time
t0 = time.time()

# ----------------------------- #

#   The script body goes here   #

# ----------------------------- #

RunTime = time.time() - t0

#%Displaying the runtime:
if RunTime<60: #if less than a minute 
	print('RunTime = '+str(RunTime)+' sec')
elif RunTime<3600: # if less than an hour
	print('RunTime = '+str(RunTime/60.0)+' min')
else: # If took more than an hour
	print('RunTime = '+str(RunTime/3600.0),' hour')	
