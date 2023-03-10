#!/usr/bin/env python3

from ros_basic_tutorial.srv import AddTwoInts
from ros_basic_tutorial.srv import AddTwoIntsRequest
from ros_basic_tutorial.srv import AddTwoIntsResponse

import rospy
import sys


def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp = add_two_ints(x, y)
        return resp.sum
    except rospy.ServiceException as e:
        print("Service call failed %s"%(e))


if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print("%s [x y]"%(sys.argv[0]))
        sys.exit(1)

    print("Requesting %s+%s"%(x, y))
    response = add_two_ints_client(x, y)
    print ("%s + %s = %s"%(x, y, response))
