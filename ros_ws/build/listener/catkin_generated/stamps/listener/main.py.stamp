#!/usr/bin/env python3
import rospy as rp
from std_msgs.msg import String

#define a callback: function called whenever we receive a message
def mycallback(msg):
    print(msg.data)


if __name__ == "__main__":
    # init the node
    rp.init_node("listenerNode")

    #create a subscriber
    mysub = rp.Subscriber("/chat",String, callback=mycallback, queue_size=1)

    rp.spin() # while true for infinite loop