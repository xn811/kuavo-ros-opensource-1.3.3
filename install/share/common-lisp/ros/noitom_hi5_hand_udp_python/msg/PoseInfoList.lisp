; Auto-generated. Do not edit!


(cl:in-package noitom_hi5_hand_udp_python-msg)


;//! \htmlinclude PoseInfoList.msg.html

(cl:defclass <PoseInfoList> (roslisp-msg-protocol:ros-message)
  ((timestamp_ms
    :reader timestamp_ms
    :initarg :timestamp_ms
    :type cl:integer
    :initform 0)
   (is_high_confidence
    :reader is_high_confidence
    :initarg :is_high_confidence
    :type cl:boolean
    :initform cl:nil)
   (is_hand_tracking
    :reader is_hand_tracking
    :initarg :is_hand_tracking
    :type cl:boolean
    :initform cl:nil)
   (poses
    :reader poses
    :initarg :poses
    :type (cl:vector noitom_hi5_hand_udp_python-msg:PoseInfo)
   :initform (cl:make-array 0 :element-type 'noitom_hi5_hand_udp_python-msg:PoseInfo :initial-element (cl:make-instance 'noitom_hi5_hand_udp_python-msg:PoseInfo))))
)

(cl:defclass PoseInfoList (<PoseInfoList>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseInfoList>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseInfoList)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name noitom_hi5_hand_udp_python-msg:<PoseInfoList> is deprecated: use noitom_hi5_hand_udp_python-msg:PoseInfoList instead.")))

(cl:ensure-generic-function 'timestamp_ms-val :lambda-list '(m))
(cl:defmethod timestamp_ms-val ((m <PoseInfoList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:timestamp_ms-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:timestamp_ms instead.")
  (timestamp_ms m))

(cl:ensure-generic-function 'is_high_confidence-val :lambda-list '(m))
(cl:defmethod is_high_confidence-val ((m <PoseInfoList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:is_high_confidence-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:is_high_confidence instead.")
  (is_high_confidence m))

(cl:ensure-generic-function 'is_hand_tracking-val :lambda-list '(m))
(cl:defmethod is_hand_tracking-val ((m <PoseInfoList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:is_hand_tracking-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:is_hand_tracking instead.")
  (is_hand_tracking m))

(cl:ensure-generic-function 'poses-val :lambda-list '(m))
(cl:defmethod poses-val ((m <PoseInfoList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:poses-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:poses instead.")
  (poses m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseInfoList>) ostream)
  "Serializes a message object of type '<PoseInfoList>"
  (cl:let* ((signed (cl:slot-value msg 'timestamp_ms)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_high_confidence) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_hand_tracking) 1 0)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'poses))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'poses))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseInfoList>) istream)
  "Deserializes a message object of type '<PoseInfoList>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'timestamp_ms) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
    (cl:setf (cl:slot-value msg 'is_high_confidence) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'is_hand_tracking) (cl:not (cl:zerop (cl:read-byte istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'poses) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'poses)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'noitom_hi5_hand_udp_python-msg:PoseInfo))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseInfoList>)))
  "Returns string type for a message object of type '<PoseInfoList>"
  "noitom_hi5_hand_udp_python/PoseInfoList")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseInfoList)))
  "Returns string type for a message object of type 'PoseInfoList"
  "noitom_hi5_hand_udp_python/PoseInfoList")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseInfoList>)))
  "Returns md5sum for a message object of type '<PoseInfoList>"
  "f56d5e4df1c0e38a423ead4bde9414b3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseInfoList)))
  "Returns md5sum for a message object of type 'PoseInfoList"
  "f56d5e4df1c0e38a423ead4bde9414b3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseInfoList>)))
  "Returns full string definition for message of type '<PoseInfoList>"
  (cl:format cl:nil "int64 timestamp_ms~%bool is_high_confidence~%bool is_hand_tracking~%PoseInfo[] poses~%================================================================================~%MSG: noitom_hi5_hand_udp_python/PoseInfo~%geometry_msgs/Point position~%geometry_msgs/Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseInfoList)))
  "Returns full string definition for message of type 'PoseInfoList"
  (cl:format cl:nil "int64 timestamp_ms~%bool is_high_confidence~%bool is_hand_tracking~%PoseInfo[] poses~%================================================================================~%MSG: noitom_hi5_hand_udp_python/PoseInfo~%geometry_msgs/Point position~%geometry_msgs/Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseInfoList>))
  (cl:+ 0
     8
     1
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'poses) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseInfoList>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseInfoList
    (cl:cons ':timestamp_ms (timestamp_ms msg))
    (cl:cons ':is_high_confidence (is_high_confidence msg))
    (cl:cons ':is_hand_tracking (is_hand_tracking msg))
    (cl:cons ':poses (poses msg))
))
