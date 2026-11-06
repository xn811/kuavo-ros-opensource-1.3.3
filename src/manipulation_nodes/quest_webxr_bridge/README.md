# Quest WebXR Bridge

ROS 1 桥接包：通过 Quest 浏览器的 WebXR 手部追踪控制 Kuavo v49 双臂和灵巧手，并可选跟随头显姿态。桥接复用 Kuavo 的 `motion_capture_ik` 和控制接口；手臂输出经过适配器的反馈、关节限位及速度检查。

## 使用文档

- [普通 v49 半身仿真启动与操作](../../../README_WEBXR.md)
- [头显 HUD 状态与故障说明](docs/headset_hud_zh.md)

需要 Kuavo ROS Noetic 工作区、Quest 手部追踪、局域网 HTTPS 证书，以及 `requirements.txt` 中的 Python 依赖。配置、编译、证书及分终端启动步骤见启动说明。

## 数据路径

```text
Quest WebXR → 手势与标定 → /ik/two_arm_hand_pose_cmd → ik_ros_uni.py
             → 安全适配器 → /kuavo_arm_traj
手部关键点 → 手指映射 → 安全适配器 → /control_robot_hand_position
头显姿态 → /robot_head_motion_data
```

双手张开、掌心向上保持 5 秒启动；双手握拳保持 3 秒暂停。完全退出需要先暂停，再双手捏合、释放并握拳确认。详细状态及操作见 HUD 文档。

## 录包工具

`scripts/rosbag_tool.py` 提供交互式录制与回放，默认读取 `config/record_topics.json`。`scripts/validate_rosbag_alignment.py` 可检查录包格式。普通场景不提供完整相机和触觉数据；咖啡杯场景的录包步骤见第二次提交中的仓库根目录说明。

## 使用限制

启动动作预检要求桥接进程环境中 `ROBOT_VERSION=49`、ROS 参数 `/only_half_up_body=true`。基础系统需关闭其内置 IK 和 VR 遥操，不能同时运行其他手臂命令发布者。代码包含 MuJoCo 抓取试验参数；真机使用前必须由现场人员确认控制配置、保护参数和急停，不能把仿真结果视为真机验证。
