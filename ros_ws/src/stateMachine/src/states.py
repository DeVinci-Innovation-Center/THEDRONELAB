import rospy as rp
import smach
import std_msgs
import pycrazyswarm as pcs
import numpy as np

class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm()
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs        

    def execute(self, ud):
        rp.loginfo("starting takeoff")
        self.allcfs.takeoff(targetHeight=0.5, duration=1.0+0.5)
        self.timeHelper.sleep(1.5+0.5)
        return 'succeeded'

class LAND(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'])
        self.mydrone = pcs.Crazyswarm()
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs
    
    def execute(self, ud):
        rp.loginfo("starting LAND")
        self.allcfs.land(targetHeight=0.02, duration=1.0+0.5)
        self.timeHelper.sleep(1.0+0.5)
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
            pos = np.array(cf.initialPosition)
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
            pos = np.array(cf.initialPosition) + np.array([0.1, 0.1, 0.5])
            cf.goTo(pos, 0, 4.0)
        self.timeHelper.sleep(4)
        return 'succeeded'