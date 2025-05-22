<a id="kuavo-strategy"></a>

#### WARNING
Before running any code examples, make sure to start the robot first by executing either:

- For simulation: `roslaunch humanoid_controllers load_kuavo_mujoco_sim.launch` (Example command)
- For real robot: `roslaunch humanoid_controllers load_kuavo_real.launch` (Example command)

#### NOTE
If using websocket mode, you need to start the rosbridge server on robot first: `roslaunch rosbridge_server rosbridge_websocket.launch` (Example command)

# Kuavo Strategy 策略模块

## 策略模块常用基础通用类 - 原子技能层级

### *class* kuavo_humanoid_sdk.KuavoRobot

Bases: `RobotBase`

#### arm_fk(q: list) → Tuple[[KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)]

Forward kinematics for the robot arm.

* **Parameters:**
  **q** (*list*) – List of joint positions in radians.
* **Returns:**
  Tuple of poses for the robot left arm and right arm,
  : or (None, None) if forward kinematics failed.
* **Return type:**
  Tuple[[KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)]

#### WARNING
This function requires initializing the SDK with the [`KuavoSDK.Options.WithIK`](api_reference.md#kuavo_humanoid_sdk.KuavoSDK.Options.WithIK).

#### arm_ik(left_pose: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), right_pose: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), left_elbow_pos_xyz: list = [0.0, 0.0, 0.0], right_elbow_pos_xyz: list = [0.0, 0.0, 0.0], arm_q0: list | None = None, params: [KuavoIKParams](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoIKParams) | None = None) → list

Inverse kinematics for the robot arm.

* **Parameters:**
  * **left_pose** ([*KuavoPose*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)) – Pose of the robot left arm, xyz and quat.
  * **right_pose** ([*KuavoPose*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)) – Pose of the robot right arm, xyz and quat.
  * **left_elbow_pos_xyz** (*list*) – Position of the robot left elbow. If [0.0, 0.0, 0.0], will be ignored.
  * **right_elbow_pos_xyz** (*list*) – Position of the robot right elbow. If [0.0, 0.0, 0.0], will be ignored.
  * **arm_q0** (*list* *,* *optional*) – Initial joint positions in radians. If None, will be ignored.
  * **params** ([*KuavoIKParams*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoIKParams) *,* *optional*) – Parameters for the inverse kinematics. If None, will be ignored.
    Contains:
    - major_optimality_tol: Major optimality tolerance
    - major_feasibility_tol: Major feasibility tolerance
    - minor_feasibility_tol: Minor feasibility tolerance
    - major_iterations_limit: Major iterations limit
    - oritation_constraint_tol: Orientation constraint tolerance
    - pos_constraint_tol: Position constraint tolerance, works when pos_cost_weight==0.0
    - pos_cost_weight: Position cost weight. Set to 0.0 for high accuracy
* **Returns:**
  List of joint positions in radians, or None if inverse kinematics failed.
* **Return type:**
  list

#### WARNING
This function requires initializing the SDK with the [`KuavoSDK.Options.WithIK`](api_reference.md#kuavo_humanoid_sdk.KuavoSDK.Options.WithIK).

#### arm_reset() → bool

Reset the robot arm.

* **Returns:**
  True if the arm is reset successfully, False otherwise.
* **Return type:**
  bool

#### control_arm_joint_positions(joint_positions: list) → bool

Control the position of the arm.

* **Parameters:**
  **joint_positions** (*list*) – The target position of the arm in radians.
* **Returns:**
  True if the arm is controlled successfully, False otherwise.
* **Return type:**
  bool
* **Raises:**
  * **ValueError** – If the joint position list is not of the correct length.
  * **ValueError** – If the joint position is outside the range of [-π, π].
  * **RuntimeError** – If the robot is not in stance state when trying to control the arm.

#### control_arm_joint_trajectory(times: list, q_frames: list) → bool

Control the target poses of the robot arm.

* **Parameters:**
  * **times** (*list*) – List of time intervals in seconds.
  * **q_frames** (*list*) – List of joint positions in radians.
* **Returns:**
  True if the control was successful, False otherwise.
* **Return type:**
  bool
* **Raises:**
  * **ValueError** – If the times list is not of the correct length.
  * **ValueError** – If the joint position list is not of the correct length.
  * **ValueError** – If the joint position is outside the range of [-π, π].
  * **RuntimeError** – If the robot is not in stance state when trying to control the arm.

#### WARNING
This is an asynchronous interface. The function returns immediately after sending the command.
Users need to wait for the motion to complete on their own.

#### control_command_pose(target_pose_x: float, target_pose_y: float, target_pose_z: float, target_pose_yaw: float) → bool

Control robot pose in base_link frame.

* **Parameters:**
  * **target_pose_x** (*float*) – The target x position in meters.
  * **target_pose_y** (*float*) – The target y position in meters.
  * **target_pose_z** (*float*) – The target z position in meters.
  * **target_pose_yaw** (*float*) – The target yaw angle in radians.
* **Returns:**
  True if the command was sent successfully, False otherwise.
* **Return type:**
  bool
* **Raises:**
  **RuntimeError** – If the robot is not in stance state when trying to control pose.

#### NOTE
This command changes the robot state to ‘command_pose’.

#### control_command_pose_world(target_pose_x: float, target_pose_y: float, target_pose_z: float, target_pose_yaw: float) → bool

Control robot pose in odom (world) frame.

* **Parameters:**
  * **target_pose_x** (*float*) – The target x position in meters.
  * **target_pose_y** (*float*) – The target y position in meters.
  * **target_pose_z** (*float*) – The target z position in meters.
  * **target_pose_yaw** (*float*) – The target yaw angle in radians.
* **Returns:**
  True if the command was sent successfully, False otherwise.
* **Return type:**
  bool
* **Raises:**
  **RuntimeError** – If the robot is not in stance state when trying to control pose.

#### NOTE
This command changes the robot state to ‘command_pose_world’.

#### control_head(yaw: float, pitch: float) → bool

Control the head of the robot.

* **Parameters:**
  * **yaw** (*float*) – The yaw angle of the head in radians, range [-1.396, 1.396] (-80 to 80 degrees).
  * **pitch** (*float*) – The pitch angle of the head in radians, range [-0.436, 0.436] (-25 to 25 degrees).
* **Returns:**
  True if the head is controlled successfully, False otherwise.
* **Return type:**
  bool

#### control_robot_end_effector_pose(left_pose: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), right_pose: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), frame: [KuavoManipulationMpcFrame](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcFrame)) → bool

Control the end effector pose of the robot arm.

* **Parameters:**
  * **left_pose** ([*KuavoPose*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)) – Pose of the robot left arm, xyz and quat.
  * **right_pose** ([*KuavoPose*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)) – Pose of the robot right arm, xyz and quat.
  * **frame** ([*KuavoManipulationMpcFrame*](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcFrame)) – Frame of the robot arm.
* **Returns:**
  True if the end effector pose is controlled successfully, False otherwise.
* **Return type:**
  bool

#### disable_head_tracking() → bool

Disable the head tracking.

#### enable_head_tracking(target_id: int) → bool

Enable the head tracking.

#### jump()

Jump the robot.

#### manipulation_mpc_reset() → bool

Reset the robot arm.

* **Returns:**
  True if the arm is reset successfully, False otherwise.
* **Return type:**
  bool

#### set_auto_swing_arm_mode() → bool

Swing the robot arm.

* **Returns:**
  True if the arm is swinging successfully, False otherwise.
* **Return type:**
  bool

#### set_external_control_arm_mode() → bool

External control the robot arm.

* **Returns:**
  True if the arm is external controlled successfully, False otherwise.
* **Return type:**
  bool

#### set_fixed_arm_mode() → bool

Freezes the robot arm.

* **Returns:**
  True if the arm is frozen successfully, False otherwise.
* **Return type:**
  bool

#### set_manipulation_mpc_control_flow(control_flow: [KuavoManipulationMpcControlFlow](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcControlFlow)) → bool

Set the manipulation mpc control flow.
:returns: True if the manipulation mpc control flow is set successfully, False otherwise.
:rtype: bool

#### set_manipulation_mpc_frame(frame: [KuavoManipulationMpcFrame](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcFrame)) → bool

Set the manipulation mpc frame.
:returns: True if the manipulation mpc frame is set successfully, False otherwise.
:rtype: bool

#### set_manipulation_mpc_mode(ctrl_mode: [KuavoManipulationMpcCtrlMode](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcCtrlMode)) → bool

Set the manipulation mpc mode.
:returns: True if the manipulation mpc mode is set successfully, False otherwise.
:rtype: bool

#### squat(height: float, pitch: float = 0.0) → bool

Control the robot’s squat height and pitch.
:param height: The height offset from normal standing height in meters, range [-0.35, 0.0],Negative values indicate squatting down.
:type height: float
:param pitch: The pitch angle of the robot’s torso in radians, range [-0.4, 0.4].
:type pitch: float

* **Returns:**
  True if the squat is controlled successfully, False otherwise.
* **Return type:**
  bool

#### stance() → bool

Put the robot into ‘stance’ mode.

* **Returns:**
  True if the robot is put into stance mode successfully, False otherwise.
* **Return type:**
  bool

#### NOTE
You can call [`KuavoRobotState.wait_for_stance()`](api_reference.md#kuavo_humanoid_sdk.KuavoRobotState.wait_for_stance) to wait until the robot enters stance mode.

#### step_by_step(target_pose: list, dt: float = 0.4, is_left_first_default: bool = True, collision_check: bool = True) → bool

Control the robot’s motion by step.

* **Parameters:**
  * **target_pose** (*list*) – The target position of the robot in [x, y, z, yaw] m, rad.
  * **dt** (*float*) – The time interval between each step in seconds. Defaults to 0.4s.
  * **is_left_first_default** (*bool*) – Whether to start with the left foot. Defaults to True.
  * **collision_check** (*bool*) – Whether to check for collisions. Defaults to True.
* **Returns:**
  True if motion is successful, False otherwise.
* **Return type:**
  bool
* **Raises:**
  * **RuntimeError** – If the robot is not in stance state when trying to control step motion.
  * **ValueError** – If target_pose length is not 4.

#### NOTE
You can call [`KuavoRobotState.wait_for_step_control()`](api_reference.md#kuavo_humanoid_sdk.KuavoRobotState.wait_for_step_control) to wait until the robot enters step-control mode.
You can call [`KuavoRobotState.wait_for_stance()`](api_reference.md#kuavo_humanoid_sdk.KuavoRobotState.wait_for_stance) to wait the step-control finish.

#### trot() → bool

Put the robot into ‘trot’ mode.

* **Returns:**
  True if the robot is put into trot mode successfully, False otherwise.
* **Return type:**
  bool

#### NOTE
You can call [`KuavoRobotState.wait_for_walk()`](api_reference.md#kuavo_humanoid_sdk.KuavoRobotState.wait_for_walk) to wait until the robot enters trot mode.

#### walk(linear_x: float, linear_y: float, angular_z: float) → bool

Control the robot’s motion.

* **Parameters:**
  * **linear_x** (*float*) – The linear velocity along the x-axis in m/s, range [-0.4, 0.4].
  * **linear_y** (*float*) – The linear velocity along the y-axis in m/s, range [-0.2, 0.2].
  * **angular_z** (*float*) – The angular velocity around the z-axis in rad/s, range [-0.4, 0.4].
* **Returns:**
  True if the motion is controlled successfully, False otherwise.
* **Return type:**
  bool

#### NOTE
You can call [`KuavoRobotState.wait_for_walk()`](api_reference.md#kuavo_humanoid_sdk.KuavoRobotState.wait_for_walk) to wait until the robot enters walk mode.

### *class* kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotVision(robot_type: str = 'kuavo')

Bases: `object`

Vision system interface for Kuavo humanoid robot.

Provides access to AprilTag detection data from different coordinate frames.

#### *property* apriltag_data_from_base *: [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)*

All detected AprilTags in camera frame (property)

* **Type:**
  [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)

#### *property* apriltag_data_from_camera *: [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)*

All detected AprilTags in camera frame (property)

* **Type:**
  [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)

#### *property* apriltag_data_from_odom *: [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)*

All detected AprilTags in camera frame (property)

* **Type:**
  [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData)

#### get_data_by_id(target_id: int, data_source: str = 'base') → dict

Get AprilTag detection data for a specific ID from specified source.

* **Parameters:**
  * **target_id** (*int*) – AprilTag ID to retrieve
  * **data_source** (*str* *,* *optional*) – Data source frame. Can be “base”, “camera”,
    or “odom”. Defaults to “base”.
* **Returns:**
  Detection data containing position, orientation and metadata
* **Return type:**
  dict

#### get_data_by_id_from_base(target_id: int) → dict

Get AprilTag data from base coordinate frame.

* **Parameters:**
  **target_id** (*int*) – AprilTag ID to retrieve
* **Returns:**
  See get_data_by_id() for return format
* **Return type:**
  dict

#### get_data_by_id_from_camera(target_id: int) → dict

Get AprilTag data from camera coordinate frame.

* **Parameters:**
  **target_id** (*int*) – AprilTag ID to retrieve
* **Returns:**
  See get_data_by_id() for return format
* **Return type:**
  dict

#### get_data_by_id_from_odom(target_id: int) → dict

Get AprilTag data from odom coordinate frame.

* **Parameters:**
  **target_id** (*int*) – AprilTag ID to retrieve
* **Returns:**
  See get_data_by_id() for return format
* **Return type:**
  dict

### *class* kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotState(robot_type: str = 'kuavo')

Bases: `object`

#### angular_velocity() → Tuple[float, float, float]

Returns the robot’s angular velocity in world coordinates.

* **Returns:**
  Angular velocity (x, y, z).
* **Return type:**
  Tuple[float, float, float]

#### arm_control_mode() → [KuavoArmCtrlMode](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoArmCtrlMode)

Get the current control mode of the robot arm.

* **Returns:**
  Current arm control mode:
  : ArmFixed: 0 - The robot arm is in a fixed position.
    AutoSwing: 1 - The robot arm is in automatic swing mode.
    ExternalControl: 2 - The robot arm is controlled externally.
    or None.
* **Return type:**
  [KuavoArmCtrlMode](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoArmCtrlMode)

#### arm_joint_state() → [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)

Get the current state of the robot arm joints.

Get the current state of the robot arm joints, including:
: - Joint positions (angles) in radians
  - Joint velocities in radians/second
  - Joint torques/efforts in Newton-meters, A
  - Joint acceleration

* **Returns:**
  Arm joint data containing:
  : position: list[float] \* arm_dof(14)
    velocity: list[float] \* arm_dof(14)
    torque: list[float]   \* arm_dof(14)
    acceleration: list[float] \* arm_dof(14)
* **Return type:**
  [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)

#### *property* com_height *: float*

Get the height of the robot’s center of mass.

* **Returns:**
  The height of the robot’s center of mass in meters.
* **Return type:**
  float

#### eef_state() → Tuple[[EndEffectorState](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.EndEffectorState), [EndEffectorState](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.EndEffectorState)]

Get the current state of the robot’s end effectors.

* **Returns:**
  A tuple containing the state of the left and right end effectors.
  : Each EndEffectorState contains:
    : - position: (float, float, float) - XYZ position in meters
      - orientation: (float, float, float, float) - Quaternion orientation
      - state: EndEffectorState.GraspingState - Current grasping state (UNKNOWN, OPEN, CLOSED)
* **Return type:**
  Tuple[[EndEffectorState](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.EndEffectorState), [EndEffectorState](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.EndEffectorState)]

#### gait_name() → str

Get the current gait name of the robot.

* **Returns:**
  The name of the current gait, e.g. ‘trot’, ‘walk’, ‘stance’, ‘custom_gait’.
* **Return type:**
  str

#### head_joint_state() → [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)

Get the current state of the robot head joints.

Gets the current state data for the robot’s head joints, including position,
velocity, torque and acceleration values.

* **Returns:**
  A data structure containing the head joint states:
  : position (list[float]): Joint positions in radians, length=head_dof(2)
    velocity (list[float]): Joint velocities in rad/s, length=head_dof(2)
    torque (list[float]): Joint torques in Nm, length=head_dof(2)
    acceleration (list[float]): Joint accelerations in rad/s^2, length=head_dof(2)

  The joint order is [yaw, pitch].
* **Return type:**
  [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)

#### *property* imu_data *: [KuavoImuData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoImuData)*

Get Robot IMU Data.

Gets the current IMU sensor data from the robot, including gyroscope, accelerometer,
free acceleration and orientation quaternion measurements.

* **Returns:**
  IMU data containing:
  : * gyro (`tuple` of `float`): Gyroscope measurements (x, y, z) in rad/s
    * acc (`tuple` of `float`): Accelerometer measurements (x, y, z) in m/s^2
    * free_acc (`tuple` of `float`): Free acceleration (x, y, z) in m/s^2
    * quat (`tuple` of `float`): Orientation quaternion (x, y, z, w)
* **Return type:**
  `KuavoImuData`

#### is_stance() → bool

Check if the robot is currently in stance mode.

* **Returns:**
  True if robot is in stance mode, False otherwise.
* **Return type:**
  bool

#### is_step_control() → bool

Check if the robot is currently in step control mode.

* **Returns:**
  True if robot is in step control mode, False otherwise.
* **Return type:**
  bool

#### is_walk() → bool

Check if the robot is currently in walk mode.

* **Returns:**
  True if robot is in walk mode, False otherwise.
* **Return type:**
  bool

#### *property* joint_state *: [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)*

Get Robot Joint Data.

Get Robot Joint Data, including joint positions, velocities, torques and accelerations.

The data includes:
: - Joint positions (angles) in radians
  - Joint velocities in radians/second
  - Joint torques/efforts in Newton-meters, A
  - Joint acceleration

* **Returns:**
  A dictionary containing joint state data with the following keys:
  : position (list[float]): Joint positions, length = joint_dof(28)
    velocity (list[float]): Joint velocities, length = joint_dof(28)
    torque (list[float]): Joint torques, length = joint_dof(28)
    acceleration (list[float]): Joint accelerations, length = joint_dof(28)
* **Return type:**
  [KuavoJointData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoJointData)

#### linear_velocity() → Tuple[float, float, float]

Returns the robot’s linear velocity in world coordinates.

* **Returns:**
  Linear velocity (x, y, z) in m/s.
* **Return type:**
  Tuple[float, float, float]

#### manipulation_mpc_control_flow() → [KuavoManipulationMpcControlFlow](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcControlFlow)

Get the current control flow of the robot manipulation.

* **Returns:**
  Current manipulation control flow.
* **Return type:**
  [KuavoManipulationMpcControlFlow](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcControlFlow)

#### manipulation_mpc_ctrl_mode() → [KuavoManipulationMpcCtrlMode](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcCtrlMode)

Get the current control mode of the robot manipulation MPC.

* **Returns:**
  Current manipulation MPC control mode.
* **Return type:**
  [KuavoManipulationMpcCtrlMode](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcCtrlMode)

#### manipulation_mpc_frame() → [KuavoManipulationMpcFrame](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcFrame)

Get the current frame of the robot manipulation MPC.

* **Returns:**
  Current manipulation MPC frame.
* **Return type:**
  [KuavoManipulationMpcFrame](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoManipulationMpcFrame)

#### *property* odometry *: [KuavoOdometry](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoOdometry)*

Get Robot Odometry Data.

Gets the current odometry data from the robot, including position, orientation,
linear velocity and angular velocity measurements.

* **Returns:**
  A dictionary containing odometry data with the following keys:
  : position (tuple): Position (x, y, z) in meters
    orientation (tuple): Orientation as quaternion (x, y, z, w)
    linear (tuple): Linear velocity (x, y, z) in m/s
    angular (tuple): Angular velocity (x, y, z) in rad/s
* **Return type:**
  [KuavoOdometry](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoOdometry)

#### robot_orientation() → Tuple[float, float, float, float]

Returns the robot’s orientation in world coordinates.

* **Returns:**
  Orientation as quaternion (x, y, z, w).
* **Return type:**
  Tuple[float, float, float, float]

#### robot_position() → Tuple[float, float, float]

Returns the robot’s position in world coordinates.

* **Returns:**
  Position (x, y, z) in meters.
* **Return type:**
  Tuple[float, float, float]

#### wait_for_stance(timeout: float = 5.0) → bool

Wait for the robot to enter stance state.

* **Parameters:**
  **timeout** (*float*) – The maximum time to wait for the robot to enter stance state in seconds.
* **Returns:**
  True if the robot enters stance state within the specified timeout, False otherwise.
* **Return type:**
  bool

#### wait_for_step_control(timeout: float = 5.0) → bool

Wait for the robot to enter step control state.

* **Parameters:**
  **timeout** (*float*) – The maximum time to wait for the robot to enter step control state in seconds.
* **Returns:**
  True if the robot enters step control state within the specified timeout, False otherwise.
* **Return type:**
  bool

#### wait_for_trot(timeout: float = 5.0) → bool

Wait for the robot to enter trot state.

* **Parameters:**
  **timeout** (*float*) – The maximum time to wait for the robot to enter trot state in seconds.
* **Returns:**
  True if the robot enters trot state within the specified timeout, False otherwise.
* **Return type:**
  bool

#### wait_for_walk(timeout: float = 5.0) → bool

Wait for the robot to enter walk state.

* **Parameters:**
  **timeout** (*float*) – The maximum time to wait for the robot to enter walk state in seconds.
* **Returns:**
  True if the robot enters walk state within the specified timeout, False otherwise.
* **Return type:**
  bool

### *class* kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotTools

Bases: `object`

Robot tools class providing coordinate frame transformation interfaces.

This class encapsulates coordinate transformation queries between different robot frames,
supporting multiple return data formats.

#### get_base_to_odom(return_type: str = 'pose_quaternion') → [PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion) | [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix) | None

Get transformation from base_link to odom frame.

* **Parameters:**
  **return_type** (*str* *,* *optional*) – Return format type. Same as get_tf_transform.
  Defaults to “pose_quaternion”.
* **Returns:**
  Transformation data or None
* **Return type:**
  Union[[PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion), [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix), None]

#### get_camera_to_base(return_type: str = 'homogeneous') → [PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion) | [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix) | None

Get transformation from camera_link to base_link frame.

* **Parameters:**
  **return_type** (*str* *,* *optional*) – Return format type. Same as get_tf_transform.
  Defaults to “homogeneous”.
* **Returns:**
  Transformation data or None
* **Return type:**
  Union[[PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion), [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix), None]

#### get_tf_transform(target_frame: str, source_frame: str, return_type: str = 'pose_quaternion') → [PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion) | [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix) | None

Get transformation between specified coordinate frames.

* **Parameters:**
  * **target_frame** (*str*) – Name of target coordinate frame
  * **source_frame** (*str*) – Name of source coordinate frame
  * **return_type** (*str* *,* *optional*) – Return data format type. Valid values:
    “pose_quaternion” - quaternion pose format,
    “homogeneous” - homogeneous matrix format. Defaults to “pose_quaternion”.
* **Returns:**
  Transformation data in specified format, or None if failed
* **Return type:**
  Union[[PoseQuaternion](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.PoseQuaternion), [HomogeneousMatrix](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.HomogeneousMatrix), None]
* **Raises:**
  **ValueError** – If invalid return_type is provided

## 基础策略接口

### *class* kuavo_humanoid_sdk.kuavo_strategy.kuavo_strategy.KuavoRobotStrategyBase(robot: [KuavoRobot](#kuavo_humanoid_sdk.KuavoRobot), robot_state: [KuavoRobotState](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotState), robot_tools: [KuavoRobotTools](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotTools), robot_vision: [KuavoRobotVision](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotVision))

Bases: `ABC`

Kuavo机器人策略基础类，提供策略执行的抽象接口

#### *abstract* arm_move_to_target(target_info, \*\*kwargs)

手臂移动到特定的位置

* **Parameters:**
  * **target_info** – 目标信息，包含位置、姿态等
  * **arm_mode** – 手臂控制模式
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功移动到目标位置
* **Return type:**
  bool

#### *abstract* arm_transport_target_down(target_info, \*\*kwargs)

放下操作对象

* **Parameters:**
  * **target_info** – 目标信息，包含位置、姿态等
  * **arm_mode** – 手臂控制模式
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功放下操作对象
* **Return type:**
  bool

#### *abstract* arm_transport_target_up(target_info, \*\*kwargs)

提起操作对象

* **Parameters:**
  * **target_info** – 目标信息，包含位置、姿态等
  * **arm_mode** – 手臂控制模式
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功提起操作对象
* **Return type:**
  bool

#### *abstract* head_find_target(target_info, \*\*kwargs)

寻找特定ID的目标

* **Parameters:**
  * **target_id** – 目标的ID标识
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功找到目标
* **Return type:**
  bool

#### *abstract* walk_approach_target(target_info, target_distance=0.5, \*\*kwargs)

走/接近特定的目标到指定距离

* **Parameters:**
  * **target_id** – 目标的ID标识
  * **target_distance** – 与目标的期望距离(米)
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功接近目标
* **Return type:**
  bool

#### *abstract* walk_to_pose(target_info, target_distance=0.5, \*\*kwargs)

走到指定距离的目标位置

* **Parameters:**
  * **target_info** – 目标信息，包含位置、姿态等
  * **target_distance** – 与目标的期望距离(米)
  * **\*\*kwargs** – 其他参数
* **Returns:**
  是否成功接近目标
* **Return type:**
  bool

## 箱子抓取策略

### 箱子信息数据结构

### *class* kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy.BoxInfo(pose: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose), size: Tuple[float, float, float] = (0.3, 0.2, 0.15), mass: float = 1.0)

Bases: `object`

箱子信息数据类

描述箱子的位置、尺寸和质量信息，用于箱子抓取策略

#### pose

箱子的位姿信息

* **Type:**
  [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)

#### size

箱子的尺寸 (长, 宽, 高) 单位: 米

* **Type:**
  Tuple[float, float, float]

#### mass

箱子的质量 单位: 千克

* **Type:**
  float

#### mass *: float* *= 1.0*

#### pose *: [KuavoPose](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.KuavoPose)*

#### size *: Tuple[float, float, float]* *= (0.3, 0.2, 0.15)*

### 箱子抓取策略类

### *class* kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy.KuavoGraspBox(robot: [KuavoRobot](#kuavo_humanoid_sdk.KuavoRobot), robot_state: [KuavoRobotState](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotState), robot_tools: [KuavoRobotTools](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotTools), robot_vision: [KuavoRobotVision](#kuavo_humanoid_sdk.kuavo_strategy.KuavoRobotVision))

Bases: [`KuavoRobotStrategyBase`](#kuavo_humanoid_sdk.kuavo_strategy.kuavo_strategy.KuavoRobotStrategyBase)

箱子抓取策略类，继承自基础策略类

#### arm_move_to_target(target_info: BoxInfo, arm_mode='manipulation_mpc', \*\*kwargs)

手臂移动到目标位置

* **Parameters:**
  * **target_info** – 目标信息，包含位置、尺寸等
  * **approach_speed** – 接近速度(米/秒)
  * **arm_mode** – 手臂控制模式
* **Returns:**
  是否成功移动到目标位置
* **Return type:**
  bool

#### arm_transport_target_down(target_info: BoxInfo, arm_mode='manipulation_mpc')

实现手臂放下箱子的功能

* **Parameters:**
  * **target_info** – 目标放置位置信息
  * **arm_mode** – 手臂控制模式
* **Returns:**
  是否成功放下目标
* **Return type:**
  bool

#### arm_transport_target_up(target_info: BoxInfo, arm_mode='manipulation_mpc')

实现手臂搬起箱子的功能

* **Parameters:**
  * **target_info** – 目标信息，包含位置、尺寸等
  * **arm_mode** – 手臂控制模式
* **Returns:**
  是否成功搬起目标
* **Return type:**
  bool

#### head_find_target(target_info: [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData), max_search_time=None, search_pattern='rotate_head', \*\*kwargs)

使用头部旋转寻找AprilTag目标

* **Parameters:**
  * **target_info** – AprilTag的信息
  * **max_search_time** – 最大搜索时间(秒)，如果为None则使用默认值
  * **search_pattern** – 搜索模式，”rotate_head”或”rotate_body”
* **Returns:**
  是否成功找到目标
* **Return type:**
  bool

logic:
: 1. 判断目标位置是否在机器人FOV(70度视场角)内
  2. 如果不在FOV内且search_pattern为”rotate_body”，先旋转机器人身体朝向目标位置
  3. 无论如何都使用头部搜索模式尝试找到目标
  4. 找到apriltag_data_from_odom之后，马上开始头部追踪

#### walk_approach_target(target_info: [AprilTagData](api_reference.md#kuavo_humanoid_sdk.interfaces.data_types.AprilTagData), target_distance=0.5, approach_speed=0.15, \*\*kwargs)

走路接近AprilTag目标

* **Parameters:**
  * **target_info** – AprilTag的信息
  * **target_distance** – 与目标的期望距离(米)
  * **approach_speed** – 接近速度(米/秒)
* **Returns:**
  是否成功接近目标
* **Return type:**
  bool

#### walk_to_pose(target_info: BoxInfo, target_distance=0.5, approach_speed=0.15, \*\*kwargs)

让机器人走到指定的位姿

* **Parameters:**
  * **target_pose** – 目标位姿
  * **target_distance** – 与目标的期望距离(米)
  * **approach_speed** – 接近速度(米/秒)
* **Returns:**
  是否成功到达目标位姿
* **Return type:**
  bool

## 使用示例

以下是一个使用箱子抓取策略的基本示例:

```python
import time
import numpy as np
from kuavo_humanoid_sdk import KuavoRobot, KuavoRobotState, KuavoRobotTools, KuavoRobotVision
from kuavo_humanoid_sdk.interfaces.data_types import KuavoPose, AprilTagData, PoseQuaternion
from kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy import KuavoGraspBox, BoxInfo

def main():
    print("初始化机器人...")
    # 初始化机器人及相关组件
    robot = KuavoRobot()
    robot_state = KuavoRobotState()
    robot_tools = KuavoRobotTools()
    robot_vision = KuavoRobotVision()

    # 初始化箱子抓取策略
    grasp_strategy = KuavoGraspBox(robot, robot_state, robot_tools, robot_vision)

    # 创建AprilTag数据对象
    target_april_tag = AprilTagData(
        id=[2],  # AprilTag ID
        size=[0.088],  # AprilTag 标签尺寸
        pose=[PoseQuaternion(
            position=(0.0, -1.0, 0.8),  # 位置
            orientation=(0.0, 0.0, 0.0, 1.0)  # 四元数方向
        )]
    )

    # 创建箱子信息对象
    box_info = BoxInfo(
        pose=KuavoPose(
            position=(0.0, -1.0, 0.9),  # 箱子位置
            orientation=(0.0, 0.0, 0.0, 1.0)  # 箱子朝向
        ),
        size=(0.3, 0.2, 0.15),  # 箱子尺寸(长、宽、高)，单位：米
        mass=1.0  # 箱子重量，单位：千克
    )

    # 创建放置位置的箱子信息
    placement_box_info = BoxInfo(
        pose=KuavoPose(
            position=(0.0, 1.0, 0.9),  # 目标放置位置坐标
            orientation=(0, 0, 0.7071, 0.7071)  # 目标放置方向（四元数）
        ),
        size=(0.3, 0.2, 0.15),  # 使用相同尺寸
        mass=1.0  # 使用相同质量
    )

    time.sleep(1)
    # 执行完整抓取策略
    try:
        print("========== 开始执行箱子抓取策略 ==========")

        # 步骤1：使用头部寻找目标
        print("\n1. 寻找目标箱子...")
        grasp_strategy.robot.disable_head_tracking()
        print("✅ 已关闭头部追踪")

        find_success = grasp_strategy.head_find_target(
            target_april_tag,
            max_search_time=15.0,
            search_pattern="rotate_body" #  rotate_head
        )

        if not find_success:
            print("❌ 寻找目标失败，无法继续执行")
            return

        print("✅ 已找到目标箱子")
        time.sleep(1)  # 短暂暂停

        # 步骤2：走路接近目标
        # for i in range(1):
        print("\n2. 走路接近目标...")
        approach_success = grasp_strategy.walk_approach_target(
            target_april_tag,
            target_distance=0.6,  # 与目标箱子保持0.6米的距离
            approach_speed=0.2    # 接近速度0.2米/秒
        )

        if not approach_success:
            print("❌ 接近目标失败，无法继续执行")
            return

        print("✅ 已成功接近目标")
        time.sleep(1)  # 短暂暂停

        # 步骤3：手臂移动到抓取位置
        print("\n3. 手臂移动到抓取位置...")
        move_success = grasp_strategy.arm_move_to_target(
            box_info,
            arm_mode="manipulation_mpc"
        )

        if not move_success:
            print("❌ 手臂移动失败，无法继续执行")
            return

        print("✅ 手臂已到达抓取位置")
        # grasp_strategy.robot.arm_reset()
        time.sleep(1.0)  # 短暂暂停


        # 步骤4：提起箱子
        print("\n4. 提起箱子...")
        transport_up_success = grasp_strategy.arm_transport_target_up(
            box_info,
            arm_mode="manipulation_mpc"
        )

        if not transport_up_success:
            print("❌ 提起箱子失败")
            return
        time.sleep(1.0)  # 短暂暂停

        print("✅ 成功提起箱子")
        # grasp_strategy.robot.arm_reset()
        time.sleep(1.0)  # 展示一下成功提起的状态

        # 步骤5：移动到放置位置
        print("\n5. 移动到放置位置...")
        move_success = grasp_strategy.walk_to_pose(
            placement_box_info,
            target_distance=0.6,
            approach_speed=0.2,
        )
        if not move_success:
            print("❌ 移动到放置位置失败")
            return
        time.sleep(1.0)  # 短暂暂停
        # 步骤6：放下箱子
        print("\n6. 放下箱子...")
        transport_down_success = grasp_strategy.arm_transport_target_down(
            placement_box_info,
            arm_mode="manipulation_mpc"
        )

        if not transport_down_success:
            print("❌ 放下箱子失败")
            return

        print("✅ 成功放下箱子")
        time.sleep(1.0)  # 短暂暂停
        grasp_strategy.robot.arm_reset()

        print("\n========== 箱子抓取任务完成 ==========")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 确保机器人回到安全状态
        print("将机器人恢复到安全姿态...")
        # 这里可以添加使机器人回到默认姿态的代码
```

if \_\_name_\_ == “_\_main_\_”:
: main()
