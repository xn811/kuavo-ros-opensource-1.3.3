; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude gaitTimeName.msg.html

(cl:defclass <gaitTimeName> (roslisp-msg-protocol:ros-message)
  ((start_time
    :reader start_time
    :initarg :start_time
    :type cl:float
    :initform 0.0)
   (gait_name
    :reader gait_name
    :initarg :gait_name
    :type cl:string
    :initform ""))
)

(cl:defclass gaitTimeName (<gaitTimeName>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <gaitTimeName>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'gaitTimeName)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<gaitTimeName> is deprecated: use kuavo_msgs-msg:gaitTimeName instead.")))

(cl:ensure-generic-function 'start_time-val :lambda-list '(m))
(cl:defmethod start_time-val ((m <gaitTimeName>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:start_time-val is deprecated.  Use kuavo_msgs-msg:start_time instead.")
  (start_time m))

(cl:ensure-generic-function 'gait_name-val :lambda-list '(m))
(cl:defmethod gait_name-val ((m <gaitTimeName>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:gait_name-val is deprecated.  Use kuavo_msgs-msg:gait_name instead.")
  (gait_name m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <gaitTimeName>) ostream)
  "Serializes a message object of type '<gaitTimeName>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'start_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'gait_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'gait_name))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <gaitTimeName>) istream)
  "Deserializes a message object of type '<gaitTimeName>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'start_time) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'gait_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'gait_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<gaitTimeName>)))
  "Returns string type for a message object of type '<gaitTimeName>"
  "kuavo_msgs/gaitTimeName")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'gaitTimeName)))
  "Returns string type for a message object of type 'gaitTimeName"
  "kuavo_msgs/gaitTimeName")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<gaitTimeName>)))
  "Returns md5sum for a message object of type '<gaitTimeName>"
  "c694c8dbb2e8c9d73614407bfe314692")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'gaitTimeName)))
  "Returns md5sum for a message object of type 'gaitTimeName"
  "c694c8dbb2e8c9d73614407bfe314692")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<gaitTimeName>)))
  "Returns full string definition for message of type '<gaitTimeName>"
  (cl:format cl:nil "float32 start_time~%string  gait_name~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'gaitTimeName)))
  "Returns full string definition for message of type 'gaitTimeName"
  (cl:format cl:nil "float32 start_time~%string  gait_name~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <gaitTimeName>))
  (cl:+ 0
     4
     4 (cl:length (cl:slot-value msg 'gait_name))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <gaitTimeName>))
  "Converts a ROS message object to a list"
  (cl:list 'gaitTimeName
    (cl:cons ':start_time (start_time msg))
    (cl:cons ':gait_name (gait_name msg))
))
