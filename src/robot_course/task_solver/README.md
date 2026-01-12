# Task Solver - 基于YOLOv8的物品3D检测与抓取

使用YOLOv8进行物品检测，结合深度相机和TF变换计算物体3D位置，并控制机械臂完成抓取任务。

## 功能

- **YOLOv8物品检测**：实时检测杯子、盘子、剪刀
- **3D位置计算**：结合深度图计算物体在base_link和odom坐标系下的位置
- **物体追踪**：基于odom坐标系的稳定ID追踪，机器人移动后ID不变
- **位置滤波**：滑动窗口平均滤波减少抖动
- **桌面高度过滤**：根据odom坐标系z值过滤非桌面物体
- **智能抓取**：支持侧面抓取(杯子)和顶部抓取(盘子/剪刀)两种姿态
- **ROS服务接口**：提供抓取/放置服务，支持外部程序调用
- **仿真/实机兼容**：仿真使用吸附服务，实机使用手指控制
- **AprilTag定位**：基于AprilTag二维码定位物品和放置点
- **闭环运动控制**：基于odom的三阶段移动（转向→行走→调整朝向）
- **完整课程流程**：整合抓取放置和搬箱子任务
- **RViz可视化**：MarkerArray显示检测结果和物体ID

## 快速开始

### 1. 依赖安装

```bash
pip install ultralytics scipy
```

### 2. 编译

```bash
cd ~/kuavo_ws
catkin build task_solver
source devel/setup.bash
```

### 3. 启动系统

```bash
# 1. 启动Gazebo场景
roslaunch gazebo_sim gazebo_course_task.launch random_seed:=110

# 2. 启动检测和抓取服务
roslaunch task_solver task_grasp.launch
```

### 4. 调用抓取服务

```bash
# 抓取杯子（只抓取不释放）
rosservice call /grasp_controller/grasp "target_class: 'cup'
track_id: -1
grasp_only: true
hand: 'right'"

# 放置物体
rosservice call /grasp_controller/place "hand: ''"
```

---

## 完整课程解决方案 (full_course_solver.py)

整合抓取放置和搬箱子两个任务的完整流程。

### 流程

```
阶段0 (可选): 导航到识别点 (move_base)
    ↓
阶段1: 抓取放置任务 (grasp_demo.py)
    ├─ 检测AprilTag定位物品
    ├─ 移动到物品前方
    ├─ 抓取物品
    ├─ 移动到放置点
    ├─ 放置物品
    └─ 后退并复位手臂
    ↓
阶段2: 搬箱子任务 (grasp_box_course_solver.py)
    ├─ 检测AprilTag定位箱子
    ├─ 移动到箱子前方
    ├─ 双手抓取箱子
    ├─ 搬运到目标位置
    └─ 放下箱子
```

### 基本用法

```bash
# 运行完整流程（抓取放置 + 搬箱子）
rosrun task_solver full_course_solver.py

# 仿真模式
rosrun task_solver full_course_solver.py --sim

# 跳过抓取任务，只运行搬箱子
rosrun task_solver full_course_solver.py --skip_grasp

# 跳过搬箱子任务，只运行抓取放置
rosrun task_solver full_course_solver.py --skip_box

# 先导航到识别点再开始任务
rosrun task_solver full_course_solver.py --nav_to_start \
    --nav_x 1.0 --nav_y 2.0 --nav_z 0.707 --nav_w 0.707
```

### 完整参数示例

```bash
rosrun task_solver full_course_solver.py \
    --nav_to_start --nav_x 1.0 --nav_y 2.0 --nav_z 0.0 --nav_w 1.0 \
    --grasp_tag_id 0 \
    --lateral_offset 0.75 \
    --grasp_offset 0.15 \
    --place_lateral_offset -0.50 \
    --place_offset 0.32 \
    --backward_distance 1.0
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| **通用参数** | | |
| `--sim` | false | 仿真模式 |
| `--skip_grasp` | false | 跳过抓取放置任务 |
| `--skip_box` | false | 跳过搬箱子任务 |
| `--wait_between` | 3.0 | 任务之间等待时间(秒) |
| **导航参数** | | |
| `--nav_to_start` | false | 启用导航到识别点 |
| `--nav_x` | 0.0 | 识别点X坐标 |
| `--nav_y` | 0.0 | 识别点Y坐标 |
| `--nav_z` | 0.0 | 朝向四元数z分量 |
| `--nav_w` | 1.0 | 朝向四元数w分量 |
| **抓取放置参数** | | |
| `--target` | cup | 抓取目标 |
| `--grasp_tag_id` | 0 | AprilTag ID |
| `--lateral_offset` | 0.75 | 物品横向偏移(正=右) |
| `--forward_offset` | 0.0 | 物品前向偏移 |
| `--grasp_offset` | 0.15 | 抓取距离 |
| `--place_offset` | 0.32 | 放置距离 |
| `--place_lateral_offset` | -0.50 | 放置点横向偏移 |
| `--backward_distance` | 1.0 | 放置后后退距离 |
| `--grasp_hand` | right | 抓取用手 |
| `--lateral` | false | 使用左右平移 |
| `--speed` | 0.1 | 移动速度(m/s) |
| `--tolerance` | 0.1 | 位置精度(m) |
| **搬箱子参数** | | |
| `--velocity_turn` | true | 使用速度控制转向(默认启用) |
| `--no_velocity_turn` | false | 禁用速度控制转向 |
| `--max_yaw_step` | None | 单步最大转向角度 |

---

## 抓取演示程序 (grasp_demo.py)

提供完整的导航+抓取+放置流程演示，支持多种定位方式。

### 定位方式

1. **AprilTag定位**（推荐）：基于AprilTag二维码定位物品位置
2. **YOLO检测定位**：基于3D检测结果定位
3. **固定坐标**：使用预设的固定坐标

### AprilTag定位模式（推荐）

```bash
# 基本用法
rosrun task_solver grasp_demo.py --use_apriltag --tag_id 0

# 完整参数
rosrun task_solver grasp_demo.py --use_apriltag --tag_id 0 \
    --lateral_offset 0.75 \
    --grasp_offset 0.15 \
    --place_lateral_offset -0.50 \
    --place_offset 0.32 \
    --backward_distance 1.0
```

### AprilTag偏移量说明

```
                    AprilTag
                       │
    ←── lateral_offset ──→
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    物品位置      AprilTag位置    放置位置
  (lateral>0)                  (lateral<0)
         │             │             │
         └─────────────┼─────────────┘
                       │
                       ↓ forward_offset
                       │
                    机器人
                  (grasp_offset)
```

- `lateral_offset`: 物品相对AprilTag的横向偏移（正=机器人右边，负=左边）
- `forward_offset`: 物品相对AprilTag的前向偏移
- `grasp_offset`: 机器人停在物品前方的距离
- `place_lateral_offset`: 放置点相对AprilTag的横向偏移
- `place_offset`: 机器人停在放置点前方的距离
- `backward_distance`: 放置后后退距离

### YOLO检测定位模式

```bash
rosrun task_solver grasp_demo.py --use_detection --target cup --grasp_offset 0.5
```

### 固定坐标模式

```bash
rosrun task_solver grasp_demo.py --position_mode gazebo \
    --grasp_x -0.28 --grasp_y -4.4 \
    --place_x 0.88 --place_y -4.35
```

### 运行模式

| 模式 | 说明 |
|------|------|
| `--mode auto` | 自动导航+抓取+放置（默认） |
| `--mode manual` | 等待机器人到达位置后触发 |
| `--mode grasp` | 只在当前位置抓取 |
| `--mode place` | 只在当前位置放置 |

### 移动方式

```bash
# 转向+前进（默认，三阶段控制）
rosrun task_solver grasp_demo.py --use_apriltag --tag_id 0

# 左右平移（全向移动，保持朝向不变）
rosrun task_solver grasp_demo.py --use_apriltag --tag_id 0 --lateral
```

### 三阶段移动控制

```
阶段1: 转向目标方向
    └─ 原地旋转直到面向目标点
    └─ 角度误差 < 0.1 rad (≈5.7°)
    ↓
阶段2: 直线行走到目标位置
    └─ 边走边微调方向
    └─ 位置误差 < 0.1m
    ↓
阶段3: 调整最终朝向
    └─ 原地旋转到目标朝向
    └─ 角度误差 < 0.1 rad
```

### 完整参数列表

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--mode` | auto | 运行模式 |
| `--position_mode` | gazebo | 位置判断：odom/gazebo |
| `--target` | cup | 抓取目标 |
| `--grasp_hand` | right | 抓取用手：left/right/auto |
| `--lateral` | false | 使用左右平移 |
| `--speed` | 0.1 | 移动速度(m/s) |
| `--tolerance` | 0.1 | 位置精度(m) |
| **AprilTag参数** | | |
| `--use_apriltag` | false | 启用AprilTag定位 |
| `--tag_id` | 0 | AprilTag ID |
| `--lateral_offset` | 0.75 | 物品横向偏移(m) |
| `--forward_offset` | 0.0 | 物品前向偏移(m) |
| `--grasp_offset` | 0.15 | 抓取距离(m) |
| `--place_offset` | 0.32 | 放置距离(m) |
| `--place_lateral_offset` | -0.50 | 放置点横向偏移(m) |
| `--backward_distance` | 1.0 | 后退距离(m) |
| **YOLO检测参数** | | |
| `--use_detection` | false | 启用YOLO检测定位 |
| **固定坐标参数** | | |
| `--grasp_x/y` | -0.28, -4.4 | 抓取位置 |
| `--place_x/y` | 0.88, -4.35 | 放置位置 |
| `--robot_model` | biped_s42 | Gazebo模型名称 |

---

## 抓取服务接口

launch文件启动后，`grasp_controller` 以服务模式运行，提供以下服务：

### /grasp_controller/grasp

抓取物体服务。

**请求参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `target_class` | string | 目标类别：cup/plate/scissors |
| `track_id` | int32 | 指定track_id抓取，-1表示自动选择最近的 |
| `grasp_only` | bool | true: 只抓取不释放，false: 抓取后释放 |
| `hand` | string | 指定使用的手：left/right/auto |

**返回：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否成功 |
| `message` | string | 结果信息 |
| `grasped_track_id` | int32 | 抓取的物体track_id |
| `grasped_hand` | string | 使用的手：left/right |

### /grasp_controller/place

放置物体服务。

**请求参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `hand` | string | 使用的手：left/right，空字符串表示自动 |
| `reset_arm` | bool | 是否复位手臂，false时只释放物体不复位 |

**返回：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否成功 |
| `message` | string | 结果信息 |

### /grasp_controller/reset_arm

手臂复位服务（放置后后退再调用）。

**请求参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `hand` | string | 使用的手：left/right |

**返回：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否成功 |
| `message` | string | 结果信息 |

### 服务调用示例

```bash
# 按类别抓取最近的杯子（右手）
rosservice call /grasp_controller/grasp "target_class: 'cup'
track_id: -1
grasp_only: true
hand: 'right'"

# 按track_id抓取指定物体
rosservice call /grasp_controller/grasp "target_class: ''
track_id: 3
grasp_only: true
hand: 'auto'"

# 放置物体（不复位手臂）
rosservice call /grasp_controller/place "hand: 'right'
reset_arm: false"

# 复位手臂
rosservice call /grasp_controller/reset_arm "hand: 'right'"
```

---

## 抓取演示程序 (grasp_demo.py) - 命令行模式

除了上面详细介绍的AprilTag模式，还支持以下简单用法：

### 运行模式

```bash
# 自动模式：导航到抓取区 -> 抓取 -> 导航到放置区 -> 放置
rosrun task_solver grasp_demo.py --mode auto --target cup

# 使用Gazebo真实位置 + 左右平移
rosrun task_solver grasp_demo.py --mode auto --position_mode gazebo --lateral --target cup

# 自定义抓取/放置位置
rosrun task_solver grasp_demo.py --mode auto --position_mode gazebo --lateral \
    --grasp_x -0.28 --grasp_y -4.4 \
    --place_x -0.88 --place_y -4.4 \
    --target cup

# 手动模式：等待机器人到达指定位置后触发抓取/放置
rosrun task_solver grasp_demo.py --mode manual --target cup

# 只抓取（在当前位置）
rosrun task_solver grasp_demo.py --mode grasp --target cup

# 只放置
rosrun task_solver grasp_demo.py --mode place --hand right
```

---

## 命令行抓取（独立运行）

如果不使用服务模式，可以直接运行抓取控制器：

```bash
# 仿真模式 - 抓取最近的杯子
rosrun task_solver grasp_controller.py --sim --target cup

# 仿真模式 - 抓取所有杯子
rosrun task_solver grasp_controller.py --sim --target cup --grasp_all_same

# 实机模式 - 启用偏移量补偿
rosrun task_solver grasp_controller.py --target cup --use_offset

# 服务模式 - 只启动服务等待调用
rosrun task_solver grasp_controller.py --sim --service
```

### 命令参数

| 参数 | 说明 |
|------|------|
| `--sim` | 仿真模式，使用Gazebo吸附服务 |
| `--service` | 服务模式，只启动服务等待调用 |
| `--use_offset` | 启用偏移量补偿（实机使用） |
| `--target` | 抓取目标：cup/plate/scissors/all |
| `--track_id` | 按物体ID抓取指定目标 |
| `--index` | 按序号抓取（0=最近，1=次近...） |
| `--grasp_all_same` | 抓取所有相同类别的物体 |
| `--list` | 列出当前检测到的所有目标 |

### 抓取姿态

| 物品 | 抓取类型 | 说明 |
|------|----------|------|
| cup | 侧面抓取 | 手掌朝侧面，类似抓水瓶 |
| plate | 顶部抓取 | 手掌朝下，从上方抓取 |
| scissors | 顶部抓取 | 手掌朝下，从上方抓取 |

## 抓取/放置动作流程

### grasp_only 抓取流程（服务调用 grasp_only=true）

```
1. 低头检测目标 (head pitch=20)
   ↓
2. 获取目标位置，判断左右手 (y>0用左手)
   ↓
3. 设置手臂外部控制模式 (mode=2)
   ↓
4. IK逆解计算关节角度
   ↓
5. 执行抓取动作序列：
   ├─ 阶段1: 初始位置 [20, 0, 0, -30, ...]
   ├─ 阶段2: 侧抬准备 [20, ±90, 0, -30, ...] + 张开手
   ├─ 阶段3: 弯肘中间 [20, ±90, 0, -110, ...]
   ├─ 阶段4: IK目标位置
   ├─ 阶段5: 抓取 (仿真吸附/实机闭合手指)
   └─ 阶段6: 抬起到搬运位置 [20, ±90, 0, -110, ...]
   ↓
6. 抬头复位，保持外部控制模式
   ↓
7. 返回成功，物体保持在手中
```

### place_only 放置流程（服务调用）

```
1. 设置手臂外部控制模式 (mode=2)
   ↓
2. 从搬运位置开始：
   ├─ 阶段1: 侧抬 [20, ±90, 0, -110, ...]
   ├─ 阶段2: 伸出放置 [-60, 0, 0, -30, ...]
   ├─ 阶段3: 释放 (仿真解除吸附/实机张开手)
   ├─ 阶段4: 复位动作 (_arm_reset)
   └─ 阶段5: 回到初始位置 [6, 0, 0, -20, ...]
   ↓
3. 切换回自动摆手模式 (mode=1)
   ↓
4. 返回成功
```

### 手臂关节角度说明

7个关节角度 (度)：
- `[0]` 肩部前后摆动 (pitch)
- `[1]` 肩部侧向抬起 (roll)，左手正值/右手负值
- `[2]` 肩部旋转
- `[3]` 肘部弯曲，负值弯曲
- `[4-6]` 手腕关节

关键姿态：
| 姿态 | 左手角度 | 右手角度 | 说明 |
|------|----------|----------|------|
| 初始位置 | [20, 0, 0, -30, 0, 0, 0] | 同左 | 自然下垂 |
| 侧抬准备 | [20, 90, 0, -30, ...] | [20, -90, 0, -30, ...] | 手臂侧抬90度 |
| 弯肘中间 | [20, 90, 0, -110, ...] | [20, -90, 0, -110, ...] | 搬运姿态 |
| 放置伸出 | [-60, 0, 0, -30, ...] | 同左 | 手臂向前伸出 |

## 物体追踪

检测节点为每个物体分配稳定的 `track_id`：

- 使用odom坐标系进行追踪匹配，机器人移动后ID保持稳定
- 物体短暂消失（<30秒）后再次出现，如果位置接近会恢复原ID
- 同类物体按距离排序，`class_index=0` 表示最近的

### 3D检测结果格式

```json
{
  "class_name": "cup",
  "confidence": 0.85,
  "position": {"x": 0.5, "y": 0.1, "z": 0.8},
  "distance": 0.52,
  "track_id": 0,
  "class_index": 0,
  "depth_mm": 520.0,
  "bbox": [280, 180, 360, 300]
}
```

## 查看结果

```bash
# 查看3D检测结果（包含track_id）
rostopic echo /yolo/detections_3d

# RViz可视化（显示 cup#0 [ID:0] 格式）
rviz  # 添加MarkerArray，话题选择 /yolo/markers

# 图像可视化
rqt_image_view /yolo/detection_image

# 动态调参
rosrun rqt_reconfigure rqt_reconfigure
```

## 启动参数

**task_grasp.launch**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `yolo_model` | models/best.pt | YOLO模型路径 |
| `confidence_threshold` | 0.5 | 检测置信度阈值 |
| `window_size` | 5 | 滑动窗口大小(帧数) |
| `table_height` | 0.8 | 桌面高度(m) |
| `table_height_tolerance` | 0.15 | 高度容差(m) |

```bash
# 示例
roslaunch task_solver task_grasp.launch table_height:=0.75 window_size:=10
```

## 话题

| 话题 | 类型 | 说明 |
|------|------|------|
| `/yolo/detections` | String | 2D检测结果(JSON) |
| `/yolo/detections_3d` | String | base_link坐标系3D位置(JSON) |
| `/yolo/detections_3d_odom` | String | odom坐标系3D位置(JSON) |
| `/yolo/markers` | MarkerArray | base_link坐标系RViz标记 |
| `/yolo/markers_odom` | MarkerArray | odom坐标系RViz标记 |
| `/yolo/detection_image` | Image | 带标注的检测图像 |

## 训练自定义模型

### 1. 采集数据

```bash
rosrun task_solver collect_dataset.py _auto_mode:=true _save_interval:=2.0
```

### 2. 标注数据

推荐使用 [Roboflow](https://roboflow.com/) 在线标注，导出YOLOv8格式。

### 3. 训练

```bash
rosrun task_solver train_yolo.py --data /path/to/data.yaml --epochs 100
```

### 4. 使用模型

```bash
roslaunch task_solver task_grasp.launch yolo_model:=/path/to/best.pt
```

## 文件结构

```
task_solver/
├── scripts/
│   ├── yolo_detector.py        # YOLO检测节点
│   ├── detection_3d.py         # 3D位置计算+物体追踪
│   ├── grasp_controller.py     # 抓取控制器（支持服务模式）
│   ├── grasp_demo.py           # 抓取放置演示程序
│   ├── full_course_solver.py   # 完整课程解决方案
│   ├── test_position_compare.py  # 位置精度测试工具
│   ├── collect_dataset.py      # 数据采集工具
│   └── train_yolo.py           # 模型训练脚本
├── launch/
│   └── task_grasp.launch       # 启动文件（含抓取服务）
├── srv/
│   ├── GraspObject.srv         # 抓取服务定义
│   ├── PlaceObject.srv         # 放置服务定义
│   └── ResetArm.srv            # 手臂复位服务定义
├── models/
│   └── best.pt                 # 训练好的YOLO模型
├── cfg/
│   └── GraspController.cfg     # 动态参数配置
└── dataset/                    # 训练数据集
```

## 系统架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  yolo_detector  │────▶│  detection_3d   │────▶│grasp_controller │
│   (YOLO检测)    │     │  (3D位置计算)   │     │   (抓取服务)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
  /yolo/detections      /yolo/detections_3d    /grasp_controller/grasp
  /yolo/detection_image /yolo/markers          /grasp_controller/place
                        /yolo/detections_3d_odom /grasp_controller/reset_arm
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   grasp_demo    │
                                               │  (演示程序)     │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │full_course_solver│
                                               │  (完整流程)     │
                                               └─────────────────┘
                                                        │
                                        ┌───────────────┴───────────────┐
                                        ▼                               ▼
                               抓取放置任务                      搬箱子任务
                             (grasp_demo.py)           (grasp_box_course_solver.py)
```

### 典型使用流程

```bash
# 终端1: 启动Gazebo仿真
roslaunch gazebo_sim gazebo_course_task.launch random_seed:=110

# 终端2: 启动检测和抓取服务
roslaunch task_solver task_grasp.launch

# 终端3: 运行完整课程流程
rosrun task_solver full_course_solver.py

# 或者只运行抓取放置演示
rosrun task_solver grasp_demo.py --use_apriltag --tag_id 0
```

### 抓取放置流程图

```
grasp_demo.py                    grasp_controller.py
     │                                  │
     │  GraspObject(cup, hand=right, grasp_only=true)
     │─────────────────────────────────▶│
     │                                  │ grasp_only()
     │                                  │ ├─ 低头检测
     │                                  │ ├─ IK求解
     │                                  │ ├─ 执行抓取
     │                                  │ └─ 抬起到搬运位置
     │◀─────────────────────────────────│
     │  success, track_id, hand         │
     │                                  │
     │  (机器人移动到放置区)            │
     │                                  │
     │  PlaceObject(hand, reset_arm=false)
     │─────────────────────────────────▶│
     │                                  │ place_only()
     │                                  │ ├─ 伸出手臂
     │                                  │ └─ 释放物体
     │◀─────────────────────────────────│
     │  success                         │
     │                                  │
     │  (机器人后退1m)                  │
     │                                  │
     │  ResetArm(hand)                  │
     │─────────────────────────────────▶│
     │                                  │ reset_arm()
     │                                  │ └─ 复位手臂
     │◀─────────────────────────────────│
     │  success                         │
```

## 参考

- [YOLOv8文档](https://docs.ultralytics.com/)
- [Gazebo Link Attacher](../gazebo_ros_link_attacher/README.md)
