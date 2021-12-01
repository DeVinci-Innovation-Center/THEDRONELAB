import rospy as rp
import smach
import std_msgs
import pycrazyswarm as pcs
import numpy as np

print("starting")
mydrone = pcs.Crazyswarm()
print("swarm aquired")
timeHelper = mydrone.timeHelper
allcfs = mydrone.allcfs 

