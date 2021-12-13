#!/usr/bin/env python3
from logging import error
import numpy as np
import rospy as rp
from rospy.client import on_shutdown
from rospy.core import signal_shutdown
import smach
import smach_ros
import std_msgs
import signal
import sys
try:
    import mypkg.states as states
except Exception:
    print("import states from local")
    # sys.path = "/home/orca/dvic/THEDRONELAB/ros_ws/src/stateMachine/src"
    import states
from pynput import keyboard
global sm


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
    try:
        sm.userdata.id = int(rp.get_param("~dn"))
    except KeyError:
        print("failed to get drone number")
        sm.userdata.id = 1
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

    print("created state machine start init")
    # Open the container
    with sm:
        # Add states to the container
        print("adding state TAKEOFF")
        smach.StateMachine.add("TAKEOFF", states.TAKEOFF(), transitions={"succeeded": "FOLLOWCSV", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state CONDSTATE")
        smach.StateMachine.add("CONDSTATE", states.CONDSTATE(), transitions={"continu": "FOLLOWCSV", "finish": "HOME"}, remapping={'points': 'points', 'index': 'index', 'maxreps': 'maxreps'})
        print("adding csv states FOLLOWCSV")
        smach.StateMachine.add("FOLLOWCSV", states.FOLLOWCSV(), transitions={"succeeded": "FOLLOWCSV", "aborted": "HOME", "preempted": "HOME", 'finished': 'CONDSTATE'}, remapping={'id': 'id', 'points': 'points', 'index': 'index'})
        print("adding state HOME")
        smach.StateMachine.add("HOME", states.HOME(), transitions={"succeeded": "LAND", "aborted": "LAND", "preempted": "LAND"}, remapping={'id': 'id'})
        print("adding state LAND")
        smach.StateMachine.add("LAND", states.LAND(), transitions={"succeeded": "FINISHED", "aborted": "ENDED", "preempted": "ENDED"}, remapping={'id': 'id'})

    # Execute SMACH plan
    print("STARTING STATE MACHINE")
    outcome = sm.execute()
    rp.signal_shutdown(str(outcome))


if __name__ == '__main__':
    print("starting ...")
    kl = keyboard.Listener(on_press=signal_handler)
    kl.start()
    main()
