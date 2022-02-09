#!/usr/bin/env python
import rospy
import numpy as np
import time
import sys
from pycrazyswarm import *


def main():
    rospy.init_node("CrazyflieDecentralized", anonymous=True)

    # logic to identify the id
    try:
        cfid = rospy.get_param("~cfid")
        print("got param cfid", cfid)
    except Exception:
        cfid = 1
    cs = Crazyswarm(crazyflies_yaml="/home/orca/dvic/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml", args=sys.argv)
    timeHelper = cs.timeHelper
    print("created crazyflie")
    for drone in cs.allcfs.crazyflies:
        if drone.id == cfid:
            cf = drone
    steps = 0
    st = 0.05
    r = 0
    dir = 0.01
    maxr = 3
    minr = 0.0
    dt = 0.1
    pos = cf.initialPosition
    while not rospy.is_shutdown():
        if r < maxr and dir > 0:
            r += dir
        elif r > maxr and dir > 0:
            dir *= -1
        if r > minr and dir < 0:
            r += dir
        elif r < minr and dir < 0:
            dir *= -1
        steps += st
        dpos = cf.initialPosition + np.array([r*np.cos(steps), r*np.sin(steps), 0])
        vel = np.linalg.norm(dpos-pos)/dt
        print(r, steps, vel)
        pos = dpos
        cf.cmdPosition(pos)
        timeHelper.sleep(dt)


if __name__ == "__main__":
    main()
