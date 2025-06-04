#!/bin/bash

# 设置默认路径（用户可通过设置环境变量覆盖）
PROJECT_DIR="${PROJECT_DIR:-/home/lab/kuavo_venv}"
VENV_NAME="joint_cali"
VENV_PATH="$PROJECT_DIR/$VENV_NAME"
#当前目录
pre_dir=$(cd "$(dirname "$0")" || exit; pwd)


echo "📦 正在创建虚拟环境：$VENV_PATH"

if ! command -v python3 >/dev/null; then
    echo "🔧 未检测到 python3，开始安装..."
    sudo apt update
    sudo apt install -y python3
fi

if ! python3 -m venv -h >/dev/null 2>&1; then
    echo "🔧 未检测到 python3-venv，开始安装..."
    sudo apt update
    sudo apt install -y python3-venv
fi


mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "❌ 无法进入目录 $PROJECT_DIR"; exit 1; }

# 3. 创建虚拟环境（如果尚未创建）
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 正在创建虚拟环境 $VENV_PATH ..."
    python3 -m venv "$VENV_NAME"
else
    echo "✅ 虚拟环境已存在：$VENV_PATH"
fi


source "$VENV_PATH/bin/activate"


# REQ_FILE="$(pwd)/scripts/joint_cali/requirements.txt"
REQ_FILE="$pre_dir/requirements.txt"
echo "📦 正在安装依赖：$REQ_FILE"
if [ -f "$REQ_FILE" ]; then
    echo "📦 正在安装依赖..."
    pip install -r "$REQ_FILE"
else
    echo "⚠️ 未找到 requirements.txt，请确保在项目根目录！"
fi

# 等待前面的依赖安准完成后安装
echo "📦正在安装cyipopt,pin"
pip install cyipopt==1.1.0
pip install pin==3.4.0
pip install PyQt5==5.15.11

echo "📌 当前 Python 版本: $(python --version)"
echo "📌 请注意：后续需要激活环境，运行：source \"$VENV_PATH/bin/activate\""
sleep 1
echo "                                   
 ▄▄▄▄                   ██              
 ▀▀██                   ▀▀              
   ██       ▄████▄    ████     ██    ██ 
   ██      ██▄▄▄▄██     ██     ██    ██ 
   ██      ██▀▀▀▀▀▀     ██     ██    ██ 
   ██▄▄▄   ▀██▄▄▄▄█     ██     ██▄▄▄███ 
    ▀▀▀▀     ▀▀▀▀▀      ██      ▀▀▀▀ ▀▀ 
                     ████▀              
                                   
"

# export LD_LIBRARY_PATH=/opt/openrobots/lib:$LD_LIBRARY_PATH
# export PYTHONPATH=/opt/openrobots/lib/python3/dist-packages:$PYTHONPATH
