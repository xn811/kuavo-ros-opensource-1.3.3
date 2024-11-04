; Auto-generated. Do not edit!


(cl:in-package motion_capture_ik-msg)


;//! \htmlinclude ikSolveParam.msg.html

(cl:defclass <ikSolveParam> (roslisp-msg-protocol:ros-message)
  ((major_optimality_tol
    :reader major_optimality_tol
    :initarg :major_optimality_tol
    :type cl:float
    :initform 0.0)
   (major_feasibility_tol
    :reader major_feasibility_tol
    :initarg :major_feasibility_tol
    :type cl:float
    :initform 0.0)
   (minor_feasibility_tol
    :reader minor_feasibility_tol
    :initarg :minor_feasibility_tol
    :type cl:float
    :initform 0.0)
   (major_iterations_limit
    :reader major_iterations_limit
    :initarg :major_iterations_limit
    :type cl:float
    :initform 0.0)
   (oritation_constraint_tol
    :reader oritation_constraint_tol
    :initarg :oritation_constraint_tol
    :type cl:float
    :initform 0.0)
   (pos_constraint_tol
    :reader pos_constraint_tol
    :initarg :pos_constraint_tol
    :type cl:float
    :initform 0.0)
   (pos_cost_weight
    :reader pos_cost_weight
    :initarg :pos_cost_weight
    :type cl:float
    :initform 0.0))
)

(cl:defclass ikSolveParam (<ikSolveParam>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ikSolveParam>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ikSolveParam)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name motion_capture_ik-msg:<ikSolveParam> is deprecated: use motion_capture_ik-msg:ikSolveParam instead.")))

(cl:ensure-generic-function 'major_optimality_tol-val :lambda-list '(m))
(cl:defmethod major_optimality_tol-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:major_optimality_tol-val is deprecated.  Use motion_capture_ik-msg:major_optimality_tol instead.")
  (major_optimality_tol m))

(cl:ensure-generic-function 'major_feasibility_tol-val :lambda-list '(m))
(cl:defmethod major_feasibility_tol-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:major_feasibility_tol-val is deprecated.  Use motion_capture_ik-msg:major_feasibility_tol instead.")
  (major_feasibility_tol m))

(cl:ensure-generic-function 'minor_feasibility_tol-val :lambda-list '(m))
(cl:defmethod minor_feasibility_tol-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:minor_feasibility_tol-val is deprecated.  Use motion_capture_ik-msg:minor_feasibility_tol instead.")
  (minor_feasibility_tol m))

(cl:ensure-generic-function 'major_iterations_limit-val :lambda-list '(m))
(cl:defmethod major_iterations_limit-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:major_iterations_limit-val is deprecated.  Use motion_capture_ik-msg:major_iterations_limit instead.")
  (major_iterations_limit m))

(cl:ensure-generic-function 'oritation_constraint_tol-val :lambda-list '(m))
(cl:defmethod oritation_constraint_tol-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:oritation_constraint_tol-val is deprecated.  Use motion_capture_ik-msg:oritation_constraint_tol instead.")
  (oritation_constraint_tol m))

(cl:ensure-generic-function 'pos_constraint_tol-val :lambda-list '(m))
(cl:defmethod pos_constraint_tol-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:pos_constraint_tol-val is deprecated.  Use motion_capture_ik-msg:pos_constraint_tol instead.")
  (pos_constraint_tol m))

(cl:ensure-generic-function 'pos_cost_weight-val :lambda-list '(m))
(cl:defmethod pos_cost_weight-val ((m <ikSolveParam>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader motion_capture_ik-msg:pos_cost_weight-val is deprecated.  Use motion_capture_ik-msg:pos_cost_weight instead.")
  (pos_cost_weight m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ikSolveParam>) ostream)
  "Serializes a message object of type '<ikSolveParam>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'major_optimality_tol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'major_feasibility_tol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'minor_feasibility_tol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'major_iterations_limit))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'oritation_constraint_tol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'pos_constraint_tol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'pos_cost_weight))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ikSolveParam>) istream)
  "Deserializes a message object of type '<ikSolveParam>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'major_optimality_tol) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'major_feasibility_tol) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'minor_feasibility_tol) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'major_iterations_limit) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'oritation_constraint_tol) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'pos_constraint_tol) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'pos_cost_weight) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ikSolveParam>)))
  "Returns string type for a message object of type '<ikSolveParam>"
  "motion_capture_ik/ikSolveParam")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ikSolveParam)))
  "Returns string type for a message object of type 'ikSolveParam"
  "motion_capture_ik/ikSolveParam")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ikSolveParam>)))
  "Returns md5sum for a message object of type '<ikSolveParam>"
  "be29d8b02ad14da680464b8c4f590f98")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ikSolveParam)))
  "Returns md5sum for a message object of type 'ikSolveParam"
  "be29d8b02ad14da680464b8c4f590f98")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ikSolveParam>)))
  "Returns full string definition for message of type '<ikSolveParam>"
  (cl:format cl:nil "# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ikSolveParam)))
  "Returns full string definition for message of type 'ikSolveParam"
  (cl:format cl:nil "# snopt params~%float64 major_optimality_tol~%float64 major_feasibility_tol~%float64 minor_feasibility_tol~%float64 major_iterations_limit~%# constraint and cost params~%float64 oritation_constraint_tol~%float64 pos_constraint_tol # work when pos_cost_weight > 0.0~%float64 pos_cost_weight~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ikSolveParam>))
  (cl:+ 0
     8
     8
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ikSolveParam>))
  "Converts a ROS message object to a list"
  (cl:list 'ikSolveParam
    (cl:cons ':major_optimality_tol (major_optimality_tol msg))
    (cl:cons ':major_feasibility_tol (major_feasibility_tol msg))
    (cl:cons ':minor_feasibility_tol (minor_feasibility_tol msg))
    (cl:cons ':major_iterations_limit (major_iterations_limit msg))
    (cl:cons ':oritation_constraint_tol (oritation_constraint_tol msg))
    (cl:cons ':pos_constraint_tol (pos_constraint_tol msg))
    (cl:cons ':pos_cost_weight (pos_cost_weight msg))
))
