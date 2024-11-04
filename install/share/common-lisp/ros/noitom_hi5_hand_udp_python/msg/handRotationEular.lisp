; Auto-generated. Do not edit!


(cl:in-package noitom_hi5_hand_udp_python-msg)


;//! \htmlinclude handRotationEular.msg.html

(cl:defclass <handRotationEular> (roslisp-msg-protocol:ros-message)
  ((eulerAngles
    :reader eulerAngles
    :initarg :eulerAngles
    :type (cl:vector noitom_hi5_hand_udp_python-msg:Vector4)
   :initform (cl:make-array 0 :element-type 'noitom_hi5_hand_udp_python-msg:Vector4 :initial-element (cl:make-instance 'noitom_hi5_hand_udp_python-msg:Vector4))))
)

(cl:defclass handRotationEular (<handRotationEular>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <handRotationEular>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'handRotationEular)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name noitom_hi5_hand_udp_python-msg:<handRotationEular> is deprecated: use noitom_hi5_hand_udp_python-msg:handRotationEular instead.")))

(cl:ensure-generic-function 'eulerAngles-val :lambda-list '(m))
(cl:defmethod eulerAngles-val ((m <handRotationEular>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:eulerAngles-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:eulerAngles instead.")
  (eulerAngles m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <handRotationEular>) ostream)
  "Serializes a message object of type '<handRotationEular>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'eulerAngles))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'eulerAngles))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <handRotationEular>) istream)
  "Deserializes a message object of type '<handRotationEular>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'eulerAngles) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'eulerAngles)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'noitom_hi5_hand_udp_python-msg:Vector4))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<handRotationEular>)))
  "Returns string type for a message object of type '<handRotationEular>"
  "noitom_hi5_hand_udp_python/handRotationEular")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'handRotationEular)))
  "Returns string type for a message object of type 'handRotationEular"
  "noitom_hi5_hand_udp_python/handRotationEular")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<handRotationEular>)))
  "Returns md5sum for a message object of type '<handRotationEular>"
  "75ea7fdfd1913bbabb0a96c424b42024")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'handRotationEular)))
  "Returns md5sum for a message object of type 'handRotationEular"
  "75ea7fdfd1913bbabb0a96c424b42024")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<handRotationEular>)))
  "Returns full string definition for message of type '<handRotationEular>"
  (cl:format cl:nil "noitom_hi5_hand_udp_python/Vector4[] eulerAngles~%~%================================================================================~%MSG: noitom_hi5_hand_udp_python/Vector4~%float32 x~%float32 y~%float32 z~%float32 w~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'handRotationEular)))
  "Returns full string definition for message of type 'handRotationEular"
  (cl:format cl:nil "noitom_hi5_hand_udp_python/Vector4[] eulerAngles~%~%================================================================================~%MSG: noitom_hi5_hand_udp_python/Vector4~%float32 x~%float32 y~%float32 z~%float32 w~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <handRotationEular>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'eulerAngles) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <handRotationEular>))
  "Converts a ROS message object to a list"
  (cl:list 'handRotationEular
    (cl:cons ':eulerAngles (eulerAngles msg))
))
