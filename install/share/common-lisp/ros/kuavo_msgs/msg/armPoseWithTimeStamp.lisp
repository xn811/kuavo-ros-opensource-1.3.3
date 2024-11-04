; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude armPoseWithTimeStamp.msg.html

(cl:defclass <armPoseWithTimeStamp> (roslisp-msg-protocol:ros-message)
  ((offset
    :reader offset
    :initarg :offset
    :type cl:integer
    :initform 0)
   (left_hand_pose
    :reader left_hand_pose
    :initarg :left_hand_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (right_hand_pose
    :reader right_hand_pose
    :initarg :right_hand_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass armPoseWithTimeStamp (<armPoseWithTimeStamp>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <armPoseWithTimeStamp>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'armPoseWithTimeStamp)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<armPoseWithTimeStamp> is deprecated: use kuavo_msgs-msg:armPoseWithTimeStamp instead.")))

(cl:ensure-generic-function 'offset-val :lambda-list '(m))
(cl:defmethod offset-val ((m <armPoseWithTimeStamp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:offset-val is deprecated.  Use kuavo_msgs-msg:offset instead.")
  (offset m))

(cl:ensure-generic-function 'left_hand_pose-val :lambda-list '(m))
(cl:defmethod left_hand_pose-val ((m <armPoseWithTimeStamp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:left_hand_pose-val is deprecated.  Use kuavo_msgs-msg:left_hand_pose instead.")
  (left_hand_pose m))

(cl:ensure-generic-function 'right_hand_pose-val :lambda-list '(m))
(cl:defmethod right_hand_pose-val ((m <armPoseWithTimeStamp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:right_hand_pose-val is deprecated.  Use kuavo_msgs-msg:right_hand_pose instead.")
  (right_hand_pose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <armPoseWithTimeStamp>) ostream)
  "Serializes a message object of type '<armPoseWithTimeStamp>"
  (cl:let* ((signed (cl:slot-value msg 'offset)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'left_hand_pose))))
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
   (cl:slot-value msg 'left_hand_pose))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'right_hand_pose))))
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
   (cl:slot-value msg 'right_hand_pose))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <armPoseWithTimeStamp>) istream)
  "Deserializes a message object of type '<armPoseWithTimeStamp>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'offset) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'left_hand_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'left_hand_pose)))
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
  (cl:setf (cl:slot-value msg 'right_hand_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'right_hand_pose)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<armPoseWithTimeStamp>)))
  "Returns string type for a message object of type '<armPoseWithTimeStamp>"
  "kuavo_msgs/armPoseWithTimeStamp")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'armPoseWithTimeStamp)))
  "Returns string type for a message object of type 'armPoseWithTimeStamp"
  "kuavo_msgs/armPoseWithTimeStamp")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<armPoseWithTimeStamp>)))
  "Returns md5sum for a message object of type '<armPoseWithTimeStamp>"
  "3404338b5cb042ac3b3cf3de3f0fcb4f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'armPoseWithTimeStamp)))
  "Returns md5sum for a message object of type 'armPoseWithTimeStamp"
  "3404338b5cb042ac3b3cf3de3f0fcb4f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<armPoseWithTimeStamp>)))
  "Returns full string definition for message of type '<armPoseWithTimeStamp>"
  (cl:format cl:nil "int32 offset~%float64[] left_hand_pose~%float64[] right_hand_pose~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'armPoseWithTimeStamp)))
  "Returns full string definition for message of type 'armPoseWithTimeStamp"
  (cl:format cl:nil "int32 offset~%float64[] left_hand_pose~%float64[] right_hand_pose~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <armPoseWithTimeStamp>))
  (cl:+ 0
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'left_hand_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'right_hand_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <armPoseWithTimeStamp>))
  "Converts a ROS message object to a list"
  (cl:list 'armPoseWithTimeStamp
    (cl:cons ':offset (offset msg))
    (cl:cons ':left_hand_pose (left_hand_pose msg))
    (cl:cons ':right_hand_pose (right_hand_pose msg))
))
