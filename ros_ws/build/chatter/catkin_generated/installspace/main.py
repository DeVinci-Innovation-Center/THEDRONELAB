import rospy as rp
from rospy.timer import sleep
from std_msgs.msg import String
import time

rp.init_node("chatter")

pub = rp.Publisher("/chat",String,queue_size=1)

start = time.time()
while time.time()-start <60:
    time.sleep(1)
    msg = String()
    msg.data = "hello"
    pub.publish(msg)
