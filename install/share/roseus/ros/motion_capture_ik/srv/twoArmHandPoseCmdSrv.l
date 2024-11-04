;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::twoArmHandPoseCmdSrv)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'twoArmHandPoseCmdSrv (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRV")
  (make-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRV"))
(unless (find-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRVREQUEST")
  (make-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRVREQUEST"))
(unless (find-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRVRESPONSE")
  (make-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMDSRVRESPONSE"))

(in-package "ROS")





(defclass motion_capture_ik::twoArmHandPoseCmdSrvRequest
  :super ros::object
  :slots (_twoArmHandPoseCmdRequest ))

(defmethod motion_capture_ik::twoArmHandPoseCmdSrvRequest
  (:init
   (&key
    ((:twoArmHandPoseCmdRequest __twoArmHandPoseCmdRequest) (instance motion_capture_ik::twoArmHandPoseCmd :init))
    )
   (send-super :init)
   (setq _twoArmHandPoseCmdRequest __twoArmHandPoseCmdRequest)
   self)
  (:twoArmHandPoseCmdRequest
   (&rest __twoArmHandPoseCmdRequest)
   (if (keywordp (car __twoArmHandPoseCmdRequest))
       (send* _twoArmHandPoseCmdRequest __twoArmHandPoseCmdRequest)
     (progn
       (if __twoArmHandPoseCmdRequest (setq _twoArmHandPoseCmdRequest (car __twoArmHandPoseCmdRequest)))
       _twoArmHandPoseCmdRequest)))
  (:serialization-length
   ()
   (+
    ;; motion_capture_ik/twoArmHandPoseCmd _twoArmHandPoseCmdRequest
    (send _twoArmHandPoseCmdRequest :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; motion_capture_ik/twoArmHandPoseCmd _twoArmHandPoseCmdRequest
       (send _twoArmHandPoseCmdRequest :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; motion_capture_ik/twoArmHandPoseCmd _twoArmHandPoseCmdRequest
     (send _twoArmHandPoseCmdRequest :deserialize buf ptr-) (incf ptr- (send _twoArmHandPoseCmdRequest :serialization-length))
   ;;
   self)
  )

(defclass motion_capture_ik::twoArmHandPoseCmdSrvResponse
  :super ros::object
  :slots (_success _with_torso _q_arm _q_torso _time_cost _hand_poses ))

(defmethod motion_capture_ik::twoArmHandPoseCmdSrvResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:with_torso __with_torso) nil)
    ((:q_arm __q_arm) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_torso __q_torso) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:time_cost __time_cost) 0.0)
    ((:hand_poses __hand_poses) (instance motion_capture_ik::twoArmHandPose :init))
    )
   (send-super :init)
   (setq _success __success)
   (setq _with_torso __with_torso)
   (setq _q_arm __q_arm)
   (setq _q_torso __q_torso)
   (setq _time_cost (float __time_cost))
   (setq _hand_poses __hand_poses)
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:with_torso
   (&optional (__with_torso :null))
   (if (not (eq __with_torso :null)) (setq _with_torso __with_torso)) _with_torso)
  (:q_arm
   (&optional __q_arm)
   (if __q_arm (setq _q_arm __q_arm)) _q_arm)
  (:q_torso
   (&optional __q_torso)
   (if __q_torso (setq _q_torso __q_torso)) _q_torso)
  (:time_cost
   (&optional __time_cost)
   (if __time_cost (setq _time_cost __time_cost)) _time_cost)
  (:hand_poses
   (&rest __hand_poses)
   (if (keywordp (car __hand_poses))
       (send* _hand_poses __hand_poses)
     (progn
       (if __hand_poses (setq _hand_poses (car __hand_poses)))
       _hand_poses)))
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; bool _with_torso
    1
    ;; float64[] _q_arm
    (* 8    (length _q_arm)) 4
    ;; float64[] _q_torso
    (* 8    (length _q_torso)) 4
    ;; float64 _time_cost
    8
    ;; motion_capture_ik/twoArmHandPose _hand_poses
    (send _hand_poses :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; bool _with_torso
       (if _with_torso (write-byte -1 s) (write-byte 0 s))
     ;; float64[] _q_arm
     (write-long (length _q_arm) s)
     (dotimes (i (length _q_arm))
       (sys::poke (elt _q_arm i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _q_torso
     (write-long (length _q_torso) s)
     (dotimes (i (length _q_torso))
       (sys::poke (elt _q_torso i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64 _time_cost
       (sys::poke _time_cost (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; motion_capture_ik/twoArmHandPose _hand_poses
       (send _hand_poses :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _with_torso
     (setq _with_torso (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64[] _q_arm
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_arm (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_arm i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _q_torso
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_torso (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_torso i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64 _time_cost
     (setq _time_cost (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; motion_capture_ik/twoArmHandPose _hand_poses
     (send _hand_poses :deserialize buf ptr-) (incf ptr- (send _hand_poses :serialization-length))
   ;;
   self)
  )

(defclass motion_capture_ik::twoArmHandPoseCmdSrv
  :super ros::object
  :slots ())

(setf (get motion_capture_ik::twoArmHandPoseCmdSrv :md5sum-) "4cedfbf98f38ce7e92b358cb2d3ef39d")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrv :datatype-) "motion_capture_ik/twoArmHandPoseCmdSrv")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrv :request) motion_capture_ik::twoArmHandPoseCmdSrvRequest)
(setf (get motion_capture_ik::twoArmHandPoseCmdSrv :response) motion_capture_ik::twoArmHandPoseCmdSrvResponse)

(defmethod motion_capture_ik::twoArmHandPoseCmdSrvRequest
  (:response () (instance motion_capture_ik::twoArmHandPoseCmdSrvResponse :init)))

(setf (get motion_capture_ik::twoArmHandPoseCmdSrvRequest :md5sum-) "4cedfbf98f38ce7e92b358cb2d3ef39d")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrvRequest :datatype-) "motion_capture_ik/twoArmHandPoseCmdSrvRequest")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrvRequest :definition-)
      "twoArmHandPoseCmd twoArmHandPoseCmdRequest

================================================================================
MSG: motion_capture_ik/twoArmHandPoseCmd
twoArmHandPose  hand_poses
# params for the IK solver
bool use_custom_ik_param
bool joint_angles_as_q0
ikSolveParam ik_param
================================================================================
MSG: motion_capture_ik/twoArmHandPose
Header header
armHandPose  left_pose
armHandPose  right_pose
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: motion_capture_ik/armHandPose
float64[3] pos_xyz
float64[4] quat_xyzw

float64[3] elbow_pos_xyz

float64[7] joint_angles
================================================================================
MSG: motion_capture_ik/ikSolveParam
# snopt params
float64 major_optimality_tol
float64 major_feasibility_tol
float64 minor_feasibility_tol
float64 major_iterations_limit
# constraint and cost params
float64 oritation_constraint_tol
float64 pos_constraint_tol # work when pos_cost_weight > 0.0
---
bool success
bool with_torso
float64[] q_arm
float64[] q_torso

float64   time_cost # unit: ms
# ik result
twoArmHandPose  hand_poses

================================================================================
MSG: motion_capture_ik/twoArmHandPose
Header header
armHandPose  left_pose
armHandPose  right_pose
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: motion_capture_ik/armHandPose
float64[3] pos_xyz
float64[4] quat_xyzw

float64[3] elbow_pos_xyz

")

(setf (get motion_capture_ik::twoArmHandPoseCmdSrvResponse :md5sum-) "4cedfbf98f38ce7e92b358cb2d3ef39d")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrvResponse :datatype-) "motion_capture_ik/twoArmHandPoseCmdSrvResponse")
(setf (get motion_capture_ik::twoArmHandPoseCmdSrvResponse :definition-)
      "twoArmHandPoseCmd twoArmHandPoseCmdRequest

================================================================================
MSG: motion_capture_ik/twoArmHandPoseCmd
twoArmHandPose  hand_poses
# params for the IK solver
bool use_custom_ik_param
bool joint_angles_as_q0
ikSolveParam ik_param
================================================================================
MSG: motion_capture_ik/twoArmHandPose
Header header
armHandPose  left_pose
armHandPose  right_pose
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: motion_capture_ik/armHandPose
float64[3] pos_xyz
float64[4] quat_xyzw

float64[3] elbow_pos_xyz

float64[7] joint_angles
================================================================================
MSG: motion_capture_ik/ikSolveParam
# snopt params
float64 major_optimality_tol
float64 major_feasibility_tol
float64 minor_feasibility_tol
float64 major_iterations_limit
# constraint and cost params
float64 oritation_constraint_tol
float64 pos_constraint_tol # work when pos_cost_weight > 0.0
---
bool success
bool with_torso
float64[] q_arm
float64[] q_torso

float64   time_cost # unit: ms
# ik result
twoArmHandPose  hand_poses

================================================================================
MSG: motion_capture_ik/twoArmHandPose
Header header
armHandPose  left_pose
armHandPose  right_pose
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: motion_capture_ik/armHandPose
float64[3] pos_xyz
float64[4] quat_xyzw

float64[3] elbow_pos_xyz

")



(provide :motion_capture_ik/twoArmHandPoseCmdSrv "4cedfbf98f38ce7e92b358cb2d3ef39d")


