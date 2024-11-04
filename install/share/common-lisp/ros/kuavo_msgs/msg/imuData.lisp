; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude imuData.msg.html

(cl:defclass <imuData> (roslisp-msg-protocol:ros-message)
  ((gyro
    :reader gyro
    :initarg :gyro
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (acc
    :reader acc
    :initarg :acc
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (free_acc
    :reader free_acc
    :initarg :free_acc
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (quat
    :reader quat
    :initarg :quat
    :type geometry_msgs-msg:Quaternion
    :initform (cl:make-instance 'geometry_msgs-msg:Quaternion)))
)

(cl:defclass imuData (<imuData>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <imuData>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'imuData)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<imuData> is deprecated: use kuavo_msgs-msg:imuData instead.")))

(cl:ensure-generic-function 'gyro-val :lambda-list '(m))
(cl:defmethod gyro-val ((m <imuData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:gyro-val is deprecated.  Use kuavo_msgs-msg:gyro instead.")
  (gyro m))

(cl:ensure-generic-function 'acc-val :lambda-list '(m))
(cl:defmethod acc-val ((m <imuData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:acc-val is deprecated.  Use kuavo_msgs-msg:acc instead.")
  (acc m))

(cl:ensure-generic-function 'free_acc-val :lambda-list '(m))
(cl:defmethod free_acc-val ((m <imuData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:free_acc-val is deprecated.  Use kuavo_msgs-msg:free_acc instead.")
  (free_acc m))

(cl:ensure-generic-function 'quat-val :lambda-list '(m))
(cl:defmethod quat-val ((m <imuData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:quat-val is deprecated.  Use kuavo_msgs-msg:quat instead.")
  (quat m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <imuData>) ostream)
  "Serializes a message object of type '<imuData>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'gyro) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'acc) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'free_acc) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'quat) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <imuData>) istream)
  "Deserializes a message object of type '<imuData>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'gyro) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'acc) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'free_acc) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'quat) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<imuData>)))
  "Returns string type for a message object of type '<imuData>"
  "kuavo_msgs/imuData")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'imuData)))
  "Returns string type for a message object of type 'imuData"
  "kuavo_msgs/imuData")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<imuData>)))
  "Returns md5sum for a message object of type '<imuData>"
  "6406067cf839b39a677ae809cd04646a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'imuData)))
  "Returns md5sum for a message object of type 'imuData"
  "6406067cf839b39a677ae809cd04646a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<imuData>)))
  "Returns full string definition for message of type '<imuData>"
  (cl:format cl:nil "geometry_msgs/Vector3 gyro    #陀螺仪数据~%geometry_msgs/Vector3 acc     #加速计数据~%geometry_msgs/Vector3 free_acc    #无重力加速度数据~%geometry_msgs/Quaternion quat    #四元数数据~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'imuData)))
  "Returns full string definition for message of type 'imuData"
  (cl:format cl:nil "geometry_msgs/Vector3 gyro    #陀螺仪数据~%geometry_msgs/Vector3 acc     #加速计数据~%geometry_msgs/Vector3 free_acc    #无重力加速度数据~%geometry_msgs/Quaternion quat    #四元数数据~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <imuData>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'gyro))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'acc))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'free_acc))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'quat))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <imuData>))
  "Converts a ROS message object to a list"
  (cl:list 'imuData
    (cl:cons ':gyro (gyro msg))
    (cl:cons ':acc (acc msg))
    (cl:cons ':free_acc (free_acc msg))
    (cl:cons ':quat (quat msg))
))
