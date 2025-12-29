#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练自定义YOLO模型
"""

import argparse
from ultralytics import YOLO
import os


def train_yolo(args):
    """训练YOLO模型"""
    
    print("="*60)
    print("YOLOv8 Training Script")
    print("="*60)
    print(f"Base model: {args.model}")
    print(f"Data config: {args.data}")
    print(f"Epochs: {args.epochs}")
    print(f"Image size: {args.imgsz}")
    print(f"Batch size: {args.batch}")
    print(f"Device: {args.device}")
    print("="*60)
    
    # 检查数据配置文件
    if not os.path.exists(args.data):
        print(f"\nError: Data config file not found: {args.data}")
        print("Please create a data.yaml file with the following format:")
        print("""
# data.yaml
path: /path/to/dataset  # 数据集根目录
train: images/train     # 训练集图像目录（相对于path）
val: images/val         # 验证集图像目录（相对于path）

nc: 3  # 类别数量
names: ['cup', 'plate', 'scissors']  # 类别名称
        """)
        return
    
    # 加载预训练模型
    print(f"\nLoading model: {args.model}")
    model = YOLO(args.model)
    
    # 开始训练
    print("\nStarting training...")
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        device=args.device,
        patience=args.patience,
        save=True,
        plots=True,
        verbose=True
    )
    
    print("\n" + "="*60)
    print("Training completed!")
    print(f"Best model saved to: runs/detect/{args.name}/weights/best.pt")
    print("="*60)
    
    # 验证模型
    if args.validate:
        print("\nValidating model...")
        metrics = model.val()
        print(f"\nmAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")


def main():
    parser = argparse.ArgumentParser(description='Train YOLOv8 model for object detection')
    
    # 模型参数
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Base model (yolov8n.pt, yolov8s.pt, yolov8m.pt, etc.)')
    parser.add_argument('--data', type=str, required=True,
                       help='Path to data.yaml file')
    
    # 训练参数
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs')
    parser.add_argument('--imgsz', type=int, default=640,
                       help='Image size for training')
    parser.add_argument('--batch', type=int, default=16,
                       help='Batch size')
    parser.add_argument('--device', type=str, default='0',
                       help='Device to use (0, 1, 2, ... or cpu)')
    parser.add_argument('--name', type=str, default='gazebo_objects',
                       help='Experiment name')
    parser.add_argument('--patience', type=int, default=50,
                       help='Early stopping patience')
    
    # 其他选项
    parser.add_argument('--validate', action='store_true',
                       help='Validate model after training')
    
    args = parser.parse_args()
    
    train_yolo(args)


if __name__ == '__main__':
    main()
