; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-srv)


;//! \htmlinclude setHwIntialState-request.msg.html

(cl:defclass <setHwIntialState-request> (roslisp-msg-protocol:ros-message)
  ((q_intial
    :reader q_intial
    :initarg :q_intial
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (v_intial
    :reader v_intial
    :initarg :v_intial
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass setHwIntialState-request (<setHwIntialState-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <setHwIntialState-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'setHwIntialState-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<setHwIntialState-request> is deprecated: use kuavo_msgs-srv:setHwIntialState-request instead.")))

(cl:ensure-generic-function 'q_intial-val :lambda-list '(m))
(cl:defmethod q_intial-val ((m <setHwIntialState-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:q_intial-val is deprecated.  Use kuavo_msgs-srv:q_intial instead.")
  (q_intial m))

(cl:ensure-generic-function 'v_intial-val :lambda-list '(m))
(cl:defmethod v_intial-val ((m <setHwIntialState-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:v_intial-val is deprecated.  Use kuavo_msgs-srv:v_intial instead.")
  (v_intial m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <setHwIntialState-request>) ostream)
  "Serializes a message object of type '<setHwIntialState-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'q_intial))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'q_intial))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'v_intial))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'v_intial))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <setHwIntialState-request>) istream)
  "Deserializes a message object of type '<setHwIntialState-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'q_intial) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'q_intial)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'v_intial) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'v_intial)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<setHwIntialState-request>)))
  "Returns string type for a service object of type '<setHwIntialState-request>"
  "kuavo_msgs/setHwIntialStateRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'setHwIntialState-request)))
  "Returns string type for a service object of type 'setHwIntialState-request"
  "kuavo_msgs/setHwIntialStateRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<setHwIntialState-request>)))
  "Returns md5sum for a message object of type '<setHwIntialState-request>"
  "5289a64acc27422c552070b8181b8118")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'setHwIntialState-request)))
  "Returns md5sum for a message object of type 'setHwIntialState-request"
  "5289a64acc27422c552070b8181b8118")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<setHwIntialState-request>)))
  "Returns full string definition for message of type '<setHwIntialState-request>"
  (cl:format cl:nil "float64[] q_intial  ~%float64[] v_intial  ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'setHwIntialState-request)))
  "Returns full string definition for message of type 'setHwIntialState-request"
  (cl:format cl:nil "float64[] q_intial  ~%float64[] v_intial  ~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <setHwIntialState-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'q_intial) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'v_intial) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <setHwIntialState-request>))
  "Converts a ROS message object to a list"
  (cl:list 'setHwIntialState-request
    (cl:cons ':q_intial (q_intial msg))
    (cl:cons ':v_intial (v_intial msg))
))
;//! \htmlinclude setHwIntialState-response.msg.html

(cl:defclass <setHwIntialState-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass setHwIntialState-response (<setHwIntialState-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <setHwIntialState-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'setHwIntialState-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<setHwIntialState-response> is deprecated: use kuavo_msgs-srv:setHwIntialState-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <setHwIntialState-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:success-val is deprecated.  Use kuavo_msgs-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <setHwIntialState-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:message-val is deprecated.  Use kuavo_msgs-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <setHwIntialState-response>) ostream)
  "Serializes a message object of type '<setHwIntialState-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <setHwIntialState-response>) istream)
  "Deserializes a message object of type '<setHwIntialState-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<setHwIntialState-response>)))
  "Returns string type for a service object of type '<setHwIntialState-response>"
  "kuavo_msgs/setHwIntialStateResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'setHwIntialState-response)))
  "Returns string type for a service object of type 'setHwIntialState-response"
  "kuavo_msgs/setHwIntialStateResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<setHwIntialState-response>)))
  "Returns md5sum for a message object of type '<setHwIntialState-response>"
  "5289a64acc27422c552070b8181b8118")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'setHwIntialState-response)))
  "Returns md5sum for a message object of type 'setHwIntialState-response"
  "5289a64acc27422c552070b8181b8118")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<setHwIntialState-response>)))
  "Returns full string definition for message of type '<setHwIntialState-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'setHwIntialState-response)))
  "Returns full string definition for message of type 'setHwIntialState-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <setHwIntialState-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <setHwIntialState-response>))
  "Converts a ROS message object to a list"
  (cl:list 'setHwIntialState-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'setHwIntialState)))
  'setHwIntialState-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'setHwIntialState)))
  'setHwIntialState-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'setHwIntialState)))
  "Returns string type for a service object of type '<setHwIntialState>"
  "kuavo_msgs/setHwIntialState")