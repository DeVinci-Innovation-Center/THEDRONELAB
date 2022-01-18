import rospy
import numpy as np
import time
from scripts.pycrazyswarm.crazyflie import Crazyflie

rospy.init_node("CrazyflieDecentralized", anonymous=True)

# logic to identify the id
cfid = rospy.get_param("cfid")

startpos = np.array([0, 0, 0])

cf = Crazyflie(1, startpos, 2)

steps = 0
st = 0.05
r = 0
dir = 0.1
maxr = 3
minr = 0.0
while not rospy.is_shutdown():
    if r < maxr and dir > 0:
        r += dir
    else:
        dir *= -1
    if r > minr and dir < 0:
        r += dir
    else:
        dir *= -1
    steps += st
    pos = startpos + np.array([r*np.cos(steps), r*np.sin(steps), steps])
    cf.cmdPosition(pos)
    time.sleep(0.4)
