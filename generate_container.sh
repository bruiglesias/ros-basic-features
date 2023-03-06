#!/bin/bash

mkdir -p ros_ws

# create a shared volume to store the ros_ws
docker volume create --driver local \
    --opt type="none" \
    --opt device="${PWD}/ros_ws/" \
    --opt o="bind" \
    "ros_tutorial_vol"
 
xhost +
docker run \
    --privileged \
    --net=host \
    --env="DISPLAY" \
    -it \
    --volume="ros_tutorial_vol:/home/ros/ros_ws/src/:rw" \
    --volume="/dev/bus/usb:/dev/bus/usb" \
    --volume="/dev:/dev" \
    --name=ros-noetic-tutorial \
    --device=/dev/dri:/dev/dri \
    bruiglesias/ros-noetic-ubuntu-focal:latest
