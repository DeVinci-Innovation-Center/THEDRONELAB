import rospy as rp
from rospy.timer import sleep
from std_msgs.msg import String # find the type of the msg here
import time

# init the node and give it a name
rp.init_node("chatter")

#create a publisher for the topic "/chat " and message type String
pub = rp.Publisher("/chat",String,queue_size=1)

start = time.time()

# this loop publishes a msg every second during 60s
while time.time()-start <60:
    time.sleep(1)
    msg = String()
    msg.data = "hello"
    pub.publish(msg)
