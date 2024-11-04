;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::twoArmHandPoseCmd)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'twoArmHandPoseCmd (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMD")
  (make-package "MOTION_CAPTURE_IK::TWOARMHANDPOSECMD"))

(in-package "ROS")
;;//! \htmlinclude twoArmHandPoseCmd.msg.html


(defclass motion_capture_ik::twoArmHandPoseCmd
  :super ros::object
  :slots (_hand_poses _use_custom_ik_param _joint_angles_as_q0 _ik_param ))

(defmethod motion_capture_ik::twoArmHandPoseCmd
  (:init
   (&key
    ((:hand_poses __hand_poses) (instance motion_capture_ik::twoArmHandPose :init))
    ((:use_custom_ik_param __use_custom_ik_param) nil)
    ((:joint_angles_as_q0 __joint_angles_as_q0) nil)
    ((:ik_param __ik_param) (instance motion_capture_ik::ikSolveParam :init))
    )
   (send-super :init)
   (setq _hand_poses __hand_poses)
   (setq _use_custom_ik_param __use_custom_ik_param)
   (setq _joint_angles_as_q0 __joint_angles_as_q0)
   (setq _ik_param __ik_param)
   self)
  (:hand_poses
   (&rest __hand_poses)
   (if (keywordp (car __hand_poses))
       (send* _hand_poses __hand_poses)
     (progn
       (if __hand_poses (setq _hand_poses (car __hand_poses)))
       _hand_poses)))
  (:use_custom_ik_param
   (&optional (__use_custom_ik_param :null))
   (if (not (eq __use_custom_ik_param :null)) (setq _use_custom_ik_param __use_custom_ik_param)) _use_custom_ik_param)
  (:joint_angles_as_q0
   (&optional (__joint_angles_as_q0 :null))
   (if (not (eq __joint_angles_as_q0 :null)) (setq _joint_angles_as_q0 __joint_angles_as_q0)) _joint_angles_as_q0)
  (:ik_param
   (&rest __ik_param)
   (if (keywordp (car __ik_param))
       (send* _ik_param __ik_param)
     (progn
       (if __ik_param (setq _ik_param (car __ik_param)))
       _ik_param)))
  (:serialization-length
   ()
   (+
    ;; motion_capture_ik/twoArmHandPose _hand_poses
    (send _hand_poses :serialization-length)
    ;; bool _use_custom_ik_param
    1
    ;; bool _joint_angles_as_q0
    1
    ;; motion_capture_ik/ikSolveParam _ik_param
    (send _ik_param :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; motion_capture_ik/twoArmHandPose _hand_poses
       (send _hand_poses :serialize s)
     ;; bool _use_custom_ik_param
       (if _use_custom_ik_param (write-byte -1 s) (write-byte 0 s))
     ;; bool _joint_angles_as_q0
       (if _joint_angles_as_q0 (write-byte -1 s) (write-byte 0 s))
     ;; motion_capture_ik/ikSolveParam _ik_param
       (send _ik_param :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; motion_capture_ik/twoArmHandPose _hand_poses
     (send _hand_poses :deserialize buf ptr-) (incf ptr- (send _hand_poses :serialization-length))
   ;; bool _use_custom_ik_param
     (setq _use_custom_ik_param (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _joint_angles_as_q0
     (setq _joint_angles_as_q0 (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; motion_capture_ik/ikSolveParam _ik_param
     (send _ik_param :deserialize buf ptr-) (incf ptr- (send _ik_param :serialization-length))
   ;;
   self)
  )

(setf (get motion_capture_ik::twoArmHandPoseCmd :md5sum-) "d4b6792a6f960bea428fd7158220110b")
(setf (get motion_capture_ik::twoArmHandPoseCmd :datatype-) "motion_capture_ik/twoArmHandPoseCmd")
(setf (get motion_capture_ik::twoArmHandPoseCmd :definition-)
      "twoArmHandPose  hand_poses
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
float64 pos_cost_weight
")



(provide :motion_capture_ik/twoArmHandPoseCmd "d4b6792a6f960bea428fd7158220110b")


