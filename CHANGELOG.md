# dev 分支

## Breaking Changes
- 无

## 文档相关
- 更新 README 添加了开源版本容器镜像下载链接和使用指南 [文档链接](readme.md) 

## 新增功能
- 新增辅助校准功能用于快速调整手臂零点圈数回零, 实现校准圈数、以当前位置作为零点、使能掉使能等方便调试
- 新增遥控器按键启动 VR 遥操作功能
- 新增贝塞尔曲线插值和三次样曲线插值手臂轨迹规划功能和对应的 websocket 播放服务, [文档链接](src/humanoid-control/humanoid_plan_arm_trajectory/README.md)
- 新增 VR 启动时允许指定上扳机只控制拇指+食指 or 除拇指虎口方向外的全部手指自由度
- 新增`/cmd_pose`位置控制接口
- 新增使用基于 MPC 控制机器人行走正方形/圆形/S曲线的示例 [文档链接](src/demo/trace_path/README.md)
- 新增电机 cali 模式下辅助校准功能, 增加准备阶段按`h`可查看当前操作流程提示功能
- 新增开机自启动遥控器控制机器人的功能, 目前支持 h12pro controller, [文档链接](./src/humanoid-control/h12pro_controller_node/ocs2_README.md)
- 新增简单案例: 抓取案例, 使用`/cmd_vel`控制走正方形/圆形/S曲线, 按键控制手臂微调 [文档链接](src/humanoid-control/humanoid_arm_control/README.md),[文档链接1](src/humanoid-control/humanoid_arm_control/docs/arm-control-keyboard.md)
- 兼容 4代、4pro版本的机器人, 新增单步控制功能
- 新增使用 ROBOT_VERSION 环境变量设置机器人版本号, 根据版本号选择对应的配置文件
- 新增自动根据机器人总质量修改对应模型和编译 cppad 功能
- 使用 ROS 标准方式重构开源版本的编译安装方式
- 新增 4.0 与 4.2 仿真环境的头部模型和控制, 并发布头部关节到 TF 与 Rviz 可视化

## 修复问题 
- 修复 4pro mujoco 模型手臂高度错误导致仿真中需要修改 pitch 增益才能运行问题
- 修改手臂电机使能之后存在自动回零的问题，通过发送当前位置一次之后可以避免自动回零解决
- 修复 VR 使用提示无法找到 xx_ik.py 问题, 以及手指控制跳变问题
- 修复开机自启动遥控器控制机器人功能中错误的包路径导致的安装失败问题
- 修复 youda 驱动器版本机器人行走出现全身抖动问题, 原因是缺少髋关节力控、腿部楼空版本质量、手臂末端的零速度约束...
- 修复脚本文件无可执行权限问题, 已通过在 cmake install 中追加权限解决
- 修复开源仓库硬件包查找路径错误问题, 使用 rospack 获取而不是通过维护环境变量
- 修复由于适配优达驱动器引入的 CST, CSV 下索引错误问题

## 性能优化
- 修复头部动作执行时不断读取 json 降低效率问题

## 其他改进
- dockerfile 增加 ros-noetic-rqt-graph ROS 包安装步骤
- 重构手臂电机零点调整功能, 使用单独的零点文件 arms_zero.yaml，不存在时自动获取一次当前位置作为零点
- 移除废弃的 GPU dockerfile 文件
- 整理 URDF 模型文件, mujoco 模型文件和硬件相关的配置文件到 kuavo_assets 包中统一进行管理
- 使用 config 配置目录的 EcMasterType.ini 来指定驱动器类型(youda/elmo(默认)), 并在编译时提示选择驱动器版本(4.2版本之后生效)
- 添加 CPU 温度、频率、占用率记录和发布方便观测与调试
- 优化日志打印提示, 消除编译告警和补充开源仓库缺失的一些脚本和节点
- 移除废弃的代码,脚本和编译选项