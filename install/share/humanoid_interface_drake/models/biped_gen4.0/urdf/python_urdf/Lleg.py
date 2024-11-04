import xml.etree.ElementTree as etree
from lxml import etree
# 解析URDF文件
tree = etree.parse('../biped_v5_all_joint.urdf')
root = tree.getroot()

# 定义命名空间字典
namespace = {
    'drake': 'https://drake.mit.edu'
}

def keepLinkAndJoint(keep_names):
    # 查找所有 link 标签
    all_links = root.findall('.//link')
    # 删除不在 links_to_keep 列表中的 link
    for link in all_links:
        link_name = link.attrib['name']
        if link_name not in keep_names:
            root.remove(link)

    # 查找所有 joint 标签
    all_joints = root.findall('./joint')
    
    # 删除不在 joints_to_keep 列表中的 joint
    for joint in all_joints:
        joint_name = joint.attrib['name']
        if joint_name not in keep_names:
            root.remove(joint)

def keepDrakeJoint(keep_names):
    all_drake_joint = root.findall(f".//drake:joint", namespaces=namespace)
    for drake_joint in all_drake_joint:
        drake_joint_name = drake_joint.attrib['name']
        if drake_joint_name not in keep_names:
            root.remove(drake_joint)


def keepTransmission(keep_names):
    # 查找所有 transmission 标签
    all_transmissions = root.findall('.//transmission')
    # 删除不在 transmissions_to_keep 列表中的 transmission
    for transmission in all_transmissions:
        joint = transmission.find('joint')
        if joint is not None and joint.attrib.get('name') not in keep_names:
            root.remove(transmission)

def deleteJoint(name):
    # 找到并删除joint
    joint = root.find(f".//joint[@name='{name}']")
    if joint is not None:
        root.remove(joint)
    else:
        print(f"Joint: {name} not found")

def deleteFootBallCollision(link_name):
    # 找到
    link = root.find(f"./link[@name='{link_name}']")
    if link is not None:
        for visual in link.findall('.//visual'):
            link.remove(visual)
        for collision in link.findall('.//collision'):
            link.remove(collision)
    else:
        print(f"link: {link_name} not found")
    
    visual = etree.Element('visual')    
    etree.SubElement(visual, 'origin', xyz='0 0 0', rpy='0 0 0')
    geometry = etree.SubElement(visual, 'geometry')
    mesh = etree.SubElement(geometry, 'mesh', filename=f'../meshes/{link_name}.obj')
    material = etree.SubElement(visual, 'material', name="")
    color = etree.SubElement(material, 'color', rgba="1 1 1 1")
    link.append(visual)
    

def deleteFrame():
    frames = root.findall(".//frame")
    if frames:
        for frame in frames:
            parent = root.find(f".//frame[@name='{frame.attrib['name']}']/..")
            if parent is not None:
                parent.remove(frame)
    else:
        print("No frames found")
        
def addBallConstraint(tendon_xyz, foot_xyz):
    # 创建 frame 和 drake:linear_bushing_rpy 元素
    frame1 = etree.Element('frame', link="l_l_tendon", name="l_l_tendon_frame", xyz=f'{tendon_xyz[0]}')
    frame2 = etree.Element('frame', link="l_foot_roll", name="l_foot_roll_l_frame", xyz=f'{foot_xyz[0]}')
    # 将新元素插入到根元素的末尾
    root.append(frame1)
    root.append(frame2)

    drake_linear_bushing_rpy1 = etree.Element('{https://drake.mit.edu}linear_bushing_rpy')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_frameA', name='l_l_tendon_frame')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_frameC', name='l_foot_roll_l_frame')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_force_stiffness', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_force_damping', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_torque_stiffness', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy1, '{https://drake.mit.edu}bushing_torque_damping', value='0 0 0')
    root.append(drake_linear_bushing_rpy1)

    frame3 = etree.Element('frame', link="l_r_tendon", name="l_r_tendon_frame", xyz=f'{tendon_xyz[1]}')
    frame4 = etree.Element('frame', link="l_foot_roll", name="l_foot_roll_r_frame", xyz=f'{foot_xyz[1]}')
    # 将新元素插入到根元素的末尾
    root.append(frame3)
    root.append(frame4)

    drake_linear_bushing_rpy2 = etree.Element('{https://drake.mit.edu}linear_bushing_rpy')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_frameA', name='l_r_tendon_frame')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_frameC', name='l_foot_roll_r_frame')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_force_stiffness', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_force_damping', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_torque_stiffness', value='0 0 0')
    etree.SubElement(drake_linear_bushing_rpy2, '{https://drake.mit.edu}bushing_torque_damping', value='0 0 0')
    root.append(drake_linear_bushing_rpy2)


keep_name = {'l_knee', 'l_foot_pitch', 'l_foot_roll', 'l_l_bar', 'l_l_tendon', 'l_r_bar', 'l_r_tendon'}
keep_transmission = {'l_r_bar', 'l_l_bar'}
keep_drake_joint = {'l_l_tendon', 'l_r_tendon'}
# 按照先左后右原则填入tendon和foot上的坐标点 使用有序列表
tendon_xyz = ['0 0 -0.3563', '0 0 -0.2913']
foot_xyz = ['-0.0563 0.025 0.01473', '-0.0563 -0.025 0.01473']
keepLinkAndJoint(keep_name)
keepTransmission(keep_transmission)
deleteJoint("l_knee")
deleteFrame()
deleteFootBallCollision("l_foot_roll")
addBallConstraint(tendon_xyz, foot_xyz)
keepDrakeJoint(keep_drake_joint)
# 将修改后的URDF写入新文件
tree.write('../Lleg.urdf', encoding='utf-8', xml_declaration=True)


