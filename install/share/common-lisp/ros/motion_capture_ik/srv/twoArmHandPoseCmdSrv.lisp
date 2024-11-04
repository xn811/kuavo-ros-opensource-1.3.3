; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-srv)


;//! \htmlinclude twoArmHandPoseCmdSrv-request.msg.html

(cl:defclass <twoArmHandPoseCmdSrv-request> (roslisp-msg-protocol:ros-message)
  ((twoArmHandPoseCmdRequest
    :reader twoArmHandPoseCmdRequest
    :initarg :twoArmHandPoseCmdRequest
    :type motion_capture_ik-msg:twoArmHandPoseCmd
    :initform (cl:make-instance 'motion_capture_ik-msg:twoArmHandPoseCmd)))
)

(cl:defclass twoArmHandPoseCmdSrv-request (<twoArmHandPoseCmdSrv-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <twoArmHandPoseCmdSrv-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'twoArmHandPoseCmdSrv-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-srv:<twoArmHandPoseCmdSrv-request> is deprecated: use motion_capture_ik-srv:twoArmHandPoseCmdSrv-request instead.")))

(cl:ensure-generic-function 'twoArmHandPoseCmdRequest-val :lambda-list '(m))
(cl:defmethod twoArmHandPoseCmdRequest-val ((m <twoArmHandPoseCmdSrv-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:twoArmHandPoseCmdRequest-val is deprecated.  Use motion_capture_ik-srv:twoArmHandPoseCmdRequest instead.")
  (twoArmHandPoseCmdRequest m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <twoArmHandPoseCmdSrv-request>) ostream)
  "Serializes a message object of type '<twoArmHandPoseCmdSrv-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'twoArmHandPoseCmdRequest) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <twoArmHandPoseCmdSrv-request>) istream)
  "Deserializes a message object of type '<twoArmHandPoseCmdSrv-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'twoArmHandPoseCmdRequest) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<twoArmHandPoseCmdSrv-request>)))
  "Returns string type for a service object of type '<twoArmHandPoseCmdSrv-request>"
  "motion_capture_ik/twoArmHandPoseCmdSrvRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'twoArmHandPoseCmdSrv-request)))
  "Returns string type for a service object of type 'twoArmHandPoseCmdSrv-request"
  "motion_capture_ik/twoArmHandPoseCmdSrvRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<twoArmHandPoseCmdSrv-request>)))
  "Returns md5sum for a message object of type '<twoArmHandPoseCmdSrv-request>"
  "4cedfbf98f38ce7e92b358cb2d3ef39d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'twoArmHandPoseCmdSrv-request)))
  "Returns md5sum for a message object of type 'twoArmHandPoseCmdSrv-request"
  "4cedfbf98f38ce7e92b358cb2d3ef39d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<twoArmHandPoseCmdSrv-request>)))
  "Returns full string definition for message of type '<twoArmHandPoseCmdSrv-request>"
  (cl:format cl:nil "twoArmHandPoseCmd twoArmHandPoseCmdRequest~%~%================================================================================~%MSG: motion_capture_ik/twoArmHandPoseCmd~%twoArmHandPose  hand_poses~%# params for the IK solver~%bool use_custom_ik_param~%bool joint_angles_as_q0~%ikSolveParam ik_param~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%================================================================================~%MSG: motion_capture_ik/ikSolveParam~%# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'twoArmHandPoseCmdSrv-request)))
  "Returns full string definition for message of type 'twoArmHandPoseCmdSrv-request"
  (cl:format cl:nil "twoArmHandPoseCmd twoArmHandPoseCmdRequest~%~%================================================================================~%MSG: motion_capture_ik/twoArmHandPoseCmd~%twoArmHandPose  hand_poses~%# params for the IK solver~%bool use_custom_ik_param~%bool joint_angles_as_q0~%ikSolveParam ik_param~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%================================================================================~%MSG: motion_capture_ik/ikSolveParam~%# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <twoArmHandPoseCmdSrv-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'twoArmHandPoseCmdRequest))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <twoArmHandPoseCmdSrv-request>))
  "Converts a ROS message object to a list"
  (cl:list 'twoArmHandPoseCmdSrv-request
    (cl:cons ':twoArmHandPoseCmdRequest (twoArmHandPoseCmdRequest msg))
))
;//! \htmlinclude twoArmHandPoseCmdSrv-response.msg.html

(cl:defclass <twoArmHandPoseCmdSrv-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (with_torso
    :reader with_torso
    :initarg :with_torso
    :type cl:boolean
    :initform cl:nil)
   (q_arm
    :reader q_arm
    :initarg :q_arm
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (q_torso
    :reader q_torso
    :initarg :q_torso
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (time_cost
    :reader time_cost
    :initarg :time_cost
    :type cl:float
    :initform 0.0)
   (hand_poses
    :reader hand_poses
    :initarg :hand_poses
    :type motion_capture_ik-msg:twoArmHandPose
    :initform (cl:make-instance 'motion_capture_ik-msg:twoArmHandPose)))
)

(cl:defclass twoArmHandPoseCmdSrv-response (<twoArmHandPoseCmdSrv-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <twoArmHandPoseCmdSrv-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'twoArmHandPoseCmdSrv-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-srv:<twoArmHandPoseCmdSrv-response> is deprecated: use motion_capture_ik-srv:twoArmHandPoseCmdSrv-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:success-val is deprecated.  Use motion_capture_ik-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'with_torso-val :lambda-list '(m))
(cl:defmethod with_torso-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:with_torso-val is deprecated.  Use motion_capture_ik-srv:with_torso instead.")
  (with_torso m))

(cl:ensure-generic-function 'q_arm-val :lambda-list '(m))
(cl:defmethod q_arm-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:q_arm-val is deprecated.  Use motion_capture_ik-srv:q_arm instead.")
  (q_arm m))

(cl:ensure-generic-function 'q_torso-val :lambda-list '(m))
(cl:defmethod q_torso-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:q_torso-val is deprecated.  Use motion_capture_ik-srv:q_torso instead.")
  (q_torso m))

(cl:ensure-generic-function 'time_cost-val :lambda-list '(m))
(cl:defmethod time_cost-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:time_cost-val is deprecated.  Use motion_capture_ik-srv:time_cost instead.")
  (time_cost m))

(cl:ensure-generic-function 'hand_poses-val :lambda-list '(m))
(cl:defmethod hand_poses-val ((m <twoArmHandPoseCmdSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:hand_poses-val is deprecated.  Use motion_capture_ik-srv:hand_poses instead.")
  (hand_poses m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <twoArmHandPoseCmdSrv-response>) ostream)
  "Serializes a message object of type '<twoArmHandPoseCmdSrv-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'with_torso) 1 0)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'q_arm))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'q_arm))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'q_torso))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'q_torso))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'time_cost))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'hand_poses) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <twoArmHandPoseCmdSrv-response>) istream)
  "Deserializes a message object of type '<twoArmHandPoseCmdSrv-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'with_torso) (cl:not (cl:zerop (cl:read-byte istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'q_arm) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'q_arm)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'q_torso) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'q_torso)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time_cost) (roslisp-utils:decode-double-float-bits bits)))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'hand_poses) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<twoArmHandPoseCmdSrv-response>)))
  "Returns string type for a service object of type '<twoArmHandPoseCmdSrv-response>"
  "motion_capture_ik/twoArmHandPoseCmdSrvResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'twoArmHandPoseCmdSrv-response)))
  "Returns string type for a service object of type 'twoArmHandPoseCmdSrv-response"
  "motion_capture_ik/twoArmHandPoseCmdSrvResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<twoArmHandPoseCmdSrv-response>)))
  "Returns md5sum for a message object of type '<twoArmHandPoseCmdSrv-response>"
  "4cedfbf98f38ce7e92b358cb2d3ef39d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'twoArmHandPoseCmdSrv-response)))
  "Returns md5sum for a message object of type 'twoArmHandPoseCmdSrv-response"
  "4cedfbf98f38ce7e92b358cb2d3ef39d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<twoArmHandPoseCmdSrv-response>)))
  "Returns full string definition for message of type '<twoArmHandPoseCmdSrv-response>"
  (cl:format cl:nil "bool success~%bool with_torso~%float64[] q_arm~%float64[] q_torso~%~%float64   time_cost # unit: ms~%# ik result~%twoArmHandPose  hand_poses~%~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'twoArmHandPoseCmdSrv-response)))
  "Returns full string definition for message of type 'twoArmHandPoseCmdSrv-response"
  (cl:format cl:nil "bool success~%bool with_torso~%float64[] q_arm~%float64[] q_torso~%~%float64   time_cost # unit: ms~%# ik result~%twoArmHandPose  hand_poses~%~%================================================================================~%MSG: motion_capture_ik/twoArmHandPose~%Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <twoArmHandPoseCmdSrv-response>))
  (cl:+ 0
     1
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'q_arm) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'q_torso) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'hand_poses))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <twoArmHandPoseCmdSrv-response>))
  "Converts a ROS message object to a list"
  (cl:list 'twoArmHandPoseCmdSrv-response
    (cl:cons ':success (success msg))
    (cl:cons ':with_torso (with_torso msg))
    (cl:cons ':q_arm (q_arm msg))
    (cl:cons ':q_torso (q_torso msg))
    (cl:cons ':time_cost (time_cost msg))
    (cl:cons ':hand_poses (hand_poses msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'twoArmHandPoseCmdSrv)))
  'twoArmHandPoseCmdSrv-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'twoArmHandPoseCmdSrv)))
  'twoArmHandPoseCmdSrv-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'twoArmHandPoseCmdSrv)))
  "Returns string type for a service object of type '<twoArmHandPoseCmdSrv>"
  "motion_capture_ik/twoArmHandPoseCmdSrv")