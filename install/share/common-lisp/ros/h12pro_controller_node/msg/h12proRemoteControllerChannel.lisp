; Auto-generated. Do not edit!


(cl:in-package h12pro_controller_node-msg)


;//! \htmlinclude h12proRemoteControllerChannel.msg.html

(cl:defclass <h12proRemoteControllerChannel> (roslisp-msg-protocol:ros-message)
  ((channels
    :reader channels
    :initarg :channels
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (sbus_state
    :reader sbus_state
    :initarg :sbus_state
    :type cl:fixnum
    :initform 0))
)

(cl:defclass h12proRemoteControllerChannel (<h12proRemoteControllerChannel>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <h12proRemoteControllerChannel>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'h12proRemoteControllerChannel)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name h12pro_controller_node-msg:<h12proRemoteControllerChannel> is deprecated: use h12pro_controller_node-msg:h12proRemoteControllerChannel instead.")))

(cl:ensure-generic-function 'channels-val :lambda-list '(m))
(cl:defmethod channels-val ((m <h12proRemoteControllerChannel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader h12pro_controller_node-msg:channels-val is deprecated.  Use h12pro_controller_node-msg:channels instead.")
  (channels m))

(cl:ensure-generic-function 'sbus_state-val :lambda-list '(m))
(cl:defmethod sbus_state-val ((m <h12proRemoteControllerChannel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader h12pro_controller_node-msg:sbus_state-val is deprecated.  Use h12pro_controller_node-msg:sbus_state instead.")
  (sbus_state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <h12proRemoteControllerChannel>) ostream)
  "Serializes a message object of type '<h12proRemoteControllerChannel>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'channels))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'channels))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'sbus_state)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <h12proRemoteControllerChannel>) istream)
  "Deserializes a message object of type '<h12proRemoteControllerChannel>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'channels) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'channels)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'sbus_state)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<h12proRemoteControllerChannel>)))
  "Returns string type for a message object of type '<h12proRemoteControllerChannel>"
  "h12pro_controller_node/h12proRemoteControllerChannel")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'h12proRemoteControllerChannel)))
  "Returns string type for a message object of type 'h12proRemoteControllerChannel"
  "h12pro_controller_node/h12proRemoteControllerChannel")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<h12proRemoteControllerChannel>)))
  "Returns md5sum for a message object of type '<h12proRemoteControllerChannel>"
  "fbc04b5769be8336707a1083b8b107dd")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'h12proRemoteControllerChannel)))
  "Returns md5sum for a message object of type 'h12proRemoteControllerChannel"
  "fbc04b5769be8336707a1083b8b107dd")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<h12proRemoteControllerChannel>)))
  "Returns full string definition for message of type '<h12proRemoteControllerChannel>"
  (cl:format cl:nil "uint16[] channels~%uint8 sbus_state~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'h12proRemoteControllerChannel)))
  "Returns full string definition for message of type 'h12proRemoteControllerChannel"
  (cl:format cl:nil "uint16[] channels~%uint8 sbus_state~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <h12proRemoteControllerChannel>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'channels) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <h12proRemoteControllerChannel>))
  "Converts a ROS message object to a list"
  (cl:list 'h12proRemoteControllerChannel
    (cl:cons ':channels (channels msg))
    (cl:cons ':sbus_state (sbus_state msg))
))
