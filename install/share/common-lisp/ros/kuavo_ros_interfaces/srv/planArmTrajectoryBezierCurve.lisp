; Auto-generated. Do not edit!


(cl:in-package kuavo_ros_interfaces-srv)


;//! \htmlinclude planArmTrajectoryBezierCurve-request.msg.html

(cl:defclass <planArmTrajectoryBezierCurve-request> (roslisp-msg-protocol:ros-message)
  ((multi_joint_bezier_trajectory
    :reader multi_joint_bezier_trajectory
    :initarg :multi_joint_bezier_trajectory
    :type (cl:vector kuavo_ros_interfaces-msg:jointBezierTrajectory)
   :initform (cl:make-array 0 :element-type 'kuavo_ros_interfaces-msg:jointBezierTrajectory :initial-element (cl:make-instance 'kuavo_ros_interfaces-msg:jointBezierTrajectory)))
   (start_frame_time
    :reader start_frame_time
    :initarg :start_frame_time
    :type cl:float
    :initform 0.0)
   (end_frame_time
    :reader end_frame_time
    :initarg :end_frame_time
    :type cl:float
    :initform 0.0)
   (joint_names
    :reader joint_names
    :initarg :joint_names
    :type (cl:vector cl:string)
   :initform (cl:make-array 0 :element-type 'cl:string :initial-element "")))
)

(cl:defclass planArmTrajectoryBezierCurve-request (<planArmTrajectoryBezierCurve-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <planArmTrajectoryBezierCurve-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'planArmTrajectoryBezierCurve-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-srv:<planArmTrajectoryBezierCurve-request> is deprecated: use kuavo_ros_interfaces-srv:planArmTrajectoryBezierCurve-request instead.")))

(cl:ensure-generic-function 'multi_joint_bezier_trajectory-val :lambda-list '(m))
(cl:defmethod multi_joint_bezier_trajectory-val ((m <planArmTrajectoryBezierCurve-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:multi_joint_bezier_trajectory-val is deprecated.  Use kuavo_ros_interfaces-srv:multi_joint_bezier_trajectory instead.")
  (multi_joint_bezier_trajectory m))

(cl:ensure-generic-function 'start_frame_time-val :lambda-list '(m))
(cl:defmethod start_frame_time-val ((m <planArmTrajectoryBezierCurve-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:start_frame_time-val is deprecated.  Use kuavo_ros_interfaces-srv:start_frame_time instead.")
  (start_frame_time m))

(cl:ensure-generic-function 'end_frame_time-val :lambda-list '(m))
(cl:defmethod end_frame_time-val ((m <planArmTrajectoryBezierCurve-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:end_frame_time-val is deprecated.  Use kuavo_ros_interfaces-srv:end_frame_time instead.")
  (end_frame_time m))

(cl:ensure-generic-function 'joint_names-val :lambda-list '(m))
(cl:defmethod joint_names-val ((m <planArmTrajectoryBezierCurve-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:joint_names-val is deprecated.  Use kuavo_ros_interfaces-srv:joint_names instead.")
  (joint_names m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <planArmTrajectoryBezierCurve-request>) ostream)
  "Serializes a message object of type '<planArmTrajectoryBezierCurve-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'multi_joint_bezier_trajectory))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'multi_joint_bezier_trajectory))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'start_frame_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'end_frame_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'joint_names))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((__ros_str_len (cl:length ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) ele))
   (cl:slot-value msg 'joint_names))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <planArmTrajectoryBezierCurve-request>) istream)
  "Deserializes a message object of type '<planArmTrajectoryBezierCurve-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'multi_joint_bezier_trajectory) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'multi_joint_bezier_trajectory)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'kuavo_ros_interfaces-msg:jointBezierTrajectory))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'start_frame_time) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'end_frame_time) (roslisp-utils:decode-double-float-bits bits)))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'joint_names) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'joint_names)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:aref vals i) __ros_str_idx) (cl:code-char (cl:read-byte istream))))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<planArmTrajectoryBezierCurve-request>)))
  "Returns string type for a service object of type '<planArmTrajectoryBezierCurve-request>"
  "kuavo_ros_interfaces/planArmTrajectoryBezierCurveRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'planArmTrajectoryBezierCurve-request)))
  "Returns string type for a service object of type 'planArmTrajectoryBezierCurve-request"
  "kuavo_ros_interfaces/planArmTrajectoryBezierCurveRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<planArmTrajectoryBezierCurve-request>)))
  "Returns md5sum for a message object of type '<planArmTrajectoryBezierCurve-request>"
  "4dbc940608d7275f775b6fdef47eb369")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'planArmTrajectoryBezierCurve-request)))
  "Returns md5sum for a message object of type 'planArmTrajectoryBezierCurve-request"
  "4dbc940608d7275f775b6fdef47eb369")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<planArmTrajectoryBezierCurve-request>)))
  "Returns full string definition for message of type '<planArmTrajectoryBezierCurve-request>"
  (cl:format cl:nil "kuavo_ros_interfaces/jointBezierTrajectory[] multi_joint_bezier_trajectory~%float64 start_frame_time~%float64 end_frame_time~%string[] joint_names~%~%================================================================================~%MSG: kuavo_ros_interfaces/jointBezierTrajectory~%kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points~%================================================================================~%MSG: kuavo_ros_interfaces/bezierCurveCubicPoint~%# [x, y] x is time, y is value~%~%float64[] end_point~%float64[] left_control_point~%float64[] right_control_point~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'planArmTrajectoryBezierCurve-request)))
  "Returns full string definition for message of type 'planArmTrajectoryBezierCurve-request"
  (cl:format cl:nil "kuavo_ros_interfaces/jointBezierTrajectory[] multi_joint_bezier_trajectory~%float64 start_frame_time~%float64 end_frame_time~%string[] joint_names~%~%================================================================================~%MSG: kuavo_ros_interfaces/jointBezierTrajectory~%kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points~%================================================================================~%MSG: kuavo_ros_interfaces/bezierCurveCubicPoint~%# [x, y] x is time, y is value~%~%float64[] end_point~%float64[] left_control_point~%float64[] right_control_point~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <planArmTrajectoryBezierCurve-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'multi_joint_bezier_trajectory) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     8
     8
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'joint_names) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4 (cl:length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <planArmTrajectoryBezierCurve-request>))
  "Converts a ROS message object to a list"
  (cl:list 'planArmTrajectoryBezierCurve-request
    (cl:cons ':multi_joint_bezier_trajectory (multi_joint_bezier_trajectory msg))
    (cl:cons ':start_frame_time (start_frame_time msg))
    (cl:cons ':end_frame_time (end_frame_time msg))
    (cl:cons ':joint_names (joint_names msg))
))
;//! \htmlinclude planArmTrajectoryBezierCurve-response.msg.html

(cl:defclass <planArmTrajectoryBezierCurve-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass planArmTrajectoryBezierCurve-response (<planArmTrajectoryBezierCurve-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <planArmTrajectoryBezierCurve-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'planArmTrajectoryBezierCurve-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-srv:<planArmTrajectoryBezierCurve-response> is deprecated: use kuavo_ros_interfaces-srv:planArmTrajectoryBezierCurve-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <planArmTrajectoryBezierCurve-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:success-val is deprecated.  Use kuavo_ros_interfaces-srv:success instead.")
  (success m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <planArmTrajectoryBezierCurve-response>) ostream)
  "Serializes a message object of type '<planArmTrajectoryBezierCurve-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <planArmTrajectoryBezierCurve-response>) istream)
  "Deserializes a message object of type '<planArmTrajectoryBezierCurve-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<planArmTrajectoryBezierCurve-response>)))
  "Returns string type for a service object of type '<planArmTrajectoryBezierCurve-response>"
  "kuavo_ros_interfaces/planArmTrajectoryBezierCurveResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'planArmTrajectoryBezierCurve-response)))
  "Returns string type for a service object of type 'planArmTrajectoryBezierCurve-response"
  "kuavo_ros_interfaces/planArmTrajectoryBezierCurveResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<planArmTrajectoryBezierCurve-response>)))
  "Returns md5sum for a message object of type '<planArmTrajectoryBezierCurve-response>"
  "4dbc940608d7275f775b6fdef47eb369")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'planArmTrajectoryBezierCurve-response)))
  "Returns md5sum for a message object of type 'planArmTrajectoryBezierCurve-response"
  "4dbc940608d7275f775b6fdef47eb369")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<planArmTrajectoryBezierCurve-response>)))
  "Returns full string definition for message of type '<planArmTrajectoryBezierCurve-response>"
  (cl:format cl:nil "bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'planArmTrajectoryBezierCurve-response)))
  "Returns full string definition for message of type 'planArmTrajectoryBezierCurve-response"
  (cl:format cl:nil "bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <planArmTrajectoryBezierCurve-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <planArmTrajectoryBezierCurve-response>))
  "Converts a ROS message object to a list"
  (cl:list 'planArmTrajectoryBezierCurve-response
    (cl:cons ':success (success msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'planArmTrajectoryBezierCurve)))
  'planArmTrajectoryBezierCurve-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'planArmTrajectoryBezierCurve)))
  'planArmTrajectoryBezierCurve-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'planArmTrajectoryBezierCurve)))
  "Returns string type for a service object of type '<planArmTrajectoryBezierCurve>"
  "kuavo_ros_interfaces/planArmTrajectoryBezierCurve")