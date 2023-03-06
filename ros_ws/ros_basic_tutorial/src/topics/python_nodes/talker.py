#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def talker():

    pub = rospy.Publisher('temp_topic', String, queue_size=10)

    rospy.init_node('talker', anonymous=True)
    
    rate = rospy.Rate(1) # 1 Hz  = 1 mensagem por segundo

    valor = 0

    while not rospy.is_shutdown():
        msg = "Leitura %s"%valor
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()
        valor = valor + 1


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass