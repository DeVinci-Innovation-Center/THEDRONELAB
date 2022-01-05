#!/usr/bin/env python3
<<<<<<< HEAD
from numpy.core.numeric import True_
import rospy as rp
import pycrazyswarm
=======
from logging import error
import numpy as np
import rospy as rp
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
from rospy.client import on_shutdown
from rospy.core import signal_shutdown
import smach
import smach_ros
import std_msgs
import signal
<<<<<<< HEAD
from states import *
from pynput import keyboard

from tf import listener

global sm

=======
try:
    import mystates.states as states
except Exception:
    import states
from pynput import keyboard
global sm


>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
def signal_handler(k):
    try:
        if k.char == 'q':
            global sm
<<<<<<< HEAD
        print('--------------------------------')
        print('---------PREEMPT !!!------------')
        print('--------------------------------')
        sm.request_preempt()
    except AttributeError:
        pass
    
=======
            print('--------------------------------')
            print('---------PREEMPT !!!------------')
            print('--------------------------------')
            sm.request_preempt()
    except AttributeError:
        pass

>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e

def main():
    global sm
    # rp.init_node("smach_state_machine")
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['FINISHED', 'ENDED'])
<<<<<<< HEAD
    sm.userdata.id = 5
    sm.userdata.csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathV = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathI = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/I.csv"
    sm.userdata.csvpathD = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/D.csv"
    sm.userdata.csvpathC = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/C.csv"
    
=======
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
        homedir = "/home/dronelab/DRONELAB/THEDRONELAB"
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

>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
    print("created state machine start init")
    # Open the container
    with sm:
        # Add states to the container
        print("adding state TAKEOFF")
<<<<<<< HEAD
        smach.StateMachine.add("TAKEOFF", TAKEOFF(),transitions = {"succeeded":"VFOLLOWCSV", "aborted":"LAND", "preempted":"LAND"}, remapping={'id':'id'})
        print("adding state FOLLOWCSV")
        smach.StateMachine.add("VFOLLOWCSV", FOLLOWCSV(),transitions = {"succeeded":"VFOLLOWCSV", "aborted":"HOME", "preempted":"HOME",'finished':'IFOLLOWCSV'}, remapping={'id':'id','csvpath':'csvpathV'})
        smach.StateMachine.add("IFOLLOWCSV", FOLLOWCSV(),transitions = {"succeeded":"IFOLLOWCSV", "aborted":"HOME", "preempted":"HOME",'finished':'VFOLLOWCSV'}, remapping={'id':'id','csvpath':'csvpathI'})
        print("adding state HOME")
        smach.StateMachine.add("HOME", HOME(),transitions = {"succeeded":"LAND", "aborted":"LAND", "preempted":"LAND"}, remapping={'id':'id'})
        print("adding state LAND")
        smach.StateMachine.add("LAND", LAND(),transitions = {"succeeded":"FINISHED", "aborted":"ENDED", "preempted":"ENDED"}, remapping={'id':'id'})
        
=======
        smach.StateMachine.add("TAKEOFF", states.TAKEOFF(), transitions={"succeeded": "FOLLOWCSV", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state CONDSTATE")
        smach.StateMachine.add("CONDSTATE", states.CONDSTATE(), transitions={"continu": "FOLLOWCSV", "finish": "HOME"}, remapping={'points': 'points', 'index': 'index', 'maxreps': 'maxreps'})
        print("adding csv states FOLLOWCSV")
        smach.StateMachine.add("FOLLOWCSV", states.FOLLOWCSV(), transitions={"succeeded": "FOLLOWCSV", "aborted": "HOME", "preempted": "HOME", 'finished': 'CONDSTATE'}, remapping={'id': 'id', 'points': 'points', 'index': 'index'})
        print("adding state HOME")
        smach.StateMachine.add("HOME", states.HOME(), transitions={"succeeded": "LAND", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state LAND")
        smach.StateMachine.add("LAND", states.LAND(), transitions={"succeeded": "FINISHED", "aborted": "ENDED", "preempted": "ENDED"}, remapping={'id': 'id'})

>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
    # Execute SMACH plan
    print("STARTING STATE MACHINE")
    outcome = sm.execute()
    rp.signal_shutdown(str(outcome))
<<<<<<< HEAD

if __name__ == '__main__':
    print("starting ...")
    kl = keyboard.Listener(on_press = signal_handler)
    kl.start()
    main()
=======


if __name__ == '__main__':
    print("starting ...")
    kl = keyboard.Listener(on_press=signal_handler)
    kl.start()
    main()
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
