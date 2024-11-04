#!/bin/bash

SCIRPT_ENTRY_DIR="$(pwd)"
echo "The script entry directory is: $SCIRPT_ENTRY_DIR"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -d "$( dirname "${SCRIPT_DIR}" )/install" ]; then
        mkdir -p "$( dirname "${SCRIPT_DIR}" )/install"
fi
INSTALL_DIR="$( cd "$( dirname "${SCRIPT_DIR}" )/install" && pwd )"

source /opt/ros/noetic/setup.bash
export CC="ccache gcc"
export CXX="ccache g++"
XACRO2URDF_SCIRPT="${INSTALL_DIR}/share/humanoid_interface_drake/models/batch_xacro2urdf.bash"
if [ ! -f $XACRO2URDF_SCIRPT ]; then
        echo "The xacro2urdf script does not exist: $XACRO2URDF_SCIRPT"
else
        echo "The xacro2urdf script exists: $XACRO2URDF_SCIRPT"
        sudo chmod +x $XACRO2URDF_SCIRPT
        cd "${INSTALL_DIR}/share/humanoid_interface_drake/"
        bash -c $XACRO2URDF_SCIRPT
fi

cd $SCIRPT_ENTRY_DIR


catkin config -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_ASM_COMPILER=/usr/bin/as -DOPENSOURCE=on
catkin config --install --install-space install
catkin build humanoid_controllers -j$(nproc)
EXIT_CODE=$?




