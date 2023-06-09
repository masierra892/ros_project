#!/bin/bash

script_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $script_path
cd ..

source devel/setup.bash

export TURTLEBOT3_MODEL=burger

project_directory=$script_path/catkin_ws/src/ros_project

roslaunch project_launcher project_launcher_move_base_py.launch map_path:=$project_directory/map/map.yaml
