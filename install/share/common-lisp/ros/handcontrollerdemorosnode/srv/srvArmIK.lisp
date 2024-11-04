; Auto-generated. Do not edit!


(cl:in-package handcontrollerdemorosnode-srv)


;//! \htmlinclude srvArmIK-request.msg.html

(cl:defclass <srvArmIK-request> (roslisp-msg-protocol:ros-message)
  ((left_arm_pose
    :reader left_arm_pose
    :initarg :left_arm_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (right_arm_pose
    :reader right_arm_pose
    :initarg :right_arm_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass srvArmIK-request (<srvArmIK-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <srvArmIK-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'srvArmIK-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name handcontrollerdemorosnode-srv:<srvArmIK-request> is deprecated: use handcontrollerdemorosnode-srv:srvArmIK-request instead.")))

(cl:ensure-generic-function 'left_arm_pose-val :lambda-list '(m))
(cl:defmethod left_arm_pose-val ((m <srvArmIK-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-srv:left_arm_pose-val is deprecated.  Use handcontrollerdemorosnode-srv:left_arm_pose instead.")
  (left_arm_pose m))

(cl:ensure-generic-function 'right_arm_pose-val :lambda-list '(m))
(cl:defmethod right_arm_pose-val ((m <srvArmIK-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-srv:right_arm_pose-val is deprecated.  Use handcontrollerdemorosnode-srv:right_arm_pose instead.")
  (right_arm_pose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <srvArmIK-request>) ostream)
  "Serializes a message object of type '<srvArmIK-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'left_arm_pose))))
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
   (cl:slot-value msg 'left_arm_pose))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'right_arm_pose))))
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
   (cl:slot-value msg 'right_arm_pose))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <srvArmIK-request>) istream)
  "Deserializes a message object of type '<srvArmIK-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'left_arm_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'left_arm_pose)))
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
  (cl:setf (cl:slot-value msg 'right_arm_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'right_arm_pose)))
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
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<srvArmIK-request>)))
  "Returns string type for a service object of type '<srvArmIK-request>"
  "handcontrollerdemorosnode/srvArmIKRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'srvArmIK-request)))
  "Returns string type for a service object of type 'srvArmIK-request"
  "handcontrollerdemorosnode/srvArmIKRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<srvArmIK-request>)))
  "Returns md5sum for a message object of type '<srvArmIK-request>"
  "2b5b0516bd664187d5eefa858c0bc7ee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'srvArmIK-request)))
  "Returns md5sum for a message object of type 'srvArmIK-request"
  "2b5b0516bd664187d5eefa858c0bc7ee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<srvArmIK-request>)))
  "Returns full string definition for message of type '<srvArmIK-request>"
  (cl:format cl:nil "float64[] left_arm_pose~%float64[] right_arm_pose~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'srvArmIK-request)))
  "Returns full string definition for message of type 'srvArmIK-request"
  (cl:format cl:nil "float64[] left_arm_pose~%float64[] right_arm_pose~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <srvArmIK-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'left_arm_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'right_arm_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <srvArmIK-request>))
  "Converts a ROS message object to a list"
  (cl:list 'srvArmIK-request
    (cl:cons ':left_arm_pose (left_arm_pose msg))
    (cl:cons ':right_arm_pose (right_arm_pose msg))
))
;//! \htmlinclude srvArmIK-response.msg.html

(cl:defclass <srvArmIK-response> (roslisp-msg-protocol:ros-message)
  ((joint_state
    :reader joint_state
    :initarg :joint_state
    :type sensor_msgs-msg:JointState
    :initform (cl:make-instance 'sensor_msgs-msg:JointState)))
)

(cl:defclass srvArmIK-response (<srvArmIK-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <srvArmIK-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'srvArmIK-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name handcontrollerdemorosnode-srv:<srvArmIK-response> is deprecated: use handcontrollerdemorosnode-srv:srvArmIK-response instead.")))

(cl:ensure-generic-function 'joint_state-val :lambda-list '(m))
(cl:defmethod joint_state-val ((m <srvArmIK-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-srv:joint_state-val is deprecated.  Use handcontrollerdemorosnode-srv:joint_state instead.")
  (joint_state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <srvArmIK-response>) ostream)
  "Serializes a message object of type '<srvArmIK-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'joint_state) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <srvArmIK-response>) istream)
  "Deserializes a message object of type '<srvArmIK-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'joint_state) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<srvArmIK-response>)))
  "Returns string type for a service object of type '<srvArmIK-response>"
  "handcontrollerdemorosnode/srvArmIKResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'srvArmIK-response)))
  "Returns string type for a service object of type 'srvArmIK-response"
  "handcontrollerdemorosnode/srvArmIKResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<srvArmIK-response>)))
  "Returns md5sum for a message object of type '<srvArmIK-response>"
  "2b5b0516bd664187d5eefa858c0bc7ee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'srvArmIK-response)))
  "Returns md5sum for a message object of type 'srvArmIK-response"
  "2b5b0516bd664187d5eefa858c0bc7ee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<srvArmIK-response>)))
  "Returns full string definition for message of type '<srvArmIK-response>"
  (cl:format cl:nil "sensor_msgs/JointState joint_state~%~%~%================================================================================~%MSG: sensor_msgs/JointState~%# This is a message that holds data to describe the state of a set of torque controlled joints. ~%#~%# The state of each joint (revolute or prismatic) is defined by:~%#  * the position of the joint (rad or m),~%#  * the velocity of the joint (rad/s or m/s) and ~%#  * the effort that is applied in the joint (Nm or N).~%#~%# Each joint is uniquely identified by its name~%# The header specifies the time at which the joint states were recorded. All the joint states~%# in one message have to be recorded at the same time.~%#~%# This message consists of a multiple arrays, one for each part of the joint state. ~%# The goal is to make each of the fields optional. When e.g. your joints have no~%# effort associated with them, you can leave the effort array empty. ~%#~%# All arrays in this message should have the same size, or be empty.~%# This is the only way to uniquely associate the joint name with the correct~%# states.~%~%~%Header header~%~%string[] name~%float64[] position~%float64[] velocity~%float64[] effort~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'srvArmIK-response)))
  "Returns full string definition for message of type 'srvArmIK-response"
  (cl:format cl:nil "sensor_msgs/JointState joint_state~%~%~%================================================================================~%MSG: sensor_msgs/JointState~%# This is a message that holds data to describe the state of a set of torque controlled joints. ~%#~%# The state of each joint (revolute or prismatic) is defined by:~%#  * the position of the joint (rad or m),~%#  * the velocity of the joint (rad/s or m/s) and ~%#  * the effort that is applied in the joint (Nm or N).~%#~%# Each joint is uniquely identified by its name~%# The header specifies the time at which the joint states were recorded. All the joint states~%# in one message have to be recorded at the same time.~%#~%# This message consists of a multiple arrays, one for each part of the joint state. ~%# The goal is to make each of the fields optional. When e.g. your joints have no~%# effort associated with them, you can leave the effort array empty. ~%#~%# All arrays in this message should have the same size, or be empty.~%# This is the only way to uniquely associate the joint name with the correct~%# states.~%~%~%Header header~%~%string[] name~%float64[] position~%float64[] velocity~%float64[] effort~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <srvArmIK-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'joint_state))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <srvArmIK-response>))
  "Converts a ROS message object to a list"
  (cl:list 'srvArmIK-response
    (cl:cons ':joint_state (joint_state msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'srvArmIK)))
  'srvArmIK-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'srvArmIK)))
  'srvArmIK-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'srvArmIK)))
  "Returns string type for a service object of type '<srvArmIK>"
  "handcontrollerdemorosnode/srvArmIK")