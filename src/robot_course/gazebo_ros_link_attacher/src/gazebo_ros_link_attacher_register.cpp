//
// Plugin registration file
// This file is separated to avoid cppcheck unknownMacro errors
//

#include "gazebo_ros_link_attacher.h"
#include <gazebo/common/Plugin.hh>

// Register the GazeboRosLinkAttacher plugin with Gazebo
// This macro expands to plugin factory registration code
GZ_REGISTER_WORLD_PLUGIN(gazebo::GazeboRosLinkAttacher)
