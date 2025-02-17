; Auto-generated. Do not edit!


(cl:in-package humanoid_interface_ros-msg)


;//! \htmlinclude uwbdebug.msg.html

(cl:defclass <uwbdebug> (roslisp-msg-protocol:ros-message)
  ((robot_uwb_cur_x
    :reader robot_uwb_cur_x
    :initarg :robot_uwb_cur_x
    :type cl:float
    :initform 0.0)
   (robot_uwb_cur_y
    :reader robot_uwb_cur_y
    :initarg :robot_uwb_cur_y
    :type cl:float
    :initform 0.0)
   (robot_uwb_cur_angle
    :reader robot_uwb_cur_angle
    :initarg :robot_uwb_cur_angle
    :type cl:float
    :initform 0.0)
   (robot_uwb_fir_angle
    :reader robot_uwb_fir_angle
    :initarg :robot_uwb_fir_angle
    :type cl:float
    :initform 0.0)
   (robot_uwb_fir_x
    :reader robot_uwb_fir_x
    :initarg :robot_uwb_fir_x
    :type cl:float
    :initform 0.0)
   (robot_uwb_fir_y
    :reader robot_uwb_fir_y
    :initarg :robot_uwb_fir_y
    :type cl:float
    :initform 0.0)
   (robot_uwb_avr_x
    :reader robot_uwb_avr_x
    :initarg :robot_uwb_avr_x
    :type cl:float
    :initform 0.0)
   (robot_uwb_avr_y
    :reader robot_uwb_avr_y
    :initarg :robot_uwb_avr_y
    :type cl:float
    :initform 0.0))
)

(cl:defclass uwbdebug (<uwbdebug>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <uwbdebug>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'uwbdebug)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name humanoid_interface_ros-msg:<uwbdebug> is deprecated: use humanoid_interface_ros-msg:uwbdebug instead.")))

(cl:ensure-generic-function 'robot_uwb_cur_x-val :lambda-list '(m))
(cl:defmethod robot_uwb_cur_x-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_cur_x-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_cur_x instead.")
  (robot_uwb_cur_x m))

(cl:ensure-generic-function 'robot_uwb_cur_y-val :lambda-list '(m))
(cl:defmethod robot_uwb_cur_y-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_cur_y-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_cur_y instead.")
  (robot_uwb_cur_y m))

(cl:ensure-generic-function 'robot_uwb_cur_angle-val :lambda-list '(m))
(cl:defmethod robot_uwb_cur_angle-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_cur_angle-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_cur_angle instead.")
  (robot_uwb_cur_angle m))

(cl:ensure-generic-function 'robot_uwb_fir_angle-val :lambda-list '(m))
(cl:defmethod robot_uwb_fir_angle-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_fir_angle-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_fir_angle instead.")
  (robot_uwb_fir_angle m))

(cl:ensure-generic-function 'robot_uwb_fir_x-val :lambda-list '(m))
(cl:defmethod robot_uwb_fir_x-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_fir_x-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_fir_x instead.")
  (robot_uwb_fir_x m))

(cl:ensure-generic-function 'robot_uwb_fir_y-val :lambda-list '(m))
(cl:defmethod robot_uwb_fir_y-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_fir_y-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_fir_y instead.")
  (robot_uwb_fir_y m))

(cl:ensure-generic-function 'robot_uwb_avr_x-val :lambda-list '(m))
(cl:defmethod robot_uwb_avr_x-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_avr_x-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_avr_x instead.")
  (robot_uwb_avr_x m))

(cl:ensure-generic-function 'robot_uwb_avr_y-val :lambda-list '(m))
(cl:defmethod robot_uwb_avr_y-val ((m <uwbdebug>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader humanoid_interface_ros-msg:robot_uwb_avr_y-val is deprecated.  Use humanoid_interface_ros-msg:robot_uwb_avr_y instead.")
  (robot_uwb_avr_y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <uwbdebug>) ostream)
  "Serializes a message object of type '<uwbdebug>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_cur_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_cur_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_cur_angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_fir_angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_fir_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_fir_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_avr_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'robot_uwb_avr_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <uwbdebug>) istream)
  "Deserializes a message object of type '<uwbdebug>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_cur_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_cur_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_cur_angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_fir_angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_fir_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_fir_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_avr_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'robot_uwb_avr_y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<uwbdebug>)))
  "Returns string type for a message object of type '<uwbdebug>"
  "humanoid_interface_ros/uwbdebug")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'uwbdebug)))
  "Returns string type for a message object of type 'uwbdebug"
  "humanoid_interface_ros/uwbdebug")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<uwbdebug>)))
  "Returns md5sum for a message object of type '<uwbdebug>"
  "a496166c5de3c06085e7947afcc759bc")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'uwbdebug)))
  "Returns md5sum for a message object of type 'uwbdebug"
  "a496166c5de3c06085e7947afcc759bc")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<uwbdebug>)))
  "Returns full string definition for message of type '<uwbdebug>"
  (cl:format cl:nil "# 机器人uwb x,y 轴滤波后的效果~%float32 robot_uwb_cur_x~%float32 robot_uwb_cur_y~%float32 robot_uwb_cur_angle~%float32 robot_uwb_fir_angle~%float32 robot_uwb_fir_x~%float32 robot_uwb_fir_y~%float32 robot_uwb_avr_x~%float32 robot_uwb_avr_y~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'uwbdebug)))
  "Returns full string definition for message of type 'uwbdebug"
  (cl:format cl:nil "# 机器人uwb x,y 轴滤波后的效果~%float32 robot_uwb_cur_x~%float32 robot_uwb_cur_y~%float32 robot_uwb_cur_angle~%float32 robot_uwb_fir_angle~%float32 robot_uwb_fir_x~%float32 robot_uwb_fir_y~%float32 robot_uwb_avr_x~%float32 robot_uwb_avr_y~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <uwbdebug>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <uwbdebug>))
  "Converts a ROS message object to a list"
  (cl:list 'uwbdebug
    (cl:cons ':robot_uwb_cur_x (robot_uwb_cur_x msg))
    (cl:cons ':robot_uwb_cur_y (robot_uwb_cur_y msg))
    (cl:cons ':robot_uwb_cur_angle (robot_uwb_cur_angle msg))
    (cl:cons ':robot_uwb_fir_angle (robot_uwb_fir_angle msg))
    (cl:cons ':robot_uwb_fir_x (robot_uwb_fir_x msg))
    (cl:cons ':robot_uwb_fir_y (robot_uwb_fir_y msg))
    (cl:cons ':robot_uwb_avr_x (robot_uwb_avr_x msg))
    (cl:cons ':robot_uwb_avr_y (robot_uwb_avr_y msg))
))
