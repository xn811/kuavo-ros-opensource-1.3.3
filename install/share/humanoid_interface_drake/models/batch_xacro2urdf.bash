#!/bin/bash

# 获取当前脚本所在的目录
BASE_DIR=$(dirname "$0")

# 目标脚本名称
TARGET_SCRIPT="xacro2urdf.bash"

# 遍历同级目录下的所有文件夹
for dir in "$BASE_DIR"/*; do
    # 检查是否为目录
    if [ -d "$dir" ]; then
        # 构建目标脚本的完整路径
        script="$dir/urdf/$TARGET_SCRIPT"
        
        # 检查文件是否存在并且是可执行文件
        if [ -f "$script" ]; then
            echo "Running script: $script"
            bash "$script"
        fi
    fi
done
