from lxml import etree
# 解析URDF文件
tree = etree.parse('../biped_v5_full.urdf')
root = tree.getroot()


def delete_subtree(start_link_name):
    # 找到起始标签
    found_start_tag = True    
    # 遍历父标签的所有子标签
    for child in root.findall('./*'):
        if child.tag == 'link' and child.attrib.get('name') == start_link_name:
            found_start_tag = False        
        if found_start_tag:
            # 删除找到的标签及其之后的所有同级标签
            root.remove(child)
    print(f'found_start_tag = {found_start_tag}')

# 以某个标签为起点删除所有子标签示例
delete_subtree('l_arm_pitch') 
# 将修改后的URDF写入新文件
tree.write('../biped_v5_arm.urdf', encoding='utf-8', xml_declaration=True)
