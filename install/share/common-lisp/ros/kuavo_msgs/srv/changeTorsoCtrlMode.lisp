; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-srv)


;//! \htmlinclude changeTorsoCtrlMode-request.msg.html

(cl:defclass <changeTorsoCtrlMode-request> (roslisp-msg-protocol:ros-message)
  ((control_mode
    :reader control_mode
    :initarg :control_mode
    :type cl:integer
    :initform 0))
)

(cl:defclass changeTorsoCtrlMode-request (<changeTorsoCtrlMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeTorsoCtrlMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeTorsoCtrlMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<changeTorsoCtrlMode-request> is deprecated: use kuavo_msgs-srv:changeTorsoCtrlMode-request instead.")))

(cl:ensure-generic-function 'control_mode-val :lambda-list '(m))
(cl:defmethod control_mode-val ((m <changeTorsoCtrlMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:control_mode-val is deprecated.  Use kuavo_msgs-srv:control_mode instead.")
  (control_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeTorsoCtrlMode-request>) ostream)
  "Serializes a message object of type '<changeTorsoCtrlMode-request>"
  (cl:let* ((signed (cl:slot-value msg 'control_mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeTorsoCtrlMode-request>) istream)
  "Deserializes a message object of type '<changeTorsoCtrlMode-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'control_mode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeTorsoCtrlMode-request>)))
  "Returns string type for a service object of type '<changeTorsoCtrlMode-request>"
  "kuavo_msgs/changeTorsoCtrlModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeTorsoCtrlMode-request)))
  "Returns string type for a service object of type 'changeTorsoCtrlMode-request"
  "kuavo_msgs/changeTorsoCtrlModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeTorsoCtrlMode-request>)))
  "Returns md5sum for a message object of type '<changeTorsoCtrlMode-request>"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeTorsoCtrlMode-request)))
  "Returns md5sum for a message object of type 'changeTorsoCtrlMode-request"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeTorsoCtrlMode-request>)))
  "Returns full string definition for message of type '<changeTorsoCtrlMode-request>"
  (cl:format cl:nil "int32 control_mode # 0: control 6dof, 1: control height+yaw+pitch, 2: control control height+pitch ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeTorsoCtrlMode-request)))
  "Returns full string definition for message of type 'changeTorsoCtrlMode-request"
  (cl:format cl:nil "int32 control_mode # 0: control 6dof, 1: control height+yaw+pitch, 2: control control height+pitch ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeTorsoCtrlMode-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeTorsoCtrlMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'changeTorsoCtrlMode-request
    (cl:cons ':control_mode (control_mode msg))
))
;//! \htmlinclude changeTorsoCtrlMode-response.msg.html

(cl:defclass <changeTorsoCtrlMode-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil)
   (mode
    :reader mode
    :initarg :mode
    :type cl:integer
    :initform 0)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass changeTorsoCtrlMode-response (<changeTorsoCtrlMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeTorsoCtrlMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeTorsoCtrlMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<changeTorsoCtrlMode-response> is deprecated: use kuavo_msgs-srv:changeTorsoCtrlMode-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <changeTorsoCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:result-val is deprecated.  Use kuavo_msgs-srv:result instead.")
  (result m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <changeTorsoCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:mode-val is deprecated.  Use kuavo_msgs-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <changeTorsoCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:message-val is deprecated.  Use kuavo_msgs-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeTorsoCtrlMode-response>) ostream)
  "Serializes a message object of type '<changeTorsoCtrlMode-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeTorsoCtrlMode-response>) istream)
  "Deserializes a message object of type '<changeTorsoCtrlMode-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeTorsoCtrlMode-response>)))
  "Returns string type for a service object of type '<changeTorsoCtrlMode-response>"
  "kuavo_msgs/changeTorsoCtrlModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeTorsoCtrlMode-response)))
  "Returns string type for a service object of type 'changeTorsoCtrlMode-response"
  "kuavo_msgs/changeTorsoCtrlModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeTorsoCtrlMode-response>)))
  "Returns md5sum for a message object of type '<changeTorsoCtrlMode-response>"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeTorsoCtrlMode-response)))
  "Returns md5sum for a message object of type 'changeTorsoCtrlMode-response"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeTorsoCtrlMode-response>)))
  "Returns full string definition for message of type '<changeTorsoCtrlMode-response>"
  (cl:format cl:nil "bool result~%int32 mode~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeTorsoCtrlMode-response)))
  "Returns full string definition for message of type 'changeTorsoCtrlMode-response"
  (cl:format cl:nil "bool result~%int32 mode~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeTorsoCtrlMode-response>))
  (cl:+ 0
     1
     4
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeTorsoCtrlMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'changeTorsoCtrlMode-response
    (cl:cons ':result (result msg))
    (cl:cons ':mode (mode msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'changeTorsoCtrlMode)))
  'changeTorsoCtrlMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'changeTorsoCtrlMode)))
  'changeTorsoCtrlMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeTorsoCtrlMode)))
  "Returns string type for a service object of type '<changeTorsoCtrlMode>"
  "kuavo_msgs/changeTorsoCtrlMode")