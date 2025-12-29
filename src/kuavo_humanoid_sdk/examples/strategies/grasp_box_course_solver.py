#!/usr/bin/env python3
"""
箱子抓取课程解决方案 - 使用预设关节轨迹
不使用manipulation_mpc，直接用关节位置控制
"""
import time
import numpy as np
import rospy
from kuavo_humanoid_sdk import KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose, AprilTagData, PoseQuaternion
from kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy import KuavoGraspBox, BoxInfo

# 导入link attacher服务
try:
    from gazebo_ros_link_attacher.srv import Attach, AttachRequest
    HAS_ATTACH_SERVICE = True
except ImportError:
    HAS_ATTACH_SERVICE = False
    print("警告: gazebo_ros_link_attacher 未安装，将不使用物理抓取")

# ============== 预设手臂关节位置 (角度制) ==============
# 每个手臂7个关节: [shoulder_pitch, shoulder_roll, shoulder_yaw, elbow, wrist_yaw, wrist_pitch, wrist_roll]
# 左臂(7) + 右臂(7) = 14个关节

ARM_POSES = {
    # 安全收起姿态
    "safe": [
        7.6, 68.8, 0.0, -90.8, 77.1, 0.0, 0.0,    # 左臂
        7.6, -68.8, 0.0, -90.8, -77.1, 0.0, 0.0   # 右臂
    ],
    # 准备抓取姿态 (手臂向前伸展，准备抱箱子)
    "pre_grasp": [
        -33.0, 4.7, 9.4, -40.0, 12.0, 0.0, 0.0,   # 左臂
        -33.0, -4.7, 9.4, -40.0, -12.0, 0.0, 0.0   # 右臂
    ],
    # 抓取姿态 (手臂合拢抱住箱子)
    "grasp": [
        -30.2, -2, -30.0, -40.0, 12.0, 0.0, 0.0,   # 左臂
        -30.2, 2, 30.0, -40.0, -12.0, 0.0, 0.0   # 右臂
    ],
    # 抬起搬运姿态 (抱着箱子抬高)
    "carry": [
        -30.0, 25.0, 0.0, -90.0, 0.0, 0.0, 0.0,   # 左臂
        -30.0, -25.0, 0.0, -90.0, 0.0, 0.0, 0.0   # 右臂
    ],
    # 放下姿态 (准备放下箱子)
    "place": [
        -15.0, 30.0, 0.0, -75.0, 0.0, 0.0, 0.0,   # 左臂
        -15.0, -30.0, 0.0, -75.0, 0.0, 0.0, 0.0   # 右臂
    ],
    # 松开姿态 (放开箱子)
    "release": [
        -15.0, 50.0, 0.0, -60.0, 0.0, 0.0, 0.0,   # 左臂
        -15.0, -50.0, 0.0, -60.0, 0.0, 0.0, 0.0   # 右臂
    ],
}

def deg_to_rad(positions_deg):
    """角度转弧度"""
    return [np.radians(deg) for deg in positions_deg]

def attach_box(robot_link="zarm_l7_link", box_model="block", box_link="base_link"):
    """将箱子附着到机器人手上"""
    if not HAS_ATTACH_SERVICE:
        print("⚠️ attach服务不可用")
        return True
    try:
        service_name = '/link_attacher_node/attach'
        rospy.wait_for_service(service_name, timeout=2.0)
        attach_srv = rospy.ServiceProxy(service_name, Attach)
        req = AttachRequest()
        req.model_name_1 = "biped_s42"
        req.link_name_1 = robot_link
        req.model_name_2 = box_model
        req.link_name_2 = box_link
        resp = attach_srv(req)
        if resp.ok:
            print(f"✅ 附着成功: {robot_link} <-> {box_model}/{box_link}")
        else:
            print(f"⚠️ 附着失败")
        return resp.ok
    except Exception as e:
        print(f"⚠️ attach服务调用失败: {e}")
        return False

def detach_box(robot_link="zarm_l7_link", box_model="block", box_link="base_link"):
    """将箱子从机器人手上分离"""
    if not HAS_ATTACH_SERVICE:
        print("⚠️ detach服务不可用")
        return True
    try:
        service_name = '/link_attacher_node/detach'
        rospy.wait_for_service(service_name, timeout=2.0)
        detach_srv = rospy.ServiceProxy(service_name, Attach)
        req = AttachRequest()
        req.model_name_1 = "biped_s42"
        req.link_name_1 = robot_link
        req.model_name_2 = box_model
        req.link_name_2 = box_link
        resp = detach_srv(req)
        if resp.ok:
            print(f"✅ 分离成功: {robot_link} <-> {box_model}/{box_link}")
        else:
            print(f"⚠️ 分离失败")
        return resp.ok
    except Exception as e:
        print(f"⚠️ detach服务调用失败: {e}")
        return False

def wait_for_confirm(step_name):
    """等待用户确认继续"""
    while True:
        user_input = input(f"\n>>> {step_name} - 输入 'y' 继续, 'q' 退出: ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'q':
            print("用户取消操作")
            return False
        else:
            print("请输入 'y' 或 'q'")

def move_arm_to_pose(robot, pose_name, duration=2.0):
    """移动手臂到预设姿态"""
    if pose_name not in ARM_POSES:
        print(f"❌ 未知姿态: {pose_name}")
        return False
    
    positions_rad = deg_to_rad(ARM_POSES[pose_name])
    print(f"  移动到 [{pose_name}] 姿态...")
    robot.control_arm_joint_positions(positions_rad)
    time.sleep(duration)
    print(f"  ✅ 已到达 [{pose_name}] 姿态")
    return True

def adjust_grasp_pose(robot):
    """交互式调整抓取姿态"""
    current_pose = ARM_POSES["grasp"].copy()
    
    while True:
        print(f"\n当前抓取姿态 (角度):")
        print(f"  左臂: {current_pose[:7]}")
        print(f"  右臂: {current_pose[7:]}")
        
        user_input = input("\n输入新的14个关节角度(逗号分隔), 'y'确认并抓取, 'q'退出: ").strip()
        
        if user_input.lower() == 'y':
            print("✅ 确认抓取姿态")
            return True
        elif user_input.lower() == 'q':
            print("❌ 取消抓取")
            return False
        else:
            try:
                # 解析输入的角度
                new_angles = [float(x.strip()) for x in user_input.split(',')]
                if len(new_angles) != 14:
                    print(f"⚠️ 需要14个角度值，你输入了{len(new_angles)}个")
                    continue
                
                # 更新姿态
                current_pose = new_angles
                ARM_POSES["grasp"] = current_pose
                
                # 执行新姿态
                positions_rad = deg_to_rad(current_pose)
                print("  移动到新的抓取姿态...")
                robot.control_arm_joint_positions(positions_rad)
                time.sleep(2.0)
                print("  ✅ 已到达新姿态")
                
            except ValueError as e:
                print(f"⚠️ 输入格式错误: {e}")
                print("  示例: -33.2, 2.5, -15.0, -40.0, 12.0, 0.0, 0.0, -33.2, 2.5, -15.0, -40.0, -12.0, 0.0, 0.0")

def main():
    print("初始化机器人...")
    robot = KuavoRobot()
    robot_state = KuavoRobotState()
    robot_tools = KuavoRobotTools()
    robot_vision = KuavoRobotVision()
    
    grasp_strategy = KuavoGraspBox(robot, robot_state, robot_tools, robot_vision)
    
    # AprilTag目标
    target_april_tag = AprilTagData(
        id=[0],
        size=[0.088],
        pose=[PoseQuaternion(
            position=(1.5, 0.0, 0.9),
            orientation=(0.0, 0.0, 0.0, 1.0)
        )]
    )
    
    # 放置位置 (yaw=180°)
    placement_pose = KuavoPose(
        position=(-4.80, 0.0, 0.9),
        orientation=(0.0, 0.0, 1.0, 0.0)
    )
    
    time.sleep(1)
    
    try:
        print("========== 开始执行箱子抓取策略 ==========")
        
        # 步骤1：寻找目标
        print("\n1. 寻找目标箱子...")
        robot.disable_head_tracking()
        
        find_success = grasp_strategy.head_find_target(
            target_april_tag, 
            max_search_time=15.0,
            search_pattern="rotate_body"
        )
        
        if not find_success:
            print("❌ 寻找目标失败")
            return
        print("✅ 已找到目标箱子")
        time.sleep(1)

        # 步骤2：走路接近目标
        print("\n2. 走路接近目标...")
        approach_success = grasp_strategy.walk_approach_target(
            target_april_tag,
            target_distance=0.35,
            approach_speed=0.2
        )
        
        if not approach_success:
            print("❌ 接近目标失败")
            return
        print("✅ 已成功接近目标")
        
        # if not wait_for_confirm("步骤3: 切换stance并移动手臂"):
        #     return

        # 步骤3：切换到stance，准备抓取
        print("\n3. 切换到stance状态...")
        robot.stance()
        if not robot_state.wait_for_stance(timeout=10.0):
            print("⚠️ 等待站稳超时")
            return
        print("✅ 机器人已站稳")
        
        # 移动到安全姿态
        move_arm_to_pose(robot, "safe", duration=2.0)
        
        # if not wait_for_confirm("步骤4: 手臂准备抓取"):
        #     return

        # 步骤4：手臂准备抓取
        print("\n4. 手臂准备抓取...")
        move_arm_to_pose(robot, "pre_grasp", duration=2.0)
        
        # if not wait_for_confirm("步骤5: 抓取箱子"):
        #     return

        # 步骤5：抓取
        print("\n5. 抓取箱子...")
        move_arm_to_pose(robot, "grasp", duration=2.0)
        time.sleep(2.0)  # 等待手臂到位
        # 交互式调整抓取姿态 (调试时启用)
        # if not adjust_grasp_pose(robot):
        #     return
        
        # 调用attach服务 (双手附着)
        print("🤖 执行物理抓取...")
        attach_box("zarm_l7_link", "block", "base_link")
        attach_box("zarm_r7_link", "block", "base_link")

        
        # if not wait_for_confirm("步骤6: 抬起箱子"):
        #     return

        # 步骤6：抬起搬运
        print("\n6. 抬起箱子...")
        move_arm_to_pose(robot, "carry", duration=2.0)
        print("✅ 成功抬起箱子")
        
        # if not wait_for_confirm("步骤7: 走到放置位置"):
        #     return

        # 步骤7：走到放置位置
        print("\n7. 走到放置位置...")
        robot.disable_head_tracking()
        
        # 使用walk_to_pose
        placement_box_info = BoxInfo(
            pose=placement_pose,
            size=(0.3, 0.2, 0.15),
            mass=0.5
        )
        move_success = grasp_strategy.walk_to_pose(
            placement_box_info,
            target_distance=0.4,
            approach_speed=0.2,
        )
        if not move_success:
            print("❌ 移动到放置位置失败")
            return
        
        # 到达后切换stance
        robot.stance()
        robot_state.wait_for_stance(timeout=10.0)
        print("✅ 已到达放置位置")
        
        # if not wait_for_confirm("步骤8: 放下箱子"):
        #     return

        # 步骤8：放下箱子
        print("\n8. 放下箱子...")
        move_arm_to_pose(robot, "place", duration=2.0)
        
        # 松开
        move_arm_to_pose(robot, "release", duration=2.0)
        
        # 调用detach服务 (双手分离)
        print("🤖 执行物理释放...")
        detach_box("zarm_l7_link", "block", "base_link")
        detach_box("zarm_r7_link", "block", "base_link")
        
        # 收回手臂
        move_arm_to_pose(robot, "safe", duration=2.0)
        
        print("\n========== 箱子抓取任务完成 ==========")
        
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("将机器人恢复到安全姿态...")
        try:
            robot.stance()
            robot_state.wait_for_stance(timeout=5.0)
        except:
            pass

if __name__ == "__main__":
    main()
