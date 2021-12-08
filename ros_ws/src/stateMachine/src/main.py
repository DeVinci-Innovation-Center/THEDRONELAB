#!/usr/bin/env python3
import rospy as rp
import pycrazyswarm
import smach
import smach_ros
import std_msgs
import signal
from states import *

global sm

def signal_handler(sig, frame):
    global sm
    print('--------------------------------')
    print('---------PREEMPT !!!------------')
    print('--------------------------------')
    sm.request_preempt()

def main():
    global sm
    # rp.init_node("smach_state_machine")
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['FINISHED', 'ENDED'])
    sm.userdata.id = 2
    sm.csvpath = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.csvpathV = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/V.csv"
    sm.csvpathI = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/I.csv"
    sm.csvpathD = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/D.csv"
    sm.csvpathC = "/home/dronelab/DRONELAB/THEDRONELAB/ros_ws/src/stateMachine/src/data/C.csv"
    
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
    print(outcome)

if __name__ == '__main__':
    print("starting ...")
    signal.signal(signal.SIGQUIT, signal_handler)
    main()