import xml.etree.ElementTree as etree
from lxml import etree
# 解析URDF文件
tree = etree.parse('../biped_v5_all_joint.urdf')
root = tree.getroot()

# 定义命名空间字典
namespace = {
    'drake': 'https://drake.mit.edu'
}
def deleteLinkAndJoint(name):
    # 找到并删除link
    link = root.find(f"./link[@name='{name}']")
    if link is not None:
        root.remove(link)
    # 找到并删除joint
    joint = root.find(f"./joint[@name='{name}']")
    drake_joint = root.find(f".//drake:joint[@name='{name}']", namespaces=namespace)
    if joint is not None:
        root.remove(joint)
    elif drake_joint is not None:
        root.remove(drake_joint)
    else:
        print(f"Joint: {name} not found")


def deleteFrame():
    for frame in root.findall('./frame'):
        root.remove(frame)

def addFootFrame(joint_name, frame_name, xyz_nums):
    # 遍历所有joint建立字典
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
   
    # 查找特定的<joint>元素
    joint = root.find(f".//joint[@name='{joint_name}']")    
    # 创建要添加的frame元素
    frames = [
        {'link': f'{joint_name}', 'name': f'{frame_name}_toe', 'xyz': f'{xyz_nums[0]}'},
        {'link': f'{joint_name}', 'name': f'{frame_name}_sole', 'xyz': f'{xyz_nums[1]}'},
        {'link': f'{joint_name}', 'name': f'{frame_name}_heel', 'xyz': f'{xyz_nums[2]}'}
    ]
    for frame in frames:
        # 创建 frame 元素
        new_frame = etree.Element('frame')
        new_frame.set('link', frame['link'])
        new_frame.set('name', frame['name'])
        new_frame.set('xyz', frame['xyz'])

        parent = joint_parent_map[joint]
        joint_index = list(parent).index(joint)
        parent.insert(joint_index + 1, new_frame)

def addEndFrame(joint_name,frame_name):
    # 遍历所有joint建立字典
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
   
    # 查找特定的<joint>元素
    joint = root.find(f".//joint[@name='{joint_name}']")    
    # 创建要添加的frame元素
    frames = [
        {'link': f'{joint_name}', 'name': f'{frame_name}', 'xyz': f'0 0 0'}
    ]
    for frame in frames:
        # 创建 frame 元素
        new_frame = etree.Element('frame')
        new_frame.set('link', frame['link'])
        new_frame.set('name', frame['name'])
        new_frame.set('xyz', frame['xyz'])

        parent = joint_parent_map[joint]
        joint_index = list(parent).index(joint)
        parent.insert(joint_index + 1, new_frame)


# 删除特定的 <transmission> 标签
def deleteTransmission(jointName):
    for transmission in root.findall('.//transmission'):
        joint = transmission.find('joint')
        if joint is not None and joint.attrib.get('name') == jointName:
            root.remove(transmission)


def addTransmission(jointName):
    # 遍历所有joint建立字典
    joint_parent_map = {child: parent for parent in root.iter() for child in parent}
   
    # 查找特定的<joint>元素
    joint = root.find(f".//joint[@name='{jointName}']")    
    transmission = etree.Element('transmission', type='SimpleTransmission')    
    etree.SubElement(transmission, 'joint', name=jointName)
    etree.SubElement(transmission, 'actuator', name=f"{jointName}_motor")    
    parent = joint_parent_map[joint]
    joint_index = list(parent).index(joint)
    parent.insert(joint_index + 1, transmission)


# 前中后
xyz_nums = ['0.075 -0.0 -0.055', '0 -0.0 -0.055', '-0.075 -0.0 -0.055']
deleteLinkAndJoint("l_l_bar")
deleteLinkAndJoint("l_r_bar")
deleteLinkAndJoint("r_l_bar")
deleteLinkAndJoint("r_r_bar")
deleteLinkAndJoint("l_l_tendon")
deleteLinkAndJoint("l_r_tendon")
deleteLinkAndJoint("r_l_tendon")
deleteLinkAndJoint("r_r_tendon")
deleteFrame()
addFootFrame("l_foot_roll", "l_foot", xyz_nums)
addFootFrame("r_foot_roll", "r_foot", xyz_nums)
addEndFrame("l_arm_pitch", "l_hand_sole")
addEndFrame("r_arm_pitch", "r_hand_sole")
deleteTransmission("l_l_bar")
deleteTransmission("l_r_bar")
deleteTransmission("r_l_bar")
deleteTransmission("r_r_bar")

deleteTransmission("l_l_tendon")
deleteTransmission("l_r_tendon")
deleteTransmission("r_l_tendon")
deleteTransmission("r_r_tendon")

addTransmission("l_foot_pitch")
addTransmission("r_foot_pitch")
addTransmission("l_foot_roll")
addTransmission("r_foot_roll")
# 将修改后的URDF写入新文件
tree.write('../biped_v5_full.urdf', encoding='utf-8', xml_declaration=True)