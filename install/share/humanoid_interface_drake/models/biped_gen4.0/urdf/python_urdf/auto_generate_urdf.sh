#!/bin/bash

# 启动第一个 Python 脚本，生成all_joint.urdf,必須第一個啓動
echo "Running all_joint.py"
python3 ./all_joint.py

# 启动第二个 Python 脚本,生成wbc需要的手腳，必須第二個啓動
echo "Running full.py"
python3 ./full.py
# 後續腳本沒有特殊順序
echo "Running all_arm.py"
python3 ./all_arm.py
echo "Running all_leg.py"
python3 ./all_leg.py

echo "Running Lleg.py"
python3 ./Lleg.py
echo "Running Rleg.py"
python3 ./Rleg.py
# echo "Running Larm.py"
# python3 ./Larm.py
# echo "Running Rarm.py"
# python3 ./Rarm.py