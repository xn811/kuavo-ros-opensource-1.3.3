#!/bin/bash

SERVICE_NAME="websocket_start"

# 检查服务是否active,如果active则停止服务并禁用服务
if systemctl is-active --quiet ${SERVICE_NAME}.service; then
    echo "${SERVICE_NAME}.service 正在运行，正在停止..."
    sudo systemctl stop ${SERVICE_NAME}.service
    sudo systemctl disable ${SERVICE_NAME}.service
    echo "${SERVICE_NAME}.service 已停止"
else
    echo "${SERVICE_NAME}.service 未在运行"
fi

# 更新服务脚本路径

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 拼接 websocket_start.service 的绝对路径
SERVICE_FILE="$SCRIPT_DIR/websocket_start.service"
START_SCRIPT_PATH="$SCRIPT_DIR/websocket_start_script.sh"

# 替换 ExecStart 路径
sudo sed -i "s|^ExecStart=.*|ExecStart=/bin/bash $START_SCRIPT_PATH|" $SERVICE_FILE
sudo cp $SERVICE_FILE /etc/systemd/system/

# 重新启动服务
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl start ${SERVICE_NAME}.service

echo "服务已重新启动并启用"
