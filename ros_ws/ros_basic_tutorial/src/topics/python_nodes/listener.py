#!/usr/bin/env python3

import rospy
from std_msgs.msg import String


def callback_function(message):
    rospy.loginfo("Eu li a temp.  %s", message.data)


def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('temp_topic', String, callback_function)
    rospy.spin()



if __name__ == '__main__':
    listener()