;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::twoArmHandPose)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'twoArmHandPose (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::TWOARMHANDPOSE")
  (make-package "MOTION_CAPTURE_IK::TWOARMHANDPOSE"))

(in-package "ROS")
;;//! \htmlinclude twoArmHandPose.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass motion_capture_ik::twoArmHandPose
  :super ros::object
  :slots (_header _left_pose _right_pose ))

(defmethod motion_capture_ik::twoArmHandPose
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:left_pose __left_pose) (instance motion_capture_ik::armHandPose :init))
    ((:right_pose __right_pose) (instance motion_capture_ik::armHandPose :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _left_pose __left_pose)
   (setq _right_pose __right_pose)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:left_pose
   (&rest __left_pose)
   (if (keywordp (car __left_pose))
       (send* _left_pose __left_pose)
     (progn
       (if __left_pose (setq _left_pose (car __left_pose)))
       _left_pose)))
  (:right_pose
   (&rest __right_pose)
   (if (keywordp (car __right_pose))
       (send* _right_pose __right_pose)
     (progn
       (if __right_pose (setq _right_pose (car __right_pose)))
       _right_pose)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; motion_capture_ik/armHandPose _left_pose
    (send _left_pose :serialization-length)
    ;; motion_capture_ik/armHandPose _right_pose
    (send _right_pose :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; motion_capture_ik/armHandPose _left_pose
       (send _left_pose :serialize s)
     ;; motion_capture_ik/armHandPose _right_pose
       (send _right_pose :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; motion_capture_ik/armHandPose _left_pose
     (send _left_pose :deserialize buf ptr-) (incf ptr- (send _left_pose :serialization-length))
   ;; motion_capture_ik/armHandPose _right_pose
     (send _right_pose :deserialize buf ptr-) (incf ptr- (send _right_pose :serialization-length))
   ;;
   self)
  )

(setf (get motion_capture_ik::twoArmHandPose :md5sum-) "5bdb1e027f430369b6f88e5e2f5d31ca")
(setf (get motion_capture_ik::twoArmHandPose :datatype-) "motion_capture_ik/twoArmHandPose")
(setf (get motion_capture_ik::twoArmHandPose :definition-)
      "Header header
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
")



(provide :motion_capture_ik/twoArmHandPose "5bdb1e027f430369b6f88e5e2f5d31ca")


