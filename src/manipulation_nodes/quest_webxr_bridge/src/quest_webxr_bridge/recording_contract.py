"""Rosbag contracts shared by the WebXR recorder and validator."""

from collections import OrderedDict


ARM_JOINT_NAMES = tuple("arm_joint_{}".format(index) for index in range(1, 15))

CONTROL_TOPICS = OrderedDict([
    ("/kuavo_arm_traj", "sensor_msgs/JointState"),
    ("/control_robot_hand_position", "kuavo_msgs/robotHandPosition"),
    ("/robot_head_motion_data", "kuavo_ros_interfaces/robotHeadMotionData"),
])

CONTROL_MD5 = {
    "/kuavo_arm_traj": "3066dcd76a6cfaef579bd0f34173e9fd",
    "/control_robot_hand_position": "ee45ac8dfb6e0c9a4c7712025fd69d4f",
    "/robot_head_motion_data": "400001e7cf73111efbced59084cb481a",
}

# Exact topic/type contract observed in:
# /mnt/data1/kuavo_tum_data/task1_bottle_pick/
# vr_record_2026-06-02-14-59-53.bag
TASK1_BOTTLE_PICK_TOPICS = OrderedDict([
    ("/kuavo_arm_traj", "sensor_msgs/JointState"),
    ("/control_robot_hand_position", "kuavo_msgs/robotHandPosition"),
    ("/robot_head_motion_data", "kuavo_ros_interfaces/robotHeadMotionData"),
    ("/cam_h/color/camera_info", "sensor_msgs/CameraInfo"),
    ("/cam_h/color/image_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/cam_h/color/metadata", "orbbec_camera/Metadata"),
    ("/cam_h/depth/image_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/cam_l/color/camera_info", "sensor_msgs/CameraInfo"),
    ("/cam_l/color/image_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/cam_l/color/metadata", "realsense2_camera/Metadata"),
    ("/cam_l/depth/image_rect_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/cam_r/color/camera_info", "sensor_msgs/CameraInfo"),
    ("/cam_r/color/image_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/cam_r/color/metadata", "realsense2_camera/Metadata"),
    ("/cam_r/depth/image_rect_raw/compressed", "sensor_msgs/CompressedImage"),
    ("/dexhand/state", "sensor_msgs/JointState"),
    ("/dexhand/touch_state", "kuavo_msgs/dexhandTouchState"),
    ("/humanoid_controller/wbc_arm_eef_pose", "std_msgs/Float64MultiArray"),
    ("/joint_cmd", "kuavo_msgs/jointCmd"),
    ("/sensors_data_raw", "kuavo_msgs/sensorsData"),
    ("/tf", "tf2_msgs/TFMessage"),
    ("/tf_static", "tf2_msgs/TFMessage"),
])

RECORDING_PROFILES = {
    # Simulation deliberately selects the same topic/type contract as the real
    # task. Camera and hardware-only publishers may be absent in MuJoCo, but
    # using the full selection prevents a simulation-only bag naming scheme
    # from drifting away from the real-robot dataset.
    "sim-control": TASK1_BOTTLE_PICK_TOPICS,
    "task1-bottle-pick": TASK1_BOTTLE_PICK_TOPICS,
}

# rosbag cannot materialize a connection for a topic that never publishes a
# message. In simulation those source-dependent topics are therefore allowed
# to be absent/empty, while the three WebXR control topics remain mandatory.
PROFILE_OPTIONAL_TOPICS = {
    "sim-control": frozenset(TASK1_BOTTLE_PICK_TOPICS) - frozenset(CONTROL_TOPICS),
    "task1-bottle-pick": frozenset(),
}


def profile_topics(profile):
    """Return a copy so callers cannot mutate the canonical contract."""
    try:
        return OrderedDict(RECORDING_PROFILES[profile])
    except KeyError:
        raise ValueError(
            "unknown recording profile {!r}; choose one of {}".format(
                profile, ", ".join(sorted(RECORDING_PROFILES))
            )
        )


def profile_optional_topics(profile):
    """Return topics allowed to have no recorded messages for this profile."""
    # Reuse profile_topics for one consistent unknown-profile error.
    profile_topics(profile)
    return frozenset(PROFILE_OPTIONAL_TOPICS[profile])
