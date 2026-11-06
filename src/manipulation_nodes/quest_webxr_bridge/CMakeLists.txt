cmake_minimum_required(VERSION 3.0.2)
project(quest_webxr_bridge)

find_package(catkin REQUIRED COMPONENTS
  kuavo_msgs
  kuavo_ros_interfaces
  rospy
  sensor_msgs
  std_msgs
  std_srvs
  tf2_ros
)

catkin_python_setup()
catkin_package()

catkin_install_python(PROGRAMS
  scripts/quest_webxr_kuavo_bridge.py
  scripts/quest_webxr_control_contract_adapter.py
  scripts/rosbag_tool.py
  scripts/validate_rosbag_alignment.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY config docs launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES src/quest_webxr_bridge/head_pose_client.js
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}
)
