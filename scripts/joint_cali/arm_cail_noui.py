#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Non-GUI, fully automated arm calibration script.
- No Qt or GUI code.
- Calibrates the left arm (side='l') automatically.
- Only prompts user for confirmation before writing zero points.
- Reuses logic from arm_cali.py where possible.
"""
import sys
import os
import time
import argparse
import numpy as np
import rospy
from std_msgs.msg import Float64MultiArray
from kuavo_msgs.msg import sensorsData
from arm_kinematics import HeadKinematics, ArmKinematics, get_package_path, quat_to_rot, rot_to_quat
from identifiability_analyzer import create_objective_function, identifiability_analyzer
import tf.transformations as tf_trans
import yaml
import json
from datetime import datetime
import pinocchio as pin
import nlopt
import cyipopt

# 添加终端输入相关的导入
try:
    import termios
    import tty
    import select
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False

# Import required functions directly (same as arm_cali.py)
from kuavo_msgs.srv import changeArmCtrlModeRequest, changeArmCtrlModeResponse, changeArmCtrlMode
from target_tracker import TargetTracker
from apriltag_cube import AprilTag3DRos

def safe_input_with_timeout(prompt, timeout=0.5):
    """
    安全的输入函数，带超时检测，适用于SSH环境
    如果不是真正的交互式终端或者获取输入失败，返回None
    """
    if not HAS_TERMIOS:
        return None
        
    if not sys.stdin.isatty():
        return None
    
    try:
        print(prompt, end='', flush=True)
        
        # 保存原始终端设置
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            # 设置为非阻塞模式
            tty.setraw(sys.stdin.fileno())
            
            # 使用select检查是否有输入可用
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            
            if rlist:
                # 读取一个字符
                char = sys.stdin.read(1)
                # 如果是回车键，返回空字符串表示确认
                if char == '\r' or char == '\n':
                    print()  # 换行
                    return ''
                else:
                    # 继续读取直到回车或者超时
                    line = char
                    while True:
                        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if rlist:
                            char = sys.stdin.read(1)
                            if char == '\r' or char == '\n':
                                print()  # 换行
                                return line.strip()
                            line += char
                        else:
                            break
                    print()  # 换行
                    return line.strip()
            else:
                # 超时，没有输入
                print("请确认机器人处于安全状态，按下Enter继续...")
                return None
                
        finally:
            # 恢复终端设置
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
    except Exception as e:
        print(f"\n[输入检测失败: {e}，自动继续...]")
        return None

def wait_for_user_confirmation(message, auto_continue_after=10):
    """
    等待用户确认，如果检测到输入问题或超时则自动继续
    """
    if not HAS_TERMIOS or not sys.stdin.isatty():
        print(f"{message}")
        print("⚠️  检测到非交互式环境，自动继续...")
        return True
    
    print(f"{message}")
    print(f"按Enter继续，或等待{auto_continue_after}秒自动继续...")
    
    start_time = time.time()
    while time.time() - start_time < auto_continue_after:
        result = safe_input_with_timeout("", timeout=30)
        if result is not None:  # 用户有输入
            return True
        # 继续等待
    
    print("⏰ 自动继续...")
    return True

def change_arm_ctrl_mode(control_mode):
    rospy.wait_for_service('/humanoid_change_arm_ctrl_mode')
    try:
        change_mode = rospy.ServiceProxy('/humanoid_change_arm_ctrl_mode', changeArmCtrlMode)
        req = changeArmCtrlModeRequest()
        req.control_mode = control_mode
        res = change_mode(req)
        if res.result:
            rospy.loginfo("手臂控制模式已更改为 %d", control_mode)
        else:
            rospy.logerr("无法将手臂控制模式更改为 %d", control_mode)
    except rospy.ServiceException as e:
        rospy.logerr("服务调用失败: %s", e)

def change_kinematic_mpc_ctrl_mode(control_mode):
    rospy.wait_for_service('/mobile_manipulator_mpc_control')
    try:
        change_mode = rospy.ServiceProxy('/mobile_manipulator_mpc_control', changeArmCtrlMode)
        req = changeArmCtrlModeRequest()
        req.control_mode = control_mode
        res = change_mode(req)
        if res.result:
            rospy.loginfo("运动学mpc控制模式已更改为 %d", control_mode)
        else:
            rospy.logerr("无法将运动学mpc控制模式更改为 %d", control_mode)
    except rospy.ServiceException as e:
        rospy.logerr("服务调用失败: %s", e)

def change_wbc_trajectory_ctrl_mode(control_mode):
    rospy.wait_for_service('/enable_wbc_arm_trajectory_control')
    try:
        change_mode = rospy.ServiceProxy('/enable_wbc_arm_trajectory_control', changeArmCtrlMode)
        req = changeArmCtrlModeRequest()
        req.control_mode = control_mode
        res = change_mode(req)
        if res.result:
            rospy.loginfo("wbc轨迹控制模式已更改为 %d", control_mode)
        else:
            rospy.logerr("无法将wbc轨迹控制模式更改为 %d", control_mode)
    except rospy.ServiceException as e:
        rospy.logerr("服务调用失败: %s", e)

class ArmCalibrator:
    """手臂标定器基类 - 无GUI版本"""
    def __init__(self, side='l', T_et=None, real_mode=False, plot_size=100):
        self.fk = None
        self.fk_arm = None
        self.head_fk = None
        self.side = side
        self.T_et = T_et
        self.real_mode = real_mode
        self.plot_size = plot_size

        self.is_hand_move_enabled = False
        self.data_dict_list = []
        self.result = None
        self.q = None
        
        self.pos_dis_threshold = 0.01  # m
        self.ori_dis_threshold = 0.01  # rad
        
        self.q_updated = False
        self.tag_pos_updated = False
        self.odom_updated = False
        self.condition_numbers = []

        # kinematics
        self.init_kinematics(side)

        # ros
        self.cube_detector = self.set_up_tag_detector()
        
        # 初始化头部追踪器
        asset_path = get_package_path("kuavo_assets")
        robot_version = os.environ.get('ROBOT_VERSION', '40')
        urdf_path = os.path.join(asset_path, f"models/biped_s{robot_version}/urdf/biped_s{robot_version}.urdf")
        self.target_tracker = TargetTracker(urdf_path, np.deg2rad(-35))
        self.target_tracker.back_to_zero()

        if self.real_mode:
            print("real mode")
            self.q_sub = rospy.Subscriber("/sensor_data_motor/motor_pos", Float64MultiArray, self.real_sensor_data_callback)
        else:
            print("gazebo mode")
            self.q_sub = rospy.Subscriber("/share_memory/sensor_data_raw", sensorsData, self.gazebo_sensor_data_callback)

        # test data
        self.test_data_list_dict = {
            'p_bt_meas': [],
            'quat_bt_meas': [],
            'p_bt_fk': [],
            'quat_bt_fk': []
        }
        self.data_count = 0

    def init_kinematics(self, side):
        """初始化运动学"""
        asset_path = get_package_path("kuavo_assets")
        robot_version = os.environ.get('ROBOT_VERSION', '40')
        urdf_path = os.path.join(asset_path, f"models/biped_s{robot_version}/urdf/biped_s{robot_version}.urdf")
        print(f"urdf_path: {urdf_path}")
        self.fk_arm = ArmKinematics(urdf_path, self.T_et)
        if side == "l":
            self.fk = self.fk_arm.FK_l
        else:
            self.fk = self.fk_arm.FK_r
        # head kinematics
        self.head_fk = HeadKinematics(urdf_path).FK

    def real_sensor_data_callback(self, msg):
        self.q = np.array(msg.data).flatten()
        self.q_updated = True
        self.track_target()

    def gazebo_sensor_data_callback(self, msg):
        self.q = np.array(msg.joint_data.joint_q).flatten()
        self.q_updated = True
        self.track_target()

    def track_target(self):
        """追踪目标"""
        try:
            # 更新头部追踪目标
            q_arm = self.q[12:19] if self.side == 'l' else self.q[19:26]
            p_bt_fk, R_bt_fk, _ = self.fk(q_arm)
            p_te = np.array([0, 0.16, 0])
            p_be = p_bt_fk + R_bt_fk @ p_te
            self.target_tracker.track_target(p_be)
        except Exception as e:
            print(f"Error in track_target: {e}")

    def update_from_cube_detector(self):
        """从立方体检测器获取最新的位姿数据"""
        if self.q is None:
            return
            
        position, orientation, timestamp, detected_tags = self.cube_detector.get_cube_pose()
        
        # 调试信息：每30次检查显示一次状态
        if not hasattr(self, '_debug_counter'):
            self._debug_counter = 0
        self._debug_counter += 1
        
        if self._debug_counter % 300 == 0:  # 每30秒显示一次（100Hz * 300 = 30s）
            print(f"[DEBUG] AprilTag检测状态: timestamp={timestamp}, detected_tags={len(detected_tags) if detected_tags else 0}")
        
        # 只有在检测到立方体且时间戳有效时才处理数据
        if timestamp is not None and len(detected_tags) > 0:
            # 立方体位置作为标签位置
            self.tag_pos = position
            
            # 获取方向四元数 (w,x,y,z格式)
            quat = rot_to_quat(orientation)
            self.tag_orientation = quat
            self.tag_pos_updated = True
            
            # 保存标签数据与当前关节角度
            curr_data_dict = {
                'tag_pos': self.tag_pos,
                'tag_ori': self.tag_orientation,
                'q': self.q
            }
            
            # 检查新数据是否与之前的数据有足够差异
            if len(self.data_dict_list) > 0:
                prev_data_dict = self.data_dict_list[-1]
                pos_dis = np.linalg.norm(curr_data_dict['tag_pos'] - prev_data_dict['tag_pos'])
                # 计算四元数距离
                ori_dis = 1 - np.abs(np.dot(curr_data_dict['tag_ori'], prev_data_dict['tag_ori']))
                
                if pos_dis > self.pos_dis_threshold or ori_dis > self.ori_dis_threshold:
                    self.data_dict_list.append(curr_data_dict)
                    self.data_count = len(self.data_dict_list)
                    print(f"Collected pose {len(self.data_dict_list)}")
            else:
                self.data_dict_list.append(curr_data_dict)
                self.data_count = len(self.data_dict_list)
                print("Collected first pose.")

    def set_up_tag_detector(self):
        """设置标签检测器"""
        try:
            # 加载配置文件
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'cube_config.yaml')
            
            # 检查文件是否存在
            if not os.path.exists(config_path):
                rospy.logwarn(f"配置文件不存在: {config_path}，将使用默认参数")
                return self._set_up_tag_detector_with_defaults()
                
            # 加载YAML文件
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            # 读取立方体参数
            cube_params = config.get('cube_params', {})
            cube_size = cube_params.get('cube_size', 0.11)
            tag_size = cube_params.get('tag_size', 0.088)
            connector_height = cube_params.get('connector_height', 0.165)
            
            # 读取面旋转配置
            face_rotations = config.get('face_rotations', {
                0: 0, 1: 0, 2: 0, 3: 0, 4: 0
            })
            
            # 读取标签ID映射
            tag_mappings = config.get('tag_id_mappings', {})
            side_key = 'left' if self.side == 'l' else 'right'
            tag_id_mapping = tag_mappings.get(side_key, None)
            
            if tag_id_mapping is None:
                rospy.logwarn(f"未找到{side_key}侧的标签ID映射，将使用默认映射")
                # 使用默认映射
                if self.side == 'l':
                    tag_id_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
                else:
                    tag_id_mapping = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
            
            # 创建立方体检测器
            cube_detector = AprilTag3DRos(
                a=cube_size, 
                b=tag_size,
                face_rotations=face_rotations,
                h=connector_height,
                tag_id_mapping=tag_id_mapping
            )
            
            # 读取面权重配置
            face_weights = config.get('face_weights', {})
            for face_id, weight in face_weights.items():
                cube_detector.set_face_weight(int(face_id), float(weight))
            
            # 读取过滤阈值
            filter_thresholds = config.get('filter_thresholds', {})
            position_thresh = filter_thresholds.get('position', 0.05)
            rotation_thresh = filter_thresholds.get('rotation', 0.2)
            
            # 设置过滤阈值
            cube_detector.set_filter_thresholds(
                position_thresh=position_thresh, 
                rotation_thresh=rotation_thresh
            )
            
            rospy.loginfo(f"成功从{config_path}加载立方体配置")
            cube_detector.print_params()
            return cube_detector
            
        except Exception as e:
            rospy.logerr(f"加载立方体配置时出错: {e}")
            return self._set_up_tag_detector_with_defaults()
    
    def _set_up_tag_detector_with_defaults(self):
        """使用默认参数设置标签检测器"""
        cube_size = 0.11
        tag_size = 0.088
        connector_height = 0.165
        
        face_rotations = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        
        if self.side == 'l':
            tag_id_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
        elif self.side == 'r':
            tag_id_mapping = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
        
        cube_detector = AprilTag3DRos(
            a=cube_size, 
            b=tag_size,
            face_rotations=face_rotations,
            h=connector_height,
            tag_id_mapping=tag_id_mapping
        )
        
        cube_detector.set_face_weight(0, 1.2)
        cube_detector.set_face_weight(1, 1.2)
        cube_detector.set_filter_thresholds(position_thresh=0.05, rotation_thresh=0.2)
        
        rospy.logwarn("使用默认立方体配置")
        cube_detector.print_params()
        return cube_detector

    @staticmethod
    def optimize_arm(fk, data_dict, optimizer_type='ipopt'):
        """优化手臂标定参数"""
        if optimizer_type == 'ipopt':
            return ArmCalibrator.optimize_with_ipopt(fk, data_dict)
        else:
            return ArmCalibrator.optimize_with_nlopt(fk, data_dict, nlopt.LD_MMA)

    @staticmethod
    def optimize_with_ipopt(fk, data_dict):
        """使用IPOPT优化"""
        class CalibrationProblem:
            def __init__(self, fk_func, data_dict):
                self.fk_func = fk_func
                self.data_dict = data_dict
                self.n_vars = 7
                self.iter_count = 0
                
            def objective(self, x):
                """计算目标函数值"""
                total_error = 0.0
                for q, true_pos, true_rot in zip(self.data_dict['q'], 
                                               self.data_dict['true_pos'],
                                               self.data_dict['true_rot']):
                    q = np.array(q).flatten()
                    pred_pos, pred_rot, _ = self.fk_func(q + x)
                    
                    error_pos = pred_pos - true_pos
                    error_rot = pin.log3(pred_rot @ true_rot.T)
                    error = np.concatenate([error_pos, error_rot])
                    total_error += np.sum(error**2)
                return float(total_error)
                
            def gradient(self, x):
                """计算梯度"""
                grad = np.zeros(self.n_vars)
                eps = 1e-6
                for i in range(self.n_vars):
                    x_plus = x.copy()
                    x_plus[i] += eps
                    obj_plus = self.objective(x_plus)
                    
                    x_minus = x.copy()
                    x_minus[i] -= eps
                    obj_minus = self.objective(x_minus)
                    
                    grad[i] = (obj_plus - obj_minus) / (2 * eps)
                return grad
                
            def intermediate(self, alg_mod, iter_count, obj_value, inf_pr, inf_du,
                           mu, d_norm, regularization_size, alpha_du, alpha_pr,
                           ls_trials):
                """每次迭代后的回调"""
                self.iter_count = iter_count
                if iter_count % 5 == 0:
                    print(f"Iteration {iter_count}, objective value: {obj_value}")

        try:
            time_start = time.time()
            
            # 创建问题实例
            problem = CalibrationProblem(fk, data_dict)
            
            # 设置边界
            lb = [-np.deg2rad(10)] * 7
            ub = [np.deg2rad(10)] * 7
            
            # 初始猜测
            x0 = np.zeros(7)
            
            # 创建IPOPT问题
            nlp = cyipopt.Problem(
                n=7,
                m=0,
                problem_obj=problem,
                lb=lb,
                ub=ub,
            )
            
            # 设置IPOPT选项
            nlp.add_option('max_iter', 1000)
            nlp.add_option('tol', 1e-8)
            nlp.add_option('print_level', 0)
            
            # 求解问题
            result = nlp.solve(x0)[0]
            
            time_end = time.time()
            print("IPOPT final error:", problem.objective(result))
            print("IPOPT found bias:", result)
            print(f"Optimization time: {1e3*(time_end - time_start):.2f} ms")
            print(f"Total iterations: {problem.iter_count}")
            
            return result
            
        except Exception as e:
            print("IPOPT optimization error:", e)
            return None

    @staticmethod
    def optimize_with_nlopt(fk, data_dict, algorithm):
        """使用NLopt优化"""
        n_vars = 7
        opt = nlopt.opt(algorithm, n_vars)
        opt.set_lower_bounds([-np.deg2rad(10)]*n_vars)
        opt.set_upper_bounds([+np.deg2rad(10)]*n_vars)
        
        objective = create_objective_function(fk, data_dict)
        opt.set_min_objective(objective)
        
        opt.set_ftol_rel(1e-8)
        opt.set_maxeval(1000)
        
        initial_delta = np.zeros(n_vars)
        
        try:
            time_start = time.time()
            result = opt.optimize(initial_delta)
            time_end = time.time()
            print(f"NLopt final error:", opt.last_optimum_value())
            print(f"NLopt found bias:", result)
            print(f"Optimization time: {1e3*(time_end - time_start):.2f} ms")
            return result
        except Exception as e:
            print(f"NLopt optimization error:", e)
            return None

    def cali_arm(self, n_poses):
        """标定手臂"""
        while len(self.data_dict_list) < n_poses:
            time.sleep(0.01)
        print(f"Collected {len(self.data_dict_list)} poses, start optimizing...")
        
        # 转换数据格式
        data_dict = {}
        data_dict['q'] = []
        data_dict['true_pos'] = []
        data_dict['true_rot'] = []
        
        for data in self.data_dict_list:
            q_arm = data['q'][12:12+7] if self.side == 'l' else data['q'][12+7:12+14]
            data_dict['q'].append(q_arm)
            q_head = data['q'][-2:]
            p_it = data['tag_pos']
            quat_it = data['tag_ori']
            p_bi, R_bi = self.head_fk(q_head)
            p_bt = p_bi + R_bi @ p_it
            R_bt = R_bi @ quat_to_rot(quat_it)
            data_dict['true_pos'].append(p_bt)
            data_dict['true_rot'].append(R_bt)

        delta = self.optimize_arm(self.fk, data_dict, 'ipopt')
        if delta is not None:
            print(f"optimized delta: {delta}")
            return delta
        else:
            print("Failed to optimize arm")
            return None

    def remove_noisy_data(self):
        """基于误差分析去除噪声数据"""
        if len(self.data_dict_list) < 2:
            return

        pos_errors = []
        rot_errors = []

        # 计算所有数据点的原始误差
        for data in self.data_dict_list:
            # 计算预测位置
            q_arm = data['q'][12:19] if self.side == 'l' else data['q'][19:26]
            p_bt_fk, R_bt_fk, _ = self.fk(q_arm)
            
            # 计算实际测量位置
            q_head = data['q'][-2:]
            p_bi, R_bi = self.head_fk(q_head)
            p_bt_meas = p_bi + R_bi @ data['tag_pos']
            R_bt_meas = R_bi @ quat_to_rot(data['tag_ori'])
            
            # 计算位置误差
            pos_error = np.linalg.norm(p_bt_meas - p_bt_fk)
            pos_errors.append(pos_error)
            
            # 计算方向误差
            R_error = R_bt_fk @ R_bt_meas.T
            rot_error = np.linalg.norm(pin.log3(R_error))
            rot_errors.append(rot_error)
    
        # 基于MAD的离群值检测
        def mad_based_outlier(data):
            median = np.median(data)
            mad = np.median(np.abs(data - median))
            return median, mad
        
        # 位置误差过滤
        pos_median, pos_mad = mad_based_outlier(pos_errors)
        pos_threshold = pos_median + 3 * pos_mad
        
        # 方向误差过滤  
        rot_median, rot_mad = mad_based_outlier(rot_errors)
        rot_threshold = rot_median + 3 * rot_mad
        
        # 执行过滤
        filtered_data = []
        for data, pos_err, rot_err in zip(self.data_dict_list, pos_errors, rot_errors):
            if pos_err <= pos_threshold and rot_err <= rot_threshold:
                filtered_data.append(data)
        
        # 更新数据
        original_count = len(self.data_dict_list)
        self.data_dict_list = filtered_data
        filtered_count = len(self.data_dict_list)
        
        print(f"Data filtering completed: {original_count} → {filtered_count}")

    @staticmethod
    def modify_arm_zero_yaml(yaml_file_path, delta_q_arm):
        """修改arm zero yaml文件"""
        assert len(delta_q_arm) == 12, "手的关节偏置量必须是12x1数组"
        
        # 读取YAML文件
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        # 备份原始文件
        yaml_backup_path = yaml_file_path + ".arm_cali.bak"
        with open(yaml_backup_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
            print(f"YAML backup saved to {yaml_backup_path}")

        # 检查是否存在arms_zero_position
        if "arms_zero_position" in data:
            original_value = data["arms_zero_position"]
            print(f"Original value: {original_value}")

            # 解析NumPy的二进制格式（如果存在）
            def parse_numpy_scalar(value):
                if isinstance(value, dict) and "!!binary |" in value:
                    import base64
                    import struct
                    binary_data = base64.b64decode(value["!!binary |"])
                    return struct.unpack('<d', binary_data)[0]
                return value

            for i in range(12):
                data["arms_zero_position"][i] = parse_numpy_scalar(original_value[i]) + float(delta_q_arm[i])

            # 打印修改后的值
            print("Modified values:")
            for i in range(12):
                print(f"Joint {i+1} value: {data['arms_zero_position'][i]}")

            # 将修改后的内容写回YAML文件
            with open(yaml_file_path, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        else:
            print("arms_zero_position key not found in the YAML file.")

    @staticmethod
    def modify_arm_elmo_offset_csv(delta_q):
        """修改手的elmo关节偏置"""
        try:
            assert len(delta_q) == 2, "手的elmo关节偏置量必须是2x1数组"
            
            home_dir = os.path.expanduser('~')
            offset_file_path = os.path.join(home_dir, '.config/lejuconfig/offset.csv')
            print(f"offset_file_path: {offset_file_path}")
            
            if not os.path.exists(offset_file_path):
                print(f"错误：文件不存在 {offset_file_path}")
                return False
                
            # 读取CSV文件内容
            with open(offset_file_path, 'r') as file:
                lines = file.readlines()
                
            if len(lines) < 14:
                print(f"错误：文件行数不足，需要至少14行，但只有{len(lines)}行")
                return False
                
            # 创建备份文件
            backup_file_path = offset_file_path + ".arm_cali.bak"
            with open(backup_file_path, 'w') as file:
                file.writelines(lines)
            print(f"备份文件已保存到 {backup_file_path}")
            
            # 修改第13和14行的值
            for i in range(12, 14):
                if i < len(lines):
                    try:
                        current_value = float(lines[i].strip())
                        new_value = current_value + np.rad2deg(delta_q[i-12])
                        lines[i] = f"{new_value}\n"
                        print(f"第{i+1}行: {current_value} -> {new_value}")
                    except ValueError:
                        print(f"错误：无法解析第{i+1}行的值: {lines[i]}")
                        return False
            
            # 将修改后的内容写回文件
            with open(offset_file_path, 'w') as file:
                file.writelines(lines)
                
            print(f"手的elmo关节偏置已成功修改")
            return True
            
        except Exception as e:
            print(f"修改手的elmo关节偏置时出错: {str(e)}")
            return False

class ArmCalibratorNoUI(ArmCalibrator):
    def __init__(self, side='l', T_et=None, real_mode=False, plot_size=100, no_confirm=False):
        # 调用父类初始化，但不初始化Qt/GUI元素
        super().__init__(side, T_et, real_mode, plot_size)
        self.no_confirm = no_confirm

    # 重写所有Qt相关方法为空实现
    def init_visualization(self): pass
    def update_visualization(self): pass
    def setup_head_tracking_controls(self): pass

    # 用户确认询问
    def ask_user_confirm(self, msg):
        if self.no_confirm:
            print(f"{msg} - 自动确认模式：YES")
            return True
        
        # 检查是否为真正的交互式终端
        if not HAS_TERMIOS or not sys.stdin.isatty():
            print(f"{msg}")
            print("⚠️  检测到非交互式环境，默认选择 'N' - 不保存")
            return False
        
        print("=" * 60)
        print("⚠️  重要确认 ⚠️")
        print("=" * 60)
        print(msg)
        print("=" * 60)
        print("输入选项:")
        print("  y/yes - 确认并保存标定结果")
        print("  n/no  - 取消保存（默认选项）")
        print("=" * 60)
        
        # 循环询问直到得到有效输入
        max_attempts = 3
        for attempt in range(max_attempts):
            result = safe_input_with_timeout("请输入您的选择 [y/N]: ", timeout=30.0)
            
            if result is None:
                print("⏰ 输入超时，默认选择 'N' - 不保存")
                return False
            
            ans = result.strip().lower()
            if ans in ['y', 'yes']:
                print("✅ 用户确认：将保存标定结果")
                return True
            elif ans in ['n', 'no', '']:
                print("❌ 用户取消：不保存标定结果")
                return False
            else:
                print(f"⚠️  无效输入 '{ans}'，请输入 y/yes 或 n/no")
                if attempt < max_attempts - 1:
                    print(f"剩余尝试次数: {max_attempts - attempt - 1}")
                continue
        
        # 超过最大尝试次数，默认不保存
        print("❌ 超过最大尝试次数，默认不保存标定结果")
        return False

    # 启用/禁用功能
    def enable_move(self):
        self.enable_head_tracking()
        change_arm_ctrl_mode(2)
        change_kinematic_mpc_ctrl_mode(1)
        self.is_hand_move_enabled = True
        print("The robot arm move function is enabled")
        
    def disable_move(self):
        self.disable_head_tracking()
        change_arm_ctrl_mode(1)
        change_kinematic_mpc_ctrl_mode(0)
        change_wbc_trajectory_ctrl_mode(0)
        self.is_hand_move_enabled = False
        print("The robot arm move function is disabled")
        
    def enable_head_tracking(self):
        self.target_tracker.set_tracking(True)
        print("Head tracking function is enabled")
        
    def disable_head_tracking(self):
        self.target_tracker.set_tracking(False)
        self.target_tracker.back_to_zero()
        print("Head tracking function is disabled")

    # 执行手臂运动示教
    def execute_hand_move(self):
        if not self.is_hand_move_enabled:
            print("The robot arm move function is disabled! Please enable it first.")
            return False
        try:
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bag_file = os.path.join(script_dir, "bags/new_hand_move_demo_" + ('left' if self.side == 'l' else 'right') + ".bag")
            if not os.path.exists(bag_file):
                print(f"[WARNING] Hand move demo bag file not found: {bag_file}")
                return False
            print(f"[INFO] Start executing hand move demo: {bag_file}")
            
            # 添加更多rosbag播放参数确保正确播放
            cmd = ["rosbag", "play", bag_file, "--clock", "--loop", "--rate=0.5"]
            print(f"[DEBUG] 执行命令: {' '.join(cmd)}")
            
            # 在后台播放bag文件（非阻塞）
            self.rosbag_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print("[INFO] Hand move demo started in background.")
            
            # 等待一下确保rosbag开始播放
            time.sleep(2)
            if self.rosbag_process.poll() is not None:
                print("[WARNING] Rosbag process exited immediately, checking output...")
                output, _ = self.rosbag_process.communicate()
                print(f"[DEBUG] Rosbag output: {output.decode()}")
                return False
            
            return True
        except Exception as e:
            print(f"[ERROR] Execution failed: {str(e)}")
            return False

    def is_hand_move_running(self):
        """检查手臂运动是否还在进行"""
        if hasattr(self, 'rosbag_process'):
            return self.rosbag_process.poll() is None
        return False

    def wait_for_hand_move_completion(self):
        """等待手臂运动完成，带超时机制"""
        if hasattr(self, 'rosbag_process'):
            print("等待手臂运动完成...")
            timeout = 60  # 60秒超时
            start_time = time.time()
            
            while True:
                # 检查进程是否结束
                poll_result = self.rosbag_process.poll()
                if poll_result is not None:
                    print(f"[INFO] Hand move demo finished with return code: {poll_result}")
                    return True
                
                # 检查超时
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    print(f"[WARNING] Hand move demo timeout after {timeout}s, terminating process...")
                    try:
                        self.rosbag_process.terminate()
                        time.sleep(2)
                        if self.rosbag_process.poll() is None:
                            print("[WARNING] Force killing rosbag process...")
                            self.rosbag_process.kill()
                        print("[INFO] Hand move demo process terminated.")
                    except Exception as e:
                        print(f"[ERROR] Failed to terminate rosbag process: {e}")
                    return True
                
                # 每秒检查一次
                time.sleep(1)
                
        return False

    # 标定主流程
    def calibrate(self):
        if len(self.data_dict_list) < 2:
            print("Need at least 2 collected data to calibrate")
            return
        try:
            delta_result = self.cali_arm(len(self.data_dict_list))
            print(f"delta_result: {delta_result}")
            self.result = delta_result
            
            # 显示标定结果
            print("\n" + "="*60)
            print("🎯 标定算法执行完成")
            print("="*60)
            print("标定结果 - 关节偏置量:")
            for i, bias in enumerate(delta_result):
                print(f"  关节 {i+1}: {np.rad2deg(bias):+8.4f}° ({bias:+8.6f} rad)")
            print("="*60)
            
            # 询问用户是否保存
            if self.ask_user_confirm('标定已完成，是否应用新的零点位置？'):
                print("💾 开始保存标定结果...")
                self.save_calibration_result(delta_result)
                print("✅ 标定结果已成功保存！")
            else:
                print("❌ 标定结果未保存")
                
        except Exception as e:
            print(f"❌ 标定算法执行出错: {str(e)}")
            import traceback
            traceback.print_exc()

    def save_calibration_result(self, delta_result):
        assert len(delta_result) == 7, "手的关节偏置量必须是7x1数组"
        """Save calibration result to file"""
        # negtive
        delta_result = (-1.0) * delta_result
        try:
            home_dir = os.path.expanduser('~')
            arm_zero_file_path = os.path.join(home_dir, '.config/lejuconfig/arms_zero.yaml')
            print(f"arm_zero_file_path: {arm_zero_file_path}")
            # update ruiwo and elmo bias
            extend_delta_result_ruiwo = np.zeros(12)
            extend_delta_result_elmo = np.zeros(2)
            if self.side == 'l':
                extend_delta_result_ruiwo[:6] = delta_result[1:]
                extend_delta_result_elmo[0] = delta_result[0]
            else:
                extend_delta_result_ruiwo[6:] = delta_result[1:]
                extend_delta_result_elmo[1] = delta_result[0]
            self.modify_arm_zero_yaml(arm_zero_file_path, extend_delta_result_ruiwo)
            self.modify_arm_elmo_offset_csv(extend_delta_result_elmo)
            
        except Exception as e:
            error_msg = f"保存失败: {str(e)}"
            print(error_msg)

    # 完整的自动标定流程
    def run_full_calibration(self, min_samples=10):
        """执行完整的标定流程"""
        print("=========================================================")
        print(f"           开始{('左' if self.side == 'l' else '右')}手自动标定流程")
        print("=========================================================")
        
        try:
            # 步骤1: Enable Move
            print("步骤1: 启用机器人移动功能...")
            self.enable_move()
            time.sleep(2)  # 等待服务生效
            print("✓ 机器人移动功能已启用")
            
            # 步骤2: Enable Head Tracking
            print("步骤2: 启用头部追踪...")
            self.enable_head_tracking()
            time.sleep(2)  # 等待头部追踪启动
            print("✓ 头部追踪已启用")
            
            # 步骤3: Hand Move - 执行手臂运动
            print("步骤3: 启动手臂示教运动...")
            if not self.execute_hand_move():
                print("✗ 手臂示教运动启动失败")
                return False
            print("✓ 手臂示教运动已在后台启动")
            
            # 步骤4: 数据收集 - 在运动过程中收集数据
            print("步骤4: 在手臂运动过程中收集标定数据...")
            print(f"目标收集 {min_samples} 个有效数据点...")
            
            # 数据收集循环 - 与手臂运动同时进行
            start_time = time.time()
            max_wait_time = 120  # 最大等待2分钟
            last_progress_time = start_time
            
            while len(self.data_dict_list) < min_samples:
                current_time = time.time()
                
                # 检查超时
                if current_time - start_time > max_wait_time:
                    print(f"⚠ 超时：只收集到 {len(self.data_dict_list)} 个数据点")
                    break
                
                # 更新数据
                self.update_from_cube_detector()
                
                # 显示进度 (每5秒更新一次)
                if current_time - last_progress_time >= 5:
                    hand_status = "运行中" if self.is_hand_move_running() else "已完成"
                    print(f"进度: {len(self.data_dict_list)}/{min_samples} 个数据点, 手臂运动: {hand_status}")
                    last_progress_time = current_time
                
                # 如果手臂运动完成但数据还不够，继续等待数据收集
                if not self.is_hand_move_running():
                    if len(self.data_dict_list) < min_samples:
                        remaining_time = max_wait_time - (current_time - start_time)
                        if remaining_time > 30:  # 给更多时间等待
                            if len(self.data_dict_list) > 0:  # 至少收集到了一些数据
                                print(f"手臂运动完成，继续收集剩余数据... (还需 {min_samples - len(self.data_dict_list)} 个)")
                            else:
                                print("⚠ 手臂运动完成但未收集到数据，请检查AprilTag检测")
                                print("⚠ 继续等待数据收集...")
                        else:
                            print("⚠ 手臂运动完成且时间不足，结束数据收集")
                            break
                    else:
                        # 收集到足够数据，跳出循环
                        break
                
                time.sleep(0.1)
                
            # 数据收集完成，主动停止rosbag进程
            if self.is_hand_move_running():
                print("数据收集完成，停止手臂运动...")
                try:
                    self.rosbag_process.terminate()
                    time.sleep(2)
                    if self.rosbag_process.poll() is None:
                        print("强制停止rosbag进程...")
                        self.rosbag_process.kill()
                    print("[INFO] Hand move demo stopped.")
                except Exception as e:
                    print(f"[WARNING] Failed to stop rosbag process: {e}")
            
            print(f"✓ 数据收集完成，共收集 {len(self.data_dict_list)} 个数据点")
            
            # 检查数据是否足够
            if len(self.data_dict_list) < 2:
                print("✗ 数据不足，无法进行标定")
                return False
            
            # 步骤5: Filter Noise - 过滤噪声数据
            print("步骤5: 过滤噪声数据...")
            original_count = len(self.data_dict_list)
            self.remove_noisy_data()
            filtered_count = len(self.data_dict_list)
            print(f"✓ 数据过滤完成: {original_count} → {filtered_count} 个数据点")
            
            # 再次检查过滤后的数据
            if len(self.data_dict_list) < 2:
                print("✗ 过滤后数据不足，无法进行标定")
                return False
            
            # 步骤6: Execute Calibration - 执行标定
            print("步骤6: 执行标定算法...")
            self.calibrate()
            
            # 步骤7: 禁用功能
            print("步骤7: 禁用机器人功能...")
            self.disable_head_tracking()
            time.sleep(1)
            self.disable_move()
            print("✓ 机器人功能已禁用")
            
            print("=========================================================")
            print(f"✓ {('左' if self.side == 'l' else '右')}手标定流程完成！")
            print("=========================================================")
            return True
            
        except Exception as e:
            print(f"✗ 标定过程出错: {str(e)}")
            # 确保禁用所有功能
            try:
                self.disable_head_tracking()
                self.disable_move()
            except:
                pass
            return False

    def run(self, min_samples=10, max_wait_sec=60):
        """保持原有接口兼容性"""
        return self.run_full_calibration(min_samples)

# Main entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='arm_cail_noui - 无GUI手臂标定程序')
    parser.add_argument('--size', type=int, default=20, help='每只手的采样数量')
    parser.add_argument('--real', action='store_true', help='实物模式')
    parser.add_argument('--plot_size', type=int, default=1, help='绘图大小')
    parser.add_argument('--side', type=str, default='both', choices=['l', 'r', 'both'], 
                       help='标定哪只手: l(左), r(右), both(双手)')
    parser.add_argument('--no-confirm', action='store_true', 
                       help='跳过用户确认，适用于自动化环境')
    args = parser.parse_args()

    import signal
    def signal_handler(sig, frame):
        print('\n程序被中断!')
        exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # 设置末端工具变换矩阵
    T_et = np.eye(4)
    quaternion = tf_trans.quaternion_from_euler(-np.pi/2, 0, -np.pi/2, 'sxyz')
    x,y,z,w = quaternion
    quat = np.array([w, x, y, z])
    T_et[:3, :3] = quat_to_rot(quat)
    T_et[:3, 3] = np.array([0.0, 0.0, -0.0])
    
    # 初始化ROS节点
    rospy.init_node('arm_cail_noui', anonymous=True)
    
    print("=========================================================")
    print("           机器人手臂关节标定程序 (无GUI版本)")
    print("=========================================================")
    print(f"标定模式: {'实物机器人' if args.real else '仿真机器人'}")
    print(f"采样数量: {args.size} 个数据点/手")
    print(f"标定范围: {args.side}")
    if args.no_confirm:
        print("运行模式: 自动确认（无需用户交互）")
    else:
        print("运行模式: 交互式（需要用户确认）")
    print("=========================================================")

    # 根据用户选择决定标定哪只手
    sides_to_calibrate = []
    if args.side == 'both':
        sides_to_calibrate = ['l', 'r']
    else:
        sides_to_calibrate = [args.side]

    success_count = 0
    total_count = len(sides_to_calibrate)

    # 依次标定选定的手
    for side in sides_to_calibrate:
        print(f"\n准备标定{('左' if side == 'l' else '右')}手...")
        if not args.no_confirm:
            # 使用健壮的用户确认函数
            wait_for_user_confirmation("请确认机器人处于安全状态", auto_continue_after=30)
        else:
            print("自动确认模式：跳过用户确认")
        
        # 创建标定器实例
        arm_cali_node = ArmCalibratorNoUI(side=side, T_et=T_et, real_mode=args.real, plot_size=args.plot_size, no_confirm=args.no_confirm)
        
        try:
            # 执行完整标定流程
            success = arm_cali_node.run_full_calibration(min_samples=args.size)
            if success:
                success_count += 1
                print(f"✓ {('左' if side == 'l' else '右')}手标定成功")
            else:
                print(f"✗ {('左' if side == 'l' else '右')}手标定失败")
                
        except KeyboardInterrupt:
            print(f"\n{('左' if side == 'l' else '右')}手标定被用户中断")
            break
        except Exception as e:
            print(f"✗ {('左' if side == 'l' else '右')}手标定出错: {str(e)}")
        
        # 清理资源
        del arm_cali_node
        
        # 如果还有下一只手要标定，等待一下
        if side != sides_to_calibrate[-1]:
            print("\n等待5秒后进行下一只手的标定...")
            time.sleep(5)

    # 最终结果总结
    print("\n" + "="*60)
    print("                    标定结果总结")
    print("="*60)
    print(f"成功标定: {success_count}/{total_count} 只手")
    
    if success_count == total_count:
        print("🎉 所有手臂标定成功完成！")
    elif success_count > 0:
        print("⚠ 部分手臂标定完成，请检查失败的手臂")
    else:
        print("❌ 所有手臂标定失败，请检查系统状态")
    
    print("="*60)
