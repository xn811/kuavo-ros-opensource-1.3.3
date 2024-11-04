#!/bin/bash

source /opt/ros/noetic/setup.bash
export CC="ccache gcc"
export CXX="ccache g++"
catkin config -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_ASM_COMPILER=/usr/bin/as -DOPENSOURCE=on
catkin config --install --install-space install
catkin build hardware_node
EXIT_CODE=$?


if [ $EXIT_CODE -ne 0 ]; then
        echo "Failed to build the package"
        catkin clean -y
fi
exit $EXIT_CODE
