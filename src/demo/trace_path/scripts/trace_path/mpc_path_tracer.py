#!/usr/bin/env python3

import rospy
import numpy as np
import math
import time
import tf
import tf2_ros
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist, PoseStamped, Point, Quaternion, Pose, TransformStamped
from pydrake.all import MathematicalProgram
from pydrake.all import Solve, SnoptSolver
from std_msgs.msg import Bool
from enum import Enum
from std_msgs.msg import Int8

class FollowState(Enum):
    NOT_FOLLOWING = 0
    FOLLOWING = 1
    FINISHED = 2

class Utils:
    @staticmethod
    def get_yaw_from_orientation(orientation):
        """Extract yaw from a quaternion orientation"""
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        euler = tf.transformations.euler_from_quaternion(q)
        return euler[2]  # yaw
    
    @staticmethod
    def calculate_distance(point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    @staticmethod
    def calculate_angle(goal, current):
        """Calculate angle between two points"""
        return math.atan2(goal.y - current.y, goal.x - current.x)
    
    @staticmethod
    def normalize_angle(angle):
        """Normalize angle to [-pi, pi]"""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

class PathTracerBase:
    def __init__(self, node_name='path_tracer_node'):
        # ROS setup
        self.node_name = node_name
        
        
        # State variables
        self.flag_reset_start_point = True
        self.start_point_pose = None
        self.current_pose = Pose()
        self.path = Path()
   
        
        # Get frame IDs from ROS parameters
        self.robot_frame = rospy.get_param('~robot_frame', 'base_link')
        self.world_frame = rospy.get_param('~world_frame', 'odom')
        self.v_max_linear = rospy.get_param('~v_max_linear', 0.4)
        self.v_max_angular = rospy.get_param('~v_max_angular', 0.4)
        self.dt = rospy.get_param('~dt', 0.1)
        
        rospy.loginfo(f"Using frames: robot='{self.robot_frame}', world='{self.world_frame}'")
        rospy.loginfo(f"Using max linear velocity: {self.v_max_linear} m/s")
        rospy.loginfo(f"Using max angular velocity: {self.v_max_angular} rad/s")
        
        
        # TF Listener setup
        self.tf_listener = tf.TransformListener()
        self.tf_rate = rospy.Rate(100.0) # TF query rate
        self.follow_state = FollowState.NOT_FOLLOWING
        
        # ROS publishers
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.path_pub = rospy.Publisher('trace_path/path', Path, queue_size=10)
        self.realtime_path_pub = rospy.Publisher('trace_path/realtime_path', Path, queue_size=10)
        self.follow_state_pub = rospy.Publisher('trace_path/follow_state', Int8, queue_size=10)

        
        # Initialize path
        self.path.header.frame_id = self.world_frame
        self.path.header.stamp = rospy.Time.now()

        self.timer = rospy.Timer(rospy.Duration(0.1), self.publish_follow_state)
        
        # Start TF polling thread
        import threading
        self.tf_thread = threading.Thread(target=self.tf_polling)
        self.tf_thread.daemon = True
        self.tf_thread.start()

    def publish_follow_state(self, event):
        self.follow_state_pub.publish(self.follow_state.value)

    def tf_polling(self):
        """Thread function to continuously poll for robot's pose from TF"""
        while not rospy.is_shutdown():
            try:
                self.tf_listener.waitForTransform(self.world_frame, self.robot_frame, rospy.Time(0), rospy.Duration(1.0))
                (trans, rot) = self.tf_listener.lookupTransform(self.world_frame, self.robot_frame, rospy.Time(0))
                
                # Update current pose
                self.current_pose.position.x = trans[0]
                self.current_pose.position.y = trans[1]
                self.current_pose.position.z = trans[2]
                self.current_pose.orientation.x = rot[0]
                self.current_pose.orientation.y = rot[1]
                self.current_pose.orientation.z = rot[2]
                self.current_pose.orientation.w = rot[3]
                
                # Initialize start point if needed
                if self.flag_reset_start_point:
                    self.start_point_pose = Pose()
                    self.start_point_pose.position.x = trans[0]
                    self.start_point_pose.position.y = trans[1]
                    self.start_point_pose.position.z = trans[2]
                    self.start_point_pose.orientation.x = rot[0]
                    self.start_point_pose.orientation.y = rot[1]
                    self.start_point_pose.orientation.z = rot[2]
                    self.start_point_pose.orientation.w = rot[3]
                    self.flag_reset_start_point = False
                    rospy.loginfo(f"Start point initialized at: [{trans[0]:.2f}, {trans[1]:.2f}, {trans[2]:.2f}]")
                
                # Publish realtime motion trajectory
                pose_stamped = PoseStamped()
                pose_stamped.header.frame_id = self.path.header.frame_id
                pose_stamped.header.stamp = rospy.Time.now()
                pose_stamped.pose = self.current_pose
                self.path.poses.append(pose_stamped)
                self.realtime_path_pub.publish(self.path)
                
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf2_ros.TransformException) as e:
                # rospy.logwarn(f"TF Error: {e}")
                pass
            
            self.tf_rate.sleep()

    def follow(self, global_path):
        """Base implementation of path following - to be overridden by subclasses"""
        pass
    
    def set_max_linear_velocity(self, v):
        """Set maximum linear velocity"""
        self.v_max_linear = v
    
    def set_max_angular_velocity(self, v):
        """Set maximum angular velocity"""
        self.v_max_angular = v
    
    def publish_path(self, path):
        """Publish path"""
        self.path_pub.publish(path)
    
    def publish_cmd_vel(self, linear_velocity, angular_velocity):
        """Publish velocity command"""
        cmd_vel = Twist()
        cmd_vel.linear.x = linear_velocity
        cmd_vel.angular.z = angular_velocity
        self.cmd_vel_pub.publish(cmd_vel)

def transform_to_base_link(current_pose, global_point):
    """
    Transform a point from global frame (world) to robot base_link frame
    
    Both current_pose and global_point are in world coordinate frame.
    This function transforms global_point to the robot's local coordinate frame.
    """
    # Get rotation matrix from current pose quaternion
    q = [current_pose.orientation.x, current_pose.orientation.y, 
         current_pose.orientation.z, current_pose.orientation.w]
    rot_matrix = tf.transformations.quaternion_matrix(q)[:3, :3]
    
    # Create vectors for transformation
    global_vec = np.array([
        global_point.x - current_pose.position.x,
        global_point.y - current_pose.position.y,
        0.0  # Assuming planar motion
    ])
    
    # Apply inverse rotation to get coordinates in robot's local frame
    local_vec = np.linalg.inv(rot_matrix).dot(global_vec)
    
    # Set output point
    local_point = Point()
    local_point.x = local_vec[0]
    local_point.y = local_vec[1]
    local_point.z = 0.0
    
    return local_point

class MpcPathTracer(PathTracerBase):
    def __init__(self, node_name='mpc_path_tracer_node'):
        super().__init__(node_name)
        # MPC parameters
        self.NUM_KNOTS = 31  # Number of knot points
        
        # Path and control state
        self.global_path = None
        self.stop_requested = False
        
        # MPC path publisher
        self.mpc_path_pub = rospy.Publisher('trace_path/mpc/path', Path, queue_size=10)
        
        # Topic subscribers
        self.path_sub = rospy.Subscriber('~path', Path, self.path_callback)
        self.start_sub = rospy.Subscriber('~start', Bool, self.start_callback)
        self.stop_sub = rospy.Subscriber('~stop', Bool, self.stop_callback)
        
        rospy.loginfo("MPC Path Tracer initialized. Waiting for path on ~path topic.")
    
    def path_callback(self, path_msg):
        """Callback for receiving a path"""
        if len(path_msg.poses) <= 0:
            rospy.logwarn("Received empty path. Cannot use it.")
            return
        
        # Ensure the path is in the world frame
        if path_msg.header.frame_id != self.world_frame:
            rospy.logwarn(f"Received path with frame {path_msg.header.frame_id}, but expected '{self.world_frame}'. Converting...")
            path_msg.header.frame_id = self.world_frame
        
        self.global_path = path_msg
        rospy.loginfo(f"Received path with {len(path_msg.poses)} points.")
        
        # Publish the received path for visualization
        self.publish_path(self.global_path)
    
    def start_callback(self, msg):
        """Callback to start following the path"""
        if msg.data and (self.follow_state == FollowState.NOT_FOLLOWING or self.follow_state == FollowState.FINISHED):
            if self.global_path is None or len(self.global_path.poses) <= 0:
                rospy.logwarn("No path available. Load a path before starting.")
                return
            
            # Start following in a separate thread to avoid blocking
            self.stop_requested = False
            self.follow_state = FollowState.FOLLOWING
            import threading
            self.follow_thread = threading.Thread(target=self.follow, args=(self.global_path,))
            self.follow_thread.start()
            rospy.loginfo("Path following started.")
        elif msg.data and self.follow_state == FollowState.FOLLOWING:
            rospy.logwarn("Already following a path. Stop first.")
    
    def stop_callback(self, msg):
        """Callback to stop following the path"""
        if msg.data:
            self.stop_requested = True
            rospy.loginfo("Stop requested. Stopping path following...")
    
    def follow(self, global_path):
        """Follow a given path using MPC control.
        
        Args:
            global_path (nav_msgs.msg.Path): The path to follow
        """
        rate = rospy.Rate(1)  # Control frequency

        # Wait for start point to be set
        self.flag_reset_start_point = True
        while not rospy.is_shutdown() and self.flag_reset_start_point:
            rate.sleep()
            rospy.loginfo("Waiting for start point...")

        # Validate path
        if len(global_path.poses) <= 0:
            self.follow_state = FollowState.NOT_FOLLOWING
            return

        # First publish the path for visualization
        self.publish_path(global_path)

        # Log path info
        rospy.loginfo("-------------------------------------------------------")
        rospy.loginfo(f"Path Start Pose:\n{global_path.poses[0].pose}")
        rospy.loginfo("-------------------------------------------------------")
        rospy.loginfo(f"Path End Pose:\n{global_path.poses[-1].pose}")
        rospy.loginfo("-------------------------------------------------------")
        rospy.loginfo(f"Current yaw: {Utils.get_yaw_from_orientation(self.current_pose.orientation)}")
        rospy.loginfo(f"Path Point Counts: {len(global_path.poses)}")

        # Path end point
        goal_pose = global_path.poses[-1].pose.position

        # MPC control loop
        point_counts = len(global_path.poses)
        index = 0
        unchanged_count = 0
        kNextPointUnchangedThreshold = 10  # Threshold to prevent robot from getting stuck

        while not rospy.is_shutdown() and index < point_counts and not self.stop_requested:
            # Find closest path point to current robot position considering yaw
            min_index = index
            min_cost = float('inf')
            yaw_weight = 0.5  # Weight for yaw difference in cost function

            for i in range(min_index, min(index + self.NUM_KNOTS, point_counts)):
                distance = Utils.calculate_distance(self.current_pose.position, global_path.poses[i].pose.position)
                ref_yaw = Utils.get_yaw_from_orientation(global_path.poses[i].pose.orientation)
                current_yaw = Utils.get_yaw_from_orientation(self.current_pose.orientation)
                yaw_diff = abs(Utils.normalize_angle(current_yaw - ref_yaw))

                # Calculate composite cost
                cost = distance * distance + yaw_weight * yaw_diff * yaw_diff
                if cost < min_cost:
                    min_cost = cost
                    min_index = i

            # Update index and check if stuck
            if min_index == index:
                unchanged_count += 1
            else:
                unchanged_count = 0

            index = min_index

            # Prevent robot from getting stuck
            if unchanged_count >= kNextPointUnchangedThreshold:
                unchanged_count = 0
                if index < point_counts:
                    index += 1
                else:
                    rospy.loginfo("Unable to find a path to the next point. Aborting...")
                    self.follow_state = FollowState.NOT_FOLLOWING
                    break

            # Check if reached goal
            current_yaw = Utils.get_yaw_from_orientation(self.current_pose.orientation)
            goal_yaw = Utils.get_yaw_from_orientation(global_path.poses[-1].pose.orientation)
            yaw_error = abs(Utils.normalize_angle(current_yaw - goal_yaw))
            
            if (0.1 > Utils.calculate_distance(goal_pose, self.current_pose.position) and 
                index >= point_counts - 2 and
                yaw_error < 0.03):
                rospy.loginfo("Stop moving...")
                self.publish_cmd_vel(0, 0)
                self.follow_state = FollowState.FINISHED
                break

            # Add deceleration near goal
            distance_to_goal = Utils.calculate_distance(goal_pose, self.current_pose.position)
            deceleration_distance = 1.0
            deceleration_angular_distance = 0.785
            linear_velocity_scale = 1.0
            angular_velocity_scale = 1.0

            if distance_to_goal < deceleration_distance:
                linear_velocity_scale = max(0.3, distance_to_goal / deceleration_distance)
            
            if yaw_error < deceleration_angular_distance:
                angular_velocity_scale = max(0.3, yaw_error / deceleration_angular_distance)

            # Transform reference trajectory to base_link frame
            ref_x = np.zeros(self.NUM_KNOTS)
            ref_y = np.zeros(self.NUM_KNOTS)
            ref_yaw = np.zeros(self.NUM_KNOTS)

            for i in range(self.NUM_KNOTS):
                global_index = min(index + i, point_counts - 1)
                local_point = transform_to_base_link(self.current_pose, global_path.poses[global_index].pose.position)
                ref_x[i] = local_point.x
                ref_y[i] = local_point.y
                ref_yaw[i] = Utils.normalize_angle(Utils.get_yaw_from_orientation(global_path.poses[global_index].pose.orientation) - current_yaw)

            # Setup MPC optimization problem
            prog = MathematicalProgram()

            # Decision variables
            x = prog.NewContinuousVariables(self.NUM_KNOTS, "x")
            y = prog.NewContinuousVariables(self.NUM_KNOTS, "y")
            yaw = prog.NewContinuousVariables(self.NUM_KNOTS, "yaw")
            v = prog.NewContinuousVariables(self.NUM_KNOTS, "v")
            yaw_dot = prog.NewContinuousVariables(self.NUM_KNOTS, "yaw_dot")

            # Initial constraints
            prog.AddBoundingBoxConstraint(0.0, 0.0, x[0])
            prog.AddBoundingBoxConstraint(0.0, 0.0, y[0])
            prog.AddBoundingBoxConstraint(0.0, 0.0, yaw[0])

            # Velocity constraints
            for i in range(self.NUM_KNOTS):
                prog.AddBoundingBoxConstraint(-self.v_max_linear, self.v_max_linear, v[i])
                prog.AddBoundingBoxConstraint(-self.v_max_angular, self.v_max_angular, yaw_dot[i])

            # Dynamic constraints
            dt = 0.1  # Time step
            for i in range(self.NUM_KNOTS - 1):
                prog.AddConstraint(x[i + 1] == x[i] + v[i] * np.cos(yaw[i]) * dt)
                prog.AddConstraint(y[i + 1] == y[i] + v[i] * np.sin(yaw[i]) * dt)
                prog.AddConstraint(yaw[i + 1] == yaw[i] + yaw_dot[i] * dt)

            # Cost function
            for i in range(self.NUM_KNOTS):
                prog.AddQuadraticCost((x[i] - ref_x[i])**2 + (y[i] - ref_y[i])**2)
                prog.AddQuadraticCost(0.6 * (yaw[i] - ref_yaw[i])**2)
                prog.AddQuadraticCost(0.1 * v[i]**2)
                prog.AddQuadraticCost(0.2 * yaw_dot[i]**2)

            # Solve optimization problem
            solver = SnoptSolver()
            result = Solve(prog)

            if result.is_success():
                optimal_x = result.GetSolution(x)
                optimal_y = result.GetSolution(y)
                optimal_yaw = result.GetSolution(yaw)
                optimal_v = result.GetSolution(v)
                optimal_yaw_dot = result.GetSolution(yaw_dot)

                # Apply velocity scaling
                scaled_v = optimal_v[0] * linear_velocity_scale
                scaled_yaw_dot = optimal_yaw_dot[0] * angular_velocity_scale

                # Publish control commands
                self.publish_cmd_vel(scaled_v, scaled_yaw_dot)

                # Publish MPC path for visualization
                self.publish_mpc_path(optimal_x, optimal_y, optimal_yaw)
            else:
                rospy.logerr(f"Optimization failed to find a solution: {result.get_solution_result()}")
                self.follow_state = FollowState.NOT_FOLLOWING
                break

            # Publish fixed path
            self.publish_path(global_path)
            rospy.sleep(dt)

        # Handle stop request
        if self.stop_requested:
            self.follow_state = FollowState.NOT_FOLLOWING
            self.stop_requested = False
            
        rospy.sleep(1.5)
        rospy.loginfo("Path Follower Finished!")
        self.publish_cmd_vel(0, 0)  # Ensure robot stops
        rospy.loginfo("Stop moving...")
        rospy.loginfo(f"Current pose:\n{self.current_pose}")
        
        # If we didn't explicitly set the state to FINISHED or NOT_FOLLOWING due to stop request,
        # set it based on whether we reached the end of the path
        if self.follow_state == FollowState.FOLLOWING:
            if index >= point_counts - 1:
                self.follow_state = FollowState.FINISHED
            else:
                self.follow_state = FollowState.NOT_FOLLOWING

    def publish_mpc_path(self, x, y, yaw):
        # Create a path message
        mpc_path = Path()
        mpc_path.header.stamp = rospy.Time.now()
        mpc_path.header.frame_id = self.world_frame
        
        # Get current robot pose
        q = [self.current_pose.orientation.x, self.current_pose.orientation.y,
             self.current_pose.orientation.z, self.current_pose.orientation.w]
        rot_matrix = tf.transformations.quaternion_matrix(q)[:3, :3]
        
        # Get current robot yaw
        current_yaw = Utils.get_yaw_from_orientation(self.current_pose.orientation)
        
        # Iterate through all optimization results
        for i in range(self.NUM_KNOTS):
            # Transform points from local to global coordinate system
            local_vec = np.array([x[i], y[i], 0.0])
            global_vec = rot_matrix.dot(local_vec) + np.array([
                self.current_pose.position.x,
                self.current_pose.position.y,
                0.0
            ])
            
            # Create a new path point
            pose_stamped = PoseStamped()
            pose_stamped.header = mpc_path.header
            pose_stamped.pose.position.x = global_vec[0]
            pose_stamped.pose.position.y = global_vec[1]
            pose_stamped.pose.position.z = 0.3
            
            # Convert local yaw to global yaw
            global_yaw = yaw[i] + current_yaw
            
            # Set orientation
            q = tf.transformations.quaternion_from_euler(0, 0, global_yaw)
            pose_stamped.pose.orientation.x = q[0]
            pose_stamped.pose.orientation.y = q[1]
            pose_stamped.pose.orientation.z = q[2]
            pose_stamped.pose.orientation.w = q[3]
            
            # Add to path message
            mpc_path.poses.append(pose_stamped)
        
        # Publish path
        self.mpc_path_pub.publish(mpc_path)

if __name__ == "__main__":
    try:
        rospy.init_node('mpc_path_tracer_node')
        tracer = MpcPathTracer()
        rospy.loginfo("MPC Path Tracer node started. Waiting for path on ~path topic...")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
