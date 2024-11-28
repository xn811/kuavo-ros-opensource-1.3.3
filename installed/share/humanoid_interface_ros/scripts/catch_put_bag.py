import plan_arm_traj_bezier_demo 
import simStepControl 
import rospy


# from plan_arm_traj_bezier_demo import Pre_to_catch_bag, call_change_arm_ctrl_mode_service
# from simStepControl import publish_multiple_steps

def catch_put_bag():
    # TODO: Implement catch bag demo
    
    """
        1 先抬手
        2 抓取包
        3 恢复到自然摆臂状态下的手臂
    """ 
    plan_arm_traj_bezier_demo.Pre_to_catch_bag()
    # TODO: 灵巧手抓取
    input("Press Enter to continue...")

    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(1)
    input("Press Enter to continue...")

    """
        第一段走路
        1 走几步（自然摆臂状态）
    """
    # simStepControl.publish_multiple_steps_Down_arm()
    # input("Press Enter to continue...")

    """
        第二段走路
        1 再走几步（抬起手走）
    """
    plan_arm_traj_bezier_demo.call_change_arm_ctrl_mode_service(2)
    # simStepControl.publish_multiple_steps_Up_arm()
    input("Press Enter to continue...")

def main():
    rospy.init_node('catch_put_bag_node')
    catch_put_bag()

if __name__ == '__main__':
    main()
