from kuavo_sdk.srv import controlEndHand, controlEndHandRequest, controlEndHandResponse
import rospy


def srv_controlEndHand(hand_traj):
    """
    控制机器人的手部动作。

    参数:
    hand_traj (list): 包含左手和右手位置的列表，前6个元素为左手，后6个元素为右手。

    返回:
    bool: 服务调用结果，成功返回True，失败返回False。
    """
    try:
        # 初始化服务代理，用于控制机器人的手部
        robot_control_hand_client = rospy.ServiceProxy("/control_end_hand", controlEndHand)
        # 创建请求对象
        request = controlEndHandRequest()
        # 设置左手和右手的位置
        request.left_hand_position = hand_traj[0:6]
        request.right_hand_position = hand_traj[6:]

        # 调用服务并获取响应
        response = robot_control_hand_client(request)

        # 返回结果
        return response.result

    except rospy.ServiceException as e:
        # 记录错误日志
        rospy.logerr(f"controlEndHand 服务调用失败: {e}")
        return False

def main():
    # 初始化ROS节点
    rospy.init_node('robot_hand_controller')

    # 示例手部轨迹数据，假设每只手有6个位置参数
    hand_traj = [0, 0, 0, 0, 0, 0,  # 左手位置
                 20, 20, 20, 20, 20, 20]  # 右手位置

    # 调用服务函数
    result = srv_controlEndHand(hand_traj)

    # 输出结果
    if result:
        rospy.loginfo("手部控制成功")
    else:
        rospy.loginfo("手部控制失败")


if __name__ == "__main__":
    main()