import rospy as rp
import smach
import std_msgs
import pycrazyswarm as pcs
import numpy as np

Z = 1.0

class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm()
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs        

    def execute(self, ud):
        rp.loginfo("starting takeoff")
        self.allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
        self.timeHelper.sleep(1.5+Z)
        return 'succeeded'

class LAND(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm()
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
        self.mydrone = pcs.Crazyswarm()
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs
    
    def execute(self, ud):
        rp.loginfo("starting HOME")
        for cf in self.allcfs.crazyflies:
            rp.loginfo(str(cf.id))
            pos = np.array(cf.initialPosition)+ np.array([0.0, 0.0, Z])
            cf.goTo(pos, 0, 5.0)
        self.timeHelper.sleep(5.0)
        return 'succeeded'

class DANCE(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm()
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