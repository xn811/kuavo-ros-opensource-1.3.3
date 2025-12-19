#!/usr/bin/env python3
"""
支持YAML配置的Gazebo房间生成器
- 通过YAML文件定义房间布局
- 支持外围墙体、内部隔断、门窗
"""

import math
import yaml
import argparse
import sys


# 预定义材质
MATERIALS = {
    'white': {'ambient': '0.9 0.9 0.9 1', 'diffuse': '0.9 0.9 0.9 1'},
    'gray': {'ambient': '0.7 0.7 0.7 1', 'diffuse': '0.7 0.7 0.7 1'},
    'brick': {'ambient': '0.6 0.3 0.2 1', 'diffuse': '0.7 0.35 0.25 1'},
    'concrete': {'ambient': '0.6 0.6 0.6 1', 'diffuse': '0.65 0.65 0.65 1'},
    'wood': {'ambient': '0.5 0.35 0.2 1', 'diffuse': '0.6 0.4 0.25 1'},
    'plaster': {'ambient': '0.95 0.93 0.88 1', 'diffuse': '0.95 0.93 0.88 1'},
    'blue': {'ambient': '0.3 0.4 0.6 1', 'diffuse': '0.4 0.5 0.7 1'},
    'green': {'ambient': '0.3 0.5 0.3 1', 'diffuse': '0.4 0.6 0.4 1'},
    'yellow': {'ambient': '0.9 0.85 0.6 1', 'diffuse': '0.95 0.9 0.65 1'},
    # 工业风格材质
    'black_marble': {'ambient': '0.08 0.08 0.1 1', 'diffuse': '0.12 0.12 0.15 1'},  # 黑色大理石
    'dark_concrete': {'ambient': '0.25 0.25 0.25 1', 'diffuse': '0.3 0.3 0.3 1'},   # 深色水泥
    'steel': {'ambient': '0.4 0.42 0.45 1', 'diffuse': '0.5 0.52 0.55 1'},          # 钢材
    'rust': {'ambient': '0.4 0.25 0.15 1', 'diffuse': '0.5 0.3 0.2 1'},             # 铁锈
    'industrial_gray': {'ambient': '0.35 0.38 0.4 1', 'diffuse': '0.45 0.48 0.5 1'}, # 工业灰
    'epoxy_floor': {'ambient': '0.5 0.55 0.5 1', 'diffuse': '0.55 0.6 0.55 1'},     # 环氧地坪(绿灰)
    'warehouse': {'ambient': '0.55 0.5 0.45 1', 'diffuse': '0.6 0.55 0.5 1'},       # 仓库墙面
    'metal_panel': {'ambient': '0.6 0.62 0.65 1', 'diffuse': '0.7 0.72 0.75 1'},    # 金属板
}


class RoomWithPartitionsGenerator:
    def __init__(self, name="room", wall_height=3.0, wall_thickness=0.2,
                 outer_wall_material='gray', partition_material='plaster', floor_material='wood'):
        self.name = name
        self.wall_height = wall_height
        self.wall_thickness = wall_thickness
        self.outer_wall_material = outer_wall_material
        self.partition_material = partition_material
        self.floor_material = floor_material
        self.outer_walls = []
        self.partitions = []
        self.doors = []
        self.windows = []

    def set_outer_walls(self, points, closed=True):
        if closed and points[0] != points[-1]:
            points = points + [points[0]]
        self.outer_walls = self._points_to_walls(points, "outer")
        print(f"✓ 添加了 {len(self.outer_walls)} 段外墙")

    def add_partition(self, points, closed=False):
        if closed and points[0] != points[-1]:
            points = points + [points[0]]
        partition_walls = self._points_to_walls(points, f"partition_{len(self.partitions)}")
        self.partitions.extend(partition_walls)
        print(f"✓ 添加了 {len(partition_walls)} 段隔断墙")
        return len(self.partitions) - len(partition_walls)

    def _points_to_walls(self, points, prefix):
        walls = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            wall_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            if wall_length < 0.001:
                continue
            center_x = (p1[0] + p2[0]) / 2
            center_y = (p1[1] + p2[1]) / 2
            center_z = self.wall_height / 2
            angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
            walls.append({
                'id': f"{prefix}_{i}",
                'center': (center_x, center_y, center_z),
                'size': (wall_length, self.wall_thickness, self.wall_height),
                'rotation': angle,
                'p1': p1,
                'p2': p2,
                'type': 'outer' if prefix == 'outer' else 'partition'
            })
        return walls

    def add_door(self, wall_type, wall_index, position_ratio=0.5, width=1.0, height=2.1):
        self.doors.append({
            'wall_type': wall_type,
            'wall_index': wall_index,
            'position_ratio': position_ratio,
            'width': width,
            'height': height
        })
        print(f"✓ 在{wall_type}墙段{wall_index}上添加了门")

    def add_window(self, wall_type, wall_index, position_ratio=0.5,
                   width=1.5, height=1.2, sill_height=1.0):
        self.windows.append({
            'wall_type': wall_type,
            'wall_index': wall_index,
            'position_ratio': position_ratio,
            'width': width,
            'height': height,
            'sill_height': sill_height
        })
        print(f"✓ 在{wall_type}墙段{wall_index}上添加了窗户")

    def _get_openings_for_wall(self, wall_type, wall_index):
        openings = []
        for door in self.doors:
            if door['wall_type'] == wall_type and door['wall_index'] == wall_index:
                openings.append({
                    'pos_ratio': door['position_ratio'],
                    'width': door['width'],
                    'height': door['height'],
                    'bottom': 0,
                    'type': 'door'
                })
        for window in self.windows:
            if window['wall_type'] == wall_type and window['wall_index'] == wall_index:
                openings.append({
                    'pos_ratio': window['position_ratio'],
                    'width': window['width'],
                    'height': window['height'],
                    'bottom': window['sill_height'],
                    'type': 'window'
                })
        return sorted(openings, key=lambda x: x['pos_ratio'])

    def _split_wall_with_openings(self, wall, wall_type, wall_index):
        openings = self._get_openings_for_wall(wall_type, wall_index)
        if not openings:
            return [wall]
        wall_length = wall['size'][0]
        segments = []
        current_pos = 0
        for opening in openings:
            opening_center = opening['pos_ratio'] * wall_length
            opening_start = opening_center - opening['width'] / 2
            opening_end = opening_center + opening['width'] / 2
            if opening_start > current_pos + 0.01:
                seg_length = opening_start - current_pos
                seg_center_local = (current_pos + opening_start) / 2
                segments.append({
                    'local_center': seg_center_local,
                    'length': seg_length,
                    'height': self.wall_height,
                    'bottom': 0
                })
            if opening['type'] == 'window':
                if opening['bottom'] > 0.01:
                    segments.append({
                        'local_center': opening_center,
                        'length': opening['width'],
                        'height': opening['bottom'],
                        'bottom': 0
                    })
                top_height = self.wall_height - (opening['bottom'] + opening['height'])
                if top_height > 0.01:
                    segments.append({
                        'local_center': opening_center,
                        'length': opening['width'],
                        'height': top_height,
                        'bottom': opening['bottom'] + opening['height']
                    })
            current_pos = opening_end
        if current_pos < wall_length - 0.01:
            seg_length = wall_length - current_pos
            seg_center_local = (current_pos + wall_length) / 2
            segments.append({
                'local_center': seg_center_local,
                'length': seg_length,
                'height': self.wall_height,
                'bottom': 0
            })
        result = []
        for seg in segments:
            offset_along_wall = seg['local_center'] - wall_length / 2
            cos_a = math.cos(wall['rotation'])
            sin_a = math.sin(wall['rotation'])
            global_x = wall['center'][0] + offset_along_wall * cos_a
            global_y = wall['center'][1] + offset_along_wall * sin_a
            global_z = seg['bottom'] + seg['height'] / 2
            result.append({
                'center': (global_x, global_y, global_z),
                'size': (seg['length'], self.wall_thickness, seg['height']),
                'rotation': wall['rotation'],
                'type': wall['type']
            })
        return result

    def _get_material(self, material_name):
        """获取材质颜色"""
        mat = MATERIALS.get(material_name, MATERIALS['gray'])
        return mat['ambient'], mat['diffuse']

    def _create_wall_xml(self, wall, name):
        x, y, z = wall['center']
        length, thickness, height = wall['size']
        yaw = wall['rotation']
        mat_name = self.outer_wall_material if wall['type'] == 'outer' else self.partition_material
        ambient, diffuse = self._get_material(mat_name)
        return f'''
      <link name="{name}">
        <pose>{x:.4f} {y:.4f} {z:.4f} 0 0 {yaw:.4f}</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>{length:.4f} {thickness:.4f} {height:.4f}</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>{length:.4f} {thickness:.4f} {height:.4f}</size>
            </box>
          </geometry>
          <material>
            <ambient>{ambient}</ambient>
            <diffuse>{diffuse}</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
      </link>
'''

    def calculate_floor_bounds(self):
        all_points = []
        for wall in self.outer_walls:
            all_points.append(wall['p1'])
            all_points.append(wall['p2'])
        if not all_points:
            return (0, 0), (10, 10)
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
        size = (max_x - min_x, max_y - min_y)
        return center, size

    def generate_world(self, filename="room.world", add_lighting=True):
        if not self.outer_walls:
            print("错误：没有设置外墙！")
            return
        floor_center, floor_size = self.calculate_floor_bounds()
        sdf = f'''<?xml version="1.0"?>
<sdf version="1.6">
  <world name="{self.name}_world">
    <include>
      <uri>model://sun</uri>
    </include>
    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
      <shadows>true</shadows>
    </scene>
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    <model name="{self.name}">
      <static>true</static>
      <link name="floor">
        <pose>{floor_center[0]:.4f} {floor_center[1]:.4f} 0.001 0 0 0</pose>
        <visual name="visual">
          <geometry>
            <box>
              <size>{floor_size[0]:.4f} {floor_size[1]:.4f} 0.002</size>
            </box>
          </geometry>
          <material>
            <ambient>{self._get_material(self.floor_material)[0]}</ambient>
            <diffuse>{self._get_material(self.floor_material)[1]}</diffuse>
          </material>
        </visual>
      </link>
'''
        wall_count = 0
        for i, wall in enumerate(self.outer_walls):
            wall_pieces = self._split_wall_with_openings(wall, 'outer', i)
            for j, piece in enumerate(wall_pieces):
                sdf += self._create_wall_xml(piece, f"outer_wall_{i}_{j}")
                wall_count += 1
        partition_count = 0
        for i, wall in enumerate(self.partitions):
            wall_pieces = self._split_wall_with_openings(wall, 'partition', i)
            for j, piece in enumerate(wall_pieces):
                sdf += self._create_wall_xml(piece, f"partition_{i}_{j}")
                partition_count += 1
        if add_lighting:
            sdf += f'''
      <link name="ceiling_light">
        <pose>{floor_center[0]:.4f} {floor_center[1]:.4f} {self.wall_height - 0.1:.4f} 0 0 0</pose>
        <light name="light" type="point">
          <pose>0 0 0 0 0 0</pose>
          <diffuse>1 1 1 1</diffuse>
          <specular>0.2 0.2 0.2 1</specular>
          <attenuation>
            <range>20</range>
            <constant>0.5</constant>
            <linear>0.01</linear>
            <quadratic>0.001</quadratic>
          </attenuation>
          <cast_shadows>false</cast_shadows>
        </light>
      </link>
'''
        sdf += '''
    </model>
  </world>
</sdf>
'''
        with open(filename, 'w') as f:
            f.write(sdf)
        print(f"\n✓ World文件已生成: {filename}")
        print(f"  外墙片段: {wall_count}, 隔断片段: {partition_count}")
        print(f"  地板尺寸: {floor_size[0]:.2f}m × {floor_size[1]:.2f}m")
        print(f"\n运行命令: gazebo {filename}")


def load_from_yaml(yaml_file):
    """从YAML文件加载房间配置"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    room_cfg = config.get('room', {})
    materials = config.get('materials', {})
    room = RoomWithPartitionsGenerator(
        name=room_cfg.get('name', 'room'),
        wall_height=room_cfg.get('wall_height', 3.0),
        wall_thickness=room_cfg.get('wall_thickness', 0.2),
        outer_wall_material=materials.get('outer_wall', 'gray'),
        partition_material=materials.get('partition', 'plaster'),
        floor_material=materials.get('floor', 'wood')
    )
    
    # 外墙
    outer = config.get('outer_walls', {})
    if outer.get('points'):
        points = [tuple(p) for p in outer['points']]
        room.set_outer_walls(points, closed=outer.get('closed', True))
    
    # 隔断
    for partition in config.get('partitions', []):
        points = [tuple(p) for p in partition['points']]
        room.add_partition(points, closed=partition.get('closed', False))
    
    # 门
    for door in config.get('doors', []):
        room.add_door(
            wall_type=door.get('wall_type', 'outer'),
            wall_index=door.get('wall_index', 0),
            position_ratio=door.get('position', 0.5),
            width=door.get('width', 1.0),
            height=door.get('height', 2.1)
        )
    
    # 窗户
    for window in config.get('windows', []):
        room.add_window(
            wall_type=window.get('wall_type', 'outer'),
            wall_index=window.get('wall_index', 0),
            position_ratio=window.get('position', 0.5),
            width=window.get('width', 1.5),
            height=window.get('height', 1.2),
            sill_height=window.get('sill_height', 1.0)
        )
    
    return room, config.get('output', 'room.world')


def main():
    parser = argparse.ArgumentParser(description='Gazebo房间生成器')
    parser.add_argument('yaml_file', nargs='?', help='YAML配置文件路径')
    parser.add_argument('-o', '--output', help='输出文件名（覆盖YAML中的设置）')
    parser.add_argument('--no-light', action='store_true', help='不添加照明')
    args = parser.parse_args()
    
    if not args.yaml_file:
        print("用法: python3 gazebo_room_generate.py <config.yaml> [-o output.world]")
        print("\n示例YAML配置文件已生成: room_config_example.yaml")
        create_example_yaml()
        return
    
    room, default_output = load_from_yaml(args.yaml_file)
    output_file = args.output or default_output
    room.generate_world(output_file, add_lighting=not args.no_light)


def create_example_yaml():
    """创建示例YAML配置文件"""
    example = '''# Gazebo房间配置文件示例
# 单位：米

room:
  name: my_room
  wall_height: 3.0
  wall_thickness: 0.2

# 外墙顶点（顺时针或逆时针）
outer_walls:
  points:
    - [5, 5]      # 右上
    - [5, -5]     # 右下
    - [-5, -5]    # 左下
    - [-5, 5]     # 左上
  closed: true

# 内部隔断（可添加多个）
partitions:
  - points:       # L型隔断
      - [0, 0]
      - [0, 2]
      - [3, 2]
    closed: false
  - points:       # 直线隔断
      - [-3, -2]
      - [-3, 2]
    closed: false

# 门
doors:
  - wall_type: outer      # outer或partition
    wall_index: 0         # 墙段索引
    position: 0.5         # 位置比例(0-1)
    width: 1.0
    height: 2.1
  - wall_type: partition
    wall_index: 0
    position: 0.6
    width: 0.9

# 窗户
windows:
  - wall_type: outer
    wall_index: 1
    position: 0.3
    width: 1.5
    height: 1.2
    sill_height: 1.0
  - wall_type: outer
    wall_index: 3
    position: 0.5
    width: 2.0

# 输出文件名
output: my_room.world
'''
    with open('room_config_example.yaml', 'w', encoding='utf-8') as f:
        f.write(example)
    print("✓ 示例配置文件已创建: room_config_example.yaml")


if __name__ == "__main__":
    main()
