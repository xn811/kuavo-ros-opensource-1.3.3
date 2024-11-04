; Auto-generated. Do not edit!


(cl:in-package kuavo_msgs-srv)


;//! \htmlinclude singleStepControl-request.msg.html

(cl:defclass <singleStepControl-request> (roslisp-msg-protocol:ros-message)
  ((foot_pose_target_trajectories
    :reader foot_pose_target_trajectories
    :initarg :foot_pose_target_trajectories
    :type kuavo_msgs-msg:footPoseTargetTrajectories
    :initform (cl:make-instance 'kuavo_msgs-msg:footPoseTargetTrajectories)))
)

(cl:defclass singleStepControl-request (<singleStepControl-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <singleStepControl-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'singleStepControl-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<singleStepControl-request> is deprecated: use kuavo_msgs-srv:singleStepControl-request instead.")))

(cl:ensure-generic-function 'foot_pose_target_trajectories-val :lambda-list '(m))
(cl:defmethod foot_pose_target_trajectories-val ((m <singleStepControl-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:foot_pose_target_trajectories-val is deprecated.  Use kuavo_msgs-srv:foot_pose_target_trajectories instead.")
  (foot_pose_target_trajectories m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <singleStepControl-request>) ostream)
  "Serializes a message object of type '<singleStepControl-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'foot_pose_target_trajectories) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <singleStepControl-request>) istream)
  "Deserializes a message object of type '<singleStepControl-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'foot_pose_target_trajectories) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<singleStepControl-request>)))
  "Returns string type for a service object of type '<singleStepControl-request>"
  "kuavo_msgs/singleStepControlRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'singleStepControl-request)))
  "Returns string type for a service object of type 'singleStepControl-request"
  "kuavo_msgs/singleStepControlRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<singleStepControl-request>)))
  "Returns md5sum for a message object of type '<singleStepControl-request>"
  "9a5a8ad57a17963a16bf197fc7a66fa4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'singleStepControl-request)))
  "Returns md5sum for a message object of type 'singleStepControl-request"
  "9a5a8ad57a17963a16bf197fc7a66fa4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<singleStepControl-request>)))
  "Returns full string definition for message of type '<singleStepControl-request>"
  (cl:format cl:nil "footPoseTargetTrajectories foot_pose_target_trajectories~%~%================================================================================~%MSG: kuavo_msgs/footPoseTargetTrajectories~%float64[]    timeTrajectory~%int32[]      footIndexTrajectory~%footPose[]   footPoseTrajectory~%================================================================================~%MSG: kuavo_msgs/footPose~%float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'singleStepControl-request)))
  "Returns full string definition for message of type 'singleStepControl-request"
  (cl:format cl:nil "footPoseTargetTrajectories foot_pose_target_trajectories~%~%================================================================================~%MSG: kuavo_msgs/footPoseTargetTrajectories~%float64[]    timeTrajectory~%int32[]      footIndexTrajectory~%footPose[]   footPoseTrajectory~%================================================================================~%MSG: kuavo_msgs/footPose~%float64[4] footPose # x, y, z, yaw~%float64[4] torsoPose # x, y, z, yaw~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <singleStepControl-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'foot_pose_target_trajectories))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <singleStepControl-request>))
  "Converts a ROS message object to a list"
  (cl:list 'singleStepControl-request
    (cl:cons ':foot_pose_target_trajectories (foot_pose_target_trajectories msg))
))
;//! \htmlinclude singleStepControl-response.msg.html

(cl:defclass <singleStepControl-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass singleStepControl-response (<singleStepControl-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <singleStepControl-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'singleStepControl-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_msgs-srv:<singleStepControl-response> is deprecated: use kuavo_msgs-srv:singleStepControl-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <singleStepControl-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:success-val is deprecated.  Use kuavo_msgs-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <singleStepControl-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_msgs-srv:message-val is deprecated.  Use kuavo_msgs-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <singleStepControl-response>) ostream)
  "Serializes a message object of type '<singleStepControl-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <singleStepControl-response>) istream)
  "Deserializes a message object of type '<singleStepControl-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<singleStepControl-response>)))
  "Returns string type for a service object of type '<singleStepControl-response>"
  "kuavo_msgs/singleStepControlResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'singleStepControl-response)))
  "Returns string type for a service object of type 'singleStepControl-response"
  "kuavo_msgs/singleStepControlResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<singleStepControl-response>)))
  "Returns md5sum for a message object of type '<singleStepControl-response>"
  "9a5a8ad57a17963a16bf197fc7a66fa4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'singleStepControl-response)))
  "Returns md5sum for a message object of type 'singleStepControl-response"
  "9a5a8ad57a17963a16bf197fc7a66fa4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<singleStepControl-response>)))
  "Returns full string definition for message of type '<singleStepControl-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'singleStepControl-response)))
  "Returns full string definition for message of type 'singleStepControl-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <singleStepControl-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <singleStepControl-response>))
  "Converts a ROS message object to a list"
  (cl:list 'singleStepControl-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'singleStepControl)))
  'singleStepControl-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'singleStepControl)))
  'singleStepControl-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'singleStepControl)))
  "Returns string type for a service object of type '<singleStepControl>"
  "kuavo_msgs/singleStepControl")