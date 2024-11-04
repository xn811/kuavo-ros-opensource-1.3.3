
import xml.etree.ElementTree as ET
# 解析URDF文件
tree = ET.parse('../biped_s5.urdf')
root = tree.getroot()

# # 找到并删除l_leg_roll链接
# l_leg_roll_link = root.find("./link[@name='l_leg_roll']/collision")
# if l_leg_roll_link is not None:
#     root.remove(l_leg_roll_link)

# # 找到并删除l_leg_roll关节
# l_leg_roll_joint = root.find("./joint[@name='l_leg_roll']")
# if l_leg_roll_joint is not None:
#     root.remove(l_leg_roll_joint)

# # 找到l_leg_yaw关节并修改其parent和origin
# l_leg_yaw_joint = root.find("./joint[@name='l_leg_yaw']")
# if l_leg_yaw_joint is not None:
#     parent_link = l_leg_yaw_joint.find('parent')
#     if parent_link is not None:
#         parent_link.attrib['link'] = 'torso'
#     origin = l_leg_yaw_joint.find('origin')
#     if origin is not None:
#         origin.attrib['xyz'] = '-0.139 0.088087 -0.098999'

def addXmlns():
    # 找到robot标签
    robot = root.find('.')
    # 添加xmlns:drake属性
    robot.set('xmlns:drake', 'https://drake.mit.edu')

# 删除所有的collision标签
def deleteCollision():
    for link in root.findall('./link'):
        for collision in link.findall('collision'):
            link.remove(collision)

# 为每个 joint 标签添加相应的 transmission 标签
# 需要手动跟踪父元素
def addTransmission():
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
    for joint in root.findall('./joint'):
        joint_name = joint.attrib['name']
        transmission = ET.Element('transmission', type='SimpleTransmission')
        
        ET.SubElement(transmission, 'joint', name=joint_name)
        ET.SubElement(transmission, 'actuator', name=f"{joint_name}_motor")
        
        parent = joint_parent_map[joint]
        joint_index = list(parent).index(joint)
        parent.insert(joint_index + 1, transmission)

# 遍历所有的<mesh>标签并修改filename属性
def changeFilename():
    for mesh in root.findall('.//mesh'):
        filename = mesh.get('filename')
        if filename and filename.startswith('package://biped_s5/meshes/'):
            # 提取文件名并更改路径
            new_filename = '../meshes/' + filename.split('/')[-1].replace('.STL', '.obj')
            mesh.set('filename', new_filename)

# 查找并修改特定的 <transmission> 标签
def changeTransmission(jointName):
    for transmission in root.findall('.//transmission'):
        joint = transmission.find('joint')
        if joint is not None and joint.attrib.get('name') == jointName:
            actuator = transmission.find('actuator')
            if actuator is not None and actuator.attrib.get('name') == f'{jointName}_motor':
                # 添加新的子元素
                drake_gear_ratio = ET.SubElement(actuator, 'drake:gear_ratio')
                drake_gear_ratio.set('value', '36.0')
                drake_rotor_inertia = ET.SubElement(actuator, 'drake:rotor_inertia')
                drake_rotor_inertia.set('value', '0.0001002')

# 删除特定的 <transmission> 标签
def deleteTransmission(jointName):
    for transmission in root.findall('.//transmission'):
        joint = transmission.find('joint')
        if joint is not None and joint.attrib.get('name') == jointName:
            root.remove(transmission)

def changAxis():
    for axis in root.findall('.//axis'):
        xyz = axis.get('xyz')
        if xyz == "-1 0 0":
            axis.set('xyz', "1 0 0")
        elif xyz == "0 -1 0":
            axis.set('xyz', "0 1 0")
        elif xyz == "0 0 -1":
            axis.set('xyz', "0 0 1")    

# 创建一个新的<limit>标签
def addLimit():
    limit = ET.Element('limit')
    limit.set('lower', '-1.50')
    limit.set('upper', '1.50')
    limit.set('effort', '74')
    limit.set('velocity', '47')
    for parent in root.findall('./joint'):
        for axis in parent.findall('axis'):
            # 在<axis>标签的同级后面添加<limit>标签
            parent.insert(list(parent).index(axis) + 1, limit)

def addFootBallCollision(link_name):
    # 查找特定的<link>元素
    link = root.find(f".//link[@name='{link_name}']")
    
    if link is not None:
        # 创建要添加的元素
        new_elements = [
            {'type': 'visual', 'rpy': "0 0 0", 'xyz': "-0.075 0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'collision', 'rpy': "0 0 0", 'xyz': "-0.075 0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'visual', 'rpy': "0 0 0", 'xyz': "-0.075 -0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'collision', 'rpy': "0 0 0", 'xyz': "-0.075 -0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'visual', 'rpy': "0 0 0", 'xyz': "0.075 0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'collision', 'rpy': "0 0 0", 'xyz': "0.075 0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'visual', 'rpy': "0 0 0", 'xyz': "0.075 -0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'},
            {'type': 'collision', 'rpy': "0 0 0", 'xyz': "0.075 -0.03 -0.055", 'geometry': 'sphere', 'radius': '0.005'}
        ]
        for elem in new_elements:
            # 创建 visual 或 collision 元素
            new_element = ET.Element(elem['type'])
            origin = ET.SubElement(new_element, 'origin')
            origin.set('rpy', elem['rpy'])
            origin.set('xyz', elem['xyz'])
            
            geometry = ET.SubElement(new_element, 'geometry')
            sphere = ET.SubElement(geometry, elem['geometry'])
            sphere.set('radius', elem['radius'])
            
            # 将新元素添加到 link 中
            link.append(new_element)
    else:print(f"can not find {link_name}")

def addFootFrame(joint_name, xyz_nums):
    # 遍历所有joint建立字典
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
   
    # 查找特定的<joint>元素
    joint = root.find(f".//joint[@name='{joint_name}']")    
    # 创建要添加的frame元素
    frames = [
        {'link': f'{joint_name}', 'name': f'{joint_name}_l_frame', 'xyz': f'{xyz_nums[0]}'},
        {'link': f'{joint_name}', 'name': f'{joint_name}_r_frame', 'xyz': f'{xyz_nums[1]}'}
    ]
    for frame in frames:
        # 创建 frame 元素
        new_frame = ET.Element('frame')
        new_frame.set('link', frame['link'])
        new_frame.set('name', frame['name'])
        new_frame.set('xyz', frame['xyz'])

        parent = joint_parent_map[joint]
        joint_index = list(parent).index(joint)
        parent.insert(joint_index + 1, new_frame)

def addTendonFrame(joint_name,length):
    # 遍历所有joint建立字典
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
   
    # 查找特定的<joint>元素
    joint = root.find(f".//joint[@name='{joint_name}']")    
    # 创建要添加的frame元素
    frames = [
        {'link': f'{joint_name}', 'name': f'{joint_name}_frame', 'xyz': f'0 0 -{length}'}
    ]
    for frame in frames:
        # 创建 frame 元素
        new_frame = ET.Element('frame')
        new_frame.set('link', frame['link'])
        new_frame.set('name', frame['name'])
        new_frame.set('xyz', frame['xyz'])

        parent = joint_parent_map[joint]
        joint_index = list(parent).index(joint)
        parent.insert(joint_index + 1, new_frame)
# 这个函数必须在frame下面，不然会导致frame缺失
def changeJoint(name):
    # 找到并删除r_l_tendon链接
    joint = root.find(f"./joint[@name='{name}']")
    if joint is not None:
        origin = joint.find('origin')
        parent = joint.find('parent')
        child = joint.find('child')
        origin_xyz = origin.attrib['xyz']
        parent_link = parent.attrib['link']
        child_link = child.attrib['link']
        root.remove(joint)
    # 遍历所有link建立字典
    link_parent_map = {child: parent for parent in root.iter() for child in parent}   
    # 查找特定的<joint>元素
    link = root.find(f".//link[@name='{name}']") 
    drake_joint = ET.Element('drake:joint', name=f'{name}', type='universal')    
    ET.SubElement(drake_joint, 'origin', xyz=f'{origin_xyz}', rpy='0 0 0')
    ET.SubElement(drake_joint, 'parent', link=f'{parent_link}')
    ET.SubElement(drake_joint, 'child', link=f'{child_link}')
    parent = link_parent_map[link]
    link_index = list(parent).index(link)
    parent.insert(link_index + 1, drake_joint)

    
# 辅助函数，增加缩进
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# 先左後右
xyz_nums = ['-0.0563 0.025 0.01473', '-0.0563 -0.025 0.01473']
addXmlns()
deleteCollision()
addTransmission()
changeFilename()
changeTransmission('l_l_bar')
changeTransmission('l_r_bar')
changeTransmission('r_l_bar')
changeTransmission('r_r_bar')
deleteTransmission('l_foot_pitch')
deleteTransmission('l_foot_roll')
deleteTransmission('r_foot_pitch')
deleteTransmission('r_foot_roll')
deleteTransmission('l_l_tendon')
deleteTransmission('l_r_tendon')
deleteTransmission('r_l_tendon')
deleteTransmission('r_r_tendon')
changAxis()
addLimit()
addFootBallCollision('r_foot_roll')
addFootBallCollision('l_foot_roll')
addFootFrame('l_foot_roll', xyz_nums)
addFootFrame('r_foot_roll', xyz_nums)
addTendonFrame('l_l_tendon','0.3563' )
addTendonFrame('r_r_tendon','0.3563' )
addTendonFrame('l_r_tendon','0.29134' )
addTendonFrame('r_l_tendon','0.29134' )
changeJoint('l_l_tendon')
changeJoint('l_r_tendon')
changeJoint('r_l_tendon')
changeJoint('r_r_tendon')
# 增加缩进
# indent(root)
# 将修改后的URDF写入新文件
tree.write('../biped_v5_all_joint.urdf', encoding='utf-8', xml_declaration=True)
