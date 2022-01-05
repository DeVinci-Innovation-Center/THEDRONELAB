import rospy as rp
import smach
import std_msgs
import time
try:
    import pycrazyswarm.pycrazyswarm as pcs
    print("importing from pycrazyswarm")
except Exception:
    print("importing pycrazyswarm from local")
    import pycrazyswarm as pcs
import numpy as np

<<<<<<< HEAD
Z = 0.4
yamlpath ="/home/dronelab/DRONELAB/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'], input_keys=['id'])
        print("yes")
=======
Z = 1
try:
    yamlpath = rp.get_param("crazyflies_yaml_path")
except KeyError:
    print("no yamlpath given in parameters so loading default: ")
    yamlpath = "/home/dronelab/DRONELAB/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
    print(yamlpath)
# csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"


class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
        print("init crazyswarm is done")
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        self.mydrone = pcs.Crazyswarm(yamlpath)
        print("init crazyswarm is done")
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            if cf.id == int(ud.id):
                rp.loginfo("starting takeoff")
                cf.takeoff(targetHeight=Z, duration=1.0+Z)
                self.timeHelper.sleep(Z)
                time.sleep(3)
<<<<<<< HEAD
            time.sleep(5)
=======
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        return 'succeeded'


class LAND(smach.State):
    def __init__(self):
<<<<<<< HEAD
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'], input_keys=['id'])
=======
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            if cf.id == ud.id:
                rp.loginfo("starting LAND")
                cf.land(targetHeight=0.02, duration=1.0+Z)
                self.timeHelper.sleep(1.0+Z)
        # self.allcfs.stop()
        return 'succeeded'


class HOME(smach.State):
    def __init__(self):
<<<<<<< HEAD
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'], input_keys=['id'])
=======
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            if cf.id == ud.id:
                rp.loginfo(str(cf.id))
<<<<<<< HEAD
                pos = np.array(cf.initialPosition)+ np.array([0.0, 0.0, Z])
=======
                pos = np.array(cf.initialPosition) + np.array([0.0, 0.0, Z])
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
                cf.goTo(pos, 0, 5.0)
        self.timeHelper.sleep(5.0)
        return 'succeeded'


class DANCE(smach.State):
    def __init__(self):
<<<<<<< HEAD
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted'], input_keys=['id'])
=======
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        rp.loginfo("starting DANCE")
        for cf in self.allcfs.crazyflies:
            if cf.id == ud.id:
                rp.loginfo(str(cf.id))
                pos = np.array(cf.initialPosition) + np.array([0.2, 0.2, Z])
                cf.goTo(pos, 0, 4.0)
            self.timeHelper.sleep(4)
        return 'succeeded'


class CONDSTATE(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['continu', 'finish'], input_keys=['points', 'index', 'maxreps'])

    def execute(self, ud):
        ud.index += 1
        if(ud.index/len(ud.points) > ud.maxreps):
            return 'finish'
        return 'continu'


class FOLLOWCSV(smach.State):
    def __init__(self):
<<<<<<< HEAD
        smach.State.__init__(self, outcomes=['succeeded','preempted','aborted','finished'], input_keys=['id','csvpath'])
=======
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted', 'finished'], input_keys=['id', 'points', 'index'])
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs
        global csvpath
        self.points = []
        self.curentindex = 0
        self.pindex = -1

    def execute(self, ud):
        rp.loginfo("starting FOLLOWCSV")
        try:
<<<<<<< HEAD
            self.points = np.genfromtxt(ud.csvpath, delimiter=",")
            self.points+=np.array([0,0,Z])
            for cf in self.allcfs.crazyflies:
                if cf.id == ud.id:
                    cf.setGroupMask(ud.id)
                    # cf.uploadTrajectory("traj",np.array([0,0,0]),self.points)
                    # cf.startTrajectory("traj")
                    target = np.array(self.points[self.curentindex%len(self.points)])
                    duration = calctime(cf.position(),target)
                    cf.goTo(target,0, duration, relative = False, groupMask = ud.id)
                    # cf.cmdPosiiton(target)
                    while np.linalg.norm(target - cf.position())>0.1:
                        if self.preempt_requested():
                            self.service_preempt()
                            return 'preempted'
                        # self.timeHelper.sleep(duration)
                        time.sleep(duration/100)
                        # print(f'on our way  to {self.curentindex}!!!')
            self.curentindex+=1
            if len(self.points)<=self.curentindex:
=======
            if ud.index != self.pindex:
                print("changed pattern !!!  ", ud.index)
                self.pindex = ud.index % len(ud.points)
                self.points = np.array(ud.points[ud.index])
                self.points += np.array([0, 0, Z])
                self.curentindex = 1
            # self.points = np.genfromtxt(ud.csvpath, delimiter=",")
            # self.points += np.array([0, 0, Z])
            for cf in self.allcfs.crazyflies:
                if cf.id == ud.id:
                    cf.setGroupMask(ud.id)
                    target = np.array(self.points[self.curentindex % len(self.points)])
                    duration = calctime(cf.position(), target)
                    cf.goTo(target, 0, duration, relative=False, groupMask=ud.id)
                    while np.linalg.norm(target - cf.position()) > 0.1:
                        if self.preempt_requested():
                            self.service_preempt()
                            return 'preempted'
                        time.sleep(duration/100)
            self.curentindex += 1
            if len(self.points) <= self.curentindex:
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
                self.curentindex = 0
                return 'finished'
            return 'succeeded'
        except Exception:
<<<<<<< HEAD
            return 'aborted'
=======
            print("AN EXCEPTION OCCURED !!!!!!!")
            return 'aborted'

>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e

def calctime(posDrone, posTarget):
    diff = posDrone-posTarget
    dist = np.linalg.norm(diff)
    return dist*2
<<<<<<< HEAD
    
=======
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
