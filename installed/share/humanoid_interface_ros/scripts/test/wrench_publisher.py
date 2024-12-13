#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64MultiArray, MultiArrayDimension

def publish_wrench():
    # 初始化 ROS 节点
    rospy.init_node('wrench_publisher', anonymous=True)
    
    # 创建一个发布者，发布到 /hand_wrench_cmd 主题
    pub = rospy.Publisher('/hand_wrench_cmd', Float64MultiArray, queue_size=10)
    rospy.sleep(0.5)  # 等待发布者连接到主题

    # 创建 Float64MultiArray 消息
    wrench_msg = Float64MultiArray()
    # 正确初始化 dim
    dim = MultiArrayDimension()
    dim.label = ''
    dim.size = 12    # 根据需要调整尺寸
    dim.stride = 12  # 根据需要调整步幅
    wrench_msg.layout.dim.append(dim)  # 将 dim 添加到 layout

    wrench_msg.layout.data_offset = 0
    # wrench_msg.data = [0.0, 20.0, 0.0, 0.0, 0.0, 0.0,
    #                    0.0, -20.0, 0.0, 0.0, 0.0, 0.0]  # 力和力矩数据
    wrench_msg.data = [0.0 for i in range(12)]
    force_x = 0.0
    force_y = 10.0
    force_z = -0.0
    wrench_msg.data[:3] = [force_x,  +force_y, force_z]
    wrench_msg.data[6:9] = [force_x, -force_y, force_z]

    # 发布消息
    pub.publish(wrench_msg)
    rospy.loginfo("Published Wrench: %s", wrench_msg.data)
        

if __name__ == '__main__':
    try:
        publish_wrench()
    except rospy.ROSInterruptException:
        pass
