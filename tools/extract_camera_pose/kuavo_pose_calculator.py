#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Lejurobot 2025
# This file is used to transform the kuavo robot pose to the camera pose.

import numpy as np 
from pydrake.multibody.parsing import Parser
from pydrake.multibody.plant import MultibodyPlant

class KuavoPoseCalculator:
    def __init__(self, urdf_path):
        self.plant = MultibodyPlant(0.0)
        Parser(self.plant).AddModelFromFile(urdf_path)

        self.base_link_frame = self.plant.GetFrameByName("base_link") # 基座坐标系
        self.plant.WeldFrames(self.plant.world_frame(), self.base_link_frame)
        self.plant.Finalize()
        self.context = self.plant.CreateDefaultContext()
        self.nq = self.plant.num_positions() # 关节数
        
        # Debug
        print("----------------------------------------------------------------------------")
        joint_names = self.plant.GetPositionNames(add_model_instance_prefix=False, always_add_suffix=False)
        l_leg_joints = [name for name in joint_names if name.startswith('leg_l')]
        r_leg_joints = [name for name in joint_names if name.startswith('leg_r')]
        l_arm_joints = [name for name in joint_names if name.startswith('zarm_l')]
        r_arm_joints = [name for name in joint_names if name.startswith('zarm_r')]
        head_joints = [name for name in joint_names if name.startswith('zhead')]
        print("关节数量:", self.nq)
        print("左腿关节:", l_leg_joints)
        print("右腿关节:", r_leg_joints)
        print("左臂关节:", l_arm_joints)
        print("右臂关节:", r_arm_joints)
        print("头部关节:", head_joints)
        print("----------------------------------------------------------------------------")

    def get_camera_pose(self, head_q:list):
        """计算头部相机在基座坐标系中的位姿。
        
        Args:
            head_q (list): 头部关节角度列表, 长度为2, 分别对应头部的两个关节角度(yaw, pitch), 单位为弧度.
            
        Returns:
            RigidTransform: 头部相机在基座坐标系中的位姿变换矩阵。
            
        Raises:
            ValueError: 当head_q长度不为2 或关节角度列表中包含非数字值时抛出异常。
        """
        if len(head_q) != 2:
            raise ValueError(f"head_q must have length 2, but got {len(head_q)}")
        # 检查关节角度列表中是否包含非数字值
        for i, angle in enumerate(head_q):
            if not isinstance(angle, (int, float)) or np.isnan(angle) or np.isinf(angle):
                raise ValueError(f"head_q[{i}] must be a valid number, but got {angle}")
        
        q = np.zeros(self.nq)
        q[-2:] = head_q
        self.plant.SetPositions(self.context, q)
        # fk
        camera_pose_in_base = self.plant.GetFrameByName("camera_base").CalcPose(
            self.context, self.base_link_frame
        )
        return camera_pose_in_base
    
    def get_l_hand_camera_pose(self, larm_q:list):
        """
        计算左臂相机在基座坐标系中的位姿。
        
        Args:
            larm_q (list): 左臂关节角度列表, 长度为7, 分别对应左臂的7个关节角度, 单位为弧度.
            
        Returns:
            RigidTransform: 左臂相机在基座坐标系中的位姿变换矩阵。

        Raises:
            ValueError: 当larm_q长度不为7 或关节角度列表中包含非数字值时抛出异常。
        """
        if len(larm_q) != 7:
            raise ValueError(f"larm_q must have length 7, but got {len(larm_q)}")
        
        # 检查关节角度列表中是否包含非数字值
        for i, angle in enumerate(larm_q):
            if not isinstance(angle, (int, float)) or np.isnan(angle) or np.isinf(angle):
                raise ValueError(f"larm_q[{i}] must be a valid number, but got {angle}")
        
        q = np.zeros(self.nq)
        q[12:19] = larm_q # 左臂关节索引为 12-18 下标从 0 开始
        self.plant.SetPositions(self.context, q)
        # fk
        camera_pose_in_base = self.plant.GetFrameByName("l_hand_camera").CalcPose(
            self.context, self.base_link_frame
        )
        return camera_pose_in_base
    
    def get_r_hand_camera_pose(self, rarm_q:list):
        """
        计算右臂相机在基座坐标系中的位姿。
        
        Args:
            rarm_q (list): 右臂关节角度列表, 长度为7, 分别对应右臂的7个关节角度, 单位为弧度.
            
        Returns:
            RigidTransform: 右臂相机在基座坐标系中的位姿变换矩阵。

        Raises:
            ValueError: 当rarm_q长度不为7 或关节角度列表中包含非数字值时抛出异常。
        """
        if len(rarm_q) != 7:
            raise ValueError(f"rarm_q must have length 7, but got {len(rarm_q)}")
        
        # 检查关节角度列表中是否包含非数字值
        for i, angle in enumerate(rarm_q):
            if not isinstance(angle, (int, float)) or np.isnan(angle) or np.isinf(angle):
                raise ValueError(f"rarm_q[{i}] must be a valid number, but got {angle}")
        
        q = np.zeros(self.nq)
        q[19:26] = rarm_q # 右臂关节索引为 19-25 下标从 0 开始
        self.plant.SetPositions(self.context, q)
        # fk
        camera_pose_in_base = self.plant.GetFrameByName("r_hand_camera").CalcPose(
            self.context, self.base_link_frame
        )
        return camera_pose_in_base

if __name__ == "__main__":
    # 使用示例 需要替换成您实际的 URDF 路径
    kuavo_camera_pose_calculator = KuavoPoseCalculator("../../src/kuavo_assets/models/biped_s45/urdf/biped_s45.urdf")
    
    head_camera_pose = kuavo_camera_pose_calculator.get_camera_pose([0.0, 0.0])
    print("head_camera pose:", head_camera_pose)
    l_hand_camera_pose = kuavo_camera_pose_calculator.get_l_hand_camera_pose([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    print("lhand_camera pose:", l_hand_camera_pose)
    r_hand_camera_pose = kuavo_camera_pose_calculator.get_r_hand_camera_pose([0.25, -1.0, -1.0, -1.208, 0.156, 0.658, 0.13])
    print("rhand_camera pose: ", r_hand_camera_pose)
