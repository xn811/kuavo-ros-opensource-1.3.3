; Auto-generated. Do not edit!


(cl:in-package kuavo_ros_interfaces-msg)


;//! \htmlinclude jointBezierTrajectory.msg.html

(cl:defclass <jointBezierTrajectory> (roslisp-msg-protocol:ros-message)
  ((bezier_curve_points
    :reader bezier_curve_points
    :initarg :bezier_curve_points
    :type (cl:vector kuavo_ros_interfaces-msg:bezierCurveCubicPoint)
   :initform (cl:make-array 0 :element-type 'kuavo_ros_interfaces-msg:bezierCurveCubicPoint :initial-element (cl:make-instance 'kuavo_ros_interfaces-msg:bezierCurveCubicPoint))))
)

(cl:defclass jointBezierTrajectory (<jointBezierTrajectory>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <jointBezierTrajectory>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'jointBezierTrajectory)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-msg:<jointBezierTrajectory> is deprecated: use kuavo_ros_interfaces-msg:jointBezierTrajectory instead.")))

(cl:ensure-generic-function 'bezier_curve_points-val :lambda-list '(m))
(cl:defmethod bezier_curve_points-val ((m <jointBezierTrajectory>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-msg:bezier_curve_points-val is deprecated.  Use kuavo_ros_interfaces-msg:bezier_curve_points instead.")
  (bezier_curve_points m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <jointBezierTrajectory>) ostream)
  "Serializes a message object of type '<jointBezierTrajectory>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'bezier_curve_points))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'bezier_curve_points))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <jointBezierTrajectory>) istream)
  "Deserializes a message object of type '<jointBezierTrajectory>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'bezier_curve_points) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'bezier_curve_points)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'kuavo_ros_interfaces-msg:bezierCurveCubicPoint))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<jointBezierTrajectory>)))
  "Returns string type for a message object of type '<jointBezierTrajectory>"
  "kuavo_ros_interfaces/jointBezierTrajectory")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'jointBezierTrajectory)))
  "Returns string type for a message object of type 'jointBezierTrajectory"
  "kuavo_ros_interfaces/jointBezierTrajectory")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<jointBezierTrajectory>)))
  "Returns md5sum for a message object of type '<jointBezierTrajectory>"
  "734a11eb72071b59bdbb297c6a53338c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'jointBezierTrajectory)))
  "Returns md5sum for a message object of type 'jointBezierTrajectory"
  "734a11eb72071b59bdbb297c6a53338c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<jointBezierTrajectory>)))
  "Returns full string definition for message of type '<jointBezierTrajectory>"
  (cl:format cl:nil "kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points~%================================================================================~%MSG: kuavo_ros_interfaces/bezierCurveCubicPoint~%# [x, y] x is time, y is value~%~%float64[] end_point~%float64[] left_control_point~%float64[] right_control_point~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'jointBezierTrajectory)))
  "Returns full string definition for message of type 'jointBezierTrajectory"
  (cl:format cl:nil "kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points~%================================================================================~%MSG: kuavo_ros_interfaces/bezierCurveCubicPoint~%# [x, y] x is time, y is value~%~%float64[] end_point~%float64[] left_control_point~%float64[] right_control_point~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <jointBezierTrajectory>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'bezier_curve_points) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <jointBezierTrajectory>))
  "Converts a ROS message object to a list"
  (cl:list 'jointBezierTrajectory
    (cl:cons ':bezier_curve_points (bezier_curve_points msg))
))
