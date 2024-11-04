; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude footPoseTargetTrajectories.msg.html

(cl:defclass <footPoseTargetTrajectories> (roslisp-msg-protocol:ros-message)
  ((timeTrajectory
    :reader timeTrajectory
    :initarg :timeTrajectory
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (footIndexTrajectory
    :reader footIndexTrajectory
    :initarg :footIndexTrajectory
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0))
   (footPoseTrajectory
    :reader footPoseTrajectory
    :initarg :footPoseTrajectory
    :type (cl:vector kuavo_msgs-msg:footPose)
   :initform (cl:make-array 0 :element-type 'kuavo_msgs-msg:footPose :initial-element (cl:make-instance 'kuavo_msgs-msg:footPose))))
)

(cl:defclass footPoseTargetTrajectories (<footPoseTargetTrajectories>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <footPoseTargetTrajectories>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'footPoseTargetTrajectories)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<footPoseTargetTrajectories> is deprecated: use kuavo_msgs-msg:footPoseTargetTrajectories instead.")))

(cl:ensure-generic-function 'timeTrajectory-val :lambda-list '(m))
(cl:defmethod timeTrajectory-val ((m <footPoseTargetTrajectories>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:timeTrajectory-val is deprecated.  Use kuavo_msgs-msg:timeTrajectory instead.")
  (timeTrajectory m))

(cl:ensure-generic-function 'footIndexTrajectory-val :lambda-list '(m))
(cl:defmethod footIndexTrajectory-val ((m <footPoseTargetTrajectories>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:footIndexTrajectory-val is deprecated.  Use kuavo_msgs-msg:footIndexTrajectory instead.")
  (footIndexTrajectory m))

(cl:ensure-generic-function 'footPoseTrajectory-val :lambda-list '(m))
(cl:defmethod footPoseTrajectory-val ((m <footPoseTargetTrajectories>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:footPoseTrajectory-val is deprecated.  Use kuavo_msgs-msg:footPoseTrajectory instead.")
  (footPoseTrajectory m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <footPoseTargetTrajectories>) ostream)
  "Serializes a message object of type '<footPoseTargetTrajectories>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'timeTrajectory))))
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
   (cl:slot-value msg 'timeTrajectory))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'footIndexTrajectory))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'footIndexTrajectory))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'footPoseTrajectory))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'footPoseTrajectory))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <footPoseTargetTrajectories>) istream)
  "Deserializes a message object of type '<footPoseTargetTrajectories>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'timeTrajectory) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'timeTrajectory)))
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
  (cl:setf (cl:slot-value msg 'footIndexTrajectory) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'footIndexTrajectory)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'footPoseTrajectory) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'footPoseTrajectory)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'kuavo_msgs-msg:footPose))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<footPoseTargetTrajectories>)))
  "Returns string type for a message object of type '<footPoseTargetTrajectories>"
  "kuavo_msgs/footPoseTargetTrajectories")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'footPoseTargetTrajectories)))
  "Returns string type for a message object of type 'footPoseTargetTrajectories"
  "kuavo_msgs/footPoseTargetTrajectories")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<footPoseTargetTrajectories>)))
  "Returns md5sum for a message object of type '<footPoseTargetTrajectories>"
  "6854923406c37831b40979cd2570e027")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'footPoseTargetTrajectories)))
  "Returns md5sum for a message object of type 'footPoseTargetTrajectories"
  "6854923406c37831b40979cd2570e027")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<footPoseTargetTrajectories>)))
  "Returns full string definition for message of type '<footPoseTargetTrajectories>"
  (cl:format cl:nil "float64[]    timeTrajectory~%int32[]      footIndexTrajectory~%footPose[]   footPoseTrajectory~%================================================================================~%MSG: kuavo_msgs/footPose~%float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'footPoseTargetTrajectories)))
  "Returns full string definition for message of type 'footPoseTargetTrajectories"
  (cl:format cl:nil "float64[]    timeTrajectory~%int32[]      footIndexTrajectory~%footPose[]   footPoseTrajectory~%================================================================================~%MSG: kuavo_msgs/footPose~%float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <footPoseTargetTrajectories>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'timeTrajectory) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'footIndexTrajectory) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'footPoseTrajectory) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <footPoseTargetTrajectories>))
  "Converts a ROS message object to a list"
  (cl:list 'footPoseTargetTrajectories
    (cl:cons ':timeTrajectory (timeTrajectory msg))
    (cl:cons ':footIndexTrajectory (footIndexTrajectory msg))
    (cl:cons ':footPoseTrajectory (footPoseTrajectory msg))
))
