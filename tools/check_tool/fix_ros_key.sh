#!/bin/bash

echo ">>> 开始修复 ROS/ROS2 清华源 GPG 密钥过期问题..."

# 创建 keyring 目录
sudo mkdir -p /usr/share/keyrings

# 下载并添加最新 ROS 公钥
curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | \
  gpg --dearmor | sudo tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null

# 写入 ROS1 清华源（带 signed-by）
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu focal main" | \
  sudo tee /etc/apt/sources.list.d/ros1.list

# 写入 ROS2 清华源（带 signed-by）
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu focal main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list

# 更新 apt
echo ">>> 更新软件源..."
sudo apt update

echo ">>> 修复完成。"
