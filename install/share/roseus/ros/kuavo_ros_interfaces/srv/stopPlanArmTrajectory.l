;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::stopPlanArmTrajectory)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'stopPlanArmTrajectory (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORY")
  (make-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORY"))
(unless (find-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORYREQUEST")
  (make-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORYREQUEST"))
(unless (find-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORYRESPONSE")
  (make-package "KUAVO_ROS_INTERFACES::STOPPLANARMTRAJECTORYRESPONSE"))

(in-package "ROS")





(defclass kuavo_ros_interfaces::stopPlanArmTrajectoryRequest
  :super ros::object
  :slots ())

(defmethod kuavo_ros_interfaces::stopPlanArmTrajectoryRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass kuavo_ros_interfaces::stopPlanArmTrajectoryResponse
  :super ros::object
  :slots (_result ))

(defmethod kuavo_ros_interfaces::stopPlanArmTrajectoryResponse
  (:init
   (&key
    ((:result __result) nil)
    )
   (send-super :init)
   (setq _result __result)
   self)
  (:result
   (&optional (__result :null))
   (if (not (eq __result :null)) (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; bool _result
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _result
       (if _result (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _result
     (setq _result (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass kuavo_ros_interfaces::stopPlanArmTrajectory
  :super ros::object
  :slots ())

(setf (get kuavo_ros_interfaces::stopPlanArmTrajectory :md5sum-) "eb13ac1f1354ccecb7941ee8fa2192e8")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectory :datatype-) "kuavo_ros_interfaces/stopPlanArmTrajectory")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectory :request) kuavo_ros_interfaces::stopPlanArmTrajectoryRequest)
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectory :response) kuavo_ros_interfaces::stopPlanArmTrajectoryResponse)

(defmethod kuavo_ros_interfaces::stopPlanArmTrajectoryRequest
  (:response () (instance kuavo_ros_interfaces::stopPlanArmTrajectoryResponse :init)))

(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryRequest :md5sum-) "eb13ac1f1354ccecb7941ee8fa2192e8")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryRequest :datatype-) "kuavo_ros_interfaces/stopPlanArmTrajectoryRequest")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryRequest :definition-)
      "---
bool result
")

(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryResponse :md5sum-) "eb13ac1f1354ccecb7941ee8fa2192e8")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryResponse :datatype-) "kuavo_ros_interfaces/stopPlanArmTrajectoryResponse")
(setf (get kuavo_ros_interfaces::stopPlanArmTrajectoryResponse :definition-)
      "---
bool result
")



(provide :kuavo_ros_interfaces/stopPlanArmTrajectory "eb13ac1f1354ccecb7941ee8fa2192e8")


