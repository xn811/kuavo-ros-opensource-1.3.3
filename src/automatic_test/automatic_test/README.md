# 自动测试包 (Automatic Test Package)

这是一个用于机器人控制的 ROS 自动测试包。它支持在仿真和实际硬件环境下进行测试。

## 概述

automatic_test 包旨在对机器人系统进行自动化测试。

## 配置

### 安装依赖

```bash
pip install --upgrade pytest
```

### 编译

```bash
cd <kuavo-ros-control>
catkin build automatic_test
```

### 配置环境变量

打开 `src/automatic_test/automatic_test/env/automatic_test.env` 文件，配置自动化测试的 webhook 地址和机器人序列号。

```bash
AUTOMATIC_TEST_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=595f7584-001a-42c1-91fc-5c3e6815443d
ROBOT_SERIAL_NUMBER=<机器人编号>
```

### 配置说明

参数文件位于 `config/params.yaml`，包含以下主要配置项：

#### 路径跟踪节点配置 (mpc_path_tracer_node)

1. 运动控制参数
   - `speed`: 默认运动速度 (0.4 m/s)
   - `dt`: 控制周期 (0.1 秒)
   - `v_max_linear`: 最大线速度 (0.4 m/s)
   - `v_max_angular`: 最大角速度 (0.6 rad/s)

2. 测试路径参数
   - 圆形路径 (circle)
     - `radius`: 圆形路径半径 (2.0 米)
   
   - 方形路径 (square)
     - `side_length`: 边长 (2.0 米)
     - `yaw_offset`: 偏航角偏移 (-0.785 弧度，约-45度)
   
   - S形路径 (scurve)
     - `length`: 路径长度 (1.5 米)
     - `amplitude`: 波动幅度 (1.0 米)

#### 行走测试节点配置 (test_robot_walk)

- `round`: 测试轮数 (默认: 10)

> 注意：这些参数可以根据实际测试需求进行调整。在修改参数时，请确保值在合理范围内，以确保机器人的安全运行。

## 启动参数

自动化测试通过命令行启动：

```bash
roslaunch automatic_test automatic_test.launch
```

### 参数说明

- `walk` (默认值: true): 行走测试
- `sim` (默认值: true)：启用/禁用仿真模式

## 测试流程

1. 将动捕球安装固定在测试机器人和天轨小车上

2. 确保实验室中的动捕系统已经正常工作, 能够正常获取机器人和天轨小车的 POSE 数据

3. 配置监听动捕数据流的 PC 与测试机器人的 ROS 局域网通信：

```bash
例如(请根据实际情况修改 IP 地址)：
监听动捕数据流的 PC 的 IP：192.168.1.100
测试机器人的 IP：192.168.1.101

### 在监听动捕数据流的 PC 上执行：
echo "export ROS_MASTER_URI=http://192.168.1.101:11311" | sudo tee -a /root/.bashrc
echo "export ROS_IP=192.168.1.100" | sudo tee -a /root/.bashrc

### 在测试机器人上执行：
echo "export ROS_MASTER_URI=http://192.168.1.101:11311" | sudo tee -a /root/.bashrc
echo "export ROS_IP=192.168.1.101" | sudo tee -a /root/.bashrc
```

3. 在**测试机器人**上启动 roscore

```bash
sudo su
roscore
```

4. 启动监听动捕数据流的程序，参阅文档：[动捕数据流监听程序](../motioncapture/readme.md)

5. 启动天轨小车控制程序，并且进入动捕自动跟踪模式, 参阅文档：[天轨小车控制程序](../kuavo_skyrail/README.md)

6. 将机器人挂在天轨小车上，用力移动机器人，测试天轨小车能否正常跟踪机器人

7. **开始测试:**

    7.1  请将机器人移动至测试起点，并保持静止

    7.2  请将机器人放下，直到双足触碰地面
    
    7.3  请将机器人的朝向调整至面朝前方测试空地
    
    7.4  启动测试程序：

```bash
cd <kuavo-ros-control>
sudo su
source devel/setup.bash
roslaunch automatic_test automatic_test.launch sim:=false
```

8. 测试结束后，机器人会自动回到测试起点，并且会发送测试结果到企业微信通知群
