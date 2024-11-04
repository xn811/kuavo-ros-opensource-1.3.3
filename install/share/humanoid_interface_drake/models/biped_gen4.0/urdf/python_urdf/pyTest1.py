import re
import xml.etree.ElementTree as ET

# 定义函数，从文本中提取质量属性
def extract_mass_properties(text):
    properties = {}

    # 定义正则表达式模式，用于提取不同的信息
    link_pattern = re.compile(r'(\w+) 的质量属性')
    quality_pattern_1 = re.compile(r'质量 = ([\d.]+) 千克')
    quality_pattern_2 = re.compile(r'质量（用户覆盖） = ([\d.]+) 千克')
    centroid_pattern = re.compile(r'质心（用户覆盖）\( 米 \)\s*X = ([\d.-]+)\s*Y = ([\d.-]+)\s*Z = ([\d.-]+)')
    gravity_pattern = re.compile(r'重心\s*:\s*\( 米 \)\s*X\s*=\s*([\d.-]+)\s*Y\s*=\s*([\d.-]+)\s*Z\s*=\s*([\d.-]+)')
    # 带括号 () 的部分用于捕获我们感兴趣的子字符串
    inertia_pattern = re.compile(r'\s*Lxx = ([\d.-]+)\s*Lxy = ([\d.-]+)\s*Lxz = ([\d.-]+)'
                                 r'\s*Lyx = [\d.-]+\s*Lyy = ([\d.-]+)\s*Lyz = ([\d.-]+)'
                                 r'\s*Lzx = [\d.-]+\s*Lzy = [\d.-]+\s*Lzz = ([\d.-]+)')

    for match in link_pattern.finditer(text):
        link_name = match.group(1)
        properties[link_name] = {}
        # 查找并提取重量信息 从 match.end() 位置开始查找重量信息,确保从当前link开始查找
        quality_match_1 = quality_pattern_1.search(text, match.end(), match.end()+500)
        quality_match_2 = quality_pattern_2.search(text, match.end(),match.end()+500)
        if quality_match_1:
            properties[link_name]['quality'] = [float(quality_match_1.group(1))]
            print(f"{link_name} quality: {properties[link_name]['quality']}")
        elif quality_match_2:
            properties[link_name]['quality'] = [float(quality_match_2.group(1))]
            print(f"{link_name} quality: {properties[link_name]['quality']}")
        else:
            print(f"{link_name} quality: not found")
        # 查找并提取质心信息 从 match.end() 位置开始查找质心信息
        centroid_match = centroid_pattern.search(text, match.end(), match.end()+500)
        gravity_match = gravity_pattern.search(text, match.end(), match.end()+500)
        if centroid_match:
            properties[link_name]['centroid'] = [float(centroid_match.group(i)) for i in range(1, 4)]
            print(f"{link_name} centroid: {properties[link_name]['centroid']}")
        elif gravity_match:
            # 由于存在质心覆盖和重心的区别，所以用两个
            properties[link_name]['centroid'] = [float(gravity_match.group(i)) for i in range(1, 4)]
            print(f"{link_name} centroid: {properties[link_name]['centroid']}")
        else:
            print(f"{link_name} centroid: not found")
            print(f"{link_name} gravity: also not found")
        # 查找并提取惯性张量信息
        inertia_match = inertia_pattern.search(text, match.end(), match.end()+800)
        if inertia_match:
            properties[link_name]['inertia'] = [float(inertia_match.group(i)) for i in range(1, 7)]
            # 打印每个link的惯性张量
            print(f"{link_name} inertia: {properties[link_name]['inertia']}")
        else:
            print(f"{link_name} inertia: not found")
    return properties

# 定义函数，用于更新URDF文件
def update_urdf(urdf_file, properties):
    tree = ET.parse(urdf_file)
    root = tree.getroot()

    for link_name, prop in properties.items():
        # 更新质心
        origin = root.find(f".//link[@name='{link_name}']/inertial/origin")
        # if origin is not None:
        #     if 'centroid' in prop:
        #         print(f"{link_name} both found")
        #     else:
        #         print(f"Link: {link_name}, Centroid: not found")
        # else:
        #     print(f"Link: {link_name}, origin: not found")
        if origin is not None and 'centroid' in prop:
            origin.set('xyz', ' '.join(map(str, prop['centroid'])))
            # print(f"Link: {link_name}, origin: found")
        else:
            print(f"Link: {link_name}, origin: not found")

        # 更新质量
        mass = root.find(f".//link[@name='{link_name}']/inertial/mass")
        if mass is not None and 'quality' in prop:
            mass.set('value', ' '.join(map(str, prop['quality'])))
        else:
            print(f"Link: {link_name}, mass: not found")

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
    with open('5代全身主要质量和转动惯量.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    # 提取质量属性
    properties = extract_mass_properties(text)

    # 更新URDF文件
    update_urdf('biped_s5.urdf', properties)

changOriginAndinertia()
