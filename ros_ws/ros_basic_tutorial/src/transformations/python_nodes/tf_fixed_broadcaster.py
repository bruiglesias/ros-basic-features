#!/usr/bin/env python3

import rospy
import tf2_msgs.msg
import geometry_msgs.msg

class FixedTFBroadCaster:
    def __init__(self):
        self.publisher_tf = rospy.Publisher('/tf', tf2_msgs.msg.TFMessage, queue_size=1)

        while not rospy.is_shutdown():
            rospy.sleep(0.1)

            msg = geometry_msgs.msg.TransformStamped()
            msg.header.frame_id = "robot"
            msg.header.stamp = rospy.Time.now()
            msg.child_frame_id = "laser"
            msg.transform.translation.x = 0.5
            msg.transform.translation.y = 0.0
            msg.transform.translation.z = 0.5
            msg.transform.rotation.x = 0.0
            msg.transform.rotation.y = 0.0
            msg.transform.rotation.z = 0.0
            msg.transform.rotation.w = 1.0

            tf_msg = tf2_msgs.msg.TFMessage([msg])
            self.publisher_tf.publish(tf_msg)

if __name__ == "__main__":
    rospy.init_node('fixed_tf_broadcaster')
    fixed_broadcaster = FixedTFBroadCaster()
    rospy.spin()

