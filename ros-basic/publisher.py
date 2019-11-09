#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.init_node('topic_publisher')
pub = rospy.Publisher('phrases', String, queue_size=10)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    msg_str = "hello world %s" % rospy.get_time()
    pub.publish(msg_str)
    rate.sleep()

