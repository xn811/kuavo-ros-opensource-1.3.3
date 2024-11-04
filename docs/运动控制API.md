# 运动控制API

节点的含义参考:[topics定义](./readme.topics.md)

- 控制流程图：
  
<img src=img/ocs2_topics.jpg width="90%">

- MPC节点处理目标轨迹的流程

<img src=img/targetmanager.png width="90%">

## 主要topics和srv
#### srv
- `/humanoid_change_arm_ctrl_mode` <kuavo_msgs::changeArmCtrlMode>
  - 修改手臂控制模式，control_mode 有三种模式
    - 0: keep pose 保持姿势 
    - 1: auto_swing_arm 行走时自动摆手，切换到该模式会自动运动到摆手姿态
    - 2: external_control 外部控制，手臂的运动由外部控制
- `/humanoid_get_arm_ctrl_mode` <kuavo_msgs::changeGaitMode>
  - 获取当前控制模式，返回 control_mode
- `/humanoid_auto_gait`
  - 是否自动切换gait，默认true，收到非零的 `/cmd_vel` 会自动切换到walk模式，收到全0的 `/cmd_vel` 会自动切换到stance模式。
  - 手动模式下，需要先发布 `/humanoid_mpc_mode_schedule` 才能切换gait模式
- `/humanoid_single_step_control` <kuavo_msgs::singleStepControl>
  - 单步控制，通过给出时间序列和对应的躯干位姿，可以控制机器人的单步行走
  - 时间序列和躯干位姿序列长度必须一致，时间序列需要不断递增
  - 每次服务请求的躯干位姿都是基于局部坐标系，但是一次服务请求中的躯干位姿序列需要以第一个位姿为基准不断变化

#### topics
- `/cmd_vel`    <geometry_msgs/Twist>
  - 控制指令，6dof速度指令，机器人的target指令的速度形式，包含xy方向速度、高度z和yaw方向速度，roll、pitch方向不控制。
  - 直接发送非0的 `/cmd_vel` 指令，机器人会自动切换到walk拟人步态行走
  - 行走过程中发送全0的 `/cmd_vel` 指令，机器人会自动切换到stance站立状态。

-  `/humanoid_mpc_target_arm`     <ocs2_msgs/mpc_target_trajectories>
   - 手臂规划指令，只包含手臂维度的`armTargetTrajectories`，只有在手臂控制模式为`external_control`时才会被使用。

> 注意：每次调用`/humanoid_change_arm_ctrl_mode`切换mode之后，会从旧的轨迹插值到新的轨迹的过程，需要等待插值完成才会执行新的轨迹。插值过程可以通过`/humanoid_get_arm_ctrl_mode`获取当前控制模式。

- `/humanoid_mpc_target_pose`     <ocs2_msgs/mpc_target_trajectories>
  - 躯干6dof位姿规划指令,只包含6维度`poseTargetTrajectories`
  - 注意位姿指令优先级比cmd_vel指令高，不要同时发送两种指令

- `/humanoid_mpc_mode_schedule`   <ocs2_msgs/mode_schedule>
  - 切换gait指令，发布的模板要和gait.info中定义的gait严格一致

- `/humanoid_mpc_stop_step_num`   <std_msgs/Int32>
  - 停止步数，从当前统计的步数开始，机器人会在后续第N步自动停下
  - 可以在发送`/humanoid_mpc_mode_schedule`之前或者行走时发送，步数控制没接收一次指令只作用一次

