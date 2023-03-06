#!/usr/bin/env python3

import rospy
import time
import math
from geometry_msgs.msg import Twist 
from turtlesim.msg import Pose

# inicia as variaveis de pose
x = 0
y = 0
yaw = 0

def pose_callback(pose: Pose):
    global x
    global y, yaw

    x = pose.x
    y = pose.y
    yaw = pose.theta


def moving_with_euclidian(velocity_publisher: rospy.Publisher, speed: float, distance: float, is_forward: bool):

    velocity_message = Twist()

    global x
    global y

    # Grava as posições inicial antes de executar o movimento
    x_0 = x
    y_0 = y

    # Sentido do movimento
    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    
    distance_moved = 0
    loop_rate = rospy.Rate(10) # 10hz ou 10 msgs por segundo

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

        distance_moved = abs(math.sqrt(((x - x_0)**2) + ((y - y_0) ** 2)))
        
        print(distance_moved)

        if distance_moved > distance:
            rospy.loginfo('Reached!')
            break
    
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)



def moving_with_instant_velocity(velocity_publisher: rospy.Publisher, speed: float, distance: float, is_forward: bool):

    velocity_message = Twist()

    # Sentido do movimento
    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    
    distance_moved = 0
    loop_rate = rospy.Rate(10) # 10hz ou 10 msgs por segundo

    t_0 = rospy.Time.now().to_sec()

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        
        loop_rate.sleep()
        t_1 = rospy.Time.now().to_sec()

        distance_moved = (t_1 - t_0) * speed
        
        print(distance_moved)

        if distance_moved > distance:
            rospy.loginfo('Reached!')
            break
    
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)



def rotating(velocity_publisher: rospy.Publisher, angular_speed_degree: float, relative_angle_degree: float, clockwise: bool):
    global yaw
    velocity_messsage = Twist()

    angular_speed = math.radians(abs(angular_speed_degree))

    if clockwise:
        velocity_messsage.angular.z = -abs(angular_speed)
    else:
        velocity_messsage.angular.z = abs(angular_speed)

    loop_rate = rospy.Rate(5)
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t_0 = rospy.Time.now().to_sec()

    while True:
        velocity_publisher.publish(velocity_messsage)

        t_1 = rospy.Time.now().to_sec()
        current_angle_degree = (t_1 - t_0) * angular_speed_degree
        rospy.loginfo(current_angle_degree)
        loop_rate.sleep()

        if current_angle_degree > relative_angle_degree:
            rospy.loginfo('reached')
            break
    
    velocity_messsage.angular.z = 0
    velocity_publisher.publish(velocity_messsage)


def go_to_goal(velocity_publisher: rospy.Publisher, x_goal: float, y_goal: float):
    global x
    global y, yaw

    velocity_message = Twist()

    while True:

        K_linear = 0.5
        distance = abs(math.sqrt(((x_goal - x)**2)+((y_goal - y) ** 2)))

        linear_speed = distance * K_linear


        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal - y, x_goal -x)
        angular_speed = (desired_angle_goal - yaw) * K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        velocity_publisher.publish(velocity_message)

        print('x=', x, 'y=', y)

        if distance < 0.01:
            break


def absolute_rotating(velocity_publisher: rospy.Publisher, desired_angle_radians: float):
    relative_angle_radians = desired_angle_radians - yaw

    if relative_angle_radians < 0:
        clockwise = 1
    else:
        clockwise = 0

    rotating(velocity_publisher, 15, math.degrees(abs(relative_angle_radians)), clockwise)


def spiral_clean(velocity_publisher: rospy.Publisher):
    velocity_message = Twist()
    loop_rate = rospy.Rate(1)
    wk = 4
    rk = 0

    while((x < 8) and (y < 8)):
        rk=rk+1
        velocity_message.linear.x = rk
        velocity_message.angular.z = wk
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

    velocity_message.linear.x = 0
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

if __name__ == '__main__':

    try:
        rospy.init_node('turtlesim_motion_python', anonymous=True)

        # Declaração de um velocity publisher
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        # Declaração de um pose subscriber
        pose_topic = '/turtle1/pose'
        pose_subscriber = rospy.Subscriber(pose_topic, Pose, pose_callback)
        time.sleep(2)
        
        # Tipos de movimento
        # moving_with_euclidian(velocity_publisher, 1.0, 4.0, True)
        # moving_with_instant_velocity(velocity_publisher, 1.0, 4.0, True)
        # rotating(velocity_publisher, 30, 90, False)
        # go_to_goal(velocity_publisher, 1, 1)
        # absolute_rotating(velocity_publisher, math.radians(90))
        # spiral_clean(velocity_publisher)

        x_goal = rospy.get_param('x_goal')
        y_goal = rospy.get_param('y_goal')

        go_to_goal(velocity_publisher, x_goal, y_goal)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node terminated')