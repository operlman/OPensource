# This script creates a timer
# Created by O.P at 21/12/17 (or@ieee.org)
# Changes log: 

from threading import Timer
import matplotlib.pyplot as plt
import datetime
import os #for using the operation system functions from python

print("Current time is:")
print(datetime.datetime.now())
NumMinutes = float(input("Please specify number of minutes to wait: "))

def timeout():
    #ploting T
    
    fig = plt.imshow([[1,1,1],[0,1,0]])
    plt.colorbar(ticks=[0,0.5,1],orientation = 'vertical')
    fig.set_cmap('Blues')
    plt.axis('off')
    plt.show()
    
    for ind in range(0,4):
        print('Time is up')
        os.system("espeak 'Time is up'")

    
# duration is in seconds so I multiply by 60
t = Timer(NumMinutes * 60, timeout)
t.start()


