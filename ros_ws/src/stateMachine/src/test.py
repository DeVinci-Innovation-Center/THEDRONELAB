import rospy as rp
import smach
import std_msgs
import pycrazyswarm as pcs
import numpy as np

csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"


points = np.genfromtxt(csvpath, delimiter=",") / 10

print(points)

