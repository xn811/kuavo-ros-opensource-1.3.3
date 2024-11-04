; Auto-generated. Do not edit!


(cl:in-package h12pro_controller_node-srv)


;//! \htmlinclude changeHandArmPosesByConfigName-request.msg.html

(cl:defclass <changeHandArmPosesByConfigName-request> (roslisp-msg-protocol:ros-message)
  ((config_name
    :reader config_name
    :initarg :config_name
    :type cl:string
    :initform ""))
)

(cl:defclass changeHandArmPosesByConfigName-request (<changeHandArmPosesByConfigName-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeHandArmPosesByConfigName-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeHandArmPosesByConfigName-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name h12pro_controller_node-srv:<changeHandArmPosesByConfigName-request> is deprecated: use h12pro_controller_node-srv:changeHandArmPosesByConfigName-request instead.")))

(cl:ensure-generic-function 'config_name-val :lambda-list '(m))
(cl:defmethod config_name-val ((m <changeHandArmPosesByConfigName-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader h12pro_controller_node-srv:config_name-val is deprecated.  Use h12pro_controller_node-srv:config_name instead.")
  (config_name m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeHandArmPosesByConfigName-request>) ostream)
  "Serializes a message object of type '<changeHandArmPosesByConfigName-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'config_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'config_name))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeHandArmPosesByConfigName-request>) istream)
  "Deserializes a message object of type '<changeHandArmPosesByConfigName-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'config_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'config_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeHandArmPosesByConfigName-request>)))
  "Returns string type for a service object of type '<changeHandArmPosesByConfigName-request>"
  "h12pro_controller_node/changeHandArmPosesByConfigNameRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandArmPosesByConfigName-request)))
  "Returns string type for a service object of type 'changeHandArmPosesByConfigName-request"
  "h12pro_controller_node/changeHandArmPosesByConfigNameRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeHandArmPosesByConfigName-request>)))
  "Returns md5sum for a message object of type '<changeHandArmPosesByConfigName-request>"
  "981617b9cc6699ade1d3c011b67988a7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeHandArmPosesByConfigName-request)))
  "Returns md5sum for a message object of type 'changeHandArmPosesByConfigName-request"
  "981617b9cc6699ade1d3c011b67988a7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeHandArmPosesByConfigName-request>)))
  "Returns full string definition for message of type '<changeHandArmPosesByConfigName-request>"
  (cl:format cl:nil "string config_name~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeHandArmPosesByConfigName-request)))
  "Returns full string definition for message of type 'changeHandArmPosesByConfigName-request"
  (cl:format cl:nil "string config_name~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeHandArmPosesByConfigName-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'config_name))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeHandArmPosesByConfigName-request>))
  "Converts a ROS message object to a list"
  (cl:list 'changeHandArmPosesByConfigName-request
    (cl:cons ':config_name (config_name msg))
))
;//! \htmlinclude changeHandArmPosesByConfigName-response.msg.html

(cl:defclass <changeHandArmPosesByConfigName-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass changeHandArmPosesByConfigName-response (<changeHandArmPosesByConfigName-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeHandArmPosesByConfigName-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeHandArmPosesByConfigName-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name h12pro_controller_node-srv:<changeHandArmPosesByConfigName-response> is deprecated: use h12pro_controller_node-srv:changeHandArmPosesByConfigName-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <changeHandArmPosesByConfigName-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader h12pro_controller_node-srv:result-val is deprecated.  Use h12pro_controller_node-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeHandArmPosesByConfigName-response>) ostream)
  "Serializes a message object of type '<changeHandArmPosesByConfigName-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeHandArmPosesByConfigName-response>) istream)
  "Deserializes a message object of type '<changeHandArmPosesByConfigName-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeHandArmPosesByConfigName-response>)))
  "Returns string type for a service object of type '<changeHandArmPosesByConfigName-response>"
  "h12pro_controller_node/changeHandArmPosesByConfigNameResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandArmPosesByConfigName-response)))
  "Returns string type for a service object of type 'changeHandArmPosesByConfigName-response"
  "h12pro_controller_node/changeHandArmPosesByConfigNameResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeHandArmPosesByConfigName-response>)))
  "Returns md5sum for a message object of type '<changeHandArmPosesByConfigName-response>"
  "981617b9cc6699ade1d3c011b67988a7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeHandArmPosesByConfigName-response)))
  "Returns md5sum for a message object of type 'changeHandArmPosesByConfigName-response"
  "981617b9cc6699ade1d3c011b67988a7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeHandArmPosesByConfigName-response>)))
  "Returns full string definition for message of type '<changeHandArmPosesByConfigName-response>"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeHandArmPosesByConfigName-response)))
  "Returns full string definition for message of type 'changeHandArmPosesByConfigName-response"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeHandArmPosesByConfigName-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeHandArmPosesByConfigName-response>))
  "Converts a ROS message object to a list"
  (cl:list 'changeHandArmPosesByConfigName-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'changeHandArmPosesByConfigName)))
  'changeHandArmPosesByConfigName-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'changeHandArmPosesByConfigName)))
  'changeHandArmPosesByConfigName-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandArmPosesByConfigName)))
  "Returns string type for a service object of type '<changeHandArmPosesByConfigName>"
  "h12pro_controller_node/changeHandArmPosesByConfigName")