; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-msg)


;//! \htmlinclude ikSolveError.msg.html

(cl:defclass <ikSolveError> (roslisp-msg-protocol:ros-message)
  ((ik_type
    :reader ik_type
    :initarg :ik_type
    :type cl:string
    :initform "")
   (left_pose_error
    :reader left_pose_error
    :initarg :left_pose_error
    :type motion_capture_ik-msg:handPose
    :initform (cl:make-instance 'motion_capture_ik-msg:handPose))
   (right_pose_error
    :reader right_pose_error
    :initarg :right_pose_error
    :type motion_capture_ik-msg:handPose
    :initform (cl:make-instance 'motion_capture_ik-msg:handPose)))
)

(cl:defclass ikSolveError (<ikSolveError>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ikSolveError>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ikSolveError)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-msg:<ikSolveError> is deprecated: use motion_capture_ik-msg:ikSolveError instead.")))

(cl:ensure-generic-function 'ik_type-val :lambda-list '(m))
(cl:defmethod ik_type-val ((m <ikSolveError>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:ik_type-val is deprecated.  Use motion_capture_ik-msg:ik_type instead.")
  (ik_type m))

(cl:ensure-generic-function 'left_pose_error-val :lambda-list '(m))
(cl:defmethod left_pose_error-val ((m <ikSolveError>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:left_pose_error-val is deprecated.  Use motion_capture_ik-msg:left_pose_error instead.")
  (left_pose_error m))

(cl:ensure-generic-function 'right_pose_error-val :lambda-list '(m))
(cl:defmethod right_pose_error-val ((m <ikSolveError>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:right_pose_error-val is deprecated.  Use motion_capture_ik-msg:right_pose_error instead.")
  (right_pose_error m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ikSolveError>) ostream)
  "Serializes a message object of type '<ikSolveError>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'ik_type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'ik_type))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'left_pose_error) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'right_pose_error) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ikSolveError>) istream)
  "Deserializes a message object of type '<ikSolveError>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ik_type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'ik_type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'left_pose_error) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'right_pose_error) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ikSolveError>)))
  "Returns string type for a message object of type '<ikSolveError>"
  "motion_capture_ik/ikSolveError")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ikSolveError)))
  "Returns string type for a message object of type 'ikSolveError"
  "motion_capture_ik/ikSolveError")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ikSolveError>)))
  "Returns md5sum for a message object of type '<ikSolveError>"
  "06c12c0e6e08f286627a6f856e26223c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ikSolveError)))
  "Returns md5sum for a message object of type 'ikSolveError"
  "06c12c0e6e08f286627a6f856e26223c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ikSolveError>)))
  "Returns full string definition for message of type '<ikSolveError>"
  (cl:format cl:nil "string     ik_type ~%handPose  left_pose_error~%handPose  right_pose_error~%================================================================================~%MSG: motion_capture_ik/handPose~%# pos~%float64 x~%float64 y~%float64 z~%# rpy~%float64 roll~%float64 pitch~%float64 yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ikSolveError)))
  "Returns full string definition for message of type 'ikSolveError"
  (cl:format cl:nil "string     ik_type ~%handPose  left_pose_error~%handPose  right_pose_error~%================================================================================~%MSG: motion_capture_ik/handPose~%# pos~%float64 x~%float64 y~%float64 z~%# rpy~%float64 roll~%float64 pitch~%float64 yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ikSolveError>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'ik_type))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'left_pose_error))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'right_pose_error))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ikSolveError>))
  "Converts a ROS message object to a list"
  (cl:list 'ikSolveError
    (cl:cons ':ik_type (ik_type msg))
    (cl:cons ':left_pose_error (left_pose_error msg))
    (cl:cons ':right_pose_error (right_pose_error msg))
))
