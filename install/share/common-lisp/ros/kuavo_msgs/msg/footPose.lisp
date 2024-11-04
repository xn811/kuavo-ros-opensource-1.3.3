; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-msg)


;//! \htmlinclude footPose.msg.html

(cl:defclass <footPose> (roslisp-msg-protocol:ros-message)
  ((footPose
    :reader footPose
    :initarg :footPose
    :type (cl:vector cl:float)
   :initform (cl:make-array 4 :element-type 'cl:float :initial-element 0.0))
   (torsoPose
    :reader torsoPose
    :initarg :torsoPose
    :type (cl:vector cl:float)
   :initform (cl:make-array 4 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass footPose (<footPose>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <footPose>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'footPose)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-msg:<footPose> is deprecated: use kuavo_msgs-msg:footPose instead.")))

(cl:ensure-generic-function 'footPose-val :lambda-list '(m))
(cl:defmethod footPose-val ((m <footPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:footPose-val is deprecated.  Use kuavo_msgs-msg:footPose instead.")
  (footPose m))

(cl:ensure-generic-function 'torsoPose-val :lambda-list '(m))
(cl:defmethod torsoPose-val ((m <footPose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-msg:torsoPose-val is deprecated.  Use kuavo_msgs-msg:torsoPose instead.")
  (torsoPose m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <footPose>) ostream)
  "Serializes a message object of type '<footPose>"
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'footPose))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'torsoPose))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <footPose>) istream)
  "Deserializes a message object of type '<footPose>"
  (cl:setf (cl:slot-value msg 'footPose) (cl:make-array 4))
  (cl:let ((vals (cl:slot-value msg 'footPose)))
    (cl:dotimes (i 4)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits)))))
  (cl:setf (cl:slot-value msg 'torsoPose) (cl:make-array 4))
  (cl:let ((vals (cl:slot-value msg 'torsoPose)))
    (cl:dotimes (i 4)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<footPose>)))
  "Returns string type for a message object of type '<footPose>"
  "kuavo_msgs/footPose")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'footPose)))
  "Returns string type for a message object of type 'footPose"
  "kuavo_msgs/footPose")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<footPose>)))
  "Returns md5sum for a message object of type '<footPose>"
  "b0acb7ad1ed1ee5a0a630b91b650f49a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'footPose)))
  "Returns md5sum for a message object of type 'footPose"
  "b0acb7ad1ed1ee5a0a630b91b650f49a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<footPose>)))
  "Returns full string definition for message of type '<footPose>"
  (cl:format cl:nil "float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'footPose)))
  "Returns full string definition for message of type 'footPose"
  (cl:format cl:nil "float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <footPose>))
  (cl:+ 0
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'footPose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'torsoPose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <footPose>))
  "Converts a ROS message object to a list"
  (cl:list 'footPose
    (cl:cons ':footPose (footPose msg))
    (cl:cons ':torsoPose (torsoPose msg))
))
