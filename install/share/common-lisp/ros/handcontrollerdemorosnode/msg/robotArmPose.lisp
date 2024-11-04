; Auto-generated. Do not edit!


(cl:in-package handcontrollerdemorosnode-msg)


;//! \htmlinclude robotArmPose.msg.html

(cl:defclass <robotArmPose> (roslisp-msg-protocol:ros-message)
  ((left_arm_pose
    :reader left_arm_pose
    :initarg :left_arm_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (right_arm_pose
    :reader right_arm_pose
    :initarg :right_arm_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass robotArmPose (<robotArmPose>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <robotArmPose>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'robotArmPose)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name handcontrollerdemorosnode-msg:<robotArmPose> is deprecated: use handcontrollerdemorosnode-msg:robotArmPose instead.")))

(cl:ensure-generic-function 'left_arm_pose-val :lambda-list '(m))
(cl:defmethod left_arm_pose-val ((m <robotArmPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-msg:left_arm_pose-val is deprecated.  Use handcontrollerdemorosnode-msg:left_arm_pose instead.")
  (left_arm_pose m))

(cl:ensure-generic-function 'right_arm_pose-val :lambda-list '(m))
(cl:defmethod right_arm_pose-val ((m <robotArmPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-msg:right_arm_pose-val is deprecated.  Use handcontrollerdemorosnode-msg:right_arm_pose instead.")
  (right_arm_pose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <robotArmPose>) ostream)
  "Serializes a message object of type '<robotArmPose>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'left_arm_pose))))
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
   (cl:slot-value msg 'left_arm_pose))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'right_arm_pose))))
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
   (cl:slot-value msg 'right_arm_pose))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <robotArmPose>) istream)
  "Deserializes a message object of type '<robotArmPose>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'left_arm_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'left_arm_pose)))
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
  (cl:setf (cl:slot-value msg 'right_arm_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'right_arm_pose)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<robotArmPose>)))
  "Returns string type for a message object of type '<robotArmPose>"
  "handcontrollerdemorosnode/robotArmPose")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'robotArmPose)))
  "Returns string type for a message object of type 'robotArmPose"
  "handcontrollerdemorosnode/robotArmPose")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<robotArmPose>)))
  "Returns md5sum for a message object of type '<robotArmPose>"
  "c281ae760454cca592ca88fb5b3b708b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'robotArmPose)))
  "Returns md5sum for a message object of type 'robotArmPose"
  "c281ae760454cca592ca88fb5b3b708b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<robotArmPose>)))
  "Returns full string definition for message of type '<robotArmPose>"
  (cl:format cl:nil "float64[] left_arm_pose~%float64[] right_arm_pose~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'robotArmPose)))
  "Returns full string definition for message of type 'robotArmPose"
  (cl:format cl:nil "float64[] left_arm_pose~%float64[] right_arm_pose~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <robotArmPose>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'left_arm_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'right_arm_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <robotArmPose>))
  "Converts a ROS message object to a list"
  (cl:list 'robotArmPose
    (cl:cons ':left_arm_pose (left_arm_pose msg))
    (cl:cons ':right_arm_pose (right_arm_pose msg))
))
