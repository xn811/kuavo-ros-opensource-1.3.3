import re
import xml.etree.ElementTree as ET
import os

def extract_mass_properties(text):
    properties = {}

    # 使用正则表达式提取信息
    link_pattern = re.compile(r'(\w+) 的质量属性')
    centroid_pattern = re.compile(r'质心（用户覆盖）\( 米 \)\s*X = ([\d.-]+)\s*Y = ([\d.-]+)\s*Z = ([\d.-]+)')
    inertia_pattern = re.compile(r'惯性张量: \( 千克 \* 平方米 \)\s*由重心决定，并且对齐输出的坐标系。\s*Lxx = ([\d.-]+)\s*Lxy = ([\d.-]+)\s*Lxz = ([\d.-]+)\s*Lyx = [\d.-]+\s*Lyy = ([\d.-]+)\s*Lyz = ([\d.-]+)\s*Lzx = [\d.-]+\s*Lzy = [\d.-]+\s*Lzz = ([\d.-]+)')

    for match in link_pattern.finditer(text):
        link_name = match.group(1)
        properties[link_name] = {}

        centroid_match = centroid_pattern.search(text, match.end())
        if centroid_match:
            properties[link_name]['centroid'] = [float(centroid_match.group(i)) for i in range(1, 4)]

        inertia_match = inertia_pattern.search(text, match.end())
        if inertia_match:
            properties[link_name]['inertia'] = [float(inertia_match.group(i)) for i in range(1, 7)]

    return properties

def update_urdf(urdf_file, properties):
    tree = ET.parse(urdf_file)
    root = tree.getroot()

    for link_name, prop in properties.items():
        # 更新质心
        origin = root.find(f".//link[@name='{link_name}']/inertial/origin")
        if origin is not None and 'centroid' in prop:
            origin.set('xyz', ' '.join(map(str, prop['centroid'])))

        # 更新惯性张量
        inertia = root.find(f".//link[@name='{link_name}']/inertial/inertia")
        if inertia is not None and 'inertia' in prop:
            inertia.set('ixx', str(prop['inertia'][0]))
            inertia.set('ixy', str(prop['inertia'][1]))
            inertia.set('ixz', str(prop['inertia'][2]))
            inertia.set('iyy', str(prop['inertia'][3]))
            inertia.set('iyz', str(prop['inertia'][4]))
            inertia.set('izz', str(prop['inertia'][5]))

    tree.write('updated_robot.urdf', encoding='utf-8', xml_declaration=True)

def changOriginAndinertia():
    # 读取txt文件
    with open('3代转动惯量.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    # 提取质量属性
    properties = extract_mass_properties(text)

    # 更新URDF文件
    update_urdf('biped_v5_middle_file.urdf', properties)

    # base_path = os.path.dirname(__file__)
    # txt_file = os.path.join(base_path, '3代转动惯量.txt')
    # urdf_file = os.path.join(base_path, 'biped_v5_middle_file.urdf')

    # # 读取txt文件
    # with open(txt_file, 'r', encoding='utf-8') as file:
    #     text = file.read()
    # # 提取质量属性
    # properties = extract_mass_properties(text)

    # # 更新URDF文件
    # update_urdf(urdf_file, properties)
changOriginAndinertia()
