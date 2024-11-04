#!/bin/bash
echo "Converting xacro files to urdf files..."
URDF_PATH=$HOME/.config/lejuconfig/urdf/biped_gen4.0/

if [ -d "$URDF_PATH" ]; then
    echo "The path already exists: $URDF_PATH"
else
    # 如果路径不存在，创建它
    mkdir -p "$URDF_PATH"
    echo "Created path: $URDF_PATH"
fi
BASE_DIR=$(dirname "$0")
echo "shell script path is $BASE_DIR"
echo "The path of generated urdf is $URDF_PATH"

rosrun xacro xacro $BASE_DIR/biped_v3.xacro > $URDF_PATH/biped_v3.urdf
rosrun xacro xacro $BASE_DIR/biped_v3_full.xacro > $URDF_PATH/biped_v3_full.urdf
rosrun xacro xacro $BASE_DIR/biped_v3_arm.xacro > $URDF_PATH/biped_v3_arm.urdf
rosrun xacro xacro $BASE_DIR/biped_v3_all_joint.xacro > $URDF_PATH/biped_v3_all_joint.urdf
rosrun xacro xacro $BASE_DIR/Larm.xacro > $URDF_PATH/Larm.urdf
rosrun xacro xacro $BASE_DIR/Rarm.xacro > $URDF_PATH/Rarm.urdf
rosrun xacro xacro $BASE_DIR/Lleg.xacro > $URDF_PATH/Lleg.urdf
rosrun xacro xacro $BASE_DIR/Rleg.xacro > $URDF_PATH/Rleg.urdf

# copy meshes
cp -r $BASE_DIR/../meshes $URDF_PATH/../
echo "Done!"