#!/usr/bin/env python3
import rospy as rp
import pycrazyswarm
import smach
import smach_ros
import std_msgs
from states import *


def main():
    # rp.init_node("smach_state_machine")
    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['FINISHED', 'ENDED'])
    print("created state machine start init")
    # Open the container
    with sm:
        # Add states to the container
        print("adding state TAKEOFF")
        smach.StateMachine.add("TAKEOFF", TAKEOFF(),transitions = {"succeeded":"FOLLOWCSV", "aborted":"LAND", "preempted":"LAND"})
        print("adding state FOLLOWCSV")
        smach.StateMachine.add("FOLLOWCSV", FOLLOWCSV(),transitions = {"succeeded":"FOLLOWCSV", "aborted":"LAND", "preempted":"HOME"})
        print("adding state HOME")
        smach.StateMachine.add("HOME", HOME(),transitions = {"succeeded":"LAND", "aborted":"LAND", "preempted":"LAND"})
        print("adding state LAND")
        smach.StateMachine.add("LAND", LAND(),transitions = {"succeeded":"FINISHED", "aborted":"ENDED", "preempted":"ENDED"})
        
    # Execute SMACH plan
    print("STARTING STATE MACHINE")
    outcome = sm.execute()
    print(outcome)

if __name__ == '__main__':
    print("starting ...")
    main()