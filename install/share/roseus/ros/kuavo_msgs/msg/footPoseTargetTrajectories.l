;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::footPoseTargetTrajectories)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'footPoseTargetTrajectories (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::FOOTPOSETARGETTRAJECTORIES")
  (make-package "KUAVO_MSGS::FOOTPOSETARGETTRAJECTORIES"))

(in-package "ROS")
;;//! \htmlinclude footPoseTargetTrajectories.msg.html


(defclass kuavo_msgs::footPoseTargetTrajectories
  :super ros::object
  :slots (_timeTrajectory _footIndexTrajectory _footPoseTrajectory ))

(defmethod kuavo_msgs::footPoseTargetTrajectories
  (:init
   (&key
    ((:timeTrajectory __timeTrajectory) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:footIndexTrajectory __footIndexTrajectory) (make-array 0 :initial-element 0 :element-type :integer))
    ((:footPoseTrajectory __footPoseTrajectory) ())
    )
   (send-super :init)
   (setq _timeTrajectory __timeTrajectory)
   (setq _footIndexTrajectory __footIndexTrajectory)
   (setq _footPoseTrajectory __footPoseTrajectory)
   self)
  (:timeTrajectory
   (&optional __timeTrajectory)
   (if __timeTrajectory (setq _timeTrajectory __timeTrajectory)) _timeTrajectory)
  (:footIndexTrajectory
   (&optional __footIndexTrajectory)
   (if __footIndexTrajectory (setq _footIndexTrajectory __footIndexTrajectory)) _footIndexTrajectory)
  (:footPoseTrajectory
   (&rest __footPoseTrajectory)
   (if (keywordp (car __footPoseTrajectory))
       (send* _footPoseTrajectory __footPoseTrajectory)
     (progn
       (if __footPoseTrajectory (setq _footPoseTrajectory (car __footPoseTrajectory)))
       _footPoseTrajectory)))
  (:serialization-length
   ()
   (+
    ;; float64[] _timeTrajectory
    (* 8    (length _timeTrajectory)) 4
    ;; int32[] _footIndexTrajectory
    (* 4    (length _footIndexTrajectory)) 4
    ;; kuavo_msgs/footPose[] _footPoseTrajectory
    (apply #'+ (send-all _footPoseTrajectory :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _timeTrajectory
     (write-long (length _timeTrajectory) s)
     (dotimes (i (length _timeTrajectory))
       (sys::poke (elt _timeTrajectory i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; int32[] _footIndexTrajectory
     (write-long (length _footIndexTrajectory) s)
     (dotimes (i (length _footIndexTrajectory))
       (write-long (elt _footIndexTrajectory i) s)
       )
     ;; kuavo_msgs/footPose[] _footPoseTrajectory
     (write-long (length _footPoseTrajectory) s)
     (dolist (elem _footPoseTrajectory)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _timeTrajectory
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _timeTrajectory (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _timeTrajectory i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; int32[] _footIndexTrajectory
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _footIndexTrajectory (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _footIndexTrajectory i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;; kuavo_msgs/footPose[] _footPoseTrajectory
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _footPoseTrajectory (let (r) (dotimes (i n) (push (instance kuavo_msgs::footPose :init) r)) r))
     (dolist (elem- _footPoseTrajectory)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get kuavo_msgs::footPoseTargetTrajectories :md5sum-) "6854923406c37831b40979cd2570e027")
(setf (get kuavo_msgs::footPoseTargetTrajectories :datatype-) "kuavo_msgs/footPoseTargetTrajectories")
(setf (get kuavo_msgs::footPoseTargetTrajectories :definition-)
      "float64[]    timeTrajectory
int32[]      footIndexTrajectory
footPose[]   footPoseTrajectory
================================================================================
MSG: kuavo_msgs/footPose
float64[4] footPose # x, y, z, yaw
float64[4] torsoPose # x, y, z, yaw
")



(provide :kuavo_msgs/footPoseTargetTrajectories "6854923406c37831b40979cd2570e027")


