# Gazebo 房间生成器

通过 YAML 配置文件快速生成 Gazebo 仿真房间。

## 使用方法

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

## 配置文件说明

### 基本参数

```yaml
room:
  name: my_room         # 房间名称
  wall_height: 3.0      # 墙高(米)
  wall_thickness: 0.2   # 墙厚(米)
```

### 材质

```yaml
materials:
  outer_wall: brick     # 外墙
  partition: plaster    # 隔断
  floor: wood           # 地板
```

可选: `white`, `gray`, `brick`, `concrete`, `wood`, `plaster`, `blue`, `green`, `yellow`

### 外墙

```yaml
outer_walls:
  points:
    - [5, 5]    # 顶点坐标 [x, y]
    - [5, -5]
    - [-5, -5]
    - [-5, 5]
  closed: true  # 首尾闭合
```

### 隔断

```yaml
partitions:
  - points:
      - [0, 0]
      - [0, 3]
      - [2, 3]
    closed: false
```

### 门

```yaml
doors:
  - wall_type: outer    # outer/partition
    wall_index: 0       # 墙段索引
    position: 0.5       # 位置(0-1)
    width: 1.0
    height: 2.1
```

### 窗户

```yaml
windows:
  - wall_type: outer
    wall_index: 1
    position: 0.5
    width: 1.5
    height: 1.2
    sill_height: 1.0    # 窗台高度
```

## 运行仿真

```bash
gazebo my_room.world
```
