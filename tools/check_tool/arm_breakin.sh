#!/bin/bash
###
 # @Author: Name
 # @Date: 2025-04-01 16:56:55
 # @LastEditors: Please set LastEditors
 # @LastEditTime: 2025-04-01 16:56:55
 # @FilePath: /kuavo/tools/check_tool/arm_breakin.sh
 # @Description: 手臂磨线脚本
### 

# 获取当前脚本所在文件夹的绝对路径
current_script_dir=$(dirname "$(realpath "$0")")

# 使用字符串操作来截取前部分路径
prefix="${current_script_dir%/tools/check_tool}"

# 构建 arm_breakin.py 的路径
arm_breakin_folder_path="$prefix/src/kuavo-ros-control-lejulib/hardware_node/lib/ruiwo_controller"
arm_breakin_file_path="$arm_breakin_folder_path/arm_breakin.py"

# 检查文件是否存在
if [ -f "$arm_breakin_file_path" ]; then
    # 执行 Python 脚本
    python3 "$arm_breakin_file_path"
else
    echo "The file $arm_breakin_file_path does not exist."
    exit 1
fi
