"""
Pico VR device integration with ROS.

This module provides tools for:
- ROS node management
- Pose and gesture handling
- Visualization
- Service control
"""

import os
import sys
import signal
import json
import rospy
import rospkg
import tf
import numpy as np
import enum
from typing import List, Optional, Any
from tf2_msgs.msg import TFMessage
from std_msgs.msg import Float64MultiArray,Float64
from kuavo_msgs.msg import (
    twoArmHandPoseCmd, robotBodyMatrices, picoPoseInfoList,
    robotHeadMotionData, ikSolveParam, footPoseTargetTrajectories,
    JoySticks, sensorsData
)
from kuavo_msgs.srv import changeArmCtrlMode, changeTorsoCtrlMode, changeTorsoCtrlModeRequest, changeArmCtrlMode, changeArmCtrlModeRequest
from kuavo_msgs.srv import fkSrv
from kuavo_msgs.msg import JoySticks 
from std_msgs.msg import Float32MultiArray, Int32
from .pico_utils import KuavoPicoInfoTransformer
from common.logger import SDKLogger
from .joysticks_handler import JoySticksHandler
from typing import Set
from copy import deepcopy
from scipy.spatial.transform import Rotation as R
from ..config.pico_vr_config import PicoVrConfig, HandWrenchConfig

class ControlMode(enum.Enum):
        NONE_MODE = 0
        MOBILE_MPC_MODE = 1    # 运动学MPC模式
        FOLLOW_MODE = 2         # 手臂跟随模式
        INCREMENTAL_MODE = 3    # 增量控制模式

class IncrementalMpcCtrlMode(enum.Enum):
    """表示Kuavo机器人 Manipulation MPC 控制模式的枚举类"""
    NoControl = 0
    """无控制"""
    ArmOnly = 1
    """仅控制手臂"""
    BaseOnly = 2
    """仅控制底座"""
    BaseArm = 3
    """同时控制底座和手臂"""
    ERROR = -1
    """错误状态"""
    

class KuavoPicoNodeManager:
    """Singleton class for managing ROS node initialization."""
    
    _instance = None
    _node_initialized = False

    @classmethod
    def get_instance(cls, node_name: str = 'kuavo_pico_node') -> 'KuavoPicoNodeManager':
        """Get singleton instance."""
        if not cls._instance:
            cls._instance = cls(node_name)
        return cls._instance

    def __init__(self, node_name: str):
        """Initialize the node manager."""
        if not KuavoPicoNodeManager._node_initialized:
            rospy.init_node(node_name)
            KuavoPicoNodeManager._node_initialized = True

    @staticmethod
    def get_ros_is_shutdown() -> bool:
        """Check if ROS is shutdown."""
        return rospy.is_shutdown()


class KuavoPicoBoneFramePublisher:
    """Class for publishing bone frame information."""
    
    def __init__(self, node_name: str = 'kuavo_pico_bone_frame_publisher'):
        """Initialize the bone frame publisher."""
        SDKLogger.info(f"[{node_name}] Initializing KuavoPicoBoneFramePublisher...")
        self.rate = rospy.Rate(100.0)
        
        # Initialize publishers
        self._init_publishers()
        
        # Create TF broadcaster
        self.tf_broadcaster = tf.TransformBroadcaster()

    def _init_publishers(self) -> None:
        """Initialize ROS publishers."""
        self.pose_info_list_pub = rospy.Publisher(
            '/leju_pico_bone_poses', 
            picoPoseInfoList, 
            queue_size=10
        )
        self.head_motion_data_pub = rospy.Publisher(
            '/robot_head_motion_data', 
            robotHeadMotionData, 
            queue_size=10
        )
        self.foot_pose_pub = rospy.Publisher(
            '/humanoid_mpc_foot_pose_world_target_trajectories',
            footPoseTargetTrajectories, 
            queue_size=10
        )

        # PICO 手柄数据
        self.pico_joy_pub = rospy.Publisher('/pico/joy', JoySticks, queue_size=10)

    def publish_pico_joys(self, joy: JoySticks) -> None:
        """Publish pico joys"""
        try:
            if not rospy.is_shutdown():
                if joy is not None:
                    self.pico_joy_pub.publish(joy)
            else:
                SDKLogger.error("ROS node is shutdown, cannot publish pico joys")
        except Exception as e:
            SDKLogger.error(f"Error publishing pico joys: {e}")

    def publish_pose_info_list(self, pose_info_list: picoPoseInfoList) -> None:
        """Publish pose information list."""
        try:
            if not rospy.is_shutdown():
                self.pose_info_list_pub.publish(pose_info_list)
            else:
                SDKLogger.error("ROS node is shutdown, cannot publish pose info list")
        except Exception as e:
            SDKLogger.error(f"Error publishing pose info list: {e}")

    def publish_foot_pose_trajectory(self, foot_pose_trajectory: footPoseTargetTrajectories) -> None:
        """Publish foot pose trajectory."""
        SDKLogger.info(f"publish_foot_pose_trajectory finished[\\\\\\\\\\\\\\\\\\\\\\\\]")
        SDKLogger.info(f"publish_foot_pose_trajectory time: {rospy.Time.now().to_sec()}")
        self.foot_pose_pub.publish(foot_pose_trajectory)

    def publish_hands_info_list(self, hands_info_list: picoPoseInfoList) -> None:
        """Publish hands information list."""
        try:
            if not rospy.is_shutdown():
                self.hands_info_list_pub.publish(hands_info_list)
            else:
                SDKLogger.error("ROS node is shutdown, cannot publish hands info list")
        except Exception as e:
            SDKLogger.error(f"Error publishing hands info list: {e}")

    def publish_tf(self, translation: List[float], rotation: List[float], 
                  child: str, parent: str) -> None:
        """Publish transform."""
        self.tf_broadcaster.sendTransform(
            translation, 
            rotation, 
            rospy.Time.now(), 
            child, 
            parent
        )

    def publish_hand_finger_tf(self, tf_msg: TFMessage) -> None:
        """Publish hand finger transform."""
        self.hand_finger_tf_pub.publish(tf_msg)

    def get_listener(self) -> tf.TransformListener:
        """Get transform listener."""
        return self.tf_listener

    def sleep(self) -> None:
        """Sleep for the configured rate."""
        self.rate.sleep()


class KuavoPicoNode:
    """Main Pico node class for handling VR device integration."""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, play_mode: bool = False):
        """Initialize the Pico node."""
        if not hasattr(self, '_initialized'):
            KuavoPicoNodeManager.get_instance('kuavo_pico_node')
            self._play_mode = play_mode
            # Initialize parameters
            self._init_parameters()
            # Initialize model and transformers
            self._init_model_and_transformers()
            # Initialize publishers
            self._init_publishers()
            # Initialize subscribers
            self._init_subscribers()

            # Initialize joy handler
            self._init_joy_handler()
            self.robot_matrix_publisher = RobotMatrixPublisher()

            self._initialized = True
            self._init_joy_controller()
            self.arm_joint_angles = None

            self.control_mode = ControlMode.MOBILE_MPC_MODE

            self._left_target_pose = (None, None)   # tuple(pos, quat), quat(x, y, z, w)
            self._right_target_pose = (None, None)  # tuple(pos, quat), quat(x, y, z, w) 

            self._left_anchor_pose = (None, None)
            self._right_anchor_pose = (None, None)

            self.last_control_mode = None
            self.is_in_incremental_mode = True

            self.ik_error_norm = [0.0, 0.0]

            self.interp_left_pos = None
            self.interp_right_pos = None
            self.control_mode_changing = True

        else:
            # Allow updating play_mode if already initialized
            self._play_mode = play_mode

    def set_play_mode(self, enable: bool):
        """Enable or disable play mode (controls /robot_body_matrices subscription)."""
        if hasattr(self, '_play_mode') and self._play_mode == enable:
            return
        self._play_mode = enable
        # Remove or add the subscriber as needed
        if enable:
            if not hasattr(self, '_robot_body_matrices_sub') or self._robot_body_matrices_sub is None:
                self._robot_body_matrices_sub = rospy.Subscriber(
                    "/robot_body_matrices",
                    robotBodyMatrices,
                    self.robot_body_matrices_callback
                )
        else:
            if hasattr(self, '_robot_body_matrices_sub') and self._robot_body_matrices_sub is not None:
                self._robot_body_matrices_sub.unregister()
                self._robot_body_matrices_sub = None

    def _init_parameters(self) -> None:
        """Initialize node parameters."""
        self.use_custom_ik_param = True
        self.ik_solve_param = ikSolveParam()
        self.set_ik_solver_params()
        
        self.send_srv = True
        self.last_pico_running_state = False
        self.button_y_last = False
        self.config_manager = PicoVrConfig()

        # hand wrench
        self.hand_wrench_config = self.config_manager.get_default_hand_wrench_config()
        self.option_hand_wrench = False  # 施加/松开

    def _init_model_and_transformers(self) -> None:
        """Initialize model and transformers."""
        model_path = self.set_robot_model_params()
        self.bone_frame_publisher = KuavoPicoBoneFramePublisher()
        self.tf_broadcaster = tf.TransformBroadcaster()
        self.pico_info_transformer = KuavoPicoInfoTransformer(
            model_path, 
            tf_broadcaster=self.tf_broadcaster,
            bone_frame_publisher=self.bone_frame_publisher
        )

    def _init_publishers(self) -> None:
        """Initialize ROS publishers."""
        self.pub = rospy.Publisher(
            '/mm/two_arm_hand_pose_cmd', 
            twoArmHandPoseCmd, 
            queue_size=10
        )
        self.pub_ik = rospy.Publisher(
            '/ik/two_arm_hand_pose_cmd', 
            twoArmHandPoseCmd, 
            queue_size=10
        )
        self.pub_hand_wrench_cmd = rospy.Publisher( # 发布手臂末端 6 维力
            '/hand_wrench_cmd', 
            Float64MultiArray, 
            queue_size=1)
        

    def _init_subscribers(self) -> None:
        """Initialize ROS subscribers."""
        rospy.Subscriber(
            "/leju_pico_bone_poses", 
            picoPoseInfoList, 
            # self.pico_hands_poses_callback
            # self.pico_hands_poses_callback_incremental
            # self.pico_hands_poses_callback_ik
            self.pico_hands_poses_callback_choose
        )
        # Only subscribe to /robot_body_matrices if play_mode is True
        self._robot_body_matrices_sub = None
        if getattr(self, '_play_mode', False):
            self._robot_body_matrices_sub = rospy.Subscriber(
                "/robot_body_matrices",
                robotBodyMatrices,
                self.robot_body_matrices_callback
            )
        
        rospy.Subscriber(
            "/pico/joy", 
            JoySticks, 
            self.pico_joy_callback
        )   
        rospy.Subscriber("/sensors_data_raw", sensorsData, self.sensors_data_raw_callback)
        rospy.Subscriber("/ik/error_norm", Float32MultiArray, self.ik_error_norm_callback)
        rospy.Subscriber("/pico/control_mode", Int32, self.set_control_mode_callback)
        rospy.Subscriber("/pico/incremental_mode", Int32, self.set_incremental_mode_callback)
    
    """Joy Callbacks"""
    def _hand_wrench_callback(self, key_combination: Set[str], joy:JoySticks)->None:
        """Callback for hand wrench."""
        if not self.option_hand_wrench:
            SDKLogger.info(f"施加手部力:{self.hand_wrench_config}")
            if self.hand_wrench_config:
                mass_force =  {
                    'item_mass': self.hand_wrench_config.itemMass, # 物品重量 单位 kg
                    'lforce': [self.hand_wrench_config.lforceX, self.hand_wrench_config.lforceY, self.hand_wrench_config.lforceZ],
                    'rforce': [self.hand_wrench_config.lforceX, -self.hand_wrench_config.lforceY, self.hand_wrench_config.lforceZ],
                }
                self.publish_hand_wrench_cmd(mass_force)
                self.option_hand_wrench = True
            else:
                SDKLogger.error("------------- item_mass_force is None --------------")
        else:
            SDKLogger.info(f"松开手部力")
            mass_force =  {
                'item_mass': 0.0, # 物品重量 单位 kg
                'lforce': [0.0, 0.0, 0.0],
                'rforce': [0.0, 0.0, 0.0],
            }
            self.publish_hand_wrench_cmd(mass_force)
            self.option_hand_wrench = False

    def _init_joy_handler(self) -> None:
        """Initialize joy handler."""
        self.joy_handler = JoySticksHandler()
        # 手柄 XYAB 组合键映射
        JOY_BTN_MAPPING = {
            "hand_wrench": { # 临时的,如果冲突需要重新定义
                # X 长按 + Y 长按 + A 按下 + B 空闲
                'key_combination': set(['X_LONG_PRESSED', 'Y_LONG_PRESSED', 'A_PRESSED', 'B_IDLE']),
                'callback': self._hand_wrench_callback
            }
        }
        for key, value in JOY_BTN_MAPPING.items():
            self.joy_handler.add_callback(key, 
                                          value['key_combination'], 
                                          value['callback'])

    def _init_joy_controller(self) -> None:
        """Initialize joy controller"""
        self.joy_button_handler = JoySticksHandler()
        rospy.Subscriber("/pico/joy", JoySticks, self.sub_callback)
        self.joy_button_handler.add_callback("torso on", {"Y_PRESSED"}, self.torso_on_callback)
        self.joy_button_handler.add_callback("torso off", {"Y_LONG_PRESSED"}, self.torso_off_callback)
        self.joy_button_handler.add_callback("WholeBody Mode", {"X_LONG_PRESSED"}, self.whole_body_callback)
        self.joy_button_handler.add_callback("UpperBody Mode", {"B_LONG_PRESSED"}, self.upper_body_callback)
        self.joy_button_handler.add_callback("LowerBody Mode", {"A_LONG_PRESSED"}, self.lower_body_callback)

    def sub_callback(self, joy: JoySticks) -> None:
        self.joy_button_handler.update(joy)

    def torso_on_callback(self, keys: Set[str], joy: JoySticks) -> None:
        self.last_pico_running_state = False
        self.pico_info_transformer.set_control_torso_mode(True)
    
    def torso_off_callback(self, keys: Set[str], joy: JoySticks) -> None:
        self.last_pico_running_state = False
        self.pico_info_transformer.set_control_torso_mode(False)

    def whole_body_callback(self, keys: Set[str], joy: JoySticks) -> None:
        self.last_pico_running_state = False
        self.pico_info_transformer.set_control_mode("WholeBody")

    def upper_body_callback(self, keys: Set[str], joy: JoySticks) -> None:
        self.last_pico_running_state = False
        self.pico_info_transformer.set_control_mode("UpperBody")

    def lower_body_callback(self, keys: Set[str], joy: JoySticks) -> None:
        self.last_pico_running_state = False
        self.pico_info_transformer.set_control_mode("LowerBody")

    def set_robot_model_params(self) -> str:
        """Set robot model parameters."""
        SDKLogger.info("Setting robot model parameters...")
        kuavo_assests_path = self._get_package_path("kuavo_assets")
        robot_version = os.environ.get('ROBOT_VERSION', '45')
        model_config_file = kuavo_assests_path + f"/config/kuavo_v{robot_version}/kuavo.json"
        
        with open(model_config_file, 'r') as f:
            model_config = json.load(f)
            
        rospy.set_param("/pico/upper_arm_length", model_config["upper_arm_length"])
        rospy.set_param("/pico/lower_arm_length", model_config["lower_arm_length"])
        rospy.set_param("/pico/shoulder_width", model_config["shoulder_width"])
        
        return kuavo_assests_path + f"/models/biped_s{robot_version}"

    def _get_package_path(self, package_name: str) -> Optional[str]:
        """Get the path of a ROS package."""
        try:
            rospack = rospkg.RosPack()
            return rospack.get_path(package_name)
        except rospkg.ResourceNotFound:
            SDKLogger.error(f"Package {package_name} not found")
            return None

    def set_ik_solver_params(self) -> None:
        """Set IK solver parameters."""
        SDKLogger.info("Setting IK solver parameters...")
        self.ik_solve_param.major_optimality_tol = 9e-3
        self.ik_solve_param.major_feasibility_tol = 9e-3
        self.ik_solve_param.minor_feasibility_tol = 9e-3
        self.ik_solve_param.major_iterations_limit = 50
        self.ik_solve_param.oritation_constraint_tol = 9e-3
        self.ik_solve_param.pos_constraint_tol = 9e-3
        self.ik_solve_param.pos_cost_weight = 10.0
        SDKLogger.info("IK solver parameters set successfully")

    def change_arm_ctrl_mode(self, mode: int) -> None:
        """Change arm control mode."""
        try:
            rospy.wait_for_service("/change_arm_ctrl_mode")
            changeHandTrackingMode_srv = rospy.ServiceProxy("/change_arm_ctrl_mode", changeArmCtrlMode)
            changeHandTrackingMode_srv(mode)
        except Exception as e:
            SDKLogger.error(f"Service /change_arm_ctrl_mode call failed: {e}")

    def change_mobile_ctrl_mode(self, mode: int) -> None:
        """Change mobile control mode."""
        try:
            rospy.wait_for_service("/mobile_manipulator_mpc_control")
            changeHandTrackingMode_srv = rospy.ServiceProxy("/mobile_manipulator_mpc_control", changeArmCtrlMode)
            changeHandTrackingMode_srv(mode)
            print(f"=================================changeHandTrackingMode_srv({mode})=============================================")
        except Exception as e:
            SDKLogger.error(f"Service /mobile_manipulator_mpc_control call failed: {e}")

    def change_mm_wbc_arm_ctrl_mode(self, mode: int) -> None:
        """Change MM WBC arm control mode."""
        try:
            rospy.wait_for_service("/enable_mm_wbc_arm_trajectory_control")
            changeHandTrackingMode_srv = rospy.ServiceProxy("/enable_mm_wbc_arm_trajectory_control", changeArmCtrlMode)
            changeHandTrackingMode_srv(mode)
        except Exception as e:
            SDKLogger.error(f"Service /enable_mm_wbc_arm_trajectory_control call failed: {e}")


    def reset_mm_mpc(self):
        try:
            rospy.wait_for_service('/reset_mm_mpc', timeout=3.0)
            reset_mpc = rospy.ServiceProxy('/reset_mm_mpc', changeTorsoCtrlMode)
            req = changeTorsoCtrlModeRequest()
            res = reset_mpc(req)
            if res.result:
                rospy.loginfo("Mobile manipulator MPC reset successfully")
            else:
                rospy.logerr("Failed to reset mobile manipulator MPC")
        except rospy.ServiceException as e:
            rospy.logerr("Service call to %s failed: %s", '/reset_mm_mpc', e)
        except rospy.ROSException as e:
            rospy.logerr("Failed to connect to service %s: %s", '/reset_mm_mpc', e)
        except Exception as e:
            rospy.logerr("Failed to reset mobile manipulator MPC: %s", e)


    def robot_body_matrices_callback(self, robot_body_matrices_msg: robotBodyMatrices) -> None:
        """Callback for robot body matrices."""

        # process data of hands
        robot_urdf_matrices, current_time = self.robot_matrix_publisher.get_all_matrices_from_message(robot_body_matrices_msg)
        self.pico_info_transformer.publish_local_poses(robot_urdf_matrices, current_time)

        # process data of foots
        self.pico_info_transformer.process_foot_poses_parallel(robot_urdf_matrices)

    def publish_hand_wrench_cmd(self, item_mass_force: dict) -> None:
        """Publish hand wrench command."""
        msg = Float64MultiArray()
        left_force = item_mass_force['lforce'] + [0,0,0]
        right_force = item_mass_force['rforce'] + [0,0,0]
        msg.data = left_force + right_force
        self.pub_hand_wrench_cmd.publish(msg)
    
    def pico_joy_callback(self, pico_joy_msg: JoySticks) -> None:
        """Callback for Pico joy."""        
        # 处理手柄按键逻辑，组合按键会在内部回调
        self.joy_handler.update(pico_joy_msg)

    def pico_hands_poses_callback(self, pico_hands_poses_msg: picoPoseInfoList) -> None:
        """Callback for Pico hands poses."""
        self.pico_info_transformer.read_msg_hand(pico_hands_poses_msg)

        left_pose, left_elbow_pos = self.pico_info_transformer.get_hand_pose("Left")
        right_pose, right_elbow_pos = self.pico_info_transformer.get_hand_pose("Right")
        
        eef_pose_msg = twoArmHandPoseCmd()
        eef_pose_msg.hand_poses.left_pose.pos_xyz = left_pose[0]
        eef_pose_msg.hand_poses.left_pose.quat_xyzw = left_pose[1]
        eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = left_elbow_pos

        eef_pose_msg.hand_poses.right_pose.pos_xyz = right_pose[0]
        eef_pose_msg.hand_poses.right_pose.quat_xyzw = right_pose[1]
        eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = right_elbow_pos
        eef_pose_msg.ik_param = self.ik_solve_param
        # eef_pose_msg.use_custom_ik_param = self.use_custom_ik_param
        eef_pose_msg.use_custom_ik_param = False
        eef_pose_msg.frame = 1
        
        
        # Check for VR errors
        if self.pico_info_transformer.check_if_vr_error():
            SDKLogger.error("Detected VR ERROR!!! Please check the Pico device connection and status!")
            return
            
        if self.pico_info_transformer.is_running:
            if self.control_mode_changing:
                eef_pose_msg = self.interpolate_eef_pose(eef_pose_msg)
            self.pub.publish(eef_pose_msg)
            # if self.pico_info_transformer.control_torso_mode:
            #     self.pico_info_transformer.pub_head_body_pose_msg(self.pico_info_transformer.head_body_pose)
        else:
            SDKLogger.warn("Not publishing to /mm/two_arm_hand_pose_cmd because is_running is False")
        
        # Handle service mode changes
        if self.send_srv and (self.last_pico_running_state != self.pico_info_transformer.is_running):
            SDKLogger.info(f"Pico running state change to: {self.pico_info_transformer.is_running}")
            mode = 2 if self.pico_info_transformer.is_running else 0
            if self.pico_info_transformer.control_torso_mode:
                mobile_mode = 3 if self.pico_info_transformer.is_running else 0
            else:
                mobile_mode = 1 if self.pico_info_transformer.is_running else 0
            wbc_mode = 1 if self.pico_info_transformer.is_running else 0
            self.change_arm_ctrl_mode(mode)
            self.change_mobile_ctrl_mode(mobile_mode)
            self.change_mm_wbc_arm_ctrl_mode(wbc_mode)
            self.last_pico_running_state = self.pico_info_transformer.is_running

    def pico_hands_poses_callback_ik(self, pico_hands_poses_msg: picoPoseInfoList) -> None:
        """Callback for Pico hands poses."""
        self.pico_info_transformer.read_msg_hand(pico_hands_poses_msg)

        left_pose, left_elbow_pos = self.pico_info_transformer.get_hand_pose("Left")
        right_pose, right_elbow_pos = self.pico_info_transformer.get_hand_pose("Right")
        
        eef_pose_msg = twoArmHandPoseCmd()
        eef_pose_msg.hand_poses.left_pose.pos_xyz = left_pose[0]
        eef_pose_msg.hand_poses.left_pose.quat_xyzw = left_pose[1]
        eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = left_elbow_pos

        eef_pose_msg.hand_poses.right_pose.pos_xyz = right_pose[0]
        eef_pose_msg.hand_poses.right_pose.quat_xyzw = right_pose[1]
        eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = right_elbow_pos
        eef_pose_msg.ik_param = self.ik_solve_param
        eef_pose_msg.use_custom_ik_param = self.use_custom_ik_param
        
        # Check for VR errors
        if self.pico_info_transformer.check_if_vr_error():
            SDKLogger.error("Detected VR ERROR!!! Please check the Pico device connection and status!")
            return
            
        if self.pico_info_transformer.is_running:
            if self.control_mode_changing:
                eef_pose_msg = self.interpolate_eef_pose(eef_pose_msg)
            self.pub_ik.publish(eef_pose_msg)
        else:
            SDKLogger.warn("Not publishing to /ik/two_arm_hand_pose_cmd because is_running is False")
            # Handle service mode changes
        if self.send_srv and (self.last_pico_running_state != self.pico_info_transformer.is_running):
            SDKLogger.info(f"Pico running state change to: {self.pico_info_transformer.is_running}")
            mode = 2 if self.pico_info_transformer.is_running else 0
            mobile_mode = 0 if self.pico_info_transformer.is_running else 0
            wbc_mode = 0 if self.pico_info_transformer.is_running else 0
            self.change_arm_ctrl_mode(mode)
            self.change_mobile_ctrl_mode(mobile_mode)
            self.change_mm_wbc_arm_ctrl_mode(wbc_mode)
            self.last_pico_running_state = self.pico_info_transformer.is_running
    def set_item_mass_force(self, case_name:str, hand_wrench_config:HandWrenchConfig)->None:
        """Set item mass force."""
        self.hand_wrench_config = hand_wrench_config
        SDKLogger.info(f"Set item mass force: {case_name} --- {hand_wrench_config}")
        
    def set_control_mode_callback(self, control_mode: Int32) -> None:
        """Set control mode."""
        self._set_control_mode(control_mode.data)
    
    def _set_control_mode(self, control_mode: int) -> None:
        """Set control mode."""
        if control_mode == ControlMode.INCREMENTAL_MODE.value:
            self.set_control_mode("incremental")
            print("\033[93m--------------------进入增量模式-----------------\033[0m")
        elif control_mode == ControlMode.FOLLOW_MODE.value:
            self.set_control_mode("follow")
            print("\033[93m--------------------进入跟随模式-----------------\033[0m")
        elif control_mode == ControlMode.MOBILE_MPC_MODE.value:
            self.set_control_mode("mobile_mpc")
            print("\033[93m--------------------进入运动学MPC模式-----------------\033[0m")
        else:
            SDKLogger.error(f"Invalid control mode: {control_mode}")
    def set_incremental_mode_callback(self, incremental_mode: Int32) -> None:
        """Set incremental mode."""
        if incremental_mode.data == 1:
            self.set_in_incremental_mode(True)
        else:
            self.set_in_incremental_mode(False)

    def set_in_incremental_mode(self, incremental_mode: bool) -> None:
        """Set incremental mode."""
        self.is_in_incremental_mode = incremental_mode

    def set_control_mode(self, control_mode: str) -> None:
        """Set control mode."""
        if self.last_control_mode == ControlMode.INCREMENTAL_MODE and control_mode != "incremental":
            print("\033[93m--------------------退出增量模式-----------------\033[0m")
            self.change_mobile_ctrl_mode(IncrementalMpcCtrlMode.ArmOnly.value)
            self._left_target_pose = (None, None)
            self._right_target_pose = (None, None)  ## 清空上一次目标位姿
        self.last_control_mode = self.control_mode
        self.last_pico_running_state = not self.pico_info_transformer.is_running
        self.control_mode_changing = True
        if control_mode == "incremental":
            self.control_mode = ControlMode.INCREMENTAL_MODE
        elif control_mode == "follow":
            self.control_mode = ControlMode.FOLLOW_MODE
        elif control_mode == "mobile_mpc":
            self.control_mode = ControlMode.MOBILE_MPC_MODE
        else:
            SDKLogger.error(f"Invalid control mode: {control_mode}")

    def sensors_data_raw_callback(self, msg):
        if len(msg.joint_data.joint_q) >= 26:
            self.arm_joint_angles = msg.joint_data.joint_q[12:26]
    
    def ik_error_norm_callback(self, msg):
        """
        Callback for left hand error norm messages.
        """
        self.ik_error_norm = msg.data

    def fk_srv_client(self, joint_angles):
        service_name = "/ik/fk_srv"
        try:
            rospy.wait_for_service(service_name, timeout=3.0)
            fk_srv = rospy.ServiceProxy(service_name, fkSrv)
            fk_result = fk_srv(joint_angles)
            # rospy.loginfo(f"FK result: {fk_result.success}")
            return fk_result.hand_poses
        except rospy.ROSException:
            rospy.logerr(f"Service {service_name} not available")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
        return None

    def pico_hands_poses_callback_incremental(self, pico_hands_poses_msg: picoPoseInfoList) -> None:
        """Callback for Pico hands poses."""
        self.pico_info_transformer.read_msg_hand(pico_hands_poses_msg)

        left_pose, left_elbow_pos = self.pico_info_transformer.get_hand_pose("Left")
        right_pose, right_elbow_pos = self.pico_info_transformer.get_hand_pose("Right")
        
        eef_pose_msg = twoArmHandPoseCmd()
        eef_pose_msg.hand_poses.left_pose.pos_xyz = left_pose[0]
        eef_pose_msg.hand_poses.left_pose.quat_xyzw = left_pose[1]
        eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = left_elbow_pos

        eef_pose_msg.hand_poses.right_pose.pos_xyz = right_pose[0]
        eef_pose_msg.hand_poses.right_pose.quat_xyzw = right_pose[1]
        eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = right_elbow_pos
        eef_pose_msg.ik_param = self.ik_solve_param
        # eef_pose_msg.use_custom_ik_param = self.use_custom_ik_param
        eef_pose_msg.use_custom_ik_param = False
        eef_pose_msg.frame = 3

        if self.is_in_incremental_mode:
            if self.last_control_mode != ControlMode.INCREMENTAL_MODE:
                print("\033[93m++++++++++++++++++++开始增量模式+++++++++++++++++\033[0m")
                # 刚开始切换到增量控制模式
                self.control_mode = ControlMode.INCREMENTAL_MODE
                
                # 重置MPC状态
                print("\033[94m重置 Mobile Manipulator MPC...\033[0m")
                self.reset_mm_mpc()
                
                self.change_mobile_ctrl_mode(IncrementalMpcCtrlMode.ArmOnly.value)
                # 设置当前VR的末端位姿为锚点
                self._left_anchor_pose = left_pose
                self._right_anchor_pose = right_pose
                
                # 只有在目标位姿为空时才重新获取FK，避免抖动
                def is_pose_empty(pose):
                    return pose[0] is None or pose[1] is None
                
                if is_pose_empty(self._left_target_pose) or is_pose_empty(self._right_target_pose):
                    self._left_target_pose = left_pose
                    self._right_target_pose = right_pose
                else:
                    print("********************************* 使用上次目标位姿 (避免抖动) *********************************")
                    print("\033[92m左手保持目标位置: {}\033[0m".format(self._left_target_pose[0]))
                    print("\033[92m左手保持目标姿态(四元数): {}\033[0m".format(self._left_target_pose[1]))
                    print("\033[92m右手保持目标位置: {}\033[0m".format(self._right_target_pose[0]))
                    print("\033[92m右手保持目标姿态(四元数): {}\033[0m".format(self._right_target_pose[1]))
                self.last_control_mode = ControlMode.INCREMENTAL_MODE
            # 计算位置增量
            l_xyz_delta = np.subtract(left_pose[0], self._left_anchor_pose[0])
            r_xyz_delta = np.subtract(right_pose[0], self._right_anchor_pose[0])
            
            # 添加位置变化阈值，减少噪声影响
            position_threshold = 0.001  # 1mm
            if np.linalg.norm(l_xyz_delta) < position_threshold:
                l_xyz_delta = np.zeros(3)
            if np.linalg.norm(r_xyz_delta) < position_threshold:
                r_xyz_delta = np.zeros(3)

            def quaternion_inverse(q):
                norm = np.sum(np.array(q)**2)
                return np.array([-q[0], -q[1], -q[2], q[3]]) / norm

            def quaternion_multiply(q1, q2):
                x1, y1, z1, w1 = q1
                x2, y2, z2, w2 = q2
                return np.array([
                    w1*x2 + x1*w2 + y1*z2 - z1*y2,
                    w1*y2 - x1*z2 + y1*w2 + z1*x2,
                    w1*z2 + x1*y2 - y1*x2 + z1*w2,
                    w1*w2 - x1*x2 - y1*y2 - z1*z2
                ])
            def normalize_quaternion(q):
                norm = np.linalg.norm(q)
                return q / norm if norm > 0 else q

            l_anchor_quat_inv = quaternion_inverse(self._left_anchor_pose[1])
            r_anchor_quat_inv = quaternion_inverse(self._right_anchor_pose[1])
            l_delta_quat = quaternion_multiply(left_pose[1], l_anchor_quat_inv)
            r_delta_quat = quaternion_multiply(right_pose[1], r_anchor_quat_inv)
            
            # 添加姿态变化阈值，减少噪声影响
            def quaternion_angle(q):
                # 计算四元数对应的旋转角度
                w = abs(q[3])  # 确保w为正
                if w > 1.0:
                    w = 1.0
                return 2.0 * np.arccos(w)
            
            orientation_threshold = 0.01  # 约0.57度
            if quaternion_angle(l_delta_quat) < orientation_threshold:
                l_delta_quat = np.array([0, 0, 0, 1])  # 单位四元数
            if quaternion_angle(r_delta_quat) < orientation_threshold:
                r_delta_quat = np.array([0, 0, 0, 1])  # 单位四元数
            
            # 只有在有显著变化时才更新锚点
            if np.linalg.norm(l_xyz_delta) > 0 or quaternion_angle(l_delta_quat) > 0:
                self._left_anchor_pose = left_pose
            if np.linalg.norm(r_xyz_delta) > 0 or quaternion_angle(r_delta_quat) > 0:
                self._right_anchor_pose = right_pose
                
            l_target_quat = quaternion_multiply(l_delta_quat, self._left_target_pose[1])
            r_target_quat = quaternion_multiply(r_delta_quat, self._right_target_pose[1])

            l_target_quat = normalize_quaternion(l_target_quat)
            r_target_quat = normalize_quaternion(r_target_quat)

            self._left_target_pose = (self._left_target_pose[0] + l_xyz_delta, l_target_quat)
            self._right_target_pose = (self._right_target_pose[0] + r_xyz_delta, r_target_quat)
            left_elbow_pos = left_elbow_pos
            right_elbow_pos = right_elbow_pos

            eef_pose_msg = twoArmHandPoseCmd()
            eef_pose_msg.hand_poses.left_pose.pos_xyz = self._left_target_pose[0]
            eef_pose_msg.hand_poses.left_pose.quat_xyzw = self._left_target_pose[1]
            eef_pose_msg.hand_poses.left_pose.elbow_pos_xyz = left_elbow_pos
            eef_pose_msg.hand_poses.right_pose.pos_xyz = self._right_target_pose[0]
            eef_pose_msg.hand_poses.right_pose.quat_xyzw = self._right_target_pose[1]
            eef_pose_msg.hand_poses.right_pose.elbow_pos_xyz = right_elbow_pos

        else:
            if self.last_control_mode == ControlMode.INCREMENTAL_MODE:
                print("\033[93m--------------------暂停增量模式-----------------\033[0m")
                self.change_mobile_ctrl_mode(IncrementalMpcCtrlMode.NoControl.value)
                # 注意：这里不清空目标位姿，保持状态以避免下次进入时的抖动
                print("\033[94m保持目标位姿以避免下次进入增量模式时的抖动\033[0m")
            # self.control_mode = ControlMode.NONE_MODE
            self.last_control_mode = ControlMode.NONE_MODE

        
        if eef_pose_msg is not None:
            eef_pose_msg.ik_param = self.ik_solve_param
            # eef_pose_msg.use_custom_ik_param = self.use_custom_ik_param
            eef_pose_msg.use_custom_ik_param = False
            eef_pose_msg.frame = 3

            if any(error > 75.0 for error in self.ik_error_norm):
                rospy.logwarn(f"Hand error norm too large: {self.ik_error_norm}, skipping arm trajectory publication")
            elif self.pico_info_transformer.is_running:
                if self.control_mode_changing:
                    eef_pose_msg = self.interpolate_eef_pose(eef_pose_msg)
                self.pub.publish(eef_pose_msg)
        
        # Handle service mode changes
        if self.send_srv and (self.last_pico_running_state != self.pico_info_transformer.is_running):
            SDKLogger.info(f"Pico running state change to: {self.pico_info_transformer.is_running}")
            mode = 2 if self.pico_info_transformer.is_running else 0
            mobile_mode = 1 if self.pico_info_transformer.is_running else 0
            wbc_mode = 1 if self.pico_info_transformer.is_running else 0
            self.change_arm_ctrl_mode(mode)
            self.change_mobile_ctrl_mode(mobile_mode)
            self.change_mm_wbc_arm_ctrl_mode(wbc_mode)
            self.last_pico_running_state = self.pico_info_transformer.is_running

    def pico_hands_poses_callback_choose(self, pico_hands_poses_msg: picoPoseInfoList) -> None:
        """Callback for Pico hands poses."""
        if self.control_mode == ControlMode.INCREMENTAL_MODE:
            self.pico_hands_poses_callback_incremental(pico_hands_poses_msg)
        elif self.control_mode == ControlMode.FOLLOW_MODE:
            self.change_mobile_ctrl_mode(IncrementalMpcCtrlMode.NoControl.value)
            self.pico_hands_poses_callback_ik(pico_hands_poses_msg)
        elif self.control_mode == ControlMode.MOBILE_MPC_MODE:
            self.pico_hands_poses_callback(pico_hands_poses_msg)
        else:
            SDKLogger.error(f"Invalid control mode: {self.control_mode}")

    def interpolate_eef_pose(self, eef_pose_msg: 'twoArmHandPoseCmd', max_dist_threshold: float = 0.3, interp_alpha: float = 0.1
) -> 'twoArmHandPoseCmd':
        """对双手末端位姿进行线性插值，返回插值后的消息。"""

        if self.arm_joint_angles is None:
            return None

        # 拷贝原始消息，避免副作用
        interp_msg = deepcopy(eef_pose_msg)

        # 目标位姿（VR输入）
        l_target_pos = np.array(eef_pose_msg.hand_poses.left_pose.pos_xyz)
        r_target_pos = np.array(eef_pose_msg.hand_poses.right_pose.pos_xyz)

        # 获取当前实际末端（通过FK服务）
        hand_poses = self.fk_srv_client(self.arm_joint_angles)
        if hand_poses is not None:
            l_current_pos = np.array(hand_poses.left_pose.pos_xyz)
            r_current_pos = np.array(hand_poses.right_pose.pos_xyz)

            l_dist = np.linalg.norm(l_target_pos - l_current_pos)
            r_dist = np.linalg.norm(r_target_pos - r_current_pos)

            if l_dist > max_dist_threshold or r_dist > max_dist_threshold:
                # 插值平移
                new_l_pos = (1 - interp_alpha) * l_current_pos + interp_alpha * (l_target_pos - l_current_pos)
                new_r_pos = (1 - interp_alpha) * r_current_pos + interp_alpha * (r_target_pos - r_current_pos)
            else:
                # 距离较小，不插值
                new_l_pos = l_target_pos
                new_r_pos = r_target_pos
                self.control_mode_changing = False
        else:
            # FK失败，直接使用目标
            new_l_pos = l_target_pos
            new_r_pos = r_target_pos

        # 填入新数据
        interp_msg.hand_poses.left_pose.pos_xyz = new_l_pos.tolist()
        interp_msg.hand_poses.right_pose.pos_xyz = new_r_pos.tolist()

        return interp_msg
class RobotMatrixPublisher:
    """Publisher for robot body matrices data recording."""
    
    def __init__(self, topic_name="/robot_body_matrices", queue_size=100):
        """
        Initialize the publisher.
        
        Args:
            topic_name (str): ROS topic name for publishing
            queue_size (int): Queue size for the publisher
        """
        self.publisher = rospy.Publisher(
            topic_name, 
            robotBodyMatrices, 
            queue_size=queue_size
        )
        
        # 身体部位名称列表 - 与BODY_TRACKER_ROLES对应
        self.body_parts = [
            "Pelvis", "LEFT_HIP", "RIGHT_HIP", "SPINE1", "LEFT_KNEE", 
            "RIGHT_KNEE", "SPINE2", "LEFT_ANKLE", "RIGHT_ANKLE", "SPINE3",
            "LEFT_FOOT", "RIGHT_FOOT", "NECK", "LEFT_COLLAR", "RIGHT_COLLAR",
            "HEAD", "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", 
            "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_HAND", "RIGHT_HAND"
        ]
        
        self.data_source = "pico_vr_teleoperation"
        SDKLogger.info(f"RobotMatrixPublisher initialized on topic: {topic_name}")
    
    def publish_matrices(self, robot_urdf_matrices, current_time):
        """
        Publish robot body matrices data.
        
        Args:
            robot_urdf_matrices (np.ndarray): Shape [N, 4, 4] transformation matrices
            current_time (rospy.Time): Current ROS time
        """
        try:
            # 创建消息
            msg = robotBodyMatrices()
            
            # 设置header
            msg.header.stamp = current_time
            msg.header.frame_id = "world"
            
            # 设置时间戳
            msg.timestamp = current_time
            
            # 展平矩阵数据
            matrices_flat = []
            for matrix in robot_urdf_matrices:
                matrices_flat.extend(matrix.flatten())
            msg.matrices_data = matrices_flat
            
            # 设置矩阵数量
            msg.num_matrices = len(robot_urdf_matrices)
            
            # 设置身体部位名称
            msg.body_parts = self.body_parts[:msg.num_matrices]
            
            # 设置数据来源
            msg.data_source = self.data_source
            
            # 发布消息
            self.publisher.publish(msg)
            
        except Exception as e:
            SDKLogger.error(f"Error publishing robot matrices: {e}")
    
    def get_matrix_from_message(self, msg, matrix_index):
        """
        Extract a specific matrix from the message.
        
        Args:
            msg (RobotBodyMatrices): The message
            matrix_index (int): Index of the matrix to extract
            
        Returns:
            np.ndarray: 4x4 transformation matrix
        """
        if matrix_index >= msg.num_matrices:
            raise ValueError(f"Matrix index {matrix_index} out of range")
        
        start_idx = matrix_index * 16
        end_idx = start_idx + 16
        matrix_data = msg.matrices_data[start_idx:end_idx]
        timestamp = msg.timestamp
        
        return np.array(matrix_data).reshape(4, 4), timestamp
    
    def get_all_matrices_from_message(self, msg):
        """
        Extract all matrices from the message.
        
        Args:
            msg (RobotBodyMatrices): The message
            
        Returns:
            np.ndarray: Shape [N, 4, 4] transformation matrices
        """
        matrices = []
        for i in range(msg.num_matrices):
            matrix, timestamp = self.get_matrix_from_message(msg, i)
            matrices.append(matrix)
        
        return np.array(matrices), timestamp

def signal_handler(sig: int, frame: Any) -> None:
    """Handle signal for graceful exit."""
    print('Exiting gracefully...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        # Initialize the publisher
        publisher = KuavoPicoNode()
        
        # Keep the node running
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    