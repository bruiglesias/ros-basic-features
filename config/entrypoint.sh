#!/bin/bash
# Esse arquivo nao está sendo usado
set -e 
# setup environment
source $HOME/.bashrc 
# start in home directory 
cd  
exec bash -i -c $@

# Adding all the necessary ros sourcing
echo "" >> ~/.bashrc
echo "## ROS" >> ~/.bashrc
echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
echo "source ~/ros_ws/devel/setup.bash" >> ~/.bashrc

catkin_make
