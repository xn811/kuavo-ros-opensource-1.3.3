; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude sensorsData.msg.html

(cl:defclass <sensorsData> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (sensor_time
    :reader sensor_time
    :initarg :sensor_time
    :type cl:real
    :initform 0)
   (joint_data
    :reader joint_data
    :initarg :joint_data
    :type kuavo_msgs-msg:jointData
    :initform (cl:make-instance 'kuavo_msgs-msg:jointData))
   (imu_data
    :reader imu_data
    :initarg :imu_data
    :type kuavo_msgs-msg:imuData
    :initform (cl:make-instance 'kuavo_msgs-msg:imuData))
   (end_effector_data
    :reader end_effector_data
    :initarg :end_effector_data
    :type kuavo_msgs-msg:endEffectorData
    :initform (cl:make-instance 'kuavo_msgs-msg:endEffectorData)))
)

(cl:defclass sensorsData (<sensorsData>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <sensorsData>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'sensorsData)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<sensorsData> is deprecated: use kuavo_msgs-msg:sensorsData instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <sensorsData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:header-val is deprecated.  Use kuavo_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'sensor_time-val :lambda-list '(m))
(cl:defmethod sensor_time-val ((m <sensorsData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:sensor_time-val is deprecated.  Use kuavo_msgs-msg:sensor_time instead.")
  (sensor_time m))

(cl:ensure-generic-function 'joint_data-val :lambda-list '(m))
(cl:defmethod joint_data-val ((m <sensorsData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:joint_data-val is deprecated.  Use kuavo_msgs-msg:joint_data instead.")
  (joint_data m))

(cl:ensure-generic-function 'imu_data-val :lambda-list '(m))
(cl:defmethod imu_data-val ((m <sensorsData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:imu_data-val is deprecated.  Use kuavo_msgs-msg:imu_data instead.")
  (imu_data m))

(cl:ensure-generic-function 'end_effector_data-val :lambda-list '(m))
(cl:defmethod end_effector_data-val ((m <sensorsData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:end_effector_data-val is deprecated.  Use kuavo_msgs-msg:end_effector_data instead.")
  (end_effector_data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <sensorsData>) ostream)
  "Serializes a message object of type '<sensorsData>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'sensor_time)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'sensor_time) (cl:floor (cl:slot-value msg 'sensor_time)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'joint_data) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'imu_data) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'end_effector_data) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <sensorsData>) istream)
  "Deserializes a message object of type '<sensorsData>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'sensor_time) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'joint_data) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'imu_data) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'end_effector_data) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<sensorsData>)))
  "Returns string type for a message object of type '<sensorsData>"
  "kuavo_msgs/sensorsData")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'sensorsData)))
  "Returns string type for a message object of type 'sensorsData"
  "kuavo_msgs/sensorsData")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<sensorsData>)))
  "Returns md5sum for a message object of type '<sensorsData>"
  "54439d3ac2ef33d46fd7cf6d324860c3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'sensorsData)))
  "Returns md5sum for a message object of type 'sensorsData"
  "54439d3ac2ef33d46fd7cf6d324860c3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<sensorsData>)))
  "Returns full string definition for message of type '<sensorsData>"
  (cl:format cl:nil "std_msgs/Header header~%time sensor_time~%kuavo_msgs/jointData joint_data~%kuavo_msgs/imuData imu_data~%kuavo_msgs/endEffectorData end_effector_data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: kuavo_msgs/jointData~%float64[] joint_q  ~%float64[] joint_v  ~%float64[] joint_vd    ~%float64[] joint_current  ~%~%================================================================================~%MSG: kuavo_msgs/imuData~%geometry_msgs/Vector3 gyro    #陀螺仪数据~%geometry_msgs/Vector3 acc     #加速计数据~%geometry_msgs/Vector3 free_acc    #无重力加速度数据~%geometry_msgs/Quaternion quat    #四元数数据~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: kuavo_msgs/endEffectorData~%string[] name  ~%float64[] position~%float64[] velocity  ~%float64[] effort~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'sensorsData)))
  "Returns full string definition for message of type 'sensorsData"
  (cl:format cl:nil "std_msgs/Header header~%time sensor_time~%kuavo_msgs/jointData joint_data~%kuavo_msgs/imuData imu_data~%kuavo_msgs/endEffectorData end_effector_data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: kuavo_msgs/jointData~%float64[] joint_q  ~%float64[] joint_v  ~%float64[] joint_vd    ~%float64[] joint_current  ~%~%================================================================================~%MSG: kuavo_msgs/imuData~%geometry_msgs/Vector3 gyro    #陀螺仪数据~%geometry_msgs/Vector3 acc     #加速计数据~%geometry_msgs/Vector3 free_acc    #无重力加速度数据~%geometry_msgs/Quaternion quat    #四元数数据~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: kuavo_msgs/endEffectorData~%string[] name  ~%float64[] position~%float64[] velocity  ~%float64[] effort~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <sensorsData>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'joint_data))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'imu_data))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'end_effector_data))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <sensorsData>))
  "Converts a ROS message object to a list"
  (cl:list 'sensorsData
    (cl:cons ':header (header msg))
    (cl:cons ':sensor_time (sensor_time msg))
    (cl:cons ':joint_data (joint_data msg))
    (cl:cons ':imu_data (imu_data msg))
    (cl:cons ':end_effector_data (end_effector_data msg))
))
