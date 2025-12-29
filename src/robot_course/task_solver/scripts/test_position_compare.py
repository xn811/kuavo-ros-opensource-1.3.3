#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
位置对比测试脚本
对比Gazebo真实位置和YOLO检测位置，验证检测精度
"""

import rospy
import json
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from std_msgs.msg import String
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PoseStamped


class PositionCompare:
    def __init__(self):
        rospy.init_node('position_compare', anonymous=True)
        
        # 机器人模型名称
        self.robot_model = 'biped_s42'
        
        # TF2
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        # YOLO检测结果
        self.detections_3d = []
        self.detection_sub = rospy.Subscriber(
            '/yolo/detections_3d', String, self.detection_callback, queue_size=10
        )
        
        # Gazebo服务
        rospy.wait_for_service('/gazebo/get_model_state')
        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        
        rospy.loginfo("PositionCompare initialized")
    
    def detection_callback(self, msg):
        """处理YOLO检测结果"""
        try:
            self.detections_3d = json.loads(msg.data)
        except json.JSONDecodeError:
            self.detections_3d = []
    
    def get_gazebo_model_pose(self, model_name, reference_frame='world'):
        """从Gazebo获取模型位置"""
        try:
            req = GetModelStateRequest()
            req.model_name = model_name
            req.relative_entity_name = reference_frame
            resp = self.get_model_state(req)
            
            if resp.success:
                pos = resp.pose.position
                return (pos.x, pos.y, pos.z)
            else:
                return None
        except Exception as e:
            rospy.logerr(f"获取模型 {model_name} 位置失败: {e}")
            return None
    
    def get_gazebo_pose_relative_to_robot(self, model_name):
        """从Gazebo获取物体相对于机器人的真实位置（手动计算）"""
        # 获取物体世界坐标
        obj_pos = self.get_gazebo_model_pose(model_name, 'world')
        if obj_pos is None:
            return None
        
        # 获取机器人世界坐标和朝向
        try:
            req = GetModelStateRequest()
            req.model_name = self.robot_model
            req.relative_entity_name = 'world'
            resp = self.get_model_state(req)
            
            if not resp.success:
                return None
            
            robot_pos = resp.pose.position
            robot_ori = resp.pose.orientation
            
            # 计算相对位置（世界坐标系）
            rel_x = obj_pos[0] - robot_pos.x
            rel_y = obj_pos[1] - robot_pos.y
            rel_z = obj_pos[2] - robot_pos.z
            
            # 从四元数计算yaw角
            import math
            siny_cosp = 2 * (robot_ori.w * robot_ori.z + robot_ori.x * robot_ori.y)
            cosy_cosp = 1 - 2 * (robot_ori.y * robot_ori.y + robot_ori.z * robot_ori.z)
            yaw = math.atan2(siny_cosp, cosy_cosp)
            
            # 旋转到机器人坐标系 (base_link: x前, y左, z上)
            cos_yaw = math.cos(-yaw)
            sin_yaw = math.sin(-yaw)
            
            base_x = rel_x * cos_yaw - rel_y * sin_yaw
            base_y = rel_x * sin_yaw + rel_y * cos_yaw
            base_z = rel_z
            
            return (base_x, base_y, base_z)
            
        except Exception as e:
            rospy.logerr(f"计算相对位置失败: {e}")
            return None
    
    def get_robot_pose(self):
        """获取机器人在世界坐标系中的位置"""
        return self.get_gazebo_model_pose(self.robot_model)
    
    def world_to_base_link(self, world_pos):
        """将世界坐标转换为base_link坐标（通过机器人位置计算）"""
        robot_pos = self.get_robot_pose()
        if robot_pos is None:
            return None
        
        # 简单计算：物体相对于机器人的位置
        # 假设机器人朝向Y负方向（根据场景）
        rel_x = world_pos[0] - robot_pos[0]
        rel_y = world_pos[1] - robot_pos[1]
        rel_z = world_pos[2] - robot_pos[2]
        
        # 机器人朝向Y负方向，需要旋转坐标系
        # base_link: x朝前, y朝左, z朝上
        # 如果机器人朝Y负方向: 前方是-Y, 左方是-X
        base_x = -rel_y  # 前方
        base_y = -rel_x  # 左方
        base_z = rel_z   # 上方
        
        return (base_x, base_y, base_z)
    
    def list_gazebo_models(self):
        """列出场景中的物体模型"""
        # 常见的物体名称模式 - 扩展搜索范围
        possible_models = []
        for base in ['cup', 'plate', 'scissors', 'bottle', 'mug']:
            possible_models.append(base)
            for i in range(1, 10):
                possible_models.append(f'{base}{i}')
                possible_models.append(f'{base}_{i}')
        
        found_models = []
        for model in possible_models:
            pos = self.get_gazebo_model_pose(model)
            if pos is not None:
                found_models.append((model, pos))
        
        return found_models
    
    def compare_positions(self):
        """对比Gazebo真实位置和YOLO检测位置"""
        rospy.loginfo("\n" + "="*60)
        rospy.loginfo("位置对比测试")
        rospy.loginfo("="*60)
        
        # 1. 获取机器人位置和朝向
        try:
            req = GetModelStateRequest()
            req.model_name = self.robot_model
            req.relative_entity_name = 'world'
            resp = self.get_model_state(req)
            
            if resp.success:
                pos = resp.pose.position
                ori = resp.pose.orientation
                # 计算yaw角
                import math
                siny_cosp = 2 * (ori.w * ori.z + ori.x * ori.y)
                cosy_cosp = 1 - 2 * (ori.y * ori.y + ori.z * ori.z)
                yaw = math.atan2(siny_cosp, cosy_cosp)
                rospy.loginfo(f"\n机器人 {self.robot_model}:")
                rospy.loginfo(f"  位置(world): ({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f})")
                rospy.loginfo(f"  朝向(yaw):   {math.degrees(yaw):.1f}°")
            else:
                rospy.logwarn("无法获取机器人位置")
                yaw = 0
        except Exception as e:
            rospy.logerr(f"获取机器人状态失败: {e}")
            return
        
        # 2. 获取Gazebo中的物体
        rospy.loginfo("\n--- Gazebo物体位置 ---")
        gazebo_models = self.list_gazebo_models()
        
        gazebo_base_positions = {}
        for model_name, world_pos in gazebo_models:
            # 计算相对于机器人的位置
            rel_x = world_pos[0] - pos.x
            rel_y = world_pos[1] - pos.y
            rel_z = world_pos[2] - pos.z
            
            # 旋转到base_link坐标系
            cos_yaw = math.cos(-yaw)
            sin_yaw = math.sin(-yaw)
            base_x = rel_x * cos_yaw - rel_y * sin_yaw
            base_y = rel_x * sin_yaw + rel_y * cos_yaw
            base_z = rel_z
            
            dist = (base_x**2 + base_y**2 + base_z**2)**0.5
            gazebo_base_positions[model_name] = (base_x, base_y, base_z)
            
            rospy.loginfo(f"{model_name}:")
            rospy.loginfo(f"  World:     ({world_pos[0]:.3f}, {world_pos[1]:.3f}, {world_pos[2]:.3f})")
            rospy.loginfo(f"  Base_link: ({base_x:.3f}, {base_y:.3f}, {base_z:.3f}) dist={dist:.3f}m")
        
        # 3. 获取YOLO检测结果
        rospy.loginfo("\n--- YOLO检测位置 (base_link) ---")
        
        if not self.detections_3d:
            rospy.logwarn("未收到YOLO检测结果")
        
        for det in self.detections_3d:
            p = det['position']
            rospy.loginfo(f"{det['class_name']} (ID:{det.get('track_id', '?')}): "
                         f"({p['x']:.3f}, {p['y']:.3f}, {p['z']:.3f}) "
                         f"dist={det.get('distance', 0):.3f}m conf={det.get('confidence', 0):.2f}")
        
        # 4. 对比误差 - 每个YOLO检测找最近的同类Gazebo物体
        rospy.loginfo("\n--- 位置误差对比 (YOLO检测 vs 最近同类Gazebo物体) ---")
        
        for det in self.detections_3d:
            yolo_pos = det['position']
            class_name = det['class_name']
            
            # 找同类物体中位置最近的
            best_match = None
            min_dist = float('inf')
            
            for model_name, base_pos in gazebo_base_positions.items():
                # 检查是否同类
                if class_name in model_name.lower() or model_name.lower().startswith(class_name):
                    dist = ((yolo_pos['x'] - base_pos[0])**2 + 
                           (yolo_pos['y'] - base_pos[1])**2 + 
                           (yolo_pos['z'] - base_pos[2])**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        best_match = (model_name, base_pos)
            
            if best_match:
                model_name, base_pos = best_match
                error_x = yolo_pos['x'] - base_pos[0]
                error_y = yolo_pos['y'] - base_pos[1]
                error_z = yolo_pos['z'] - base_pos[2]
                error_total = (error_x**2 + error_y**2 + error_z**2)**0.5
                
                status = "✓" if error_total < 0.15 else "✗"
                rospy.loginfo(f"{status} {class_name}(ID:{det.get('track_id','?')}) vs {model_name}:")
                rospy.loginfo(f"    YOLO:   ({yolo_pos['x']:.3f}, {yolo_pos['y']:.3f}, {yolo_pos['z']:.3f})")
                rospy.loginfo(f"    Gazebo: ({base_pos[0]:.3f}, {base_pos[1]:.3f}, {base_pos[2]:.3f})")
                rospy.loginfo(f"    误差:   ({error_x:.3f}, {error_y:.3f}, {error_z:.3f}) 总={error_total*100:.1f}cm")
            else:
                rospy.logwarn(f"{class_name}(ID:{det.get('track_id','?')}): 未找到对应的Gazebo物体")
        
        # 5. 关键分析：YOLO检测位置最近的是哪个Gazebo物体？
        rospy.loginfo("\n--- 位置验证 (YOLO位置最近的Gazebo物体是什么?) ---")
        for det in self.detections_3d:
            yolo_pos = det['position']
            class_name = det['class_name']
            
            # 找YOLO位置最近的Gazebo物体
            closest_model = None
            min_dist = float('inf')
            for model_name, base_pos in gazebo_base_positions.items():
                dist = ((yolo_pos['x'] - base_pos[0])**2 + 
                       (yolo_pos['y'] - base_pos[1])**2 + 
                       (yolo_pos['z'] - base_pos[2])**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    closest_model = model_name
            
            if closest_model:
                if class_name in closest_model.lower():
                    rospy.loginfo(f"✓ YOLO={class_name} -> 最近物体={closest_model} (距离{min_dist*100:.1f}cm) 匹配正确")
                else:
                    rospy.logerr(f"✗ YOLO={class_name} -> 最近物体={closest_model} (距离{min_dist*100:.1f}cm) 位置错误!")
        
        rospy.loginfo("\n" + "="*60)
    
    def run_continuous(self, rate_hz=1):
        """持续对比"""
        rate = rospy.Rate(rate_hz)
        while not rospy.is_shutdown():
            self.compare_positions()
            rate.sleep()
    
    def run_once(self):
        """单次对比"""
        rospy.sleep(2.0)  # 等待数据
        self.compare_positions()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="位置对比测试")
    parser.add_argument("--continuous", action="store_true", help="持续对比模式")
    parser.add_argument("--rate", type=float, default=0.5, help="对比频率(Hz)")
    args = parser.parse_args()
    
    try:
        compare = PositionCompare()
        
        if args.continuous:
            compare.run_continuous(args.rate)
        else:
            compare.run_once()
    
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
