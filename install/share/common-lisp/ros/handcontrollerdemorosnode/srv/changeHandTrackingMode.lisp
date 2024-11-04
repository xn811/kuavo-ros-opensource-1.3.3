; Auto-generated. Do not edit!


(cl:in-package handcontrollerdemorosnode-srv)


;//! \htmlinclude changeHandTrackingMode-request.msg.html

(cl:defclass <changeHandTrackingMode-request> (roslisp-msg-protocol:ros-message)
  ((enable
    :reader enable
    :initarg :enable
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass changeHandTrackingMode-request (<changeHandTrackingMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeHandTrackingMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeHandTrackingMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name handcontrollerdemorosnode-srv:<changeHandTrackingMode-request> is deprecated: use handcontrollerdemorosnode-srv:changeHandTrackingMode-request instead.")))

(cl:ensure-generic-function 'enable-val :lambda-list '(m))
(cl:defmethod enable-val ((m <changeHandTrackingMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-srv:enable-val is deprecated.  Use handcontrollerdemorosnode-srv:enable instead.")
  (enable m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeHandTrackingMode-request>) ostream)
  "Serializes a message object of type '<changeHandTrackingMode-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'enable) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeHandTrackingMode-request>) istream)
  "Deserializes a message object of type '<changeHandTrackingMode-request>"
    (cl:setf (cl:slot-value msg 'enable) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeHandTrackingMode-request>)))
  "Returns string type for a service object of type '<changeHandTrackingMode-request>"
  "handcontrollerdemorosnode/changeHandTrackingModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandTrackingMode-request)))
  "Returns string type for a service object of type 'changeHandTrackingMode-request"
  "handcontrollerdemorosnode/changeHandTrackingModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeHandTrackingMode-request>)))
  "Returns md5sum for a message object of type '<changeHandTrackingMode-request>"
  "29d58f387352c15c4e4f5763022ae875")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeHandTrackingMode-request)))
  "Returns md5sum for a message object of type 'changeHandTrackingMode-request"
  "29d58f387352c15c4e4f5763022ae875")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeHandTrackingMode-request>)))
  "Returns full string definition for message of type '<changeHandTrackingMode-request>"
  (cl:format cl:nil "bool enable~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeHandTrackingMode-request)))
  "Returns full string definition for message of type 'changeHandTrackingMode-request"
  (cl:format cl:nil "bool enable~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeHandTrackingMode-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeHandTrackingMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'changeHandTrackingMode-request
    (cl:cons ':enable (enable msg))
))
;//! \htmlinclude changeHandTrackingMode-response.msg.html

(cl:defclass <changeHandTrackingMode-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass changeHandTrackingMode-response (<changeHandTrackingMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <changeHandTrackingMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'changeHandTrackingMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name handcontrollerdemorosnode-srv:<changeHandTrackingMode-response> is deprecated: use handcontrollerdemorosnode-srv:changeHandTrackingMode-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <changeHandTrackingMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader handcontrollerdemorosnode-srv:result-val is deprecated.  Use handcontrollerdemorosnode-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <changeHandTrackingMode-response>) ostream)
  "Serializes a message object of type '<changeHandTrackingMode-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <changeHandTrackingMode-response>) istream)
  "Deserializes a message object of type '<changeHandTrackingMode-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<changeHandTrackingMode-response>)))
  "Returns string type for a service object of type '<changeHandTrackingMode-response>"
  "handcontrollerdemorosnode/changeHandTrackingModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandTrackingMode-response)))
  "Returns string type for a service object of type 'changeHandTrackingMode-response"
  "handcontrollerdemorosnode/changeHandTrackingModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<changeHandTrackingMode-response>)))
  "Returns md5sum for a message object of type '<changeHandTrackingMode-response>"
  "29d58f387352c15c4e4f5763022ae875")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'changeHandTrackingMode-response)))
  "Returns md5sum for a message object of type 'changeHandTrackingMode-response"
  "29d58f387352c15c4e4f5763022ae875")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<changeHandTrackingMode-response>)))
  "Returns full string definition for message of type '<changeHandTrackingMode-response>"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'changeHandTrackingMode-response)))
  "Returns full string definition for message of type 'changeHandTrackingMode-response"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <changeHandTrackingMode-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <changeHandTrackingMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'changeHandTrackingMode-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'changeHandTrackingMode)))
  'changeHandTrackingMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'changeHandTrackingMode)))
  'changeHandTrackingMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'changeHandTrackingMode)))
  "Returns string type for a service object of type '<changeHandTrackingMode>"
  "handcontrollerdemorosnode/changeHandTrackingMode")