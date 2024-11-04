; Auto-generated. Do not edit!


(cl:in-package noitom_hi5_hand_udp_python-msg)


;//! \htmlinclude PoseInfo.msg.html

(cl:defclass <PoseInfo> (roslisp-msg-protocol:ros-message)
  ((position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (orientation
    :reader orientation
    :initarg :orientation
    :type geometry_msgs-msg:Quaternion
    :initform (cl:make-instance 'geometry_msgs-msg:Quaternion)))
)

(cl:defclass PoseInfo (<PoseInfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseInfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseInfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name noitom_hi5_hand_udp_python-msg:<PoseInfo> is deprecated: use noitom_hi5_hand_udp_python-msg:PoseInfo instead.")))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <PoseInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:position-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'orientation-val :lambda-list '(m))
(cl:defmethod orientation-val ((m <PoseInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:orientation-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:orientation instead.")
  (orientation m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseInfo>) ostream)
  "Serializes a message object of type '<PoseInfo>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'orientation) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseInfo>) istream)
  "Deserializes a message object of type '<PoseInfo>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'orientation) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseInfo>)))
  "Returns string type for a message object of type '<PoseInfo>"
  "noitom_hi5_hand_udp_python/PoseInfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseInfo)))
  "Returns string type for a message object of type 'PoseInfo"
  "noitom_hi5_hand_udp_python/PoseInfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseInfo>)))
  "Returns md5sum for a message object of type '<PoseInfo>"
  "e45d45a5a1ce597b249e23fb30fc871f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseInfo)))
  "Returns md5sum for a message object of type 'PoseInfo"
  "e45d45a5a1ce597b249e23fb30fc871f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseInfo>)))
  "Returns full string definition for message of type '<PoseInfo>"
  (cl:format cl:nil "geometry_msgs/Point position~%geometry_msgs/Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseInfo)))
  "Returns full string definition for message of type 'PoseInfo"
  (cl:format cl:nil "geometry_msgs/Point position~%geometry_msgs/Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseInfo>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'orientation))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseInfo>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseInfo
    (cl:cons ':position (position msg))
    (cl:cons ':orientation (orientation msg))
))
