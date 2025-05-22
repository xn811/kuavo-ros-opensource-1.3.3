import time
import math
from kuavo_humanoid_sdk.kuavo_strategy.kuavo_strategy import KuavoRobotStrategyBase
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose
from kuavo_humanoid_sdk.interfaces.data_types import KuavoManipulationMpcFrame, KuavoManipulationMpcCtrlMode, KuavoManipulationMpcControlFlow
from kuavo_humanoid_sdk.interfaces.data_types import EndEffectorSide
from kuavo_humanoid_sdk.interfaces.data_types import AprilTagData, HomogeneousMatrix, PoseQuaternion
from kuavo_humanoid_sdk import KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from dataclasses import dataclass
from typing import Tuple
import numpy as np
from scipy.spatial.transform import Rotation as R


@dataclass
class BoxInfo:
    """箱子信息数据类
    
    描述箱子的位置、尺寸和质量信息，用于箱子抓取策略
    
    Attributes:
        pose (KuavoPose): 箱子的位姿信息
        size (Tuple[float, float, float]): 箱子的尺寸 (长, 宽, 高) 单位: 米
        mass (float): 箱子的质量 单位: 千克 
    """
    pose: KuavoPose
    size: Tuple[float, float, float] = (0.3, 0.2, 0.15)  # 默认箱子尺寸
    mass: float = 1.0  # 默认箱子质量(kg)
    
class KuavoGraspBox(KuavoRobotStrategyBase):
    """箱子抓取策略类，继承自基础策略类"""
    
    def __init__(self, robot:KuavoRobot, robot_state:KuavoRobotState, robot_tools:KuavoRobotTools, robot_vision:KuavoRobotVision):
        """初始化箱子抓取策略类
        
        Args:
            robot: KuavoRobot实例
            robot_state: KuavoRobotState实例
            robot_tools: KuavoRobotTools实例
            robot_vision: KuavoRobotVision实例
        """
        super().__init__(robot, robot_state, robot_tools, robot_vision)
        
        # 箱子抓取相关的配置参数
        self.search_timeout = 20.0  # 搜索超时时间(秒)
        self.approach_timeout = 30.0  # 接近超时时间(秒)
        self.grasp_height_offset = 0.2  # 抓取高度偏移量(米)
        self.grasp_orientation = [0, -0.67566370964, 0, 0.73720997571945]
        # 存放头部寻找AprilTag的目标，初始化为异常ID 9999
        self.head_find_target_current_info_pose = AprilTagData(
            id=[9999],  # 异常ID
            size=[0.0],  # 默认尺寸为0
            pose=[PoseQuaternion(
                position=(0.0, 0.0, 0.0),  # 默认零位置
                orientation=(0.0, 0.0, 0.0, 1.0)  # 默认朝向（无旋转）
            )]
        )
            
    def head_find_target(self, target_info:AprilTagData, max_search_time=None, search_pattern="rotate_head", **kwargs):
        """使用头部旋转寻找AprilTag目标
        
        Args:
            target_info: AprilTag的信息
            max_search_time: 最大搜索时间(秒)，如果为None则使用默认值
            search_pattern: 搜索模式，"rotate_head"或"rotate_body"
            
        Returns:
            bool: 是否成功找到目标
        
        logic:
            1. 判断目标位置是否在机器人FOV(70度视场角)内
            2. 如果不在FOV内且search_pattern为"rotate_body"，先旋转机器人身体朝向目标位置
            3. 无论如何都使用头部搜索模式尝试找到目标
            4. 找到apriltag_data_from_odom之后，马上开始头部追踪
        """
        # 初始目标赋值
        self.head_find_target_current_info_pose = target_info
        
        # 设置搜索超时时间
        if max_search_time is None:
            max_search_time = self.search_timeout
        
        # 获取需要追踪的目标ID
        target_id = target_info.id[0]
        
        if target_id > 9999:
            print(f"target_id: {target_id} 大于 9999, 无效的AprilTag家族ID")
            return False
        
        # 判断目标位置是否在FOV内
        if len(target_info.pose) > 0:
            target_position = target_info.pose[0].position
            robot_position = self.state.robot_position()
            robot_orientation = self.state.robot_orientation()
            
            # 计算目标相对于机器人的位置向量
            dx = target_position[0] - robot_position[0]
            dy = target_position[1] - robot_position[1]
            
            # 计算目标相对于机器人的角度
            target_angle = math.atan2(dy, dx)
            
            # 获取机器人当前朝向的yaw角
            robot_yaw = self._extract_yaw_from_quaternion(robot_orientation)
            
            # 计算目标与机器人朝向的角度差
            angle_diff = target_angle - robot_yaw
            # 标准化角度到[-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # 检查是否在FOV内（70度 = 约1.22弧度）
            FOV_HALF_ANGLE = math.radians(35)  # 70度/2 = 35度
            is_in_fov = abs(angle_diff) <= FOV_HALF_ANGLE
            
            print(f"目标位置: ({target_position[0]:.2f}, {target_position[1]:.2f})")
            print(f"机器人位置: ({robot_position[0]:.2f}, {robot_position[1]:.2f})")
            print(f"目标角度: {math.degrees(target_angle):.2f}度")
            print(f"机器人朝向: {math.degrees(robot_yaw):.2f}度")
            print(f"角度差: {math.degrees(angle_diff):.2f}度")
            print(f"是否在FOV内: {is_in_fov}")
            
            # 如果目标不在FOV内且模式允许旋转身体，先旋转机器人身体
            if not is_in_fov and search_pattern == "rotate_body":
                print("目标超出FOV，调整机器人朝向...")
                # 调整机器人朝向
                print(f"开始调整 - 机器人位置: {robot_position}")
                print(f"开始调整 - 目标角度: {math.degrees(target_angle):.2f}度")
                print(f"开始调整 - 目标角度: {target_angle}")
                self.robot.control_command_pose_world(
                    robot_position[0], # 保持机器人当前x位置
                    robot_position[1], # 保持机器人当前y位置
                    0.0, # 保持当前z高度
                    target_angle # 朝向目标位置 转换为弧度
                )
                
                # 等待机器人旋转到位，使用闭环控制替代固定时间等待
                self._wait_for_orientation(target_angle, max_wait_time=10.0, angle_threshold=0.1)
        
        # 开始搜索计时
        start_time = time.time()
        found_target = False
        
        # 执行头部搜索模式，无论search_pattern是什么
        # 定义头部搜索参数（角度制）
        pitch_angles_deg = [12, -12]  # 两档pitch角度：抬头和低头，角度制
        yaw_angles_deg = [-30, -15, 0, 15, 30]  # 左右扫描的yaw角度，角度制
        
        # 在超时前循环搜索
        while time.time() - start_time < max_search_time and not found_target:
            # 遍历两档pitch角度
            for pitch_deg in pitch_angles_deg:
                # 遍历yaw角度进行左右扫描
                for yaw_deg in yaw_angles_deg:
                    # 将角度转换为弧度
                    yaw_rad = yaw_deg * 0.0174533  # 度转弧度，math.pi/180
                    pitch_rad = pitch_deg * 0.0174533  # 度转弧度
                    
                    # 控制头部旋转（使用弧度）
                    self.robot.control_head(yaw=yaw_rad, pitch=pitch_rad)
                    # 等待头部移动到位
                    time.sleep(0.5)
                    
                    # 检查是否找到目标
                    target_data = self.vision.get_data_by_id_from_odom(target_id)
                    print(f"target_data: {target_data}")

                    if (target_data is not None and isinstance(target_data, dict) and 
                        'poses' in target_data and len(target_data['poses']) > 0):
                        print(f"Target AprilTag {target_id} found!")
                        found_target = True
                        # 开始头部追踪
                        print("---- 开始头部追踪 ---- ")
                        self.robot.enable_head_tracking(target_id) # self.robot.disable_head_tracking()
                        break
                
                if found_target:
                    break
        
        return found_target

    def _is_orientation_aligned(self, orientation1, orientation2, threshold=0.3):
        """检查两个朝向是否大致一致
        
        Args:
            orientation1: 第一个朝向的四元数
            orientation2: 第二个朝向的四元数
            threshold: 判断为一致的阈值
            
        Returns:
            bool: 朝向是否一致
        """
        # 这里简化实现，实际应用需要进行四元数计算
        # 提取两个朝向的yaw角并比较差异
        yaw1 = self._extract_yaw_from_quaternion(orientation1)
        yaw2 = self._extract_yaw_from_quaternion(orientation2)
        
        # 计算角度差异
        diff = abs(yaw1 - yaw2)
        while diff > math.pi:
            diff -= 2 * math.pi
        
        return abs(diff) < threshold

    def _extract_yaw_from_quaternion(self, quaternion):
        """从四元数中提取yaw角
        
        Args:
            quaternion: 四元数 (x, y, z, w)
            
        Returns:
            float: yaw角（弧度）
        """
        if not quaternion or len(quaternion) != 4:
            print("无法获取有效的四元数")
            return 0.0
            
        # 计算yaw角 (围绕z轴的旋转)
        # 四元数到欧拉角的简化计算，仅提取yaw
        x, y, z, w = quaternion
        yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
        return yaw

    def _track_target_with_head(self, target_data):
        """使用头部追踪目标
        
        Args:
            target_data: 目标数据，包含位置信息
        """
        # 从目标数据中提取相对位置
        position = target_data["position"]
        
        # 计算目标相对于机器人的方向
        dx = position[0]
        dy = position[1]
        dz = position[2]
        
        # 计算yaw和pitch角度来指向目标
        # 简单的反正切计算（结果为弧度）
        yaw_rad = math.atan2(dy, dx)
        distance = math.sqrt(dx*dx + dy*dy)
        pitch_rad = math.atan2(dz, distance)
        
        # 限制角度范围（弧度）
        yaw_rad = min(math.radians(80), max(math.radians(-80), yaw_rad))  # 限制在±80度
        pitch_rad = min(math.radians(25), max(math.radians(-25), pitch_rad))  # 限制在±25度
        
        # 控制头部指向目标（输入为弧度）
        self.robot.control_head(yaw=yaw_rad, pitch=pitch_rad)
    
    def walk_approach_target(self, target_info:AprilTagData, target_distance=0.5, approach_speed=0.15, **kwargs):
        """走路接近AprilTag目标
        
        Args:
            target_info: AprilTag的信息
            target_distance: 与目标的期望距离(米)
            approach_speed: 接近速度(米/秒)
            
        Returns:
            bool: 是否成功接近目标
        """
        approach_success = False
        start_time = time.time()
        tag_id = target_info.id[0]
        target_data = self.vision.get_data_by_id_from_odom(tag_id)
        if target_data is None:
            print(f"未找到目标ID: {tag_id} 的目标数据!")
            return False
        target_pose = target_data["poses"][0]
        print(f"target_pose in _approach_target: {target_pose}")
        while not approach_success:
            approach_success = self._approach_target(target_pose, target_distance, approach_speed, **kwargs)
            time.sleep(1)
            time_cost = time.time() - start_time
            print(f"walking approach target..., time_cost: {time_cost:.2f}秒.")
        return approach_success
    
    def _approach_target(self, target_pose, target_distance=0.5, approach_speed=0.15, **kwargs):
        """根据目标信息和目标距离计算目标位姿
        
        Args:
            target_pose: 目标位姿信息
            target_distance: 与目标的期望距离(米)
            approach_speed: 接近速度(米/秒)
        
        Returns:
            bool: 是否成功接近目标
        """
        p_wa = np.array([target_pose.position.x, target_pose.position.y, target_pose.position.z])
        quat_wa = np.array([target_pose.orientation.x, target_pose.orientation.y, target_pose.orientation.z, target_pose.orientation.w]) # x,y,z,w
        R_wa = R.from_quat(quat_wa).as_matrix()
        def get_target_pose_by_distance(p_wa, R_wa, target_distance=0.5):
            """根据目标信息和目标距离计算目标位姿"""
            p_at = np.array([0, 0, target_distance], np.float32)
            p_at_w = R_wa @ p_at
            p_wt = p_wa + p_at_w
            yaw = math.atan2(p_at_w[1], p_at_w[0])
            yaw += math.pi
            while yaw > math.pi:
                yaw -= 2 * math.pi
            while yaw < -math.pi:
                yaw += 2 * math.pi
            return p_wt, yaw
        
        p_wt, angle = get_target_pose_by_distance(p_wa, R_wa, target_distance)
        self.robot.control_command_pose_world(p_wt[0], p_wt[1], 0, angle)
        
        yaw_reached = self._yaw_check(angle)
        pos_reached = self._pos_check(p_wt)
        stance_check = (self.state == 'stance')
        print(f"yaw_reached: {yaw_reached}, pos_reached: {pos_reached}, stance_check: {stance_check}")
        return yaw_reached and pos_reached # and stance_check
    
    def _check_target_reachable(self, target_info:BoxInfo) -> bool:
        """检查目标位置是否在机器人手臂可达区域内
        
        Args:
            target_info: 目标信息，包含位置、尺寸等
            
        Returns:
            bool: 目标是否可达
            
        Note:
            此函数为预留接口，待实现以下功能：
            1. 获取机器人当前位姿
            2. 获取机器人手臂工作空间范围
            3. 检查目标位置是否在工作空间内
        """
        # TODO: 实现可达性检查逻辑
        # 1. 获取机器人当前位姿
        # robot_pose = self.state.robot_pose()
        
        # 2. 获取机器人手臂工作空间范围
        # workspace_range = self.robot.get_arm_workspace()
        
        # 3. 检查目标位置是否在工作空间内
        # target_position = target_info.pose.position
        # is_in_workspace = check_position_in_workspace(target_position, workspace_range)
        
        # 临时返回True，等待接口实现后修改
        return True

    def arm_move_to_target(self, target_info:BoxInfo, arm_mode="manipulation_mpc", **kwargs):
        """手臂移动到目标位置
        
        Args:
            target_info: 目标信息，包含位置、尺寸等
            approach_speed: 接近速度(米/秒)
            arm_mode: 手臂控制模式
        Returns:
            bool: 是否成功移动到目标位置
        """
        # 设置手臂控制模式
        if arm_mode == "manipulation_mpc":
            self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.BaseArm)
        else:
            self.robot.set_fixed_arm_mode()

        left_pose, right_pose = self._get_target_pose(target_info)

        if left_pose is None:
            return False
        
        # 控制手臂移动到目标位置
        if not self.robot.control_robot_end_effector_pose(
            left_pose,
            right_pose,
            KuavoManipulationMpcFrame.LocalFrame
        ) or not self._check_target_reachable(left_pose) or not self._check_target_reachable(right_pose):
            return False
        
        time.sleep(2)
        self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.NoControl)
        self.robot.set_manipulation_mpc_control_flow(KuavoManipulationMpcControlFlow.ThroughFullBodyMpc)
        
        return True
    
    def _get_target_pose(self, target_info:BoxInfo, **kwargs):
        """获取目标位置和抓取姿态
        
        Args:
            target_info: 目标信息，包含位置、尺寸等
        Returns:
            left_pose: 左臂抓取位置
            right_pose: 右臂抓取位置
        """
        # 计算抓取姿态
        box_position = list(target_info.pose.position)
        print(f"原始世界坐标系下的位置: {box_position}")
        
        # 转换为齐次坐标
        box_position_homogeneous = np.array(box_position + [1.0])
        print(f"齐次坐标: {box_position_homogeneous}")

        # 获取从世界坐标系到局部坐标系的变换矩阵
        transform = self.tools.get_tf_transform("base_link", "odom", return_type="homogeneous")
        if transform is not None:
            # 从HomogeneousMatrix对象中获取矩阵数据
            transform_matrix = transform.matrix
            print(f"变换矩阵:\n{transform_matrix}")
            
            # 应用坐标变换
            box_position_local = transform_matrix @ box_position_homogeneous
            print(f"变换后的齐次坐标: {box_position_local}")
            
            # 移除齐次坐标的第四个元素
            grasp_position = box_position_local[:3].tolist()
            print(f"最终局部坐标系下的位置: {grasp_position}")
        else:
            print("警告：无法获取变换矩阵，使用原始位置作为抓取位置")
            return None, None
        
        # odom->base_link->LocalFrame
        grasp_position[2] += self.state.com_height
        
        # 计算末端位姿
        left_pose = KuavoPose(
            position=[grasp_position[0],
                    grasp_position[1] + target_info.size[1] + self.grasp_height_offset,
                    grasp_position[2] - target_info.size[2] / 2],
            orientation=self.grasp_orientation
        )
        
        right_pose = KuavoPose(
            position=[grasp_position[0],
                    grasp_position[1] - target_info.size[1] - self.grasp_height_offset,
                    grasp_position[2] - target_info.size[2] / 2],
            orientation=self.grasp_orientation
        )
        return left_pose, right_pose

    def _check_box_lifting_status(self, target_info:BoxInfo) -> bool:
        """检查箱子是否成功抬起
        
        Args:
            target_info: 目标信息，包含位置、尺寸等
            
        Returns:
            bool: 是否成功抬起箱子
            
        Note:
            此函数为预留接口，待实现以下功能：
            1. 获取手部力反馈数据
            2. 根据箱子重量和力反馈判断是否成功抬起
            3. 检查力反馈是否稳定
        """
        # TODO: 实现力反馈检测逻辑
        # 1. 获取手部力反馈数据
        # left_force = self.state.get_end_effector_force(EndEffectorSide.Left)
        # right_force = self.state.get_end_effector_force(EndEffectorSide.Right)
        
        # 2. 根据箱子重量和力反馈判断
        # expected_force = target_info.mass * 9.8
        # actual_force = calculate_total_force(left_force, right_force)
        
        # 3. 检查力反馈稳定性
        # force_stable = check_force_stability()
        
        # 临时返回True，等待接口实现后修改
        return True

    def arm_transport_target_up(self, target_info:BoxInfo, arm_mode="manipulation_mpc"):
        """实现手臂搬起箱子的功能
        
        Args:
            target_info: 目标信息，包含位置、尺寸等
            arm_mode: 手臂控制模式
            
        Returns:
            bool: 是否成功搬起目标
        """
        # 设置手臂控制模式
        if arm_mode == "manipulation_mpc":
            self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.BaseArm)
        else:
            self.robot.set_fixed_arm_mode()

        left_pose, right_pose = self._get_target_pose(target_info)

        if left_pose is None:
            return False
        
        # Convert position tuples to lists for modification
        left_pose.position = list(left_pose.position)
        right_pose.position = list(right_pose.position)
        
        left_pose.position[1] -= (target_info.size[1] / 4 + self.grasp_height_offset)
        right_pose.position[1] += (target_info.size[1] / 4 + self.grasp_height_offset)
        self.robot.control_robot_end_effector_pose(
            left_pose,
            right_pose,
            KuavoManipulationMpcFrame.LocalFrame
        )
        time.sleep(1.0)

        left_pose.position[1] -= target_info.size[1] / 4
        right_pose.position[1] += target_info.size[1] / 4
        self.robot.control_robot_end_effector_pose(
            left_pose,
            right_pose,
            KuavoManipulationMpcFrame.LocalFrame
        )
        time.sleep(1.0)

        left_pose.position[2] += self.grasp_height_offset * 2
        right_pose.position[2] += self.grasp_height_offset * 2
        
        if not self.robot.control_robot_end_effector_pose(
            left_pose,
            right_pose,
            KuavoManipulationMpcFrame.LocalFrame
        ) and self._check_box_lifting_status(target_info):
            
            return False
        
        time.sleep(2)
        self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.NoControl)
        self.robot.set_manipulation_mpc_control_flow(KuavoManipulationMpcControlFlow.ThroughFullBodyMpc)
        
        return True
    
    def _arrive_pose(self, target_position: list, target_yaw: float, timeout: float = 10.0) -> bool:
        """控制机器人移动到指定位姿并等待到达
        
        Args:
            target_position: 目标位置 [x, y, z]
            target_yaw: 目标朝向角度（弧度）
            timeout: 等待超时时间（秒）
            
        Returns:
            bool: 是否成功到达目标位姿
        """
        # 控制机器人移动到目标位姿
        self.robot.control_command_pose_world(
            target_position[0],  # x
            target_position[1],  # y
            0,                   # z (保持当前高度)
            target_yaw          # 目标朝向
        )
        
        # 等待机器人到达目标位姿
        start_time = time.time()
        rate_hz = 10  # 检查频率
        wait_interval = 1.0 / rate_hz
        
        while time.time() - start_time < timeout:
            # 检查位置和朝向是否到位
            pos_reached = self._pos_check(target_position)
            yaw_reached = self._yaw_check(target_yaw)
            
            if pos_reached and yaw_reached:
                print("机器人已到达目标位姿!")
                return True
            
            # 短暂等待再次检查
            time.sleep(wait_interval)
        
        # 超时
        print(f"等待机器人到达目标位姿超时!")
        return False
    
    def walk_to_pose(self, target_info: BoxInfo, target_distance=0.5, approach_speed=0.15, **kwargs):
        """让机器人走到指定的位姿
        
        Args:
            target_pose: 目标位姿
            target_distance: 与目标的期望距离(米)
            approach_speed: 接近速度(米/秒)
            
        Returns:
            bool: 是否成功到达目标位姿
        """
        # 获取目标位置和朝向
        target_position = target_info.pose.position
        target_orientation = target_info.pose.orientation
        print(f"target_position: {target_position}, target_orientation: {target_orientation}")
        
        # 从四元数中提取yaw角
        target_yaw = self._extract_yaw_from_quaternion(target_orientation)
        print(f"target_yaw: {target_yaw}")
        
        # 计算偏移后的位置
        # 根据目标朝向计算偏移方向
        offset_x = -target_distance * math.cos(target_yaw)  # 负号是因为要远离目标
        offset_y = -target_distance * math.sin(target_yaw)
        
        # 计算新的目标位置
        new_target_position = [
            target_position[0] + offset_x,
            target_position[1] + offset_y,
            target_position[2]
        ]
        
        print(f"开始移动到目标位姿:")
        print(f"原始目标位置: ({target_position[0]:.2f}, {target_position[1]:.2f}, {target_position[2]:.2f})")
        print(f"偏移后位置: ({new_target_position[0]:.2f}, {new_target_position[1]:.2f}, {new_target_position[2]:.2f})")
        print(f"目标朝向: {math.degrees(target_yaw):.2f}度")
        
        if not self._arrive_pose(
            new_target_position,
            target_yaw
        ):
            return False
        
        return True

    

    def arm_transport_target_down(self, target_info:BoxInfo, arm_mode="manipulation_mpc"):
        """实现手臂放下箱子的功能
        
        Args:
            target_info: 目标放置位置信息
            arm_mode: 手臂控制模式
            
        Returns:
            bool: 是否成功放下目标
        """
        # 设置手臂控制模式
        if arm_mode == "manipulation_mpc":
            self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.BaseArm)
        else:
            self.robot.set_fixed_arm_mode()
            
        # 计算放置位置
        left_pose, right_pose = self._get_target_pose(target_info)

        if left_pose is None:
            return False
        
        # 将position元组转换为列表
        left_pose.position = list(left_pose.position)
        right_pose.position = list(right_pose.position)
        left_pose.position[1] -= (target_info.size[1] / 2 + self.grasp_height_offset)
        right_pose.position[1] += (target_info.size[1] / 2 + self.grasp_height_offset)
        
        # 控制手臂移动到放置位置
        if not self.robot.control_robot_end_effector_pose(
            left_pose,
            right_pose,
            KuavoManipulationMpcFrame.LocalFrame
        ):
            print("移动到放置位置失败")
            return False
        
        time.sleep(2)
        
         # 抬起手臂离开箱子
        left_pose.position[1] += self.grasp_height_offset
        right_pose.position[1] -= self.grasp_height_offset
        
        lift_pose_l = KuavoPose(
            position=left_pose.position,
            orientation=left_pose.orientation
        )
        lift_pose_r = KuavoPose(
            position=right_pose.position,
            orientation=right_pose.orientation
        )
        
        if not self.robot.control_robot_end_effector_pose(
            lift_pose_l,
            lift_pose_r,
            KuavoManipulationMpcFrame.LocalFrame
        ):
            print("抬起手臂离开箱子失败")
            return False
            
        time.sleep(2)
        self.robot.set_manipulation_mpc_mode(KuavoManipulationMpcCtrlMode.NoControl)
        self.robot.set_manipulation_mpc_control_flow(KuavoManipulationMpcControlFlow.ThroughFullBodyMpc)
        
        return True

    def _wait_for_orientation(self, target_angle, max_wait_time=10.0, angle_threshold=0.1):
        """等待机器人旋转到指定朝向
        
        Args:
            target_angle: 目标朝向角度（弧度）
            max_wait_time: 最大等待时间（秒）
            angle_threshold: 角度阈值（弧度），小于此阈值认为已到位
            
        Returns:
            bool: 是否成功到达目标朝向
        """
        start_time = time.time()
        rate_hz = 10  # 检查频率
        wait_interval = 1.0 / rate_hz
        
        print(f"等待机器人旋转到位，目标角度: {math.degrees(target_angle):.2f}度")
        
        while time.time() - start_time < max_wait_time:
            if self._yaw_check(target_angle, angle_threshold):
                return True
            
            # 短暂等待再次检查
            time.sleep(wait_interval)
        
        # 超时
        print(f"等待机器人旋转到位超时! 已经等待了 {max_wait_time:.2f}秒")
        return False

    def _yaw_check(self, yaw_angle_target, angle_threshold=0.1):
        """检查机器人当前朝向与目标朝向的差异
        
        Args:
            yaw_angle_target: 目标朝向角度（弧度）
            angle_threshold: 角度阈值（弧度），小于此阈值认为已到位
            
        Returns:
            bool: 是否成功到达目标朝向
        """
        # 获取当前机器人朝向
        current_orientation = self.state.robot_orientation()
        current_yaw = self._extract_yaw_from_quaternion(current_orientation)
        
        # 计算角度差
        angle_diff = yaw_angle_target - current_yaw
        # 标准化到[-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # 输出当前状态
        print(f"当前朝向: {math.degrees(current_yaw):.2f}度, 目标朝向: {math.degrees(yaw_angle_target):.2f}度, 差值: {math.degrees(abs(angle_diff)):.2f}度")
        
        # 检查是否已到位
        if abs(angle_diff) < angle_threshold:
            print(f"机器人已旋转到位!")
            return True
        else:
            return False
        
    def _pos_check(self, pos_target, pos_threshold=0.2):
        """检查机器人当前位置(x, y)与目标位置的差异
        
        Args:
            pos_target: 目标位置
            pos_threshold: 位置阈值（米），小于此阈值认为已到位
        """
        current_pos = self.state.robot_position()
        if not current_pos or len(current_pos) < 2:
            print("无法获取有效的机器人当前位置")
            return False
            
        # print(f"current_pos: {current_pos}, pos_target: {pos_target}")
        pos_diff = np.linalg.norm(np.array(pos_target[:2]) - np.array(current_pos[:2]))
        print(f"当前位置(x,y): ({current_pos[0]:.2f}, {current_pos[1]:.2f}), 目标位置(x,y): ({pos_target[0]:.2f}, {pos_target[1]:.2f}), 距离: {pos_diff:.2f}米")
        if pos_diff < pos_threshold:
            print(f"机器人已到达目标位置!")
            return True
        else:
            return False

            return False
