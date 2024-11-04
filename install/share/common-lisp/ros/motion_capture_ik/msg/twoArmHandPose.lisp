; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-msg)


;//! \htmlinclude twoArmHandPose.msg.html

(cl:defclass <twoArmHandPose> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (left_pose
    :reader left_pose
    :initarg :left_pose
    :type motion_capture_ik-msg:armHandPose
    :initform (cl:make-instance 'motion_capture_ik-msg:armHandPose))
   (right_pose
    :reader right_pose
    :initarg :right_pose
    :type motion_capture_ik-msg:armHandPose
    :initform (cl:make-instance 'motion_capture_ik-msg:armHandPose)))
)

(cl:defclass twoArmHandPose (<twoArmHandPose>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <twoArmHandPose>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'twoArmHandPose)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-msg:<twoArmHandPose> is deprecated: use motion_capture_ik-msg:twoArmHandPose instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <twoArmHandPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:header-val is deprecated.  Use motion_capture_ik-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'left_pose-val :lambda-list '(m))
(cl:defmethod left_pose-val ((m <twoArmHandPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:left_pose-val is deprecated.  Use motion_capture_ik-msg:left_pose instead.")
  (left_pose m))

(cl:ensure-generic-function 'right_pose-val :lambda-list '(m))
(cl:defmethod right_pose-val ((m <twoArmHandPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:right_pose-val is deprecated.  Use motion_capture_ik-msg:right_pose instead.")
  (right_pose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <twoArmHandPose>) ostream)
  "Serializes a message object of type '<twoArmHandPose>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'left_pose) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'right_pose) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <twoArmHandPose>) istream)
  "Deserializes a message object of type '<twoArmHandPose>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'left_pose) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'right_pose) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<twoArmHandPose>)))
  "Returns string type for a message object of type '<twoArmHandPose>"
  "motion_capture_ik/twoArmHandPose")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'twoArmHandPose)))
  "Returns string type for a message object of type 'twoArmHandPose"
  "motion_capture_ik/twoArmHandPose")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<twoArmHandPose>)))
  "Returns md5sum for a message object of type '<twoArmHandPose>"
  "5bdb1e027f430369b6f88e5e2f5d31ca")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'twoArmHandPose)))
  "Returns md5sum for a message object of type 'twoArmHandPose"
  "5bdb1e027f430369b6f88e5e2f5d31ca")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<twoArmHandPose>)))
  "Returns full string definition for message of type '<twoArmHandPose>"
  (cl:format cl:nil "Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'twoArmHandPose)))
  "Returns full string definition for message of type 'twoArmHandPose"
  (cl:format cl:nil "Header header~%armHandPose  left_pose~%armHandPose  right_pose~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: motion_capture_ik/armHandPose~%float64[3] pos_xyz~%float64[4] quat_xyzw~%~%float64[3] elbow_pos_xyz~%~%float64[7] joint_angles~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <twoArmHandPose>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'left_pose))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'right_pose))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <twoArmHandPose>))
  "Converts a ROS message object to a list"
  (cl:list 'twoArmHandPose
    (cl:cons ':header (header msg))
    (cl:cons ':left_pose (left_pose msg))
    (cl:cons ':right_pose (right_pose msg))
))
