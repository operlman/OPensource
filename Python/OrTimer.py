# This script creates a timer
# Created by O.P at 21/12/17 (or@ieee.org)
# Changes log: 

import numpy as np
from threading import Timer
import numpy as np
import datetime
import time
import os #for using the operation system functions from python

print("Current time is:")
print(datetime.datetime.now())
NumMinutes = float(input("Please specify number of minutes to wait: "))

def timeout():

	for ind in range(0,4):
		print('Time is up')
		os.system("espeak 'Time is up'")

# duration is in seconds so I multiply by 60
t = Timer(NumMinutes * 60, timeout)
t.start()


