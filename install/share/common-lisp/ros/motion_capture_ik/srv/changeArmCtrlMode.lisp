; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-srv)


;//! \htmlinclude changeArmCtrlMode-request.msg.html

(cl:defclass <changeArmCtrlMode-request> (roslisp-msg-protocol:ros-message)
  ((control_mode
    :reader control_mode
    :initarg :control_mode
    :type cl:integer
    :initform 0))
)

(cl:defclass changeArmCtrlMode-request (<changeArmCtrlMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeArmCtrlMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeArmCtrlMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-srv:<changeArmCtrlMode-request> is deprecated: use motion_capture_ik-srv:changeArmCtrlMode-request instead.")))

(cl:ensure-generic-function 'control_mode-val :lambda-list '(m))
(cl:defmethod control_mode-val ((m <changeArmCtrlMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:control_mode-val is deprecated.  Use motion_capture_ik-srv:control_mode instead.")
  (control_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeArmCtrlMode-request>) ostream)
  "Serializes a message object of type '<changeArmCtrlMode-request>"
  (cl:let* ((signed (cl:slot-value msg 'control_mode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeArmCtrlMode-request>) istream)
  "Deserializes a message object of type '<changeArmCtrlMode-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'control_mode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeArmCtrlMode-request>)))
  "Returns string type for a service object of type '<changeArmCtrlMode-request>"
  "motion_capture_ik/changeArmCtrlModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeArmCtrlMode-request)))
  "Returns string type for a service object of type 'changeArmCtrlMode-request"
  "motion_capture_ik/changeArmCtrlModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeArmCtrlMode-request>)))
  "Returns md5sum for a message object of type '<changeArmCtrlMode-request>"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeArmCtrlMode-request)))
  "Returns md5sum for a message object of type 'changeArmCtrlMode-request"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeArmCtrlMode-request>)))
  "Returns full string definition for message of type '<changeArmCtrlMode-request>"
  (cl:format cl:nil "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeArmCtrlMode-request)))
  "Returns full string definition for message of type 'changeArmCtrlMode-request"
  (cl:format cl:nil "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeArmCtrlMode-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeArmCtrlMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'changeArmCtrlMode-request
    (cl:cons ':control_mode (control_mode msg))
))
;//! \htmlinclude changeArmCtrlMode-response.msg.html

(cl:defclass <changeArmCtrlMode-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass changeArmCtrlMode-response (<changeArmCtrlMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeArmCtrlMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeArmCtrlMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-srv:<changeArmCtrlMode-response> is deprecated: use motion_capture_ik-srv:changeArmCtrlMode-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <changeArmCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:result-val is deprecated.  Use motion_capture_ik-srv:result instead.")
  (result m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <changeArmCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:mode-val is deprecated.  Use motion_capture_ik-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <changeArmCtrlMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-srv:message-val is deprecated.  Use motion_capture_ik-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeArmCtrlMode-response>) ostream)
  "Serializes a message object of type '<changeArmCtrlMode-response>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeArmCtrlMode-response>) istream)
  "Deserializes a message object of type '<changeArmCtrlMode-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeArmCtrlMode-response>)))
  "Returns string type for a service object of type '<changeArmCtrlMode-response>"
  "motion_capture_ik/changeArmCtrlModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeArmCtrlMode-response)))
  "Returns string type for a service object of type 'changeArmCtrlMode-response"
  "motion_capture_ik/changeArmCtrlModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeArmCtrlMode-response>)))
  "Returns md5sum for a message object of type '<changeArmCtrlMode-response>"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeArmCtrlMode-response)))
  "Returns md5sum for a message object of type 'changeArmCtrlMode-response"
  "8a8d154c05ee16e8f5d2b72d9bb51026")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeArmCtrlMode-response>)))
  "Returns full string definition for message of type '<changeArmCtrlMode-response>"
  (cl:format cl:nil "bool result~%int32 mode ~%string message~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeArmCtrlMode-response)))
  "Returns full string definition for message of type 'changeArmCtrlMode-response"
  (cl:format cl:nil "bool result~%int32 mode ~%string message~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeArmCtrlMode-response>))
  (cl:+ 0
     1
     4
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeArmCtrlMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'changeArmCtrlMode-response
    (cl:cons ':result (result msg))
    (cl:cons ':mode (mode msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'changeArmCtrlMode)))
  'changeArmCtrlMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'changeArmCtrlMode)))
  'changeArmCtrlMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeArmCtrlMode)))
  "Returns string type for a service object of type '<changeArmCtrlMode>"
  "motion_capture_ik/changeArmCtrlMode")