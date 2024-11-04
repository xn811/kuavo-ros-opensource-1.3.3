;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::singleStepControl)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'singleStepControl (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::SINGLESTEPCONTROL")
  (make-package "KUAVO_MSGS::SINGLESTEPCONTROL"))
(unless (find-package "KUAVO_MSGS::SINGLESTEPCONTROLREQUEST")
  (make-package "KUAVO_MSGS::SINGLESTEPCONTROLREQUEST"))
(unless (find-package "KUAVO_MSGS::SINGLESTEPCONTROLRESPONSE")
  (make-package "KUAVO_MSGS::SINGLESTEPCONTROLRESPONSE"))

(in-package "ROS")





(defclass kuavo_msgs::singleStepControlRequest
  :super ros::object
  :slots (_foot_pose_target_trajectories ))

(defmethod kuavo_msgs::singleStepControlRequest
  (:init
   (&key
    ((:foot_pose_target_trajectories __foot_pose_target_trajectories) (instance kuavo_msgs::footPoseTargetTrajectories :init))
    )
   (send-super :init)
   (setq _foot_pose_target_trajectories __foot_pose_target_trajectories)
   self)
  (:foot_pose_target_trajectories
   (&rest __foot_pose_target_trajectories)
   (if (keywordp (car __foot_pose_target_trajectories))
       (send* _foot_pose_target_trajectories __foot_pose_target_trajectories)
     (progn
       (if __foot_pose_target_trajectories (setq _foot_pose_target_trajectories (car __foot_pose_target_trajectories)))
       _foot_pose_target_trajectories)))
  (:serialization-length
   ()
   (+
    ;; kuavo_msgs/footPoseTargetTrajectories _foot_pose_target_trajectories
    (send _foot_pose_target_trajectories :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; kuavo_msgs/footPoseTargetTrajectories _foot_pose_target_trajectories
       (send _foot_pose_target_trajectories :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; kuavo_msgs/footPoseTargetTrajectories _foot_pose_target_trajectories
     (send _foot_pose_target_trajectories :deserialize buf ptr-) (incf ptr- (send _foot_pose_target_trajectories :serialization-length))
   ;;
   self)
  )

(defclass kuavo_msgs::singleStepControlResponse
  :super ros::object
  :slots (_success _message ))

(defmethod kuavo_msgs::singleStepControlResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass kuavo_msgs::singleStepControl
  :super ros::object
  :slots ())

(setf (get kuavo_msgs::singleStepControl :md5sum-) "9a5a8ad57a17963a16bf197fc7a66fa4")
(setf (get kuavo_msgs::singleStepControl :datatype-) "kuavo_msgs/singleStepControl")
(setf (get kuavo_msgs::singleStepControl :request) kuavo_msgs::singleStepControlRequest)
(setf (get kuavo_msgs::singleStepControl :response) kuavo_msgs::singleStepControlResponse)

(defmethod kuavo_msgs::singleStepControlRequest
  (:response () (instance kuavo_msgs::singleStepControlResponse :init)))

(setf (get kuavo_msgs::singleStepControlRequest :md5sum-) "9a5a8ad57a17963a16bf197fc7a66fa4")
(setf (get kuavo_msgs::singleStepControlRequest :datatype-) "kuavo_msgs/singleStepControlRequest")
(setf (get kuavo_msgs::singleStepControlRequest :definition-)
      "footPoseTargetTrajectories foot_pose_target_trajectories

================================================================================
MSG: kuavo_msgs/footPoseTargetTrajectories
float64[]    timeTrajectory
int32[]      footIndexTrajectory
footPose[]   footPoseTrajectory
================================================================================
MSG: kuavo_msgs/footPose
float64[4] footPose # x, y, z, yaw
---
bool success
string message

")

(setf (get kuavo_msgs::singleStepControlResponse :md5sum-) "9a5a8ad57a17963a16bf197fc7a66fa4")
(setf (get kuavo_msgs::singleStepControlResponse :datatype-) "kuavo_msgs/singleStepControlResponse")
(setf (get kuavo_msgs::singleStepControlResponse :definition-)
      "footPoseTargetTrajectories foot_pose_target_trajectories

================================================================================
MSG: kuavo_msgs/footPoseTargetTrajectories
float64[]    timeTrajectory
int32[]      footIndexTrajectory
footPose[]   footPoseTrajectory
================================================================================
MSG: kuavo_msgs/footPose
float64[4] footPose # x, y, z, yaw
---
bool success
string message

")



(provide :kuavo_msgs/singleStepControl "9a5a8ad57a17963a16bf197fc7a66fa4")


