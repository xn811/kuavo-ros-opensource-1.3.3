; Auto-generated. Do not edit!


(cl:in-package noitom_hi5_hand_udp_python-msg)


;//! \htmlinclude JoySticks.msg.html

(cl:defclass <JoySticks> (roslisp-msg-protocol:ros-message)
  ((left_x
    :reader left_x
    :initarg :left_x
    :type cl:float
    :initform 0.0)
   (left_y
    :reader left_y
    :initarg :left_y
    :type cl:float
    :initform 0.0)
   (left_trigger
    :reader left_trigger
    :initarg :left_trigger
    :type cl:float
    :initform 0.0)
   (left_grip
    :reader left_grip
    :initarg :left_grip
    :type cl:float
    :initform 0.0)
   (left_first_button_pressed
    :reader left_first_button_pressed
    :initarg :left_first_button_pressed
    :type cl:boolean
    :initform cl:nil)
   (left_second_button_pressed
    :reader left_second_button_pressed
    :initarg :left_second_button_pressed
    :type cl:boolean
    :initform cl:nil)
   (left_first_button_touched
    :reader left_first_button_touched
    :initarg :left_first_button_touched
    :type cl:boolean
    :initform cl:nil)
   (left_second_button_touched
    :reader left_second_button_touched
    :initarg :left_second_button_touched
    :type cl:boolean
    :initform cl:nil)
   (right_x
    :reader right_x
    :initarg :right_x
    :type cl:float
    :initform 0.0)
   (right_y
    :reader right_y
    :initarg :right_y
    :type cl:float
    :initform 0.0)
   (right_trigger
    :reader right_trigger
    :initarg :right_trigger
    :type cl:float
    :initform 0.0)
   (right_grip
    :reader right_grip
    :initarg :right_grip
    :type cl:float
    :initform 0.0)
   (right_first_button_pressed
    :reader right_first_button_pressed
    :initarg :right_first_button_pressed
    :type cl:boolean
    :initform cl:nil)
   (right_second_button_pressed
    :reader right_second_button_pressed
    :initarg :right_second_button_pressed
    :type cl:boolean
    :initform cl:nil)
   (right_first_button_touched
    :reader right_first_button_touched
    :initarg :right_first_button_touched
    :type cl:boolean
    :initform cl:nil)
   (right_second_button_touched
    :reader right_second_button_touched
    :initarg :right_second_button_touched
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass JoySticks (<JoySticks>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <JoySticks>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'JoySticks)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name noitom_hi5_hand_udp_python-msg:<JoySticks> is deprecated: use noitom_hi5_hand_udp_python-msg:JoySticks instead.")))

(cl:ensure-generic-function 'left_x-val :lambda-list '(m))
(cl:defmethod left_x-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_x-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_x instead.")
  (left_x m))

(cl:ensure-generic-function 'left_y-val :lambda-list '(m))
(cl:defmethod left_y-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_y-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_y instead.")
  (left_y m))

(cl:ensure-generic-function 'left_trigger-val :lambda-list '(m))
(cl:defmethod left_trigger-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_trigger-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_trigger instead.")
  (left_trigger m))

(cl:ensure-generic-function 'left_grip-val :lambda-list '(m))
(cl:defmethod left_grip-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_grip-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_grip instead.")
  (left_grip m))

(cl:ensure-generic-function 'left_first_button_pressed-val :lambda-list '(m))
(cl:defmethod left_first_button_pressed-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_first_button_pressed-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_first_button_pressed instead.")
  (left_first_button_pressed m))

(cl:ensure-generic-function 'left_second_button_pressed-val :lambda-list '(m))
(cl:defmethod left_second_button_pressed-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_second_button_pressed-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_second_button_pressed instead.")
  (left_second_button_pressed m))

(cl:ensure-generic-function 'left_first_button_touched-val :lambda-list '(m))
(cl:defmethod left_first_button_touched-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_first_button_touched-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_first_button_touched instead.")
  (left_first_button_touched m))

(cl:ensure-generic-function 'left_second_button_touched-val :lambda-list '(m))
(cl:defmethod left_second_button_touched-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:left_second_button_touched-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:left_second_button_touched instead.")
  (left_second_button_touched m))

(cl:ensure-generic-function 'right_x-val :lambda-list '(m))
(cl:defmethod right_x-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_x-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_x instead.")
  (right_x m))

(cl:ensure-generic-function 'right_y-val :lambda-list '(m))
(cl:defmethod right_y-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_y-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_y instead.")
  (right_y m))

(cl:ensure-generic-function 'right_trigger-val :lambda-list '(m))
(cl:defmethod right_trigger-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_trigger-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_trigger instead.")
  (right_trigger m))

(cl:ensure-generic-function 'right_grip-val :lambda-list '(m))
(cl:defmethod right_grip-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_grip-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_grip instead.")
  (right_grip m))

(cl:ensure-generic-function 'right_first_button_pressed-val :lambda-list '(m))
(cl:defmethod right_first_button_pressed-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_first_button_pressed-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_first_button_pressed instead.")
  (right_first_button_pressed m))

(cl:ensure-generic-function 'right_second_button_pressed-val :lambda-list '(m))
(cl:defmethod right_second_button_pressed-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_second_button_pressed-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_second_button_pressed instead.")
  (right_second_button_pressed m))

(cl:ensure-generic-function 'right_first_button_touched-val :lambda-list '(m))
(cl:defmethod right_first_button_touched-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_first_button_touched-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_first_button_touched instead.")
  (right_first_button_touched m))

(cl:ensure-generic-function 'right_second_button_touched-val :lambda-list '(m))
(cl:defmethod right_second_button_touched-val ((m <JoySticks>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader noitom_hi5_hand_udp_python-msg:right_second_button_touched-val is deprecated.  Use noitom_hi5_hand_udp_python-msg:right_second_button_touched instead.")
  (right_second_button_touched m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <JoySticks>) ostream)
  "Serializes a message object of type '<JoySticks>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'left_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'left_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'left_trigger))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'left_grip))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'left_first_button_pressed) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'left_second_button_pressed) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'left_first_button_touched) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'left_second_button_touched) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'right_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'right_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'right_trigger))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'right_grip))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'right_first_button_pressed) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'right_second_button_pressed) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'right_first_button_touched) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'right_second_button_touched) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <JoySticks>) istream)
  "Deserializes a message object of type '<JoySticks>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'left_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'left_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'left_trigger) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'left_grip) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'left_first_button_pressed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'left_second_button_pressed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'left_first_button_touched) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'left_second_button_touched) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'right_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'right_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'right_trigger) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'right_grip) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'right_first_button_pressed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'right_second_button_pressed) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'right_first_button_touched) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'right_second_button_touched) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<JoySticks>)))
  "Returns string type for a message object of type '<JoySticks>"
  "noitom_hi5_hand_udp_python/JoySticks")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'JoySticks)))
  "Returns string type for a message object of type 'JoySticks"
  "noitom_hi5_hand_udp_python/JoySticks")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<JoySticks>)))
  "Returns md5sum for a message object of type '<JoySticks>"
  "c686b65cdd180a9046db651d6492ec65")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'JoySticks)))
  "Returns md5sum for a message object of type 'JoySticks"
  "c686b65cdd180a9046db651d6492ec65")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<JoySticks>)))
  "Returns full string definition for message of type '<JoySticks>"
  (cl:format cl:nil "float32 left_x~%float32 left_y~%float32 left_trigger~%float32 left_grip~%bool left_first_button_pressed~%bool left_second_button_pressed~%bool left_first_button_touched~%bool left_second_button_touched~%float32 right_x~%float32 right_y~%float32 right_trigger~%float32 right_grip~%bool right_first_button_pressed~%bool right_second_button_pressed~%bool right_first_button_touched~%bool right_second_button_touched~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'JoySticks)))
  "Returns full string definition for message of type 'JoySticks"
  (cl:format cl:nil "float32 left_x~%float32 left_y~%float32 left_trigger~%float32 left_grip~%bool left_first_button_pressed~%bool left_second_button_pressed~%bool left_first_button_touched~%bool left_second_button_touched~%float32 right_x~%float32 right_y~%float32 right_trigger~%float32 right_grip~%bool right_first_button_pressed~%bool right_second_button_pressed~%bool right_first_button_touched~%bool right_second_button_touched~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <JoySticks>))
  (cl:+ 0
     4
     4
     4
     4
     1
     1
     1
     1
     4
     4
     4
     4
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <JoySticks>))
  "Converts a ROS message object to a list"
  (cl:list 'JoySticks
    (cl:cons ':left_x (left_x msg))
    (cl:cons ':left_y (left_y msg))
    (cl:cons ':left_trigger (left_trigger msg))
    (cl:cons ':left_grip (left_grip msg))
    (cl:cons ':left_first_button_pressed (left_first_button_pressed msg))
    (cl:cons ':left_second_button_pressed (left_second_button_pressed msg))
    (cl:cons ':left_first_button_touched (left_first_button_touched msg))
    (cl:cons ':left_second_button_touched (left_second_button_touched msg))
    (cl:cons ':right_x (right_x msg))
    (cl:cons ':right_y (right_y msg))
    (cl:cons ':right_trigger (right_trigger msg))
    (cl:cons ':right_grip (right_grip msg))
    (cl:cons ':right_first_button_pressed (right_first_button_pressed msg))
    (cl:cons ':right_second_button_pressed (right_second_button_pressed msg))
    (cl:cons ':right_first_button_touched (right_first_button_touched msg))
    (cl:cons ':right_second_button_touched (right_second_button_touched msg))
))
