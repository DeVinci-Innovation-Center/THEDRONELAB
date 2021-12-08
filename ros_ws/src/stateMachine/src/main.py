#!/usr/bin/env python3
from numpy.core.numeric import True_
import rospy as rp
import pycrazyswarm
from rospy.client import on_shutdown
from rospy.core import signal_shutdown
import smach
import smach_ros
import std_msgs
import signal
from states import *
from pynput import keyboard

from tf import listener

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
    sm.userdata.id = 2
    sm.userdata.csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathV = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.userdata.csvpathI = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/I.csv"
    sm.userdata.csvpathD = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/D.csv"
    sm.userdata.csvpathC = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/C.csv"
    
    print("created state machine start init")
    # Open the container
    with sm:
        # Add states to the container
        print("adding state TAKEOFF")
        smach.StateMachine.add("TAKEOFF", TAKEOFF(),transitions = {"succeeded":"VFOLLOWCSV", "aborted":"LAND", "preempted":"LAND"}, remapping={'id':'id'})
        print("adding state FOLLOWCSV")
        smach.StateMachine.add("VFOLLOWCSV", FOLLOWCSV(),transitions = {"succeeded":"VFOLLOWCSV", "aborted":"HOME", "preempted":"HOME",'finished':'IFOLLOWCSV'}, remapping={'id':'id','csvpath':'csvpathV'})
        smach.StateMachine.add("IFOLLOWCSV", FOLLOWCSV(),transitions = {"succeeded":"IFOLLOWCSV", "aborted":"HOME", "preempted":"HOME",'finished':'VFOLLOWCSV'}, remapping={'id':'id','csvpath':'csvpathI'})
        print("adding state HOME")
        smach.StateMachine.add("HOME", HOME(),transitions = {"succeeded":"LAND", "aborted":"LAND", "preempted":"LAND"}, remapping={'id':'id'})
        print("adding state LAND")
        smach.StateMachine.add("LAND", LAND(),transitions = {"succeeded":"FINISHED", "aborted":"ENDED", "preempted":"ENDED"}, remapping={'id':'id'})
        
    # Execute SMACH plan
    print("STARTING STATE MACHINE")
    outcome = sm.execute()
    rp.signal_shutdown(str(outcome))

if __name__ == '__main__':
    print("starting ...")
    kl = keyboard.Listener(on_press = signal_handler)
    kl.start()
    main()