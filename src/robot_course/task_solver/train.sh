#!/bin/bash
# 快速训练脚本 (Docker环境)

echo "=========================================="
echo "YOLOv8 训练 - task_grasp 数据集"
echo "=========================================="

# 数据集路径
DATA_YAML="/root/kuavo_ws/src/robot_course/task_solver/dataset/task_grasp/data.yaml"

# 检查数据集是否存在
if [ ! -f "$DATA_YAML" ]; then
    echo "错误: 找不到数据集配置文件: $DATA_YAML"
    exit 1
fi

echo "数据集配置: $DATA_YAML"
echo ""
echo "开始训练..."
echo "模型: yolov8n.pt (nano - 最快)"
echo "轮数: 100"
echo "批次大小: 16"
echo ""

# 开始训练
python3 src/robot_course/task_solver/scripts/train_yolo.py \
    --data "$DATA_YAML" \
    --model yolov8n.pt \
    --epochs 100 \
    --batch 16 \
    --imgsz 640 \
    --name task_grasp_model \
    --device 0 \
    --validate

echo ""
echo "=========================================="
echo "训练完成！"
echo "模型保存在: runs/detect/task_grasp_model/weights/best.pt"
echo ""
echo "使用训练好的模型："
echo "roslaunch task_solver task_grasp.launch yolo_model:=/root/kuavo_ws/runs/detect/task_grasp_model/weights/best.pt"
echo "=========================================="
