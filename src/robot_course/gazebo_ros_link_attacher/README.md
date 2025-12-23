# Gazebo ROS Link Attacher

Gazebo插件，用于在仿真中动态连接/分离两个模型的链接，实现机器人抓取功能。

## 功能

- **attach/detach服务**：连接或分离任意两个模型的链接（通用吸附）
- **grasp服务**：机器人手臂抓取/释放物品，自动检测距离范围内的可抓取物品
- **独立的距离限制**：attach服务和grasp服务使用各自独立的距离参数
- **配置文件**：通过YAML文件配置机器人、手臂链接和可抓取物品列表

## 编译

```bash
catkin build gazebo_ros_link_attacher
```

## 使用方法

### 快速开始

如果使用 `gazebo_course_task.launch`，所有配置已经就绪，直接启动即可：

```bash
# 1. 启动仿真（已包含插件和配置加载）
roslaunch gazebo_sim gazebo_course_task.launch

# 2. 调用抓取服务
rosrun gazebo_ros_link_attacher grasp_client.py right grasp
```

### 完整配置步骤

如果需要在其他仿真环境中使用，按以下步骤配置：

#### 步骤1：在Gazebo world文件中加载插件

在 `.world` 文件的 `<world>` 标签内添加：

```xml
<plugin name="link_attacher_plugin" filename="libgazebo_ros_link_attacher.so">
  <min_attach_distance>0.0</min_attach_distance>
  <max_attach_distance>0.25</max_attach_distance>
</plugin>
```

示例位置：`src/gazebo/gazebo-sim/worlds/course_task.world`

#### 步骤2：在launch文件中加载grasp配置参数

在 `.launch` 文件中添加：

```xml
<!-- 加载抓取服务配置参数 -->
<rosparam file="$(find gazebo_ros_link_attacher)/config/grasp_config.yaml" command="load"/>
```

示例位置：`src/gazebo/gazebo-sim/launch/gazebo_course_task.launch`

#### 步骤3：配置可抓取物品列表

编辑 `config/grasp_config.yaml`，添加需要抓取的物品：

```yaml
robot_model_name: "biped_s42"  # 修改为你的机器人模型名

graspable_objects:
  your_object_name:        # Gazebo中的模型名
    link_name: "link"      # 该模型的link名称
```

#### 步骤4：启动仿真并调用服务

```bash
# 启动仿真
roslaunch your_package your_launch_file.launch

# 使用grasp服务抓取（推荐）
rosrun gazebo_ros_link_attacher grasp_client.py right grasp

# 或使用attach服务直接指定模型
rosservice call /link_attacher_node/attach "model_name_1: 'biped_s42'
link_name_1: 'zarm_r7_link'
model_name_2: 'cup1'
link_name_2: 'link'"
```

### 查看物品的link名称

如果不确定物品的link名称，可以通过以下方式查看：

```bash
# 查看Gazebo中所有模型
gz model --list

# 查看指定模型的link
gz model --info -m cup1
```

或查看物品的URDF/SDF文件。

## 服务接口

### 1. attach/detach 服务

直接指定两个模型和链接进行连接/分离，距离限制由world文件中的SDF参数控制：

```bash
# 连接
rosservice call /link_attacher_node/attach "model_name_1: 'biped_s42'
link_name_1: 'zarm_r7_link'
model_name_2: 'cup1'
link_name_2: 'link'"

# 分离
rosservice call /link_attacher_node/detach "model_name_1: 'biped_s42'
link_name_1: 'zarm_r7_link'
model_name_2: 'cup1'
link_name_2: 'link'"
```

### 2. grasp 服务（推荐用于机器人抓取）

通过指定手臂和动作，自动查找并抓取距离范围内的物品：

```bash
# 左手抓取
rosservice call /kuavo_attacher_node/grasp "arm: 'left'
action: 'grasp'"

# 右手抓取
rosservice call /kuavo_attacher_node/grasp "arm: 'right'
action: 'grasp'"

# 左手释放
rosservice call /kuavo_attacher_node/grasp "arm: 'left'
action: 'release'"

# 右手释放
rosservice call /kuavo_attacher_node/grasp "arm: 'right'
action: 'release'"
```

或使用客户端脚本：

```bash
rosrun gazebo_ros_link_attacher grasp_client.py left grasp
rosrun gazebo_ros_link_attacher grasp_client.py right grasp
rosrun gazebo_ros_link_attacher grasp_client.py left release
rosrun gazebo_ros_link_attacher grasp_client.py right release
```

## 距离限制配置

两个服务使用独立的距离限制参数：

### attach/detach 服务距离限制

在Gazebo world文件的插件配置中设置：

```xml
<plugin name="link_attacher_plugin" filename="libgazebo_ros_link_attacher.so">
  <min_attach_distance>0.0</min_attach_distance>
  <max_attach_distance>0.25</max_attach_distance>
</plugin>
```

### grasp 服务距离限制

在 `config/grasp_config.yaml` 中设置：

```yaml
# 抓取距离限制 (米)
min_grasp_distance: 0.0   # 最小抓取距离
max_grasp_distance: 0.25  # 最大抓取距离
```

## 配置文件说明

配置文件位于 `config/grasp_config.yaml`：

```yaml
# 机器人模型名称 (Gazebo中spawn时指定的模型名)
robot_model_name: "biped_s42"

# 手臂链接配置 (机器人URDF中的link名称)
arm_links:
  left:
    link_name: "zarm_l7_link"   # 左手末端link
  right:
    link_name: "zarm_r7_link"   # 右手末端link

# 抓取距离限制 (米)
min_grasp_distance: 0.0   # 太近不抓取
max_grasp_distance: 0.25  # 太远不抓取

# 可抓取物品列表
# key: Gazebo中的模型名称
# link_name: 该模型用于计算距离和吸附的link名称
graspable_objects:
  cup1:
    link_name: "link"
  cup2:
    link_name: "link"
  plate1:
    link_name: "link_0"
  plate2:
    link_name: "link_0"
  scissors1:
    link_name: "link_0"
  scissors2:
    link_name: "link_0"
```

## 服务消息定义

### Grasp.srv

```
# 请求
string arm      # "left" 或 "right"
string action   # "grasp" 或 "release"
---
# 响应
bool ok              # 是否成功
string message       # 结果信息
string object_name   # 抓取/释放的物品名称
float64 distance     # 物品距离（米）
```

### Attach.srv

```
# 请求
string model_name_1  # 第一个模型名称
string link_name_1   # 第一个模型的link名称
string model_name_2  # 第二个模型名称
string link_name_2   # 第二个模型的link名称
---
# 响应
bool ok              # 是否成功
string message       # 结果信息
```

## 常见问题

### Q: 抓取失败，提示 "No graspable objects found"

A: 检查以下几点：
1. `grasp_config.yaml` 是否正确加载（查看启动日志）
2. 物品名称是否与Gazebo中的模型名一致
3. 物品是否已添加到 `graspable_objects` 列表

### Q: 抓取失败，提示距离太远

A: 调整 `max_grasp_distance` 参数，或将机器人手臂移动到更近的位置。

### Q: 如何查看当前加载的配置

A: 查看启动日志，会显示：
```
[Grasp Service] Robot model name: biped_s42
[Grasp Service] Min grasp distance: 0m
[Grasp Service] Max grasp distance: 0.25m
[Grasp Service] Loaded 6 graspable objects
```

## 原理

通过在两个链接之间创建一个运动范围为0的revolute关节，实现固定连接效果。当调用attach时，插件会在Gazebo物理引擎中动态创建关节；调用detach时移除关节。
