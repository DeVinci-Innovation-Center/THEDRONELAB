#!/usr/bin/env python
import numpy as np
import sys
import rospy as rp
from rospy.client import on_shutdown
from rospy.core import signal_shutdown
import smach
import smach_ros
import std_msgs
import signal
import sys
import time
# import mystates as mystates
from pynput import keyboard
sys.path.append("/home/dvic/crazyswarm/ros_ws/src/crazyswarm/scripts")
# print(sys.path)
import pycrazyswarm as pcs

global sm

Z = 1
global yamlpath

print("we have been imported")


def helloworld():
    print("imported and used")


class TAKEOFF(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
        global yamlpath
        print("init crazyswarm is happening")
        self.mydrone = pcs.Crazyswarm(yamlpath)
        print("init crazyswarm is done")
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            if cf.id == int(ud.id):
                rp.loginfo("starting takeoff")
                print("starting takeoff")
                cf.takeoff(targetHeight=Z, duration=1.0+Z)
                # self.timeHelper.sleep(Z)
                time.sleep(5)
        return 'succeeded'


class LAND(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
        global yamlpath
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
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
        global yamlpath
        self.mydrone = pcs.Crazyswarm(yamlpath)
        self.timeHelper = self.mydrone.timeHelper
        self.allcfs = self.mydrone.allcfs

    def execute(self, ud):
        for cf in self.allcfs.crazyflies:
            if cf.id == ud.id:
                rp.loginfo(str(cf.id))
                pos = np.array(cf.initialPosition) + np.array([0.0, 0.0, Z])
                cf.goTo(pos, 0, 5.0)
        self.timeHelper.sleep(5.0)
        return 'succeeded'


class DANCE(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'], input_keys=['id'])
        global yamlpath
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
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted', 'finished'], input_keys=['id', 'points', 'index'])
        global yamlpath
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
                self.curentindex = 0
                return 'finished'
            return 'succeeded'
        except Exception:
            print("AN EXCEPTION OCCURED !!!!!!!")
            return 'aborted'


def calctime(posDrone, posTarget):
    diff = posDrone-posTarget
    dist = np.linalg.norm(diff)
    return dist*2


def signal_handler(k):
    try:
        if k.char == 'q':
            global sm
            print('--------------------------------')
            print('---------PREEMPT !!!------------')
            print('--------------------------------')
            sm.request_preempt()
    except AttributeError:
        pass


def main():
    global sm
    # rp.init_node("smach_state_machine")
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['FINISHED', 'ENDED'])
<<<<<<< HEAD
    rp.init_node("dronemachine")  # ! so we can recover the params
    # print(rp.get_name())
    # k = rp.get_param_names()
    # for k in rp.get_param_names():
    #     print(k, rp.get_param(k))
    # print("namespace ", rp.get_namespace())
    # print("name ", rp.get_name())
    # print("id ", rp.get_caller_id())
    # print("uri ", rp.get_node_uri())
    # print("_______________")
    global yamlpath
    try:
        yamlpath = rp.get_param("crazyflies_yaml_path")
    except KeyError:
        print("no yamlpath given in parameters so loading default: ")
        yamlpath = "/home/orca/dvic/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
        print(yamlpath)
    # csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
=======
<<<<<<< HEAD
    sm.userdata.id = 5
    sm.userdata.csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathV = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathI = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/I.csv"
    sm.userdata.csvpathD = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/D.csv"
    sm.userdata.csvpathC = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/C.csv"
    
=======
>>>>>>> 91edb6718f95756597dd405e93ad74f824224934
    try:
        sm.userdata.id = int(rp.get_param("~dn"))
    except KeyError:
        print("failed to get drone number")
        sm.userdata.id = 2
    try:
        sm.userdata.maxreps = int(rp.get_param("~mr"))
    except KeyError:
        print("failed to get maxreps")
        sm.userdata.maxreps = 3
    try:
        homedir = rp.get_param("csv_path")
    except KeyError:
        print("failed to get csvpath")
        homedir = "/home/orca/dvic/THEDRONELAB"
    sm.userdata.points = []
    sm.userdata.index = 0
    try:
        arrayofpaths = rp.get_param("~csvs")
        print("got csvs")
        for letters in arrayofpaths:
            try:
                print("adding: ", f"{homedir}/ros_ws/src/stateMachine/src/data/{letters}.csv")
                sm.userdata.points.append(np.genfromtxt(f"{homedir}/ros_ws/src/stateMachine/src/data/{letters}.csv", delimiter=","))
            except Exception:
                print("error while loading this csv !!!!")
    except KeyError:
        print("no csvs were passed")
        sm.userdata.points.append(f"{homedir}/ros_ws/src/stateMachine/src/data/V.csv")
        sm.userdata.points.append(f"{homedir}/ros_ws/src/stateMachine/src/data/I.csv")
        sm.userdata.points.append(f"{homedir}/ros_ws/src/stateMachine/src/data/D.csv")
        sm.userdata.points.append(f"{homedir}/ros_ws/src/stateMachine/src/data/C.csv")

<<<<<<< HEAD
    rp.signal_shutdown("switching")  # ! so pycrazyswarm can create its own node
=======
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
>>>>>>> 91edb6718f95756597dd405e93ad74f824224934
    print("created state machine start init")
    # Open the container
    with sm:
        # Add states to the container
        print("adding state TAKEOFF")
        smach.StateMachine.add("TAKEOFF", TAKEOFF(), transitions={"succeeded": "FOLLOWCSV", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state CONDSTATE")
        smach.StateMachine.add("CONDSTATE", CONDSTATE(), transitions={"continu": "FOLLOWCSV", "finish": "HOME"}, remapping={'points': 'points', 'index': 'index', 'maxreps': 'maxreps'})
        print("adding csv states FOLLOWCSV")
        smach.StateMachine.add("FOLLOWCSV", FOLLOWCSV(), transitions={"succeeded": "FOLLOWCSV", "aborted": "HOME", "preempted": "HOME", 'finished': 'CONDSTATE'}, remapping={'id': 'id', 'points': 'points', 'index': 'index'})
        print("adding state HOME")
        smach.StateMachine.add("HOME", HOME(), transitions={"succeeded": "LAND", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state LAND")
        smach.StateMachine.add("LAND", LAND(), transitions={"succeeded": "FINISHED", "aborted": "ENDED", "preempted": "ENDED"}, remapping={'id': 'id'})

    # Execute SMACH plan
    print("STARTING STATE MACHINE")
    outcome = sm.execute()
    rp.signal_shutdown(str(outcome))


if __name__ == '__main__':
    print("starting ...")
    kl = keyboard.Listener(on_press=signal_handler)
    kl.start()
    main()
