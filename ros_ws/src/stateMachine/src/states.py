import rospy as rp
import smach
import std_msgs
import time
import pycrazyswarm as pcs
import numpy as np

Z = 1.0
yamlpath ="/home/dronelab/DRONELAB/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        print("yes")
        self.mydrone = pcs.Crazyswarm(yamlpath)
        print("here")
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs        

    def execute(self, ud):
        rp.loginfo("starting takeoff")
        self.allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
        self.timeHelper.sleep(1.5+Z)
        time.sleep(5)
        return 'succeeded'

class LAND(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs
    
    def execute(self, ud):
        rp.loginfo("starting LAND")
        self.allcfs.land(targetHeight=0.02, duration=1.0+Z)
        self.timeHelper.sleep(1.0+Z)
        # self.allcfs.stop()
        return 'succeeded'

class HOME(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            rp.loginfo(str(cf.id))
            pos = np.array(cf.initialPosition)+ np.array([0.0, 0.0, Z])
            cf.goTo(pos, 0, 5.0)
        self.timeHelper.sleep(5.0)
        return 'succeeded'

class DANCE(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        rp.loginfo("starting DANCE")
        for cf in self.allcfs.crazyflies:
            rp.loginfo(str(cf.id))
            pos = np.array(cf.initialPosition) + np.array([0.2, 0.2, Z])
            cf.goTo(pos, 0, 4.0)
        self.timeHelper.sleep(4)
        return 'succeeded'

class FOLLOWCSV(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs
        global csvpath
        self.points = np.genfromtxt(csvpath, delimiter=",") / 10.0
        self.curentindex = 0

    def execute(self, ud):
        rp.loginfo("starting FOLLOWnp.array(cf.state.pos)CSV")
        for cf in self.allcfs.crazyflies:
            target = np.array(self.points[self.curentindex%len(self.points)])
            duration = calctime(cf.position(),target)
            cf.goTo(target,0, duration)
            print(duration)
            while np.linalg.norm(target - cf.position())>0.1:
                # self.timeHelper.sleep(duration)
                time.sleep(duration)

        self.curentindex+=1
        return 'succeeded'

def calctime(posDrone, posTarget):
    diff = posDrone-posTarget
    dist = np.linalg.norm(diff)
    return dist*10.0