import time
from typing import Any, Tuple, List
import numpy as np

from kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.base_event import BaseEvent, EventStatus
from kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type import Pose, Tag, Frame, Transform3D
from kuavo_humanoid_sdk.kuavo_strategy_v2.utils.utils import normalize_angle
from kuavo_humanoid_sdk.kuavo_strategy_v2.common.robot_sdk import RobotSDK


class EventWalkToPose(BaseEvent):
    def __init__(self,
                 robot_sdk: RobotSDK,
                 timeout,
                 yaw_threshold,
                 pos_threshold,
                 control_mode,
                 ):
        """
        初始化走到指定位置事件。

        参数：
            timeout (float): 事件超时时间，单位秒。
            yaw_threshold (float): 偏航角阈值，单位弧度。
            pos_threshold (float): 位置阈值，单位米。
            control_mode (str): 控制模式。
        """
        super().__init__(
            event_name="EventWalkToPose",
        )
        self.robot_sdk = robot_sdk  # 使用封装的RobotSDK类

        ## members
        self.target: Pose = None  # 目标位置
        self.robot_pose_when_target_set: Pose = None  # 记录设置目标时机器人的位姿
        self.target_executed = False  # 标记目标位置未执行

        ## params
        self.timeout = timeout  # 事件超时时间
        self.yaw_threshold = yaw_threshold  # 偏航角阈值，单位弧度
        self.pos_threshold = pos_threshold  # 位置阈值，单位米
        self.control_mode = control_mode  # 控制模式，默认为相对位置控制

    def reset(self):
        """
        重置事件状态。
        """
        self.target = None  # 目标位置
        self.robot_pose_when_target_set = None  # 记录设置目标时机器人的位姿
        self.target_executed = False  # 标记目标位置未执行

        self.control_mode = 'cmd_pos_world'

    def close(self):
        """
        关闭事件。
        """
        super().close()
        self.reset()
        # 控制原地站立
        time.sleep(3)
        self.robot_sdk.control.stance()
        # self.robot_sdk.control.walk(linear_x=0, linear_y=0, angular_z=0)

    def set_control_mode(self, control_mode: str):
        """
        设置控制模式。

        参数：
            control_mode (str): 控制模式，支持 'cmd_pos_world', 'cmd_pos', 'cmd_vel'。
        """
        valid_modes = ['cmd_pos_world', 'cmd_pos', 'cmd_vel']
        if control_mode not in valid_modes:
            raise ValueError(f"无效的控制模式: {control_mode}，支持的模式有: {valid_modes}")
        self.control_mode = control_mode
        self.logger.info(f"🔵 控制模式已设置为: {self.control_mode}")

    def step(self):
        """
        执行事件的每一步操作。
        """
        if self.control_mode == "cmd_pos_world":
            # 使用世界坐标控制模式
            # if not self.target_executed:
            if True:  # 这个可以连续发
                self.robot_sdk.control.control_command_pose_world(
                    target_pose_x=self.target.pos[0],
                    target_pose_y=self.target.pos[1],
                    # target_pose_z=self.target.pos[2],
                    target_pose_z=0.0,
                    target_pose_yaw=self.target.get_euler(degrees=False)[2]
                )
                time.sleep(0.5)
                self.target_executed = True

        elif self.control_mode == "cmd_pos":
            # 使用相对位置控制模
            if not self.target_executed:
            # if True:
                self.robot_sdk.control.control_command_pose(self.target.pos[0], self.target.pos[1], self.target.pos[2],
                                                            self.target.get_euler()[2])
                self.target_executed = True

        elif self.control_mode == "cmd_vel":
            raise NotImplementedError("cmd_vel控制模式尚未实现")

        return self.get_status()

    def set_target(self, target: Any, *args, **kwargs):
        """
        设置事件的目标。

        参数：
            target (Any): 目标。
            *args: 额外的参数。
            **kwargs: 额外的关键字参数。

        返回：
            bool: 如果目标设置成功返回True，否则返回False。
        """
        res = super().set_target(target, *args, **kwargs)
        if res:
            # 为了应对相对位置控制的情况，记录设置目标时机器人的位姿
            self.robot_pose_when_target_set = Pose(
                pos=self.robot_sdk.state.robot_position(),
                quat=self.robot_sdk.state.robot_orientation(),
                frame=Frame.ODOM
            )
            self.target = target  # 设置目标位置
            self.target_executed = False  # 标记目标位置未执行
        return res

    def _check_target_valid(self, target: Pose):
        """
        检查目标位置是否有效。

        参数：
            target (Pose): 目标位置。

        返回：
            bool: 如果目标有效返回True，否则返回False。
        """
        if self.target is not None:
            if self.target.frame != target.frame:
                print(f"事件运行途中不能更换target坐标系（从 {self.target.frame} 到 {target.frame}）")
                return False

        if not isinstance(target, Pose):
            print("目标位置必须是Pose对象")
            return False

        if target.frame not in [Frame.ODOM, Frame.BASE]:
            print("目标位姿的坐标系必须是'base_link'或'odom'")
            return False

        if self.control_mode == 'cmd_pos':
            if target.frame != Frame.BASE:
                print("使用'cmd_pos'相对位置控制模式时，目标位姿的坐标系必须是'base_link'")
                return False

        if self.control_mode == 'cmd_vel':
            if target.frame != Frame.ODOM:
                print("使用'cmd_vel'速度控制模式时，目标位姿的坐标系必须是'odom'")
                return False

        if self.control_mode == 'cmd_pose_world':
            if target.frame != Frame.ODOM:
                print("使用'cmd_pose_world'世界坐标控制模式时，目标位姿的坐标系必须是'odom'")
                return False

        return True

    def _check_failed(self):
        """
        检查事件是否失败。

        返回：
            bool: 如果事件失败返回True，否则返回False。
        """
        # 无失败状态
        return False

    def _check_success(self):
        """
        检查事件是否成功。

        返回：
            bool: 如果事件成功返回True，否则返回False。
        """
        if self.control_mode == "cmd_pos_world":
            target_yaw = self.target.get_euler(degrees=False)[2]  # 获取目标偏航角
            yaw_reached = self._check_yaw(target_yaw)

            pos_reached = self._check_position_2d(self.target.pos[0], self.target.pos[1])

            if yaw_reached and pos_reached:
                return True

        elif self.control_mode == "cmd_pos":
            # 相对位置控制模式
            transform_init_to_world = Transform3D(
                trans_pose=self.robot_pose_when_target_set,
                source_frame=Frame.BASE,  # 源坐标系为base_link
                target_frame=Frame.ODOM  # 目标坐标系为odom
            )
            target_pose = transform_init_to_world.apply_to_pose(self.target)
            yaw_reached = self._check_yaw(target_pose.get_euler()[2])
            pos_reached = self._check_position_2d(target_pose.pos[0], target_pose.pos[1])

            if yaw_reached and pos_reached:
                return True

        return False

    def _check_yaw(self, target_yaw: float) -> bool:
        """
        检查机器人当前偏航角是否在目标偏航角的阈值范围内。

        参数：
            target_yaw (float): 目标偏航角。

        返回：
            bool: 如果在阈值范围内返回True，否则返回False。
        """
        robot_pose = Pose(
            pos=self.robot_sdk.state.robot_position(),
            quat=self.robot_sdk.state.robot_orientation()
        )
        robot_yaw = robot_pose.get_euler(degrees=False)[2]  # 获取机器人的偏航角
        yaw_diff = normalize_angle(target_yaw - robot_yaw)
        self.logger.debug(f"偏航角差: {yaw_diff}, 阈值: {self.yaw_threshold}")
        return abs(yaw_diff) <= self.yaw_threshold

    def _check_position_2d(self, target_x, target_y) -> bool:
        """
        检查机器人当前位置是否在目标位置的阈值范围内。

        参数：
            target_x (float): 目标位置的x坐标。
            target_y (float): 目标位置的y坐标。

        返回：
            bool: 如果在阈值范围内返回True，否则返回False。
        """
        robot_pos = self.robot_sdk.state.robot_position()
        pos_diff = np.linalg.norm(np.array(robot_pos[:2]) - np.array([target_x, target_y]))
        self.logger.debug(f"位置差: {pos_diff}, 阈值: {self.pos_threshold}")
        return pos_diff <= self.pos_threshold

