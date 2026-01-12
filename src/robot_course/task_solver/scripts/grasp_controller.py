#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取控制器
结合YOLO 3D检测结果，实现对杯子、盘子、剪刀的抓取
提供ROS服务接口供外部调用
"""

import rospy
import math
import numpy as np
import time
import argparse
import json
import os
from collections import deque

import tf2_ros
from std_msgs.msg import String
from kuavo_msgs.msg import armTargetPoses, robotHandPosition, robotHeadMotionData
from kuavo_msgs.srv import changeArmCtrlMode, changeArmCtrlModeRequest
from kuavo_msgs.srv import twoArmHandPoseCmdSrv
from kuavo_msgs.msg import twoArmHandPoseCmd, ikSolveParam

# 抓取服务
try:
    from task_solver.srv import GraspObject, GraspObjectResponse
    from task_solver.srv import PlaceObject, PlaceObjectResponse
    from task_solver.srv import ResetArm, ResetArmResponse
    HAS_GRASP_SRV = True
except ImportError:
    HAS_GRASP_SRV = False
    rospy.logwarn("task_solver服务未编译，服务模式不可用")

# 仿真抓取服务
try:
    from gazebo_ros_link_attacher.srv import Grasp, GraspRequest
    HAS_GAZEBO_GRASP = True
except ImportError:
    HAS_GAZEBO_GRASP = False


class Quaternion:
    """四元数类"""
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0


class GraspController:
    """抓取控制器"""
    
    # 运动时间参数
    ARM_MOVE_TIME = 3      # 手臂运动时间(秒)
    ARM_WAIT_TIME = 3.0    # 手臂运动等待时间(秒)
    ARM_STAGE_WAIT = 15.0   # 中间阶段等待时间(秒)，用于固定姿态
    ARM_TF_TIMEOUT = 60.0  # TF等待超时时间(秒)，用于IK目标位置
    ARM_STABLE_THRESHOLD = 0.001  # 稳定检测阈值(米)，误差变化小于此值认为稳定
    ARM_STABLE_COUNT = 20  # 稳定检测次数，连续稳定此次数认为运动完成(20次@10Hz=2秒)
    ARM_SETTLE_TIME = 1.0  # 运动完成后额外等待时间(秒)
    
    # 目标类别映射 (YOLO类别名 -> 配置)
    # grasp_type: 'side' 侧面抓取(杯子/水瓶), 'top' 顶部抓取(盘子/剪刀/橘子)
    TARGET_CONFIG = {
        'cup': {
            'grasp_type': 'side',  # 侧面抓取
            'offset_z': 0.12,  # 减小z偏移，让手更接近杯子
            'offset_x_l': -0.045, 'offset_y_l': -0.05,
            'offset_x_r': -0.045, 'offset_y_r': 0.04,
            'offset_angle': 0.9,
            'hand_close': [80, 100, 80, 75, 75, 75],
        },
        'plate': {
            'grasp_type': 'top',  # 手掌向下抓取
            'offset_z': 0.05,  # 从上方接近
            'offset_x_l': 0.0, 'offset_y_l': 0.0,
            'offset_x_r': 0.0, 'offset_y_r': 0.0,
            'offset_angle': 1.0,
            'hand_close': [60, 100, 60, 60, 60, 60],
        },
        'scissors': {
            'grasp_type': 'top',  # 手掌向下抓取
            'offset_z': 0.05,  # 从上方接近
            'offset_x_l': 0.0, 'offset_y_l': 0.0,
            'offset_x_r': 0.0, 'offset_y_r': 0.0,
            'offset_angle': 1.0,
            'hand_close': [90, 100, 90, 80, 80, 80],
        },
    }
    
    # 手部姿态
    HAND_OPEN = [0, 100, 0, 0, 0, 0]
    HAND_ZERO = [0, 0, 0, 0, 0, 0]
    
    # 不同机器人版本的末端初始位置
    ROBOT_ZERO_CONFIG = {
        45: {'x': -0.0173, 'y': -0.2927, 'z': -0.2837},
        49: {'x': -0.0173, 'y': -0.2927, 'z': -0.2837},
        42: {'x': -0.0175, 'y': -0.25886, 'z': -0.20115},
        52: {'x': -0.012, 'y': -0.255 + 0.03, 'z': -0.315},
    }
    
    def __init__(self, use_offset=False, use_sim=False):
        # 注意: rospy.init_node 在 main() 中调用
        
        self.use_offset = use_offset
        self.use_sim = use_sim  # 仿真模式使用吸附服务
        
        # 获取机器人版本并设置对应参数
        self._init_robot_params()
        
        # 检测结果缓存
        self.detections_3d = []
        self.detection_history = {}  # 用于平滑
        self.history_size = 5
        
        # IK参数
        self.ik_solve_param = ikSolveParam()
        self.ik_solve_param.major_optimality_tol = 1e-3
        self.ik_solve_param.major_feasibility_tol = 1e-3
        self.ik_solve_param.minor_feasibility_tol = 1e-3
        self.ik_solve_param.major_iterations_limit = 500
        self.ik_solve_param.oritation_constraint_tol = 1e-3
        self.ik_solve_param.pos_constraint_tol = 1e-3
        self.ik_solve_param.pos_cost_weight = 0.0
        
        # 订阅YOLO 3D检测结果
        self.detection_sub = rospy.Subscriber(
            '/yolo/detections_3d', String, self.detection_callback, queue_size=10
        )
        
        # 发布器
        self.head_pub = rospy.Publisher('/robot_head_motion_data', robotHeadMotionData, queue_size=10)
        self.hand_pub = rospy.Publisher('/control_robot_hand_position', robotHandPosition, queue_size=10)
        self.arm_pub = rospy.Publisher('kuavo_arm_target_poses', armTargetPoses, queue_size=10)
        
        # 仿真抓取服务
        self.grasp_service_name = '/kuavo_attacher_node/grasp'
        
        # 当前抓取状态
        self.grasped_object = None   # 当前抓取的物体类别
        self.grasped_hand = None     # 使用的手: "left" / "right"
        self.grasped_track_id = -1   # 抓取的物体track_id
        
        # 注册抓取/放置服务
        if HAS_GRASP_SRV:
            self.grasp_srv = rospy.Service('/grasp_controller/grasp', GraspObject, self._handle_grasp_service)
            self.place_srv = rospy.Service('/grasp_controller/place', PlaceObject, self._handle_place_service)
            self.reset_arm_srv = rospy.Service('/grasp_controller/reset_arm', ResetArm, self._handle_reset_arm_service)
            rospy.loginfo("抓取服务已注册: /grasp_controller/grasp, /grasp_controller/place, /grasp_controller/reset_arm")
        
        # TF监听器
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.sleep(0.5)  # 等待发布器注册
        rospy.loginfo(f"GraspController initialized (sim={self.use_sim})")
    
    def _init_robot_params(self):
        """根据机器人版本初始化参数"""
        # 从环境变量获取机器人版本
        robot_version_str = os.environ.get('ROBOT_VERSION', '45')
        try:
            robot_version = int(robot_version_str)
            rospy.loginfo(f"机器人版本 (ROBOT_VERSION): {robot_version}")
        except ValueError:
            robot_version = 45
            rospy.logwarn(f"ROBOT_VERSION={robot_version_str} 无效，使用默认值: {robot_version}")
        
        # 匹配版本配置
        config = None
        for series, cfg in self.ROBOT_ZERO_CONFIG.items():
            if self._start_with_version(robot_version, series):
                config = cfg
                rospy.loginfo(f"匹配到 {series} 系列配置")
                break
        
        if config is None:
            # 默认使用45系列
            config = self.ROBOT_ZERO_CONFIG[45]
            rospy.logwarn(f"未匹配到版本 {robot_version}，使用45系列默认配置")
        
        self.robot_zero_x = config['x']
        self.robot_zero_y = config['y']
        self.robot_zero_z = config['z']
        rospy.loginfo(f"末端初始位置: x={self.robot_zero_x:.4f}, y={self.robot_zero_y:.4f}, z={self.robot_zero_z:.4f}")
    
    def _start_with_version(self, robot_version, series):
        """检查版本号是否属于某个系列"""
        # 处理类似 100045, 100049, 100052 这样的版本号
        version_str = str(robot_version)
        series_str = str(series)
        
        # 直接匹配
        if robot_version == series:
            return True
        
        # 检查版本号是否以系列号结尾或包含系列号
        if version_str.endswith(series_str):
            return True
        
        # 检查 MMMMN 格式 (如 100045 -> 45)
        if robot_version % 100000 == series:
            return True
        
        # 检查末两位
        if robot_version % 100 == series:
            return True
            
        return False
    
    def detection_callback(self, msg):
        """处理3D检测结果"""
        try:
            self.detections_3d = json.loads(msg.data)
        except json.JSONDecodeError:
            self.detections_3d = []
    
    def get_target_by_track_id(self, track_id, timeout=5.0):
        """根据track_id获取目标位置"""
        rospy.loginfo(f"查找 track_id={track_id}...")
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown() and (time.time() - start_time < timeout):
            for det in self.detections_3d:
                if det.get('track_id') == track_id:
                    pos = det['position']
                    rospy.loginfo(f"找到 ID:{track_id} {det['class_name']} ({pos['x']:.3f}, {pos['y']:.3f}, {pos['z']:.3f})")
                    return (pos['x'], pos['y'], pos['z']), det['class_name'], track_id
            rate.sleep()
        
        rospy.logwarn(f"未找到 track_id={track_id}")
        return None, None, None
    
    def get_nearest_target(self, target_class, timeout=5.0):
        """获取最近的目标 (基于track_id)"""
        rospy.loginfo(f"查找最近的 {target_class}...")
        
        start_time = time.time()
        rate = rospy.Rate(10)
        best_det = None
        sample_count = 0
        
        while not rospy.is_shutdown() and (time.time() - start_time < timeout):
            matches = [det for det in self.detections_3d if det['class_name'] == target_class]
            
            if matches:
                # 按距离排序，取最近的
                matches.sort(key=lambda x: x.get('distance', float('inf')))
                current_best = matches[0]
                
                # 确认是同一个目标 (track_id一致)
                if best_det is None or best_det.get('track_id') == current_best.get('track_id'):
                    best_det = current_best
                    sample_count += 1
                    
                    # 采样3次确认
                    if sample_count >= 3:
                        pos = best_det['position']
                        tid = best_det.get('track_id', -1)
                        rospy.loginfo(f"确认目标: {target_class} ID:{tid} ({pos['x']:.3f}, {pos['y']:.3f}, {pos['z']:.3f})")
                        return (pos['x'], pos['y'], pos['z']), target_class, tid
                else:
                    # track_id变了，重新计数
                    best_det = current_best
                    sample_count = 1
            
            rate.sleep()
        
        if best_det:
            pos = best_det['position']
            tid = best_det.get('track_id', -1)
            return (pos['x'], pos['y'], pos['z']), target_class, tid
        
        rospy.logwarn(f"未找到 {target_class}")
        return None, None, None
    
    def get_target_by_class_index(self, target_class, index=0, timeout=5.0):
        """根据类别和序号获取目标 (index=0表示最近的)"""
        rospy.loginfo(f"查找 {target_class}#{index}...")
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown() and (time.time() - start_time < timeout):
            matches = [det for det in self.detections_3d if det['class_name'] == target_class]
            # 按距离排序
            matches.sort(key=lambda x: x.get('distance', float('inf')))
            
            if len(matches) > index:
                det = matches[index]
                pos = det['position']
                tid = det.get('track_id', -1)
                rospy.loginfo(f"找到 {target_class}#{index} ID:{tid} ({pos['x']:.3f}, {pos['y']:.3f}, {pos['z']:.3f})")
                return (pos['x'], pos['y'], pos['z']), tid
            
            rate.sleep()
        
        rospy.logwarn(f"未找到 {target_class}#{index}")
        return None, None
    
    def list_all_targets(self):
        """列出当前检测到的所有目标"""
        rospy.loginfo("当前检测到的目标:")
        by_class = {}
        for det in self.detections_3d:
            cls = det['class_name']
            if cls not in by_class:
                by_class[cls] = []
            by_class[cls].append(det)
        
        for cls, objs in by_class.items():
            objs.sort(key=lambda x: x.get('class_index', 0))
            for obj in objs:
                pos = obj['position']
                rospy.loginfo(f"  {cls}#{obj.get('class_index', 0)} [ID:{obj.get('track_id')}] "
                             f"pos=({pos['x']:.2f}, {pos['y']:.2f}, {pos['z']:.2f}) dist={obj['distance']:.2f}m")
        return by_class
    
    def get_all_targets(self, target_class, timeout=5.0):
        """获取所有指定类别的目标物体位置"""
        rospy.loginfo(f"扫描所有 {target_class}...")
        
        # 用字典存储每个目标的位置历史 (按位置聚类)
        target_clusters = {}  # key: cluster_id, value: deque of positions
        cluster_threshold = 0.15  # 15cm内认为是同一个物体
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown() and (time.time() - start_time < timeout):
            for det in self.detections_3d:
                if det['class_name'] == target_class:
                    pos = (det['position']['x'], det['position']['y'], det['position']['z'])
                    
                    # 找到最近的聚类
                    matched_cluster = None
                    min_dist = cluster_threshold
                    
                    for cid, history in target_clusters.items():
                        if len(history) > 0:
                            last_pos = history[-1]
                            dist = math.sqrt(sum((a-b)**2 for a, b in zip(pos, last_pos)))
                            if dist < min_dist:
                                min_dist = dist
                                matched_cluster = cid
                    
                    if matched_cluster is not None:
                        target_clusters[matched_cluster].append(pos)
                    else:
                        # 新建聚类
                        new_id = len(target_clusters)
                        target_clusters[new_id] = deque(maxlen=self.history_size)
                        target_clusters[new_id].append(pos)
            
            rate.sleep()
        
        # 计算每个聚类的平均位置 (至少2个样本)
        results = []
        for cid, history in target_clusters.items():
            if len(history) >= 2:
                avg_pos = (
                    np.mean([p[0] for p in history]),
                    np.mean([p[1] for p in history]),
                    np.mean([p[2] for p in history])
                )
                results.append(avg_pos)
                rospy.loginfo(f"  目标{cid}: ({avg_pos[0]:.3f}, {avg_pos[1]:.3f}, {avg_pos[2]:.3f})")
        
        rospy.loginfo(f"共检测到 {len(results)} 个 {target_class}")
        return results
    
    def get_target_position(self, target_class, timeout=10.0, exclude_positions=None):
        """获取目标物体的平均位置 (可排除已抓取的位置)"""
        rospy.loginfo(f"等待检测 {target_class}...")
        
        if exclude_positions is None:
            exclude_positions = []
        exclude_threshold = 0.15  # 15cm内认为是同一个物体
        
        positions = deque(maxlen=self.history_size)
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            if time.time() - start_time > timeout:
                rospy.logwarn(f"检测 {target_class} 超时")
                return None
            
            for det in self.detections_3d:
                if det['class_name'] == target_class:
                    pos = det['position']
                    current_pos = (pos['x'], pos['y'], pos['z'])
                    
                    # 检查是否在排除列表中
                    is_excluded = False
                    for ex_pos in exclude_positions:
                        dist = math.sqrt(sum((a-b)**2 for a, b in zip(current_pos, ex_pos)))
                        if dist < exclude_threshold:
                            is_excluded = True
                            break
                    
                    if not is_excluded:
                        positions.append(current_pos)
                        rospy.loginfo(f"检测到 {target_class}: ({pos['x']:.3f}, {pos['y']:.3f}, {pos['z']:.3f})")
            
            # 收集足够样本后返回平均值
            if len(positions) >= 3:
                avg_x = np.mean([p[0] for p in positions])
                avg_y = np.mean([p[1] for p in positions])
                avg_z = np.mean([p[2] for p in positions])
                return (avg_x, avg_y, avg_z)
            
            rate.sleep()
        
        return None

    # ==================== 运动控制函数 ====================
    
    def set_head(self, yaw, pitch):
        """控制头部 yaw:[-30,30] pitch:[-25,25]"""
        msg = robotHeadMotionData()
        msg.joint_data = [yaw, pitch]
        self.head_pub.publish(msg)
        rospy.loginfo(f"头部: yaw={yaw}, pitch={pitch}")
    
    def set_hand(self, left_pos=None, right_pos=None):
        """控制手部开合 (实机模式)"""
        if self.use_sim:
            return  # 仿真模式不使用手部控制
        msg = robotHandPosition()
        msg.left_hand_position = left_pos if left_pos else self.HAND_ZERO
        msg.right_hand_position = right_pos if right_pos else self.HAND_ZERO
        self.hand_pub.publish(msg)
    
    def sim_grasp(self, arm, action):
        """
        仿真抓取/释放 (使用gazebo link attacher)
        :param arm: "left" 或 "right"
        :param action: "grasp" 或 "release"
        :return: (success, object_name)
        """
        if not self.use_sim or not HAS_GAZEBO_GRASP:
            return True, ""
        
        try:
            rospy.wait_for_service(self.grasp_service_name, timeout=5.0)
            grasp_srv = rospy.ServiceProxy(self.grasp_service_name, Grasp)
            req = GraspRequest()
            req.arm = arm
            req.action = action
            
            resp = grasp_srv(req)
            
            if resp.ok:
                rospy.loginfo(f"仿真{action}成功: {resp.object_name}")
            else:
                rospy.logwarn(f"仿真{action}失败: {resp.message}  (距离: {resp.distance:.3f}m)")
            
            return resp.ok, resp.object_name
            
        except Exception as e:
            rospy.logerr(f"仿真抓取服务调用失败: {e}")
            return False, ""
    
    def set_arm(self, duration, joint_angles):
        """控制手臂关节角度 (度)"""
        msg = armTargetPoses()
        msg.times = [duration]
        msg.values = joint_angles
        self.arm_pub.publish(msg)
        rospy.loginfo("手臂移动中...")
    
    def get_end_effector_position(self, hand="right"):
        """
        获取手末端在base_link坐标系下的位置
        :param hand: "left" 或 "right"
        :return: (x, y, z) 或 None
        """
        # 末端link名称
        if hand == "left":
            end_link = "zarm_l7_link"
        else:
            end_link = "zarm_r7_link"
        
        try:
            trans = self.tf_buffer.lookup_transform('base_link', end_link, rospy.Time(0), rospy.Duration(1.0))
            pos = trans.transform.translation
            return (pos.x, pos.y, pos.z)
        except Exception as e:
            rospy.logwarn(f"获取TF失败: {e}")
            return None
    
    def wait_arm_reach_position(self, target_pos, hand="right", timeout=None):
        """
        等待手臂运动完成（通过检测位置稳定）
        :param target_pos: 目标位置 (x, y, z)，用于计算误差
        :param hand: "left" 或 "right"
        :param timeout: 超时时间，None则使用默认值 ARM_TF_TIMEOUT
        :return: True 运动完成
        """
        if timeout is None:
            timeout = self.ARM_TF_TIMEOUT
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        # 稳定检测：记录最近几次误差
        last_error = None
        stable_count = 0
        
        while not rospy.is_shutdown():
            elapsed = time.time() - start_time
            if elapsed > timeout:
                rospy.logwarn(f"等待手臂到位超时 ({timeout}s)")
                return True  # 超时也继续
            
            current_pos = self.get_end_effector_position(hand)
            if current_pos is None:
                rate.sleep()
                continue
            
            # 计算位置误差
            error = math.sqrt(
                (current_pos[0] - target_pos[0])**2 +
                (current_pos[1] - target_pos[1])**2 +
                (current_pos[2] - target_pos[2])**2
            )
            
            # 稳定检测：误差不再变化说明运动已完成
            if last_error is not None:
                error_change = abs(error - last_error)
                if error_change < self.ARM_STABLE_THRESHOLD:
                    stable_count += 1
                    if stable_count >= self.ARM_STABLE_COUNT:
                        rospy.loginfo(f"手臂运动已稳定")
                        time.sleep(self.ARM_SETTLE_TIME)
                        return True
                else:
                    stable_count = 0  # 重置计数
            last_error = error
            
            # 每秒打印一次进度
            if int(elapsed) != int(elapsed - 0.1):
                rospy.loginfo(f"等待手臂到位... 当前:({current_pos[0]:.3f}, {current_pos[1]:.3f}, {current_pos[2]:.3f}) 误差: {error:.3f}m")
            
            rate.sleep()
        
        return True
    
    def set_arm_mode(self, mode):
        """设置手臂控制模式 1:自动摆手 2:外部控制"""
        try:
            rospy.wait_for_service('/arm_traj_change_mode', timeout=5.0)
            client = rospy.ServiceProxy('/arm_traj_change_mode', changeArmCtrlMode)
            req = changeArmCtrlModeRequest()
            req.control_mode = mode
            res = client(req)
            if res.result:
                rospy.loginfo(f"手臂模式设置为 {mode}")
            return res.result
        except Exception as e:
            rospy.logerr(f"设置手臂模式失败: {e}")
            return False
    
    # ==================== IK逆解函数 ====================
    
    def euler_to_rotation_matrix(self, yaw, pitch, roll=0):
        """欧拉角转旋转矩阵 (Z-Y-X顺序)"""
        cy, sy = np.cos(yaw), np.sin(yaw)
        cp, sp = np.cos(pitch), np.sin(pitch)
        cr, sr = np.cos(roll), np.sin(roll)
        
        R = np.array([
            [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
            [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
            [-sp,   cp*sr,            cp*cr]
        ])
        return R
    
    def rotation_matrix_to_quaternion(self, R):
        """旋转矩阵转四元数"""
        q = Quaternion()
        trace = np.trace(R)
        
        if trace > 0:
            q.w = math.sqrt(trace + 1.0) / 2
            q.x = (R[2, 1] - R[1, 2]) / (4 * q.w)
            q.y = (R[0, 2] - R[2, 0]) / (4 * q.w)
            q.z = (R[1, 0] - R[0, 1]) / (4 * q.w)
        else:
            i = np.argmax([R[0, 0], R[1, 1], R[2, 2]])
            j, k = (i + 1) % 3, (i + 2) % 3
            t = np.zeros(4)
            t[i] = math.sqrt(R[i, i] - R[j, j] - R[k, k] + 1) / 2
            t[j] = (R[i, j] + R[j, i]) / (4 * t[i])
            t[k] = (R[i, k] + R[k, i]) / (4 * t[i])
            t[3] = (R[k, j] - R[j, k]) / (4 * t[i])
            q.x, q.y, q.z, q.w = t
        
        # 归一化
        norm = math.sqrt(q.w**2 + q.x**2 + q.y**2 + q.z**2)
        if norm > 0:
            q.w, q.x, q.y, q.z = q.w/norm, q.x/norm, q.y/norm, q.z/norm
        return q
    
    def euler_to_quaternion(self, yaw, pitch, roll=0):
        """欧拉角转四元数"""
        R = self.euler_to_rotation_matrix(yaw, pitch, roll)
        return self.rotation_matrix_to_quaternion(R)
    
    def call_ik_service(self, eef_pose_msg):
        """调用IK逆解服务"""
        try:
            rospy.wait_for_service('/ik/two_arm_hand_pose_cmd_srv', timeout=5.0)
            ik_srv = rospy.ServiceProxy('/ik/two_arm_hand_pose_cmd_srv', twoArmHandPoseCmdSrv)
            res = ik_srv(eef_pose_msg)
            return res
        except Exception as e:
            rospy.logerr(f"IK服务调用失败: {e}")
            return None

    # ==================== 抓取核心逻辑 ====================
    
    def compute_grasp_pose(self, target_pos, target_class, use_left_hand):
        """计算抓取位姿和IK参数"""
        cfg = self.TARGET_CONFIG.get(target_class, self.TARGET_CONFIG['cup'])
        grasp_type = cfg.get('grasp_type', 'side')
        
        # 计算抓取位置 (加偏移量)
        if self.use_offset:
            if use_left_hand:
                grasp_x = target_pos[0] + cfg['offset_x_l']
                grasp_y = target_pos[1] + cfg['offset_y_l']
            else:
                grasp_x = target_pos[0] + cfg['offset_x_r']
                grasp_y = target_pos[1] - cfg['offset_y_r']
            grasp_z = target_pos[2] + cfg['offset_z']
        else:
            grasp_x, grasp_y = target_pos[0], target_pos[1]
            grasp_z = target_pos[2] + cfg['offset_z']
        
        # 根据抓取类型计算末端姿态
        if grasp_type == 'top':
            # 手掌向下抓取 (盘子、剪刀、橘子)
            # pitch = 0 (手掌朝下), yaw根据位置调整
            if use_left_hand:
                yaw = math.atan2(grasp_y - 0, grasp_x - self.robot_zero_x + 1e-6)
            else:
                yaw = math.atan2(grasp_y - 0, grasp_x - self.robot_zero_x + 1e-6)
            pitch = 0.0  # 手掌朝下
            roll = 0.0
            quat = self.euler_to_quaternion(yaw, pitch, roll)
            # 顶部抓取的四元数：手掌朝下
            # 使用固定的朝下姿态
            if use_left_hand:
                quat_xyzw = [-0.5, -0.5, 0.5, 0.5]  # 左手手掌朝下
            else:
                quat_xyzw = [0.5, -0.5, -0.5, 0.5]  # 右手手掌朝下
        else:
            # 侧面抓取 (杯子、水瓶)
            if use_left_hand:
                relative_angle = math.atan((self.robot_zero_y - grasp_y) / (grasp_x - self.robot_zero_x + 1e-6))
            else:
                relative_angle = math.atan((grasp_y - self.robot_zero_y) / (grasp_x - self.robot_zero_x + 1e-6))
            
            yaw = relative_angle * cfg['offset_angle']
            pitch = -1.57  # 手掌朝前/侧
            quat = self.euler_to_quaternion(yaw, pitch, 0)
            quat_xyzw = [quat.x, quat.y, quat.z, quat.w]
        
        rospy.loginfo(f"抓取类型: {grasp_type}, 位置: ({grasp_x:.3f}, {grasp_y:.3f}, {grasp_z:.3f})")
        
        # 构建IK请求
        eef_pose_msg = twoArmHandPoseCmd()
        eef_pose_msg.ik_param = self.ik_solve_param
        eef_pose_msg.use_custom_ik_param = True
        eef_pose_msg.joint_angles_as_q0 = True
        eef_pose_msg.hand_poses.left_pose.joint_angles = np.array([0.0, 0.0, 0.0, -1.57, 0.0, 0.0, 0.0])
        eef_pose_msg.hand_poses.right_pose.joint_angles = np.array([0.0, 0.0, 0.0, -1.57, 0.0, 0.0, 0.0])
        
        if use_left_hand:
            # 左手抓取
            eef_pose_msg.hand_poses.left_pose.pos_xyz = np.array([grasp_x, grasp_y, grasp_z])
            eef_pose_msg.hand_poses.left_pose.quat_xyzw = quat_xyzw
            eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = np.zeros(3)
            # 右手保持初始位置
            eef_pose_msg.hand_poses.right_pose.pos_xyz = np.array([self.robot_zero_x, self.robot_zero_y, self.robot_zero_z + 0.05])
            eef_pose_msg.hand_poses.right_pose.quat_xyzw = [0.0, 0.0, 0.0, 1.0]
            eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = np.zeros(3)
        else:
            # 左手保持初始位置
            eef_pose_msg.hand_poses.left_pose.pos_xyz = np.array([self.robot_zero_x, -self.robot_zero_y, self.robot_zero_z + 0.05])
            eef_pose_msg.hand_poses.left_pose.quat_xyzw = [0.0, 0.0, 0.0, 1.0]
            eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = np.zeros(3)
            # 右手抓取
            eef_pose_msg.hand_poses.right_pose.pos_xyz = np.array([grasp_x, grasp_y, grasp_z])
            eef_pose_msg.hand_poses.right_pose.quat_xyzw = quat_xyzw
            eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = np.zeros(3)
        
        return eef_pose_msg, cfg['hand_close'], (grasp_x, grasp_y, grasp_z)
    
    def grasp_by_track_id(self, track_id):
        """根据track_id抓取指定物体"""
        rospy.loginfo(f"========== 抓取 ID:{track_id} ==========")
        
        self.set_head(0, 20)
        time.sleep(1.5)
        
        target_pos, target_class, _ = self.get_target_by_track_id(track_id)
        if target_pos is None:
            rospy.logerr(f"未找到 ID:{track_id}")
            self.set_head(0, 0)
            return False
        
        return self._do_grasp(target_pos, target_class)
    
    def grasp_by_class_index(self, target_class, index=0):
        """根据类别和序号抓取 (index=0表示最近的)"""
        rospy.loginfo(f"========== 抓取 {target_class}#{index} ==========")
        
        self.set_head(0, 20)
        time.sleep(1.5)
        
        target_pos, track_id = self.get_target_by_class_index(target_class, index)
        if target_pos is None:
            rospy.logerr(f"未找到 {target_class}#{index}")
            self.set_head(0, 0)
            return False
        
        rospy.loginfo(f"目标 track_id={track_id}")
        return self._do_grasp(target_pos, target_class)
    
    def grasp_nearest(self, target_class):
        """抓取最近的目标 (默认方式)"""
        rospy.loginfo(f"========== 抓取最近的 {target_class} ==========")
        
        self.set_head(0, 20)
        time.sleep(1.5)
        
        target_pos, _, track_id = self.get_nearest_target(target_class)
        if target_pos is None:
            rospy.logerr(f"未找到 {target_class}")
            self.set_head(0, 0)
            return False, None
        
        rospy.loginfo(f"锁定目标 ID:{track_id}")
        success = self._do_grasp(target_pos, target_class)
        return success, track_id
    
    def _do_grasp(self, target_pos, target_class, prefer_hand=""):
        """执行抓取的核心逻辑"""
        # 判断左右手
        if prefer_hand in ["left", "right"]:
            use_left_hand = (prefer_hand == "left")
            rospy.loginfo(f"指定使用 {prefer_hand} 手")
        else:
            use_left_hand = target_pos[1] > 0  # 自动判断：y>0用左手
            rospy.loginfo(f"自动判断使用 {'left' if use_left_hand else 'right'} 手 (y={target_pos[1]:.2f})")
        
        hand_name = "左手" if use_left_hand else "右手"
        rospy.loginfo(f"使用 {hand_name} 抓取 {target_class}")
        
        # 设置手臂模式
        self.set_arm_mode(2)
        time.sleep(0.5)
        
        # IK求解
        eef_pose_msg, hand_close, _ = self.compute_grasp_pose(target_pos, target_class, use_left_hand)
        res = self.call_ik_service(eef_pose_msg)
        
        if res is None or not res.success:
            rospy.logerr("IK求解失败")
            self.set_arm_mode(1)
            self.set_head(0, 0)
            return False
        
        rospy.loginfo(f"IK求解成功, 耗时: {res.time_cost:.2f}ms")
        
        # 执行抓取
        self._execute_grasp(res, use_left_hand, hand_close)
        
        # 恢复
        self.set_head(0, 0)
        self.set_arm_mode(1)
        
        rospy.loginfo(f"========== {target_class} 抓取完成 ==========")
        return True
    
    def grasp_object(self, target_class, exclude_positions=None):
        """执行抓取流程"""
        rospy.loginfo(f"========== 开始抓取 {target_class} ==========")
        
        # 1. 低头寻找目标
        self.set_head(0, 20)
        time.sleep(1.5)
        
        # 2. 获取目标位置 (排除已抓取的)
        target_pos = self.get_target_position(target_class, timeout=15.0, exclude_positions=exclude_positions)
        if target_pos is None:
            rospy.logerr(f"未检测到 {target_class}")
            self.set_head(0, 0)
            return False, None
        
        # 3. 判断左右手 (y>0用左手)
        use_left_hand = target_pos[1] > 0
        hand_name = "左手" if use_left_hand else "右手"
        rospy.loginfo(f"使用 {hand_name} 抓取")
        
        # 4. 设置手臂为外部控制模式
        self.set_arm_mode(2)
        time.sleep(0.5)
        
        # 5. 计算IK
        eef_pose_msg, hand_close, _ = self.compute_grasp_pose(target_pos, target_class, use_left_hand)
        res = self.call_ik_service(eef_pose_msg)
        
        if res is None or not res.success:
            rospy.logerr("IK求解失败")
            self.set_arm_mode(1)
            self.set_head(0, 0)
            return False, None
        
        rospy.loginfo(f"IK求解成功, 耗时: {res.time_cost:.2f}ms")
        
        # 6. 执行抓取动作
        self._execute_grasp(res, use_left_hand, hand_close)
        
        # 7. 恢复
        self.set_head(0, 0)
        self.set_arm_mode(1)
        
        rospy.loginfo(f"========== {target_class} 抓取完成 ==========")
        return True, target_pos  # 返回抓取的位置，用于排除
    
    def grasp_all_same_class(self, target_class, max_count=5):
        """抓取所有相同类别的物体 (基于track_id排除已抓取的)"""
        rospy.loginfo(f"========== 抓取所有 {target_class} ==========")
        
        grasped_ids = set()  # 已抓取的track_id
        success_count = 0
        
        for i in range(max_count):
            rospy.loginfo(f"\n>>> 第 {i+1} 次尝试抓取 {target_class}")
            
            # 低头检测
            self.set_head(0, 20)
            time.sleep(1.5)
            
            # 找最近的未抓取目标
            target_pos, _, track_id = self._get_nearest_ungrasped(target_class, grasped_ids)
            
            if target_pos is None:
                rospy.loginfo(f"没有更多 {target_class} 可抓取")
                self.set_head(0, 0)
                break
            
            rospy.loginfo(f"锁定目标 ID:{track_id}")
            success = self._do_grasp(target_pos, target_class)
            
            if success:
                grasped_ids.add(track_id)
                success_count += 1
                rospy.loginfo(f"已成功抓取 {success_count} 个 {target_class}")
            
            time.sleep(2.0)
        
        rospy.loginfo(f"共抓取 {success_count} 个 {target_class}")
        return success_count
    
    def _get_nearest_ungrasped(self, target_class, grasped_ids, timeout=5.0):
        """获取最近的未抓取目标"""
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown() and (time.time() - start_time < timeout):
            matches = [det for det in self.detections_3d 
                       if det['class_name'] == target_class 
                       and det.get('track_id', -1) not in grasped_ids]
            
            if matches:
                matches.sort(key=lambda x: x.get('distance', float('inf')))
                det = matches[0]
                pos = det['position']
                tid = det.get('track_id', -1)
                return (pos['x'], pos['y'], pos['z']), target_class, tid
            
            rate.sleep()
        
        return None, None, None

    def _execute_grasp(self, ik_result, use_left_hand, hand_close):
        """执行抓取动作序列 - 分步接近避免碰撞"""
        arm_name = "left" if use_left_hand else "right"
        
        # 获取IK结果的关节角度
        if use_left_hand:
            target_joints = list(ik_result.hand_poses.left_pose.joint_angles)
            other_joints = [0.35, 0.0, 0.0, -0.52, 0.0, 0.0, 0.0]  # 右手保持
        else:
            target_joints = list(ik_result.hand_poses.right_pose.joint_angles)
            other_joints = [0.35, 0.0, 0.0, -0.52, 0.0, 0.0, 0.0]  # 左手保持
        
        # ========== 阶段1: 初始位置 ==========
        self.set_hand(self.HAND_ZERO, self.HAND_ZERO)
        self.set_arm(self.ARM_MOVE_TIME, [20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0,
                          20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0])
        
        # ========== 阶段2: 准备姿态（手臂侧抬） ==========
        if use_left_hand:
            # 左手侧抬
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -30, 0, 0, 0,
                               20, 0, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            self.set_hand(self.HAND_OPEN, None)
        else:
            # 右手侧抬
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                               20, -90, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            self.set_hand(None, self.HAND_OPEN)
        time.sleep(0.5)
        
        # ========== 阶段3: 中间位置（侧抬+弯肘） ==========
        if use_left_hand:
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -110, 0, 0, 0,
                               20, 0, 0, -30, 0, 0, 0])
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                               20, -90, 0, -110, 0, 0, 0])
        time.sleep(self.ARM_WAIT_TIME)
        
        # ========== 阶段4: 最终抓取位置（使用完整IK结果） ==========
        target_deg = [math.degrees(rad) for rad in target_joints]
        if use_left_hand:
            final_joints = target_deg + [math.degrees(r) for r in other_joints]
        else:
            final_joints = [math.degrees(r) for r in other_joints] + target_deg
        
        self.set_arm(self.ARM_MOVE_TIME, final_joints)
        time.sleep(self.ARM_WAIT_TIME)
        
        # ========== 阶段5: 抓取 ==========
        if self.use_sim:
            success, obj_name = self.sim_grasp(arm_name, "grasp")
            if not success:
                rospy.logwarn("仿真抓取失败")
        else:
            if use_left_hand:
                self.set_hand(hand_close, None)
            else:
                self.set_hand(None, hand_close)
        time.sleep(1.0)
        
        # ========== 阶段6: 抬起（先收肘，再侧抬） ==========
        if use_left_hand:
            # 先收肘
            self.set_arm(self.ARM_MOVE_TIME, [target_deg[0], target_deg[1], target_deg[2], -90, 0, 0, 0,
                               20, 0, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            # 侧抬收回
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -110, 0, 0, 0,
                               20, 0, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            # 递物姿态
            self.set_arm(self.ARM_MOVE_TIME, [-60.0, 0.0, 0.0, -30.0, 0, 0, 0,
                               20, 0, 0, -30, 0, 0, 0])
        else:
            # 先收肘
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                               target_deg[0], target_deg[1], target_deg[2], -90, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            # 侧抬收回
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                               20, -90, 0, -110, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            # 递物姿态
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                               -60.0, 0.0, 0.0, -30.0, 0, 0, 0])
        time.sleep(self.ARM_WAIT_TIME)
        
        # ========== 阶段7: 释放 ==========
        if self.use_sim:
            self.sim_grasp(arm_name, "release")
        else:
            if use_left_hand:
                self.set_hand(self.HAND_OPEN, None)
            else:
                self.set_hand(None, self.HAND_OPEN)
        time.sleep(1.0)
        
        # ========== 阶段8: 复位 ==========
        self._arm_reset(use_left_hand)
        self.set_hand(self.HAND_ZERO, self.HAND_ZERO)
        
        # 回到初始位置
        self.set_arm(self.ARM_MOVE_TIME, [6.0, 0.0, 0.0, -20.0, 0, 0, 0,
                          6.0, 0.0, 0.0, -20.0, 0, 0, 0])
        time.sleep(self.ARM_WAIT_TIME)
    
    def _arm_reset(self, use_left_hand):
        """手臂复位动作"""
        if use_left_hand:
            self.set_arm(self.ARM_MOVE_TIME, [6.0, 50.0, 0.0, -90.0, 0.0, 0.0, 0.0,
                               20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0])
            time.sleep(self.ARM_WAIT_TIME)
            self.set_arm(self.ARM_MOVE_TIME, [6.0, 50.0, 0.0, -20.0, 0.0, 0.0, 0.0,
                               20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0])
            time.sleep(self.ARM_WAIT_TIME)
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0,
                               6.0, -50.0, 0.0, -90.0, 0.0, 0.0, 0.0])
            time.sleep(self.ARM_WAIT_TIME)
            self.set_arm(self.ARM_MOVE_TIME, [20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0,
                               6.0, -50.0, 0.0, -20.0, 0.0, 0.0, 0.0])
            time.sleep(self.ARM_WAIT_TIME)
    
    # ==================== 服务接口 ====================
    
    def _handle_grasp_service(self, req):
        """处理抓取服务请求"""
        resp = GraspObjectResponse()
        
        rospy.loginfo(f"[服务] 收到抓取请求: class={req.target_class}, track_id={req.track_id}, grasp_only={req.grasp_only}, hand={req.hand}")
        
        try:
            if req.track_id >= 0:
                # 按track_id抓取
                success, track_id, hand = self.grasp_only(target_class=None, track_id=req.track_id, prefer_hand=req.hand)
            else:
                # 按类别抓取最近的
                success, track_id, hand = self.grasp_only(target_class=req.target_class, prefer_hand=req.hand)
            
            if success:
                if not req.grasp_only:
                    # 完整流程：抓取后释放
                    self.place_only(hand)
                    self.grasped_object = None
                    self.grasped_hand = None
                    self.grasped_track_id = -1
                
                resp.success = True
                resp.message = f"抓取成功: {req.target_class}"
                resp.grasped_track_id = track_id
                resp.grasped_hand = hand
            else:
                resp.success = False
                resp.message = "抓取失败"
                resp.grasped_track_id = -1
                resp.grasped_hand = ""
        
        except Exception as e:
            rospy.logerr(f"抓取服务异常: {e}")
            resp.success = False
            resp.message = str(e)
            resp.grasped_track_id = -1
            resp.grasped_hand = ""
        
        return resp
    
    def _handle_place_service(self, req):
        """处理放置服务请求"""
        resp = PlaceObjectResponse()
        
        rospy.loginfo(f"[服务] 收到放置请求: hand={req.hand}, reset_arm={req.reset_arm}")
        
        try:
            # 确定使用哪只手
            if req.hand:
                hand = req.hand
            elif self.grasped_hand:
                hand = self.grasped_hand
            else:
                resp.success = False
                resp.message = "未指定手，且当前没有抓取物体"
                return resp
            
            # reset_arm 默认为 True (bool 默认值是 False，所以需要特殊处理)
            # 如果请求中没有明确设置 reset_arm，默认为 True
            reset_arm = req.reset_arm if hasattr(req, 'reset_arm') else True
            # 注意：ROS srv 的 bool 默认值是 False，所以如果用户没传，会是 False
            # 为了向后兼容，我们检查是否是旧版本调用（没有 reset_arm 字段）
            
            success = self.place_only(hand, reset_arm=reset_arm)
            
            if success:
                if reset_arm:
                    self.grasped_object = None
                    self.grasped_hand = None
                    self.grasped_track_id = -1
                resp.success = True
                resp.message = "放置成功" if reset_arm else "物体已释放，等待后退后复位手臂"
            else:
                resp.success = False
                resp.message = "放置失败"
        
        except Exception as e:
            rospy.logerr(f"放置服务异常: {e}")
            resp.success = False
            resp.message = str(e)
        
        return resp
    
    def _handle_reset_arm_service(self, req):
        """处理手臂复位服务请求"""
        resp = ResetArmResponse()
        
        rospy.loginfo(f"[服务] 收到手臂复位请求: hand={req.hand}")
        
        try:
            hand = req.hand if req.hand else self.grasped_hand
            
            if not hand:
                resp.success = False
                resp.message = "未指定手"
                return resp
            
            success = self.reset_arm_after_place(hand)
            
            if success:
                self.grasped_object = None
                self.grasped_hand = None
                self.grasped_track_id = -1
                resp.success = True
                resp.message = "手臂复位成功"
            else:
                resp.success = False
                resp.message = "手臂复位失败"
        
        except Exception as e:
            rospy.logerr(f"手臂复位服务异常: {e}")
            resp.success = False
            resp.message = str(e)
        
        return resp
    
    def grasp_only(self, target_class=None, track_id=-1, prefer_hand=""):
        """
        只执行抓取动作，不释放
        :param target_class: 目标类别 (与track_id二选一)
        :param track_id: 指定track_id
        :param prefer_hand: 指定使用的手 "left"/"right"/"auto"/""，空或auto表示自动判断
        :return: (success, track_id, hand)
        """
        rospy.loginfo(f"========== 抓取 (grasp_only) ==========")
        
        # 低头检测
        self.set_head(0, 20)
        time.sleep(1.5)
        
        # 获取目标
        if track_id >= 0:
            target_pos, target_class, track_id = self.get_target_by_track_id(track_id)
        else:
            target_pos, target_class, track_id = self.get_nearest_target(target_class)
        
        if target_pos is None:
            rospy.logerr("未找到目标")
            self.set_head(0, 0)
            return False, -1, ""
        
        # 判断左右手
        if prefer_hand in ["left", "right"]:
            use_left_hand = (prefer_hand == "left")
            rospy.loginfo(f"指定使用 {prefer_hand} 手")
        else:
            use_left_hand = target_pos[1] > 0  # 自动判断：y>0用左手
            rospy.loginfo(f"自动判断使用 {'left' if use_left_hand else 'right'} 手 (y={target_pos[1]:.2f})")
        
        hand = "left" if use_left_hand else "right"
        rospy.loginfo(f"使用 {hand} 手抓取 {target_class}")
        
        # 设置手臂模式
        self.set_arm_mode(2)
        time.sleep(0.5)
        
        # IK求解
        eef_pose_msg, hand_close, grasp_pos = self.compute_grasp_pose(target_pos, target_class, use_left_hand)
        res = self.call_ik_service(eef_pose_msg)
        
        if res is None or not res.success:
            rospy.logerr("IK求解失败")
            self.set_arm_mode(1)
            self.set_head(0, 0)
            return False, -1, ""
        
        rospy.loginfo(f"IK求解成功, 耗时: {res.time_cost:.2f}ms")
        
        # 获取IK结果
        if use_left_hand:
            target_joints = list(res.hand_poses.left_pose.joint_angles)
        else:
            target_joints = list(res.hand_poses.right_pose.joint_angles)
        
        # 执行抓取动作序列 (不释放)
        self._execute_grasp_only(target_joints, use_left_hand, hand_close, target_class, grasp_pos)
        
        # 保存状态
        self.grasped_object = target_class
        self.grasped_hand = hand
        self.grasped_track_id = track_id
        
        self.set_head(0, 0)
        # 注意：不要切换回自动模式，保持外部控制模式，直到放置完成
        # self.set_arm_mode(1)
        
        rospy.loginfo(f"抓取完成，物体保持在 {hand} 手中")
        return True, track_id, hand
    
    def _execute_grasp_only(self, target_joints, use_left_hand, hand_close, target_class, grasp_pos=None):
        """执行抓取动作序列 - 只抓取不释放（完整版：包含中间姿态避免碰撞）"""
        arm_name = "left" if use_left_hand else "right"
        other_joints = [0.35, 0.0, 0.0, -0.52, 0.0, 0.0, 0.0]
        
        # ========== 阶段1: 初始位置 + 张开手 ==========
        self.set_hand(self.HAND_ZERO, self.HAND_ZERO)
        self.set_arm(self.ARM_MOVE_TIME, [20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0,
                                          20.0, 0.0, 0.0, -30.0, 0.0, 0.0, 0.0])
        
        # ========== 阶段2: 准备姿态（手臂侧抬） ==========
        if use_left_hand:
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -30, 0, 0, 0,
                                              20, 0, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_STAGE_WAIT)
            self.set_hand(self.HAND_OPEN, None)
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                                              20, -90, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_STAGE_WAIT)
            self.set_hand(None, self.HAND_OPEN)
        time.sleep(0.5)
        
        # ========== 阶段3: 中间位置（侧抬+弯肘） ==========
        if use_left_hand:
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 45, -110, 0, 0, 0,
                                              20, 0, 0, -30, 0, 0, 0])
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                                              20, -90, -45, -110, 0, 0, 0])
        time.sleep(self.ARM_STAGE_WAIT)
        
        # ========== 阶段4: 最终抓取位置（使用完整IK结果，TF等待到位） ==========
        target_deg = [math.degrees(rad) for rad in target_joints]
        rospy.loginfo(f"IK关节角度(度): {[f'{d:.1f}' for d in target_deg]}")
        
        if use_left_hand:
            final_joints = target_deg + [math.degrees(r) for r in other_joints]
        else:
            final_joints = [math.degrees(r) for r in other_joints] + target_deg
        
        rospy.loginfo(f"发送关节角度: {[f'{d:.1f}' for d in final_joints]}")
        self.set_arm(self.ARM_MOVE_TIME, final_joints)
        
        # 等待手臂开始响应指令
        time.sleep(0.5)
        
        # 使用TF等待手臂到达目标位置（超时时间较长）
        if grasp_pos is not None:
            rospy.loginfo(f"等待手臂到达抓取位置: ({grasp_pos[0]:.3f}, {grasp_pos[1]:.3f}, {grasp_pos[2]:.3f})")
            reached = self.wait_arm_reach_position(grasp_pos, hand=arm_name, timeout=self.ARM_TF_TIMEOUT)
            if not reached:
                rospy.logwarn("TF等待超时，继续执行抓取...")
        else:
            time.sleep(self.ARM_STAGE_WAIT)
        
        # ========== 阶段5: 抓取 ==========
        if self.use_sim:
            success, _ = self.sim_grasp(arm_name, "grasp")
            if not success:
                rospy.logwarn("仿真抓取失败")
        else:
            cfg = self.TARGET_CONFIG.get(target_class, self.TARGET_CONFIG['cup'])
            if use_left_hand:
                self.set_hand(cfg['hand_close'], None)
            else:
                self.set_hand(None, cfg['hand_close'])
        time.sleep(1.0)
        
        # ========== 阶段6: 抬起到搬运姿态 (侧抬+弯肘，便于行走) ==========
        if use_left_hand:
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -110, 0, 0, 0,
                                              20, 0, 0, -30, 0, 0, 0])
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                                              20, -90, 0, -110, 0, 0, 0])
        time.sleep(self.ARM_STAGE_WAIT)
    
    def place_only(self, hand=None, reset_arm=True):
        """
        只执行放置动作
        :param hand: "left" 或 "right"，None则使用当前抓取的手
        :param reset_arm: 是否复位手臂，False时只释放物体不复位（用于先后退再复位的场景）
        :return: success
        """
        if hand is None:
            hand = self.grasped_hand
        
        if hand is None:
            rospy.logwarn("未指定手，无法放置")
            return False
        
        rospy.loginfo(f"========== 放置 (place_only) {hand}手, reset_arm={reset_arm} ==========")
        
        use_left_hand = (hand == "left")
        arm_name = hand
        
        self.set_arm_mode(2)
        time.sleep(0.5)
        
        # 释放
        if self.use_sim:
            self.sim_grasp(arm_name, "release")
        else:
            if use_left_hand:
                self.set_hand(self.HAND_OPEN, None)
            else:
                self.set_hand(None, self.HAND_OPEN)
        time.sleep(1.0)
        
        # 如果不需要复位手臂，直接返回
        if not reset_arm:
            rospy.loginfo("物体已释放，手臂保持当前位置（等待后退后再复位）")
            return True
        
        # 复位手臂
        self._place_arm_reset(use_left_hand)
        
        self.set_arm_mode(1)
        rospy.loginfo("放置完成")
        return True
    
    def _place_arm_reset(self, use_left_hand):
        """放置后的手臂复位动作"""
        self._arm_reset(use_left_hand)
        self.set_hand(self.HAND_ZERO, self.HAND_ZERO)
        if use_left_hand:
            # 先侧抬，防止撞倒桌子
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -110, 0, 0, 0,
                                              20, 0, 0, -30, 0, 0, 0])
            time.sleep(self.ARM_WAIT_TIME)
            self.set_arm(self.ARM_MOVE_TIME, [20, 90, 0, -30, 0, 0, 0,
                                              20, 0, 0, -30, 0, 0, 0])
        else:
            self.set_arm(self.ARM_MOVE_TIME, [20, 0, 0, -30, 0, 0, 0,
                                              20, -90, 0, -30, 0, 0, 0])
        self.set_arm(self.ARM_MOVE_TIME, [20.0, 0.0, 0.0, -30.0, 0, 0, 0,
                                          20.0, 0.0, 0.0, -30.0, 0, 0, 0])
        time.sleep(self.ARM_WAIT_TIME)
    
    def reset_arm_after_place(self, hand=None):
        """
        放置后复位手臂（用于先后退再复位的场景）
        :param hand: "left" 或 "right"
        """
        if hand is None:
            hand = self.grasped_hand
        
        if hand is None:
            rospy.logwarn("未指定手")
            return False
        
        rospy.loginfo(f"========== 复位手臂 {hand}手 ==========")
        
        use_left_hand = (hand == "left")
        
        self.set_arm_mode(2)
        time.sleep(0.5)
        
        self._place_arm_reset(use_left_hand)
        
        self.set_arm_mode(1)
        rospy.loginfo("手臂复位完成")
        return True
    
    def get_grasp_state(self):
        """获取当前抓取状态"""
        return {
            'grasped_object': self.grasped_object,
            'grasped_hand': self.grasped_hand,
            'grasped_track_id': self.grasped_track_id
        }
    
    def grasp_all_objects(self, target_list=None):
        """依次抓取多个物体"""
        if target_list is None:
            target_list = ['cup', 'plate', 'scissors']
        
        results = {}
        for target in target_list:
            rospy.loginfo(f"\n>>> 准备抓取: {target}")
            success, _ = self.grasp_object(target)
            results[target] = success
            
            if not success:
                rospy.logwarn(f"{target} 抓取失败，继续下一个")
            
            time.sleep(2.0)  # 间隔
        
        # 汇总结果
        rospy.loginfo("\n========== 抓取结果汇总 ==========")
        for target, success in results.items():
            status = "✓ 成功" if success else "✗ 失败"
            rospy.loginfo(f"  {target}: {status}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="抓取控制器")
    parser.add_argument("--use_offset", action="store_true", help="启用偏移量补偿")
    parser.add_argument("--sim", action="store_true", help="仿真模式 (使用吸附服务)")
    parser.add_argument("--service", action="store_true", help="服务模式 (只启动服务，等待调用)")
    parser.add_argument("--target", type=str, default="all", 
                        help="抓取目标: cup/plate/scissors/all")
    parser.add_argument("--grasp_all_same", action="store_true",
                        help="抓取所有相同类别的物体")
    parser.add_argument("--index", type=int, default=0,
                        help="抓取第几个 (0=最近)")
    parser.add_argument("--track_id", type=int, default=-1,
                        help="按track_id抓取")
    parser.add_argument("--list", action="store_true",
                        help="列出所有检测到的目标")
    
    # 使用 parse_known_args 忽略ROS传递的额外参数 (__name, __log等)
    args, unknown = parser.parse_known_args()
    
    # 也支持从ROS param读取 (launch文件使用)
    rospy.init_node('grasp_controller', anonymous=True)
    use_sim = rospy.get_param('~use_sim', args.sim)
    use_offset = rospy.get_param('~use_offset', args.use_offset)
    service_mode = rospy.get_param('~service_mode', args.service)
    
    try:
        controller = GraspController(use_offset=use_offset, use_sim=use_sim)
        
        # 等待连接
        rate = rospy.Rate(10)
        while controller.arm_pub.get_num_connections() == 0 and not rospy.is_shutdown():
            rospy.loginfo("等待手臂控制订阅者连接...")
            rate.sleep()
        
        # 服务模式：只启动服务，等待调用
        if service_mode:
            rospy.loginfo("========== 服务模式 ==========")
            rospy.loginfo(f"use_sim={use_sim}, use_offset={use_offset}")
            rospy.loginfo("可用服务:")
            rospy.loginfo("  /grasp_controller/grasp     - 抓取物体")
            rospy.loginfo("  /grasp_controller/place     - 放置物体 (reset_arm=false 只释放不复位)")
            rospy.loginfo("  /grasp_controller/reset_arm - 复位手臂 (后退后调用)")
            rospy.loginfo("等待服务调用...")
            rospy.spin()
            return
        
        # 列出目标
        if args.list:
            controller.set_head(0, 20)
            time.sleep(2.0)
            controller.list_all_targets()
            controller.set_head(0, 0)
            return
        
        # 按track_id抓取
        if args.track_id >= 0:
            controller.grasp_by_track_id(args.track_id)
        elif args.target == "all":
            controller.grasp_all_objects()
        elif args.target in ['cup', 'plate', 'scissors']:
            if args.grasp_all_same:
                controller.grasp_all_same_class(args.target)
            elif args.index > 0:
                # 指定序号抓取
                controller.grasp_by_class_index(args.target, args.index)
            else:
                # 默认抓取最近的
                controller.grasp_nearest(args.target)
        else:
            rospy.logerr(f"未知目标: {args.target}")
            rospy.loginfo("可选目标: cup, plate, scissors, all")
    
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        rospy.loginfo("用户中断")


if __name__ == '__main__':
    main()
