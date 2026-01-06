#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复位Gazebo中的物品位置
用于抓取调试时快速复位被打倒的物品
"""

import rospy
import argparse
from gazebo_msgs.srv import GetWorldProperties, SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose, Point, Quaternion


# 默认物品位置配置 (从launch文件中的6个位置)
DEFAULT_OBJECT_POSITIONS = [
    {'x': -0.0, 'y': -4.8, 'z': 0.85},
    {'x': -0.43, 'y': -5.1, 'z': 0.85},
    {'x': -0.22, 'y': -4.78, 'z': 0.85},
    {'x': -0.43, 'y': -4.8, 'z': 0.85},
    {'x': 0.44, 'y': -5.02, 'z': 0.85},
    {'x': 0.42, 'y': -5.2, 'z': 0.85},
]

# 物品名称列表 (spawn_random_objects.py 中定义的)
OBJECT_NAMES = ['cup1', 'cup2', 'plate1', 'plate2', 'scissors1', 'scissors2']


def get_all_models():
    """获取Gazebo中所有模型名称"""
    try:
        rospy.wait_for_service('/gazebo/get_world_properties', timeout=5.0)
        get_world = rospy.ServiceProxy('/gazebo/get_world_properties', GetWorldProperties)
        resp = get_world()
        return resp.model_names
    except Exception as e:
        rospy.logerr(f"获取模型列表失败: {e}")
        return []


def reset_model(model_name, x, y, z, yaw=0):
    """重置单个模型的位置"""
    try:
        rospy.wait_for_service('/gazebo/set_model_state', timeout=5.0)
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        
        state = ModelState()
        state.model_name = model_name
        state.pose = Pose()
        state.pose.position = Point(x, y, z)
        # 四元数表示无旋转 (w=1)
        state.pose.orientation = Quaternion(0, 0, 0, 1)
        state.reference_frame = 'world'
        
        resp = set_state(state)
        return resp.success
    except Exception as e:
        rospy.logerr(f"重置模型 {model_name} 失败: {e}")
        return False


def reset_all_objects():
    """复位所有物品到初始位置"""
    import random
    
    models = get_all_models()
    
    # 获取随机种子 (与生成时相同)
    try:
        seed = rospy.get_param('/random_seed', 110)
    except:
        seed = 110
    
    rospy.loginfo(f"使用随机种子: {seed}")
    
    # 用相同的种子重新计算分配
    random.seed(seed)
    objects = OBJECT_NAMES.copy()
    random.shuffle(objects)
    
    # 物品名到位置的映射
    object_to_pos = {}
    for i, obj_name in enumerate(objects):
        if i < len(DEFAULT_OBJECT_POSITIONS):
            object_to_pos[obj_name] = DEFAULT_OBJECT_POSITIONS[i]
    
    rospy.loginfo(f"物品分配: {object_to_pos}")
    
    reset_count = 0
    for obj_name, pos in object_to_pos.items():
        if obj_name in models:
            if reset_model(obj_name, pos['x'], pos['y'], pos['z']):
                rospy.loginfo(f"✓ 复位 {obj_name} -> ({pos['x']}, {pos['y']}, {pos['z']})")
                reset_count += 1
        else:
            rospy.logwarn(f"未找到模型: {obj_name}")
    
    rospy.loginfo(f"共复位 {reset_count} 个物品")
    return reset_count


def reset_single_object(model_name, x=None, y=None, z=None):
    """复位单个物品"""
    import random
    
    models = get_all_models()
    
    if model_name not in models:
        # 尝试模糊匹配
        matches = [m for m in models if model_name in m]
        if len(matches) == 1:
            model_name = matches[0]
        elif len(matches) > 1:
            rospy.logwarn(f"找到多个匹配: {matches}，请指定完整名称")
            return False
        else:
            rospy.logerr(f"未找到模型: {model_name}")
            rospy.loginfo(f"可用模型: {[m for m in models if m in OBJECT_NAMES]}")
            return False
    
    # 如果没指定位置，根据随机种子计算原始位置
    if x is None or y is None or z is None:
        try:
            seed = rospy.get_param('/random_seed', 110)
        except:
            seed = 110
        
        random.seed(seed)
        objects = OBJECT_NAMES.copy()
        random.shuffle(objects)
        
        if model_name in objects:
            idx = objects.index(model_name)
            if idx < len(DEFAULT_OBJECT_POSITIONS):
                pos = DEFAULT_OBJECT_POSITIONS[idx]
                x = x if x is not None else pos['x']
                y = y if y is not None else pos['y']
                z = z if z is not None else pos['z']
    
    if x is None:
        x, y, z = 0, -4.8, 0.85  # 默认位置
    
    if reset_model(model_name, x, y, z):
        rospy.loginfo(f"✓ 复位 {model_name} -> ({x}, {y}, {z})")
        return True
    return False


def list_objects():
    """列出所有可抓取物品"""
    models = get_all_models()
    objects = [m for m in models if m in OBJECT_NAMES or any(k in m for k in ['cup', 'plate', 'scissors', 'block'])]
    
    rospy.loginfo("当前场景中的物品:")
    for obj in sorted(objects):
        rospy.loginfo(f"  - {obj}")
    return objects


def main():
    parser = argparse.ArgumentParser(description="复位Gazebo中的物品位置")
    parser.add_argument("--all", action="store_true", help="复位所有物品")
    parser.add_argument("--model", type=str, help="复位指定模型 (如 cup_0)")
    parser.add_argument("--list", action="store_true", help="列出所有物品")
    parser.add_argument("-x", type=float, help="X坐标")
    parser.add_argument("-y", type=float, help="Y坐标")
    parser.add_argument("-z", type=float, help="Z坐标")
    
    args, _ = parser.parse_known_args()
    
    rospy.init_node('reset_objects', anonymous=True)
    
    if args.list:
        list_objects()
    elif args.model:
        reset_single_object(args.model, args.x, args.y, args.z)
    elif args.all:
        reset_all_objects()
    else:
        # 默认复位所有
        reset_all_objects()


if __name__ == '__main__':
    main()
