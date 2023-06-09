FROM ros:noetic-ros-base

#
# Defining entry arguments
#

ENV ROS_DISTRO=noetic
ENV ROS_ROOT=/opt/ros/noetic
ENV ROS_PYTHON_VERSION=3
ENV DEBIAN_FRONTEND=noninteractive

#
# Python Pip Installation
#

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y python3-pip

#
# Sourcing Ros
#

RUN echo 'source /opt/ros/noetic/setup.bash' >> /root/.bashrc

#
# Ros Dependencies
#

RUN apt-get install -y python3-rosdep \
                       python3-rosinstall \
                       python3-rosinstall-generator \
                       python3-wstool \
                       build-essential \
                       git \
                       python3-rosdep && \
    rosdep update

#
# ROS DEPENDENCIES
#

RUN apt-get update && apt install -y  net-tools \
                                      wireless-tools \
                                      iputils-ping \
                                      python3-shapely \
                                      python3-vcstool


RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-amcl ros-${ROS_DISTRO}-map-server \
                                         ros-${ROS_DISTRO}-move-base ros-${ROS_DISTRO}-urdf ros-${ROS_DISTRO}-xacro \
                                         ros-${ROS_DISTRO}-rqt* ros-${ROS_DISTRO}-rviz \
                                         ros-${ROS_DISTRO}-gmapping ros-${ROS_DISTRO}-navigation \
                                         ros-${ROS_DISTRO}-turtlebot3-msgs ros-${ROS_DISTRO}-turtlebot3 \
                                         ros-${ROS_DISTRO}-turtlebot3-simulations ros-${ROS_DISTRO}-turtlebot3-gazebo

#
# Sourcing Ros
#
RUN echo 'source /opt/ros/noetic/setup.bash' >> /root/.bashrc

#
# Setup Entry Point
#
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
WORKDIR /
