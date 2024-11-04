; Auto-generated. Do not edit!


(cl:in-package kuavo_ros_interfaces-msg)


;//! \htmlinclude planArmState.msg.html

(cl:defclass <planArmState> (roslisp-msg-protocol:ros-message)
  ((progress
    :reader progress
    :initarg :progress
    :type cl:integer
    :initform 0)
   (is_finished
    :reader is_finished
    :initarg :is_finished
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass planArmState (<planArmState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <planArmState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'planArmState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-msg:<planArmState> is deprecated: use kuavo_ros_interfaces-msg:planArmState instead.")))

(cl:ensure-generic-function 'progress-val :lambda-list '(m))
(cl:defmethod progress-val ((m <planArmState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-msg:progress-val is deprecated.  Use kuavo_ros_interfaces-msg:progress instead.")
  (progress m))

(cl:ensure-generic-function 'is_finished-val :lambda-list '(m))
(cl:defmethod is_finished-val ((m <planArmState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-msg:is_finished-val is deprecated.  Use kuavo_ros_interfaces-msg:is_finished instead.")
  (is_finished m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <planArmState>) ostream)
  "Serializes a message object of type '<planArmState>"
  (cl:let* ((signed (cl:slot-value msg 'progress)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_finished) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <planArmState>) istream)
  "Deserializes a message object of type '<planArmState>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'progress) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:setf (cl:slot-value msg 'is_finished) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<planArmState>)))
  "Returns string type for a message object of type '<planArmState>"
  "kuavo_ros_interfaces/planArmState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'planArmState)))
  "Returns string type for a message object of type 'planArmState"
  "kuavo_ros_interfaces/planArmState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<planArmState>)))
  "Returns md5sum for a message object of type '<planArmState>"
  "0743feb5221b176f512f6ea58920b201")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'planArmState)))
  "Returns md5sum for a message object of type 'planArmState"
  "0743feb5221b176f512f6ea58920b201")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<planArmState>)))
  "Returns full string definition for message of type '<planArmState>"
  (cl:format cl:nil "int32 progress~%bool is_finished~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'planArmState)))
  "Returns full string definition for message of type 'planArmState"
  (cl:format cl:nil "int32 progress~%bool is_finished~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <planArmState>))
  (cl:+ 0
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <planArmState>))
  "Converts a ROS message object to a list"
  (cl:list 'planArmState
    (cl:cons ':progress (progress msg))
    (cl:cons ':is_finished (is_finished msg))
))
