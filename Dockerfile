FROM osrf/ros:noetic-desktop-full

# INSTALAÇÃO DE PACOTES
RUN apt-get update && apt-get install -y apt-utils

RUN \
  apt-get update && \
  apt-get -y install libgl1-mesa-glx libgl1-mesa-dri && \
  rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y gedit ros-noetic-joy ros-noetic-teleop-twist-joy \
  ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc \
  ros-noetic-rgbd-launch ros-noetic-rosserial-arduino \
  ros-noetic-rosserial-python ros-noetic-rosserial-client \
  ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server \
  ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro \
  ros-noetic-compressed-image-transport ros-noetic-rqt* ros-noetic-rviz \
  ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers \
  ros-noetic-turtlebot3 ros-noetic-turtlebot3-msgs ros-noetic-dynamixel-sdk

RUN apt-get update && apt-get install -y \
 wget \
 git \
 bash-completion \
 build-essential \
 sudo \
 && rm -rf /var/lib/apt/lists/*

 RUN apt-get update && apt-get install -y \
 xcb \
 sudo \
 && rm -rf /var/lib/apt/lists/*

ARG UID=1000
ARG GID=1000
RUN addgroup --gid ${GID} ros
RUN adduser --gecos "ROS User" --disabled-password --uid ${UID} --gid ${GID} ros
RUN usermod -a -G dialout ros
COPY config/99_aptget /etc/sudoers.d/99_aptget
RUN chmod 0440 /etc/sudoers.d/99_aptget && chown root:root /etc/sudoers.d/99_aptget

ENV USER ros
USER ros 

ENV HOME /home/${USER} 

# CRIANDO UM AMBIENTE (WORKSPACE)

RUN mkdir -p ${HOME}/ros_ws/src

WORKDIR ${HOME}/ros_ws/src

WORKDIR ${HOME}/ros_ws/ 

COPY --chown=${USER} ./src/ ./src/

RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cd ~/ros_ws; catkin_make'



# REMOVENDO ARQUIVOS DESNECESSÁRIOS
RUN sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* 