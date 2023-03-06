#!/usr/bin/env python3

import rospy
import tf2_msgs.msg
import geometry_msgs.msg
import math

class DinamicTFBroadCaster:
    
    def __init__(self):
        self.publisher_tf = rospy.Publisher('/tf', tf2_msgs.msg.TFMessage, queue_size=1)

        rate = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            
            rate.sleep()

            x = rospy.Time.now().to_sec() * math.pi

            
            msg = geometry_msgs.msg.TransformStamped()
            msg.header.frame_id = "laser"
            msg.header.stamp = rospy.Time.now()
            msg.child_frame_id = "signal"
            msg.transform.translation.x = 2 * math.sin(x)
            msg.transform.translation.y = 2 * math.cos(x)
            msg.transform.translation.z = 0.0
            msg.transform.rotation.x = 0.0
            msg.transform.rotation.y = 0.0
            msg.transform.rotation.z = 0.0
            msg.transform.rotation.w = 1.0

            tf_msg = tf2_msgs.msg.TFMessage([msg])
            self.publisher_tf.publish(tf_msg)

if __name__ == "__main__":
    rospy.init_node('dinamic_tf_broadcaster')
    fixed_broadcaster = DinamicTFBroadCaster()
    rospy.spin()

