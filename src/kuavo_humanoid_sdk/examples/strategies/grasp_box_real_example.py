#!/usr/bin/env python3
"""
本示例展示了如何使用 KuavoSDK 和 KuavoGraspBox 策略类来实现一个简单的箱子抓取任务。

主要步骤包括：
1. 初始化机器人及相关组件
2. 定义箱子抓取策略
3. 执行完整抓取流程
    3.1 使用头部寻找目标
    3.2 走路接近目标
    3.3 手臂移动到抓取位置
    3.4 提起箱子
    3.5 移动到放置位置
    3.6 放下箱子
4. 将机器人恢复到安全姿态
"""
import time
from kuavo_humanoid_sdk import KuavoSDK, KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose, AprilTagData, PoseQuaternion
from kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy import KuavoGraspBox, BoxInfo

""" Main Function """
def main():
    # !!! IMPORTANT 初始化 KuavoSDK 是必须的, 切记!
    if not KuavoSDK.Init(options=KuavoSDK.Options.Normal, log_level="DEBUG"):
        print("❌ 初始化失败")
        return
    
    ##############################################################################    
    # 🎯 这里定义搬箱子案例的一些信息

    # 粘贴在箱子上的 AprilTag 信息: 需要 ID，尺寸和基于odom坐标系下的大致位姿
    box_tag = AprilTagData(
        id=[1],                                 # AprilTag ID
        size=[0.1],                             # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            # TODO: 需要根据实际情况调整
            position=(0.0, -1.5, 0.8),          # 基于odom坐标系下的大致位置, 查找时会对齐到这个方向
            orientation=(0.0, 0.0, 0.0, 1.0)    # 四元数方向
        )]
    )
    
    # 粘贴在放置位置的 AprilTag 信息: 需要 ID，尺寸和基于odom坐标系下的大致位姿
    placement_tag = AprilTagData(
        id=[0],                                 # AprilTag ID
        size=[0.1],                             # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            # TODO: 需要根据实际情况调整
            position=(0.0, 1.5, 1.5),           # 基于odom坐标系下的大致位置, 查找时会对齐到这个方向
            orientation=(0.0, 0.0, 1.0, 0.0)    # 四元数方向 - 旋转180度
        )]
    )

    box_size = (0.4, 0.3, 0.22) # 箱子尺寸(长、宽、高)，单位：米
    box_mass = 2.0              # 箱子重量，单位：千克
    ###############################################################################

    print("初始化机器人...")
    
    # 初始化机器人及相关组件
    robot = KuavoRobot()
    robot_state = KuavoRobotState()
    robot_tools = KuavoRobotTools()
    robot_vision = KuavoRobotVision()
    
    # 初始化箱子抓取策略
    grasp_strategy = KuavoGraspBox(robot, robot_state, robot_tools, robot_vision)

    robot.arm_reset()
    time.sleep(1)
    # 执行完整抓取策略
    try:
        print("========== 开始执行箱子抓取策略 ==========")
        
        # 步骤1：使用头部寻找目标
        print("\n1. 寻找目标箱子...")
        grasp_strategy.robot.disable_head_tracking()
        print("✅ 已关闭头部追踪")
                
        if not grasp_strategy.head_find_target(
            box_tag, 
            max_search_time=15.0,
            search_pattern="rotate_body" #  rotate_head
        ):
            print("❌ 寻找目标失败，无法继续执行")
            return
        
        print("✅ 已找到目标箱子")
        time.sleep(1.5)  # 短暂暂停
        
        box_tag_data = robot_vision.get_data_by_id_from_odom(box_tag.id[0])
        if box_tag_data is None:
            print(f"❌ 未识别到 AprilTag ID 为{box_tag.id[0]} 的目标箱子")
            return
    
        # 步骤2：走路接近目标
        print("\n2. 走路接近目标...")        
        if not grasp_strategy.walk_approach_target(
            box_tag.id[0],
            target_distance=0.5,  # 与目标箱子保持一定的距离 
            approach_speed=0.2    # 接近速度0.2米/秒
        ):
            print("❌ 接近目标失败，无法继续执行")
            return
            
        print("✅ 已成功接近目标")
        time.sleep(1)  # 短暂暂停


        # 步骤3：手臂移动到抓取位置
        print("\n3. 手臂移动到抓取位置...")
        box_info = BoxInfo.from_apriltag(
            box_tag_data,
            xyz_offset=(box_size[1]/2, 0.0, 0.0),    # tag 粘贴在箱子正面，为了得到箱子中心点，因此偏移量为箱子宽度的一半
            size=box_size,                  # 箱子尺寸(长、宽、高)，单位：米
            mass=box_mass                   # 箱子重量，单位：千克
        )
        print(f"📦 箱子信息:{box_info}")
        
        if not grasp_strategy.arm_move_to_target(
            box_info,
            arm_mode="manipulation_mpc"
        ):
            print("❌ 手臂移动失败，无法继续执行")
            return
        print("✅ 手臂已到达抓取位置")        


        # 步骤4：提起箱子
        print("\n4. 提起箱子...")
        if not grasp_strategy.arm_transport_target_up(
            box_info,
            arm_mode="manipulation_mpc"
        ):
            print("❌ 提起箱子失败")
            return
                    
        print("✅ 成功提起箱子")
        time.sleep(1.0)  # 展示一下成功提起的状态
        # return # FIXME 先测试查找二维码功能

        ######################################
        # 步骤5：移动到放置位置
        ######################################
        grasp_strategy.robot.disable_head_tracking()
        if not grasp_strategy.head_find_target(
            placement_tag, 
            max_search_time=15.0,
            search_pattern="rotate_body" #  rotate_head
        ):
            print("❌ 寻找目标失败，无法继续执行")
            return

        if not grasp_strategy.walk_approach_target(
            placement_tag.id[0],
            target_distance=0.5,  # 与目标 Apriltag 保持0.5米的距离
            approach_speed=0.2    # 接近速度0.2米/秒
        ):
            print("❌ 接近目标失败，无法继续执行")
            return
                
        # 步骤6：放下箱子
        print("\n6. 放下箱子...")
        placement_tag_data = robot_vision.get_data_by_id_from_odom(placement_tag.id[0])
        if placement_tag_data is None:
            print(f"❌ 未识别到 AprilTag ID 为{placement_tag.id[0]} 的目标箱子")
            return

        placement_box_info = BoxInfo.from_apriltag(
            placement_tag_data,
            xyz_offset=(box_size[1]/2, 0.0, -0.5), # tag 粘贴在货架上，需要把箱子放下距离货架的高度 -0.5m
            size=box_size,  # 箱子尺寸(长、宽、高)，单位：米
            mass=box_mass  # 箱子重量，单位：千克
        )
        if not grasp_strategy.arm_transport_target_down(
            placement_box_info,
            arm_mode="manipulation_mpc"
        ):
            print("❌ 放下箱子失败")
            return
        time.sleep(1.0)  # 短暂暂停
    
        # 步骤7: 回到初始位置
        grasp_strategy.robot.disable_head_tracking()
        # 先后退
        start_time = time.time()
        while time.time() - start_time < 5.0:
            robot.walk(-0.15, 0.0, 0.0)
            time.sleep(0.1)
        # 手臂归位
        grasp_strategy.robot.stance()
        grasp_strategy.robot.arm_reset()
        # 回到原点
        grasp_strategy.walk_to_pose(
            KuavoPose(
                position=(0.0, 0.0, 0.0),
                orientation=(0.0, 0.0, 0.0, 1.0)
            ),
            target_distance=0.15,
            approach_speed=0.2
        )
        print("\n========== 搬箱子任务完成 ==========")
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 确保机器人回到安全状态
        print("将机器人恢复到安全姿态...")
        grasp_strategy.robot.disable_head_tracking()
        grasp_strategy.robot.stance()
        # grasp_strategy.robot.arm_reset()
        time.sleep(1.0)

if __name__ == "__main__":
    main() 