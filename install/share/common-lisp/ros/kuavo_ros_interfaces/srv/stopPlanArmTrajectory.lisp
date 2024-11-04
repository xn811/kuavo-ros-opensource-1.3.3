; Auto-generated. Do not edit!


(cl:in-package kuavo_ros_interfaces-srv)


;//! \htmlinclude stopPlanArmTrajectory-request.msg.html

(cl:defclass <stopPlanArmTrajectory-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass stopPlanArmTrajectory-request (<stopPlanArmTrajectory-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <stopPlanArmTrajectory-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'stopPlanArmTrajectory-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-srv:<stopPlanArmTrajectory-request> is deprecated: use kuavo_ros_interfaces-srv:stopPlanArmTrajectory-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <stopPlanArmTrajectory-request>) ostream)
  "Serializes a message object of type '<stopPlanArmTrajectory-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <stopPlanArmTrajectory-request>) istream)
  "Deserializes a message object of type '<stopPlanArmTrajectory-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<stopPlanArmTrajectory-request>)))
  "Returns string type for a service object of type '<stopPlanArmTrajectory-request>"
  "kuavo_ros_interfaces/stopPlanArmTrajectoryRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'stopPlanArmTrajectory-request)))
  "Returns string type for a service object of type 'stopPlanArmTrajectory-request"
  "kuavo_ros_interfaces/stopPlanArmTrajectoryRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<stopPlanArmTrajectory-request>)))
  "Returns md5sum for a message object of type '<stopPlanArmTrajectory-request>"
  "eb13ac1f1354ccecb7941ee8fa2192e8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'stopPlanArmTrajectory-request)))
  "Returns md5sum for a message object of type 'stopPlanArmTrajectory-request"
  "eb13ac1f1354ccecb7941ee8fa2192e8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<stopPlanArmTrajectory-request>)))
  "Returns full string definition for message of type '<stopPlanArmTrajectory-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'stopPlanArmTrajectory-request)))
  "Returns full string definition for message of type 'stopPlanArmTrajectory-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <stopPlanArmTrajectory-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <stopPlanArmTrajectory-request>))
  "Converts a ROS message object to a list"
  (cl:list 'stopPlanArmTrajectory-request
))
;//! \htmlinclude stopPlanArmTrajectory-response.msg.html

(cl:defclass <stopPlanArmTrajectory-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass stopPlanArmTrajectory-response (<stopPlanArmTrajectory-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <stopPlanArmTrajectory-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'stopPlanArmTrajectory-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name kuavo_ros_interfaces-srv:<stopPlanArmTrajectory-response> is deprecated: use kuavo_ros_interfaces-srv:stopPlanArmTrajectory-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <stopPlanArmTrajectory-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader kuavo_ros_interfaces-srv:result-val is deprecated.  Use kuavo_ros_interfaces-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <stopPlanArmTrajectory-response>) ostream)
  "Serializes a message object of type '<stopPlanArmTrajectory-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <stopPlanArmTrajectory-response>) istream)
  "Deserializes a message object of type '<stopPlanArmTrajectory-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<stopPlanArmTrajectory-response>)))
  "Returns string type for a service object of type '<stopPlanArmTrajectory-response>"
  "kuavo_ros_interfaces/stopPlanArmTrajectoryResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'stopPlanArmTrajectory-response)))
  "Returns string type for a service object of type 'stopPlanArmTrajectory-response"
  "kuavo_ros_interfaces/stopPlanArmTrajectoryResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<stopPlanArmTrajectory-response>)))
  "Returns md5sum for a message object of type '<stopPlanArmTrajectory-response>"
  "eb13ac1f1354ccecb7941ee8fa2192e8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'stopPlanArmTrajectory-response)))
  "Returns md5sum for a message object of type 'stopPlanArmTrajectory-response"
  "eb13ac1f1354ccecb7941ee8fa2192e8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<stopPlanArmTrajectory-response>)))
  "Returns full string definition for message of type '<stopPlanArmTrajectory-response>"
  (cl:format cl:nil "bool result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'stopPlanArmTrajectory-response)))
  "Returns full string definition for message of type 'stopPlanArmTrajectory-response"
  (cl:format cl:nil "bool result~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <stopPlanArmTrajectory-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <stopPlanArmTrajectory-response>))
  "Converts a ROS message object to a list"
  (cl:list 'stopPlanArmTrajectory-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'stopPlanArmTrajectory)))
  'stopPlanArmTrajectory-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'stopPlanArmTrajectory)))
  'stopPlanArmTrajectory-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'stopPlanArmTrajectory)))
  "Returns string type for a service object of type '<stopPlanArmTrajectory>"
  "kuavo_ros_interfaces/stopPlanArmTrajectory")