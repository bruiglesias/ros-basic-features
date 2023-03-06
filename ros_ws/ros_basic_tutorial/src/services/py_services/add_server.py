#!/usr/bin/env python3

from ros_basic_tutorial.srv import AddTwoInts
from ros_basic_tutorial.srv import AddTwoIntsRequest
from ros_basic_tutorial.srv import AddTwoIntsResponse

import rospy

def handle_add_two_ints(req):
    print(" Returning [%s + %s] = %s"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)


def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    service = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    print("Server up and waiting...")
    rospy.spin()

if __name__ == '__main__':
    add_two_ints_server()