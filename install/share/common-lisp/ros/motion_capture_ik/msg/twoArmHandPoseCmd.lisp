; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-msg)


;//! \htmlinclude twoArmHandPoseCmd.msg.html

(cl:defclass <twoArmHandPoseCmd> (roslisp-msg-protocol:ros-message)
  ((hand_poses
    :reader hand_poses
    :initarg :hand_poses
    :type motion_capture_ik-msg:twoArmHandPose
    :initform (cl:make-instance 'motion_capture_ik-msg:twoArmHandPose))
   (use_custom_ik_param
    :reader use_custom_ik_param
    :initarg :use_custom_ik_param
    :type cl:boolean
    :initform cl:nil)
   (joint_angles_as_q0
    :reader joint_angles_as_q0
    :initarg :joint_angles_as_q0
    :type cl:boolean
    :initform cl:nil)
   (ik_param
    :reader ik_param
    :initarg :ik_param
    :type motion_capture_ik-msg:ikSolveParam
    :initform (cl:make-instance 'motion_capture_ik-msg:ikSolveParam)))
)

(cl:defclass twoArmHandPoseCmd (<twoArmHandPoseCmd>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <twoArmHandPoseCmd>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'twoArmHandPoseCmd)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-msg:<twoArmHandPoseCmd> is deprecated: use motion_capture_ik-msg:twoArmHandPoseCmd instead.")))

(cl:ensure-generic-function 'hand_poses-val :lambda-list '(m))
(cl:defmethod hand_poses-val ((m <twoArmHandPoseCmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:hand_poses-val is deprecated.  Use motion_capture_ik-msg:hand_poses instead.")
  (hand_poses m))

(cl:ensure-generic-function 'use_custom_ik_param-val :lambda-list '(m))
(cl:defmethod use_custom_ik_param-val ((m <twoArmHandPoseCmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:use_custom_ik_param-val is deprecated.  Use motion_capture_ik-msg:use_custom_ik_param instead.")
  (use_custom_ik_param m))

(cl:ensure-generic-function 'joint_angles_as_q0-val :lambda-list '(m))
(cl:defmethod joint_angles_as_q0-val ((m <twoArmHandPoseCmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:joint_angles_as_q0-val is deprecated.  Use motion_capture_ik-msg:joint_angles_as_q0 instead.")
  (joint_angles_as_q0 m))

(cl:ensure-generic-function 'ik_param-val :lambda-list '(m))
(cl:defmethod ik_param-val ((m <twoArmHandPoseCmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:ik_param-val is deprecated.  Use motion_capture_ik-msg:ik_param instead.")
  (ik_param m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <twoArmHandPoseCmd>) ostream)
  "Serializes a message object of type '<twoArmHandPoseCmd>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'hand_poses) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'use_custom_ik_param) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'joint_angles_as_q0) 1 0)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'ik_param) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <twoArmHandPoseCmd>) istream)
  "Deserializes a message object of type '<twoArmHandPoseCmd>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'hand_poses) istream)
    (cl:setf (cl:slot-value msg 'use_custom_ik_param) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'joint_angles_as_q0) (cl:not (cl:zerop (cl:read-byte istream))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'ik_param) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<twoArmHandPoseCmd>)))
  "Returns string type for a message object of type '<twoArmHandPoseCmd>"
  "motion_capture_ik/twoArmHandPoseCmd")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'twoArmHandPoseCmd)))
  "Returns string type for a message object of type 'twoArmHandPoseCmd"
  "motion_capture_ik/twoArmHandPoseCmd")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<twoArmHandPoseCmd>)))
  "Returns md5sum for a message object of type '<twoArmHandPoseCmd>"
  "d4b6792a6f960bea428fd7158220110b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'twoArmHandPoseCmd)))
  "Returns md5sum for a message object of type 'twoArmHandPoseCmd"
  "d4b6792a6f960bea428fd7158220110b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<twoArmHandPoseCmd>)))
  "Returns full string definition for message of type '<twoArmHandPoseCmd>"
  (cl:format cl:nil "twoArmHandPose  hand_poses~%# params for the IK solver~%bool use_custom_ik_param~%bool joint_angles_as_q0~%ikSolveParam ik_param~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%================================================================================~%MSG: motion_capture_ik/ikSolveParam~%# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'twoArmHandPoseCmd)))
  "Returns full string definition for message of type 'twoArmHandPoseCmd"
  (cl:format cl:nil "twoArmHandPose  hand_poses~%# params for the IK solver~%bool use_custom_ik_param~%bool joint_angles_as_q0~%ikSolveParam ik_param~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%================================================================================~%MSG: motion_capture_ik/ikSolveParam~%# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <twoArmHandPoseCmd>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'hand_poses))
     1
     1
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'ik_param))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <twoArmHandPoseCmd>))
  "Converts a ROS message object to a list"
  (cl:list 'twoArmHandPoseCmd
    (cl:cons ':hand_poses (hand_poses msg))
    (cl:cons ':use_custom_ik_param (use_custom_ik_param msg))
    (cl:cons ':joint_angles_as_q0 (joint_angles_as_q0 msg))
    (cl:cons ':ik_param (ik_param msg))
))
