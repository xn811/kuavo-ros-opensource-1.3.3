# Gazebo 仿真脚本

## 房间生成器

通过 YAML 配置文件快速生成 Gazebo 仿真房间。

### 使用方法

```bash
# 生成示例配置文件
python3 gazebo_room_generate.py

# 使用配置文件生成房间
python3 gazebo_room_generate.py room_config_example.yaml

# 指定输出文件名
python3 gazebo_room_generate.py config.yaml -o my_room.world

# 不添加室内照明
python3 gazebo_room_generate.py config.yaml --no-light
```

### 配置文件说明

#### 基本参数

```yaml
room:
  name: my_room         # 房间名称
  wall_height: 3.0      # 墙高(米)
  wall_thickness: 0.2   # 墙厚(米)
```

#### 材质

```yaml
materials:
  outer_wall: brick     # 外墙
  partition: plaster    # 隔断
  floor: wood           # 地板
```

可选: `white`, `gray`, `brick`, `concrete`, `wood`, `plaster`, `blue`, `green`, `yellow`

#### 外墙

```yaml
outer_walls:
  points:
    - [5, 5]    # 顶点坐标 [x, y]
    - [5, -5]
    - [-5, -5]
    - [-5, 5]
  closed: true  # 首尾闭合
```

#### 隔断

```yaml
partitions:
  - points:
      - [0, 0]
      - [0, 3]
      - [2, 3]
    closed: false
```

#### 门

```yaml
doors:
  - wall_type: outer    # outer/partition
    wall_index: 0       # 墙段索引
    position: 0.5       # 位置(0-1)
    width: 1.0
    height: 2.1
```

#### 窗户

```yaml
windows:
  - wall_type: outer
    wall_index: 1
    position: 0.5
    width: 1.5
    height: 1.2
    sill_height: 1.0    # 窗台高度
```

### 运行仿真

```bash
gazebo my_room.world
```

---

## 随机化物品位置

将桌子上的6种物品（2个杯子、2个盘子、2个剪刀）随机分配到6个固定位置，增加场景随机性。

### 使用方法

```bash
# 使用随机种子启动（自动生成种子）
rosrun gazebo_sim launch_random_scene.py

# 使用指定种子启动（相同种子产生相同布局）
rosrun gazebo_sim launch_random_scene.py --seed 1234

# 指定机器人版本
rosrun gazebo_sim launch_random_scene.py --seed 1234 --robot-version 45

# 无GUI模式启动
rosrun gazebo_sim launch_random_scene.py --seed 1234 --no-gui
```

### 查看随机分配结果

```bash
rosrun gazebo_sim randomize_objects.py --seed 1234
```

输出示例：
```
Random seed: 1234
Object assignment:
  pos1: cup1 (cup) at (-0.3, -4.8)
  pos2: scissors2 (scissors) at (-0.1, -4.7)
  pos3: plate1 (plate) at (-0.3, -4.7)
  ...
```

### 6个固定位置

| 位置 | 坐标 | 描述 |
|------|------|------|
| pos1 | (-0.3, -4.8) | 左前 |
| pos2 | (-0.1, -4.70) | 右前 |
| pos3 | (-0.3, -4.70) | 左后 |
| pos4 | (-0.1, -4.8) | 右后 |
| pos5 | (0.0, -4.7) | 中间位置1 |
| pos6 | (0.1, -4.8) | 中间位置2 |

### 6种物品

- **cup1, cup2**: 塑料杯 (Plastic_Cup)
- **plate1, plate2**: 盘子 (Ecoforms_Plant_Plate_S11Turquoise)
- **scissors1, scissors2**: 剪刀 (Diamond_Visions_Scissors_Red)

### 随机种子说明

- 种子范围：0-9999
- 相同种子产生相同的物品分配
- 不指定种子时使用当前时间戳生成

### 与抓取服务配合使用

随机化后的物品仍然可以正常使用抓取服务：

```bash
# 抓取最近的物品
rosrun gazebo_ros_link_attacher grasp_client.py right grasp

# 释放物品
rosrun gazebo_ros_link_attacher grasp_client.py right release
```

抓取服务会自动检测距离范围内的可抓取物品，无需关心具体位置。
