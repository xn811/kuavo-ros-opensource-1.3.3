#!/bin/bash

# 接收一个参数，判断是否是 "body"
PARAM=$1

# 检查 ~/.bashrc 是否包含 ROS_MASTER_URI
if grep -q "^export ROS_MASTER_URI=" ~/.bashrc; then
    # 如果已经存在，则修改它的值
    sed -i 's|^export ROS_MASTER_URI=.*|export ROS_MASTER_URI=http://kuavo_master:11311|' ~/.bashrc
    echo "ROS_MASTER_URI 已更新为 http://kuavo_master:11311"
else
    # 如果不存在，则添加新的变量
    echo "export ROS_MASTER_URI=http://kuavo_master:11311" >> ~/.bashrc
    echo "ROS_MASTER_URI 已添加到 ~/.bashrc"
fi

# 如果参数是 "body"，则判断是否已设置 ROS_HOSTNAME
if [ "$PARAM" == "body" ]; then
    # 检查 ~/.bashrc 是否包含 ROS_HOSTNAME
    if grep -q "^export ROS_HOSTNAME=" ~/.bashrc; then
        # 如果已经存在，则修改它的值
        sed -i 's|^export ROS_HOSTNAME=.*|export ROS_HOSTNAME=kuavo_master|' ~/.bashrc
        echo "ROS_HOSTNAME 已更新为 kuavo_master"
    else
        # 如果不存在，则添加新的变量
        echo "export ROS_HOSTNAME=kuavo_master" >> ~/.bashrc
        echo "ROS_HOSTNAME 已添加到 ~/.bashrc"
    fi
fi
