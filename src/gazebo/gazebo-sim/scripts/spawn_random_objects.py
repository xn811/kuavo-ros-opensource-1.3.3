#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据随机种子在指定位置生成随机物品
从ROS参数服务器读取6个位置和随机种子，然后随机分配物品到这些位置
"""

import rospy
import random
import subprocess
import rospkg

def get_positions():
    """从ROS参数服务器获取6个位置"""
    positions = []
    for i in range(1, 7):
        x = rospy.get_param(f'/object_pos{i}_x', 0.0)
        y = rospy.get_param(f'/object_pos{i}_y', -4.7)
        positions.append({'name': f'pos{i}', 'x': x, 'y': y})
    return positions

def randomize_objects(seed, positions):
    """根据种子随机分配物品到位置"""
    random.seed(seed)
    
    # 定义6种物品
    objects = [
        {"type": "cup", "model": "Plastic_Cup", "name": "cup1"},
        {"type": "cup", "model": "Plastic_Cup", "name": "cup2"},
        {"type": "plate", "model": "Ecoforms_Plant_Plate_S11Turquoise", "name": "plate1"},
        {"type": "plate", "model": "Ecoforms_Plant_Plate_S11Turquoise", "name": "plate2"},
        {"type": "scissors", "model": "Diamond_Visions_Scissors_Red", "name": "scissors1"},
        {"type": "scissors", "model": "Diamond_Visions_Scissors_Red", "name": "scissors2"}
    ]
    
    # 随机打乱物品顺序
    random.shuffle(objects)
    
    # 分配物品到位置
    assignment = []
    for i, pos in enumerate(positions):
        obj = objects[i]
        assignment.append({
            'object': obj,
            'x': pos['x'],
            'y': pos['y']
        })
    
    return assignment

def spawn_object(model_name, model_file, x, y, z):
    """生成单个物品"""
    import os
    rospack = rospkg.RosPack()
    gazebo_sim_path = rospack.get_path('gazebo_sim')
    model_path = f"{gazebo_sim_path}/models/{model_file}/model.sdf"
    
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        rospy.logerr(f"Model file not found: {model_path}")
        return False
    
    cmd = [
        'rosrun', 'gazebo_ros', 'spawn_model',
        '-sdf', '-model', model_name,
        '-file', model_path,
        '-x', str(x), '-y', str(y), '-z', str(z)
    ]
    
    rospy.loginfo(f"Spawning {model_name} at ({x}, {y}, {z})")
    
    result = subprocess.call(cmd)
    if result != 0:
        rospy.logerr(f"Failed to spawn {model_name}, return code: {result}")
        return False
    return True

def main():
    rospy.init_node('spawn_random_objects', anonymous=True)
    
    # 获取随机种子
    seed = rospy.get_param('/random_seed', 110)
    rospy.loginfo(f"Using random seed: {seed}")
    
    # 获取6个位置
    positions = get_positions()
    rospy.loginfo(f"Loaded {len(positions)} positions")
    for pos in positions:
        rospy.loginfo(f"  {pos['name']}: ({pos['x']}, {pos['y']})")
    
    # 随机分配物品
    assignment = randomize_objects(seed, positions)
    
    # 打印分配结果
    rospy.loginfo("Object assignment:")
    for item in assignment:
        obj = item['object']
        rospy.loginfo(f"  {obj['name']} ({obj['type']}) at ({item['x']}, {item['y']})")
    
    # 等待Gazebo准备好
    rospy.sleep(2.5)
    
    # 并行生成所有物品
    z = 0.85  # 桌面高度
    import threading
    
    threads = []
    for item in assignment:
        obj = item['object']
        thread = threading.Thread(
            target=spawn_object,
            args=(obj['name'], obj['model'], item['x'], item['y'], z)
        )
        thread.start()
        threads.append(thread)
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    rospy.loginfo("All objects spawned successfully")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
