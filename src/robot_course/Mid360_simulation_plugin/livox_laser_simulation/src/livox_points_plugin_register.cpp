//
// Plugin registration file
// This file is separated to avoid cppcheck unknownMacro errors
//

#include "livox_laser_simulation/livox_points_plugin.h"
#include <gazebo/common/Plugin.hh>

// Register the Livox points plugin with Gazebo
// This macro expands to plugin factory registration code
GZ_REGISTER_SENSOR_PLUGIN(gazebo::LivoxPointsPlugin)
