#!/bin/bash
# 启动语音触发任务系统（仿真版）

echo "=========================================="
echo "  语音触发综合任务系统启动脚本（仿真版）"
echo "=========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查是否在ROS环境中
if [ -z "$ROS_DISTRO" ]; then
    echo "❌ 错误: 未检测到ROS环境"
    echo "请先执行: source devel/setup.zsh"
    exit 1
fi

echo "✅ ROS环境: $ROS_DISTRO"
echo ""

# 启动综合任务服务
echo "步骤1: 启动综合任务服务..."
echo "----------------------------------------"
cd "$SCRIPT_DIR"
python3 full_task_service.py &
TASK_SERVICE_PID=$!
echo "✅ 综合任务服务已启动 (PID: $TASK_SERVICE_PID)"
echo ""

# 等待服务启动
sleep 2

# 检查服务是否正常运行
if ! ps -p $TASK_SERVICE_PID > /dev/null; then
    echo "❌ 综合任务服务启动失败"
    exit 1
fi

# 启动语音任务控制器
echo "步骤2: 启动语音任务控制器..."
echo "----------------------------------------"
python3 sim_voice_controller.py &
VOICE_CONTROLLER_PID=$!
echo "✅ 语音任务控制器已启动 (PID: $VOICE_CONTROLLER_PID)"
echo ""

# 等待控制器启动
sleep 1

# 检查控制器是否正常运行
if ! ps -p $VOICE_CONTROLLER_PID > /dev/null; then
    echo "❌ 语音任务控制器启动失败"
    kill $TASK_SERVICE_PID 2>/dev/null
    exit 1
fi

echo "=========================================="
echo "  系统启动完成！"
echo "=========================================="
echo ""
echo "📢 使用说明："
echo "  1. 启动豆包语音系统（在另一个终端）："
echo "     cd ~/kuavo_ros_application/src/kuavo_doubao_model"
echo "     source ~/kuavo_ros_application/devel/setup.bash"
echo "     python3 start_communication.py"
echo ""
echo "  2. 对机器人说以下关键词触发任务："
echo "     - '综合任务'"
echo "     - '仿真任务'"
echo "     - '抓取任务'"
echo "     - '开始任务'"
echo ""
echo "  3. 机器人将自动执行抓取物品+搬箱子任务"
echo ""
echo "🔧 调试命令："
echo "  查看任务状态: rostopic echo /task_status"
echo "  查看语音识别: rostopic echo /voice_asr_result"
echo "  手动触发任务: rosservice call /start_full_task"
echo ""
echo "⏹️  停止系统: Ctrl+C"
echo ""

# 等待用户中断
trap "echo ''; echo '正在停止服务...'; kill $TASK_SERVICE_PID $VOICE_CONTROLLER_PID 2>/dev/null; echo '✅ 服务已停止'; exit 0" INT TERM

# 保持脚本运行
wait $TASK_SERVICE_PID $VOICE_CONTROLLER_PID
