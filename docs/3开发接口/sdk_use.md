# 接口使用文档
### SDK 概述

该 SDK 提供了一系列用于控制和获取机器人状态的接口，主要分为两类：话题（Topic）和服务（Service）。这些接口基于 ROS（机器人操作系统）框架，提供 Python 示例进行开发和调用。以下是 SDK 的主要功能概述：

#### 话题（Topic）

话题用于发布和订阅机器人传感器数据和控制指令。通过话题，用户可以实时获取机器人传感器的原始数据，如 IMU 数据、点云数据、图像数据等，也可以发布控制指令来控制机器人的运动和姿态。

- **传感器数据**：通过话题获取机器人传感器的原始数据，包括 IMU 数据、点云数据、图像数据等。
- **运动控制**：通过话题发布控制指令，指定机器人的运动轨迹、速度和姿态。

#### 服务（Service）

服务用于执行特定的控制命令或获取状态信息。服务调用是同步的，即用户发送请求后会等待服务返回响应。服务通常用于执行一次性操作，如播放音乐、录制音频、设置控制模式等。

- **控制命令**：通过服务接口发送控制命令，如播放音乐、录制音频、设置手臂控制模式等。
- **状态获取**：通过服务接口获取机器人的状态信息。

### 使用指南

1. **初始化 ROS 节点**：在使用 SDK 之前，需要初始化一个 ROS 节点。可以使用 `rospy.init_node()` 方法来完成节点的初始化。

2. **创建话题订阅者或发布者**：根据需要创建话题的订阅者或发布者。订阅者用于接收话题数据，发布者用于发送控制指令。

3. **创建服务代理**：对于需要调用的服务，创建一个服务代理对象，并通过该对象发送请求和接收响应。

4. **处理数据或响应**：在接收到话题数据或服务响应后，进行相应的处理或操作。

- [接口使用文档](#接口使用文档)
    - [SDK 概述](#sdk-概述)
      - [话题（Topic）](#话题topic)
      - [服务（Service）](#服务service)
    - [使用指南](#使用指南)
    - [`/play_music` 播放音频](#play_music-播放音频)
    - [功能描述](#功能描述)
    - [请求格式](#请求格式)
    - [响应格式](#响应格式)
    - [使用示例](#使用示例)
    - [`/record_music` 记录音频](#record_music-记录音频)
    - [功能描述](#功能描述-1)
    - [请求格式](#请求格式-1)
    - [响应格式](#响应格式-1)
    - [使用示例](#使用示例-1)
    - [`/livox/imu` 雷达imu数据](#livoximu-雷达imu数据)
    - [功能描述](#功能描述-2)
    - [消息类型](#消息类型)
    - [消息字段](#消息字段)
    - [使用示例](#使用示例-2)
    - [`/livox/lidar` 雷达点云数据](#livoxlidar-雷达点云数据)
    - [功能描述](#功能描述-3)
    - [消息类型](#消息类型-1)
    - [消息字段](#消息字段-1)
    - [使用示例](#使用示例-3)
    - [`/camera/depth/color/points` 相机点云数据](#cameradepthcolorpoints-相机点云数据)
    - [功能描述](#功能描述-4)
    - [消息类型](#消息类型-2)
    - [消息字段](#消息字段-2)
    - [使用示例](#使用示例-4)
    - [`/camera/color/image_raw` 相机彩色图像数据](#cameracolorimage_raw-相机彩色图像数据)
    - [功能描述](#功能描述-5)
    - [消息类型](#消息类型-3)
    - [消息字段](#消息字段-3)
    - [使用示例](#使用示例-5)
    - [`/camera/depth/image_rect_raw` 相机深度图像数据](#cameradepthimage_rect_raw-相机深度图像数据)
    - [功能描述](#功能描述-6)
    - [消息类型](#消息类型-4)
    - [消息字段](#消息字段-4)
    - [使用示例](#使用示例-6)
    - [`/arm_traj_change_mode` 设置手臂控制模式](#arm_traj_change_mode-设置手臂控制模式)
    - [功能描述](#功能描述-7)
    - [请求格式](#请求格式-2)
    - [响应格式](#响应格式-2)
    - [使用示例](#使用示例-7)
    - [`/kuavo_arm_target_poses` 手臂运动控制(指定时间内到达目标位置)](#kuavo_arm_target_poses-手臂运动控制指定时间内到达目标位置)
    - [功能描述](#功能描述-8)
    - [消息类型](#消息类型-5)
    - [消息字段](#消息字段-5)
    - [使用示例](#使用示例-8)
    - [`/kuavo_arm_traj` 手臂运动控制(用于自定义手臂运动轨迹规划)](#kuavo_arm_traj-手臂运动控制用于自定义手臂运动轨迹规划)
    - [功能描述](#功能描述-9)
    - [消息类型](#消息类型-6)
    - [消息字段](#消息字段-6)
    - [使用示例](#使用示例-9)
    - [`/robot_head_motion_data` 头部关节控制](#robot_head_motion_data-头部关节控制)
    - [功能描述](#功能描述-10)
    - [消息类型](#消息类型-7)
    - [消息字段](#消息字段-7)
    - [使用示例](#使用示例-10)
    - [`/control_end_hand` 灵巧手控制](#control_end_hand-灵巧手控制)
    - [功能描述](#功能描述-11)
    - [服务类型](#服务类型)
    - [请求消息](#请求消息)
    - [响应消息](#响应消息)
    - [使用示例](#使用示例-11)
    - [`/cmd_pose` 位置控制](#cmd_pose-位置控制)
    - [功能描述](#功能描述-12)
    - [消息类型](#消息类型-8)
    - [消息字段](#消息字段-8)
    - [使用示例](#使用示例-12)
    - [`/cmd_vel` 速度控制](#cmd_vel-速度控制)
    - [功能描述](#功能描述-13)
    - [消息类型](#消息类型-9)
    - [消息字段](#消息字段-9)
    - [使用示例](#使用示例-13)
    - [`/humanoid_controller/real_initial_start` 执行机器人站立](#humanoid_controllerreal_initial_start-执行机器人站立)
    - [功能描述](#功能描述-14)
    - [服务类型](#服务类型-1)
    - [请求消息](#请求消息-1)
    - [响应消息](#响应消息-1)
    - [使用示例](#使用示例-14)
    - [`/sensors_data_raw` 传感器数据](#sensors_data_raw-传感器数据)
    - [功能描述](#功能描述-15)
    - [消息类型](#消息类型-10)
    - [消息字段](#消息字段-10)
    - [关节数据说明](#关节数据说明)
    - [IMU 数据说明](#imu-数据说明)
    - [使用示例](#使用示例-15)


### `/play_music` 播放音频

### 功能描述

`/play_music` 服务用于控制机器人播放指定的音乐文件。用户可以通过提供音乐文件的名称或编号以及音量来实现音乐播放。

### 请求格式

- **类型**: `playmusicRequest`
- **字段**:
  - `music_number` (str): 音乐文件的名称或编号。可以是文件路径或预定义的音乐编号。
  - `volume` (int): 音乐的音量，范围通常为 0 到 100。

### 响应格式

- **类型**: `playmusicResponse`
- **字段**:
  - `success_flag` (bool): 表示音乐播放请求是否成功。`True` 表示成功，`False` 表示失败。

### 使用示例

```python
import rospy
from kuavo_sdk.srv import playmusic, playmusicRequest

# 初始化 ROS 节点
rospy.init_node('music_player_client')

# 创建服务代理
robot_music_play_client = rospy.ServiceProxy("/play_music", playmusic)

# 创建请求对象
request = playmusicRequest()
request.music_number = "/home/kuavo/你好"  # 音乐文件路径
request.volume = 80  # 音量

# 发送请求并接收响应
response = robot_music_play_client(request)
```
---

### `/record_music` 记录音频

### 功能描述

`/record_music` 服务用于控制机器人录制指定的音乐文件。用户可以通过提供音乐文件的编号以及超时时间来实现音乐录制。

### 请求格式

- **类型**: `recordmusicRequest`
- **字段**:
  - `music_number` (str): 音乐文件的编号。用于标识要录制的音乐文件。
  - `time_out` (int): 超时时间，以秒为单位。指定录制操作的最大持续时间。

### 响应格式

- **类型**: `recordmusicResponse`
- **字段**:
  - `success_flag` (bool): 表示音乐录制请求是否成功。`True` 表示成功，`False` 表示失败。

### 使用示例

```python
import rospy
from kuavo_sdk.srv import recordmusic, recordmusicRequest

# 初始化 ROS 节点
rospy.init_node('music_recorder')

# 创建服务代理
robot_record_music_client = rospy.ServiceProxy("/record_music", recordmusic)

# 创建请求对象
request = recordmusicRequest()
request.music_number = "example_music"  # 音乐文件编号
request.time_out = 30  # 超时时间

# 调用服务并获取响应
response = robot_record_music_client(request)
```
---

### `/livox/imu` 雷达imu数据
参考[雷达启动](../kuavo_sdk/sdk/02_use_lidar/readme.md)启动雷达节点
### 功能描述

`/livox/imu` 话题用于提供雷达内置 IMU（惯性测量单元）信息，包括线性加速度和角速度。

### 消息类型

- **类型**: `sensor_msgs/Imu`

### 消息字段

- **Header**: 消息头信息
  - `seq` (uint32): 序列号
  - `stamp` (time): 时间戳
  - `frame_id` (string): 坐标系 ID

- **orientation**: 方向四元数
  - `x`, `y`, `z`, `w` (float64): 四元数的分量

- **orientation_covariance**: 方向协方差矩阵 (float64[9])

- **angular_velocity**: 角速度
  - `x`, `y`, `z` (float64): 角速度的分量

- **angular_velocity_covariance**: 角速度协方差矩阵 (float64[9])

- **linear_acceleration**: 线性加速度
  - `x`, `y`, `z` (float64): 加速度的分量

- **linear_acceleration_covariance**: 加速度协方差矩阵 (float64[9])

### 使用示例

```python
import rospy
from sensor_msgs.msg import Imu

def imu_callback(data):
    rospy.loginfo("Received IMU data: %s", data)

rospy.init_node('imu_listener')
rospy.Subscriber("/livox/imu", Imu, imu_callback)
rospy.spin()
```
---

### `/livox/lidar` 雷达点云数据
参考[雷达启动](../kuavo_sdk/sdk/02_use_lidar/readme.md)启动雷达节点
### 功能描述

`/livox/lidar` 话题用于提供雷达的点云数据信息，用于三维空间的点云表示。

### 消息类型

- **类型**: `sensor_msgs/PointCloud2`

### 消息字段

- **Header**: 消息头信息
  - `seq` (uint32): 序列号
  - `stamp` (time): 时间戳
  - `frame_id` (string): 坐标系 ID

- **height** (uint32): 点云的高度（通常为 1）

- **width** (uint32): 点云的宽度（点的数量）

- **fields**: 点字段信息
  - `name` (string): 字段名称
  - `offset` (uint32): 字段偏移
  - `datatype` (uint8): 数据类型
  - `count` (uint32): 字段计数

- **is_bigendian** (bool): 是否为大端序

- **point_step** (uint32): 每个点的字节数

- **row_step** (uint32): 每行的字节数

- **data** (uint8[]): 点云数据

- **is_dense** (bool): 是否为密集点云

### 使用示例

```python
import rospy
from sensor_msgs.msg import PointCloud2

def lidar_callback(data):
    rospy.loginfo("Received LIDAR data: %s", data)

rospy.init_node('lidar_listener')
rospy.Subscriber("/livox/lidar", PointCloud2, lidar_callback)
rospy.spin()
```

---

### `/camera/depth/color/points` 相机点云数据

### 功能描述

`/camera/depth/color/points` 话题用于提供相机的点云数据，结合了深度信息和颜色信息，用于三维空间的点云表示。

### 消息类型

- **类型**: `sensor_msgs/PointCloud2`

### 消息字段

- **Header**: 消息头信息
  - `seq` (uint32): 序列号
  - `stamp` (time): 时间戳
  - `frame_id` (string): 坐标系 ID

- **height** (uint32): 点云的高度（通常为 1）

- **width** (uint32): 点云的宽度（点的数量）

- **fields**: 点字段信息
  - `name` (string): 字段名称
  - `offset` (uint32): 字段偏移
  - `datatype` (uint8): 数据类型
  - `count` (uint32): 字段计数

- **is_bigendian** (bool): 是否为大端序

- **point_step** (uint32): 每个点的字节数

- **row_step** (uint32): 每行的字节数

- **data** (uint8[]): 点云数据

- **is_dense** (bool): 是否为密集点云

### 使用示例

```python
import rospy
from sensor_msgs.msg import PointCloud2

def points_callback(data):
    rospy.loginfo("Received point cloud data")

rospy.init_node('points_listener')
rospy.Subscriber("/camera/depth/color/points", PointCloud2, points_callback)
rospy.spin()
```
---

### `/camera/color/image_raw` 相机彩色图像数据

### 功能描述

`/camera/color/image_raw` 话题用于提供相机的原始彩色图像数据。

### 消息类型

- **类型**: `sensor_msgs/Image`

### 消息字段

- **Header**: 消息头信息
  - `seq` (uint32): 序列号
  - `stamp` (time): 时间戳
  - `frame_id` (string): 坐标系 ID

- **height** (uint32): 图像高度

- **width** (uint32): 图像宽度

- **encoding** (string): 图像编码格式（如 `rgb8`）

- **is_bigendian** (uint8): 是否为大端序

- **step** (uint32): 每行的字节数

- **data** (uint8[]): 图像数据

### 使用示例

```python
import rospy
from sensor_msgs.msg import Image

def image_callback(data):
    rospy.loginfo("Received raw image data")

rospy.init_node('image_listener')
rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
rospy.spin()
```
---

### `/camera/depth/image_rect_raw` 相机深度图像数据

### 功能描述

`/camera/depth/image_rect_raw` 话题用于提供相机的深度图像数据，经过校正以消除畸变。

### 消息类型

- **类型**: `sensor_msgs/Image`

### 消息字段

- **Header**: 消息头信息
  - `seq` (uint32): 序列号
  - `stamp` (time): 时间戳
  - `frame_id` (string): 坐标系 ID

- **height** (uint32): 图像高度

- **width** (uint32): 图像宽度

- **encoding** (string): 图像编码格式（如 `16UC1`）

- **is_bigendian** (uint8): 是否为大端序

- **step** (uint32): 每行的字节数

- **data** (uint8[]): 图像数据

### 使用示例

```python
import rospy
from sensor_msgs.msg import Image

def depth_image_callback(data):
    rospy.loginfo("Received depth image data")

rospy.init_node('depth_image_listener')
rospy.Subscriber("/camera/depth/image_rect_raw", Image, depth_image_callback)
rospy.spin()
```
---

### `/arm_traj_change_mode` 设置手臂控制模式

### 功能描述

`/arm_traj_change_mode` 服务用于设置 OCS2 手臂的控制模式。用户可以通过提供控制模式编号来更改手臂的操作方式。

控制模式包括：
- `0`: 保持姿势（keep pose）
- `1`: 行走时自动摆手（auto_swing_arm）
- `2`: 外部控制（external_control）

### 请求格式

- **类型**: `changeArmCtrlModeRequest`

- **字段**:
  - `control_mode` (int): 要设置的控制模式编号。有效值为 0、1 或 2。

### 响应格式

- **类型**: `changeArmCtrlModeResponse`

- **字段**:
  - `result` (bool): 表示控制模式更改请求是否成功。`True` 表示成功，`False` 表示失败。
  - `message` (str): 包含关于操作结果的详细信息的消息。

### 使用示例

```python
import rospy
from kuavo_sdk.srv import changeArmCtrlMode, changeArmCtrlModeRequest, changeArmCtrlModeResponse

# 初始化 ROS 节点
rospy.init_node('arm_control_mode_client')

# 创建服务代理
arm_traj_change_mode_client = rospy.ServiceProxy("/arm_traj_change_mode", changeArmCtrlMode)

# 创建请求对象
request = changeArmCtrlModeRequest()
request.control_mode = 2  # 设置控制模式

# 调用服务并获取响应
response = arm_traj_change_mode_client(request)
```
---

### `/kuavo_arm_target_poses` 手臂运动控制(指定时间内到达目标位置)

### 功能描述

`/kuavo_arm_target_poses` 话题用于发布手臂的目标姿态信息，包括时间和关节角度。该话题可以用于控制手臂运动到指定的姿态。

### 消息类型

- **类型**: `kuavo_sdk/armTargetPoses`

### 消息字段

- **times** (list of float): 时间列表，表示每个姿态的目标时间点。
- **values** (list of float): 关节角度列表，表示手臂在每个时间点的目标关节角度。

### 使用示例

```python
import rospy
from kuavo_sdk.msg import armTargetPose

# 初始化ROS节点
rospy.init_node('arm_target_poses_publisher')

# 创建发布者
pub = rospy.Publisher('kuavo_arm_target_poses', armTargetPoses, queue_size=10)

# 创建消息对象
msg = armTargetPoses()
msg.times = [3]  # 时间列表
msg.values = [-20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0]  # 关节角度列表

# 发布消息
pub.publish(msg)
```
---

### `/kuavo_arm_traj` 手臂运动控制(用于自定义手臂运动轨迹规划)

### 功能描述

`/kuavo_arm_traj` 话题用于发布当前关节状态信息，包括关节名称和位置。该话题可以用于控制手臂的关节运动。

### 消息类型

- **类型**: `sensor_msgs/JointState`

### 消息字段

- **name** (list of string): 关节名称列表，假设有 14 个关节，名称为 `"arm_joint_1"` 到 `"arm_joint_14"`。
- **position** (list of float): 当前关节位置列表。
- **header.stamp** (time): 消息的时间戳，设置为当前时间。

### 使用示例

```python
import rospy
from sensor_msgs.msg import JointState
import numpy as np

# 初始化ROS节点
rospy.init_node('sim_traj')

# 创建发布者
pub = rospy.Publisher("/kuavo_arm_traj", JointState, queue_size=10)

# 创建消息对象
msg = JointState()
msg.name = ["arm_joint_" + str(i) for i in range(1, 15)]  # 关节名称列表
msg.header.stamp = rospy.Time.now()  # 当前时间戳
msg.position = np.array([-30, 60, 0, -30, 0, -30, 30, 0, 0, 0, 0, 0, 0, 0])  # 关节位置列表

# 发布消息
pub.publish(msg)
```

---

### `/robot_head_motion_data` 头部关节控制

### 功能描述

`/robot_head_motion_data` 话题用于发布机器人头部的目标运动数据，包括偏航角和俯仰角。该话题可以用于控制机器人的头部运动。

### 消息类型

- **类型**: `kuavo_sdk/robotHeadMotionData`

### 消息字段

- **joint_data** (list of float): 包含头部偏航角和俯仰角的列表。偏航角范围为 [-30, 30] 度，俯仰角范围为 [-25, 25] 度。

### 使用示例

```python
import rospy
from kuavo_sdk.msg import robotHeadMotionData

# 初始化ROS节点
rospy.init_node('robot_head_controller')

# 创建发布者
pub_head_pose = rospy.Publisher('/robot_head_motion_data', robotHeadMotionData, queue_size=10)

# 创建消息对象
head_target_msg = robotHeadMotionData()
head_target_msg.joint_data = [0, 0]  # 偏航角和俯仰角

# 发布消息
pub_head_pose.publish(head_target_msg)
```
---

### `/control_end_hand` 灵巧手控制

### 功能描述

`/control_end_hand` 服务用于控制机器人手部动作，设置左手和右手的目标位置。

### 服务类型

- **类型**: `kuavo_sdk/controlEndHand`

### 请求消息

- **left_hand_position** (list of float):  左手位置，包含6个元素。
- **right_hand_position** (list of float): 右手位置，包含6个元素。

### 响应消息

- **result** (bool): 服务调用结果，成功返回 `True`，失败返回 `False`。

### 使用示例

```python
import rospy
from kuavo_sdk.srv import controlEndHand, controlEndHandRequest

# 初始化ROS节点
rospy.init_node('robot_hand_controller')

# 初始化服务代理
robot_control_hand_client = rospy.ServiceProxy("/control_end_hand", controlEndHand)

# 创建请求对象
request = controlEndHandRequest()
request.left_hand_position = [0, 0, 0, 0, 0, 0]  # 左手位置
request.right_hand_position = [20, 20, 20, 20, 20, 20]  # 右手位置

# 调用服务
response = robot_control_hand_client(request)
```
---


### `/cmd_pose` 位置控制

### 功能描述

`/cmd_pose` 话题用于发布控制指令，指定机器人在空间中的线速度和角速度。

### 消息类型

- **类型**: `geometry_msgs/Twist`

### 消息字段

- **linear.x** (float): 基于当前位置的 x 方向线速度 (m/s)。
- **linear.y** (float): 基于当前位置的 y 方向线速度 (m/s)。
- **linear.z** (float): 增量高度 (m)。
- **angular.x** (float): 未使用，设置为 0。
- **angular.y** (float): 未使用，设置为 0。
- **angular.z** (float): yaw 方向角速度 (radian/s)。

### 使用示例

```python
import rospy
from geometry_msgs.msg import Twist

# 初始化ROS节点
rospy.init_node('cmd_pose_publisher')

# 创建发布者
cmd_pose_pub = rospy.Publisher('/cmd_pose', Twist, queue_size=10)

# 创建Twist消息对象
cmd_pose_msg = Twist()
cmd_pose_msg.linear.x = 0.5  # x 方向线速度
cmd_pose_msg.linear.y = 0.0  # y 方向线速度
cmd_pose_msg.linear.z = 0.0  # 增量高度
cmd_pose_msg.angular.z = 0.0  # yaw 方向角速度

# 发布消息
cmd_pose_pub.publish(cmd_pose_msg)
```
---

### `/cmd_vel` 速度控制

### 功能描述

`/cmd_vel` 话题用于发布控制指令，指定机器人在空间中的线速度和角速度

### 消息类型

- **类型**: `geometry_msgs/Twist`

### 消息字段

- **linear.x** (float): x 方向线速度 (m/s)。
- **linear.y** (float): y 方向线速度 (m/s)。
- **linear.z** (float): 增量高度 (m)。
- **angular.x** (float): 未使用，设置为 0。
- **angular.y** (float): 未使用，设置为 0。
- **angular.z** (float): yaw 方向角速度 (radian/s)。

### 使用示例

```python
import rospy
from geometry_msgs.msg import Twist

# 初始化ROS节点
rospy.init_node('cmd_vel_publisher')

# 创建发布者
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# 设置发布频率
rate = rospy.Rate(10)  # 10 Hz

# 创建Twist消息对象
cmd_vel_msg = Twist()
cmd_vel_msg.linear.x = 0.2  # x 方向速度
cmd_vel_msg.linear.y = 0.0  # y 方向速度
cmd_vel_msg.linear.z = 0.0  # 增量高度
cmd_vel_msg.angular.z = 0.0  # yaw 方向角速度

while not rospy.is_shutdown():
    # 发布消息
    cmd_vel_pub.publish(cmd_vel_msg)
    # 等待下一个发布周期
    rate.sleep()
```

---

### `/humanoid_controller/real_initial_start` 执行机器人站立

### 功能描述

`/humanoid_controller/real_initial_start` 服务用于触发机器人的初始化过程：机器人cali状态执行一次机器人缩腿，再执行一次机器人站立，用户需要在站立过程中用手扶住机器人以确保安全，实机才有该服务

### 服务类型

- **类型**: `std_srvs/Trigger`

### 请求消息

- 无需请求参数。

### 响应消息

- **success** (bool): 服务调用结果，成功返回 `True`，失败返回 `False`。
- **message** (string): 服务调用的响应消息，提供成功或失败的详细信息。

### 使用示例

```python
import rospy
from std_srvs.srv import Trigger

# 初始化ROS节点
rospy.init_node('init_trigger_service_caller')

# 创建服务代理
trigger_init_service = rospy.ServiceProxy('/humanoid_controller/real_initial_start', Trigger)

# 调用服务并获取响应
response = trigger_init_service()
```
---

### `/sensors_data_raw` 传感器数据

### 功能描述

`/sensors_data_raw` 话题用于发布实物机器人或仿真器的传感器原始数据，包括关节数据、IMU数据和末端执行器数据。

### 消息类型

- **类型**: `kuavo_sdk/sensorsData`

### 消息字段

| 字段               | 类型                        | 描述                              |
| ----------------- | -------------------------- | ------------------------------- |
| sensor_time       | time                       | 时间戳                           |
| joint_data        | kuavo_msgs/jointData       | 关节数据: 位置、速度、加速度、电流 |
| imu_data          | kuavo_msgs/imuData         | 包含陀螺仪、加速度计、自由加速度、四元数 |
| end_effector_data | kuavo_msgs/endEffectorData | 末端数据，暂未使用                |

### 关节数据说明

- **数组长度**: `NUM_JOINT`
- **数据顺序**:
  - 前 12 个数据为下肢电机数据:
    - 0~5 为左下肢数据 (l_leg_roll, l_leg_yaw, l_leg_pitch, l_knee, l_foot_pitch, l_foot_roll)
    - 6~11 为右下肢数据 (r_leg_roll, r_leg_yaw, r_leg_pitch, r_knee, r_foot_pitch, r_foot_roll)
  - 接着 14 个数据为手臂电机数据:
    - 12~18 左臂电机数据 ("l_arm_pitch", "l_arm_roll", "l_arm_yaw", "l_forearm_pitch", "l_hand_yaw", "l_hand_pitch", "l_hand_roll")
    - 19~25 为右臂电机数据 ("r_arm_pitch", "r_arm_roll", "r_arm_yaw", "r_forearm_pitch", "r_hand_yaw", "r_hand_pitch", "r_hand_roll")
  - 最后 2 个为头部电机数据: head_yaw 和 head_pitch

- **单位**:
  - 位置: 弧度 (radian)
  - 速度: 弧度每秒 (radian/s)
  - 加速度: 弧度每平方秒 (radian/s²)
  - 电流: 安培 (A)

### IMU 数据说明

- **gyro**: 陀螺仪的角速度，单位弧度每秒（rad/s）
- **acc**: 加速度计的加速度，单位米每平方秒（m/s²）
- **quat**: IMU的姿态（orientation）

---

### 使用示例

```python
import rospy
from kuavo_sdk.msg import sensorsData

def callback(data):
    rospy.loginfo(f"Received sensor data at time: {data.sensor_time}")

# 初始化ROS节点
rospy.init_node('sensor_data_listener')

# 订阅传感器数据话题
rospy.Subscriber('/sensors_data_raw', sensorsData, callback)

# 保持节点运行
rospy.spin()
```

---