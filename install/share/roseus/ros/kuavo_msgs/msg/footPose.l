;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::footPose)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'footPose (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::FOOTPOSE")
  (make-package "KUAVO_MSGS::FOOTPOSE"))

(in-package "ROS")
;;//! \htmlinclude footPose.msg.html


(defclass kuavo_msgs::footPose
  :super ros::object
  :slots (_footPose _torsoPose ))

(defmethod kuavo_msgs::footPose
  (:init
   (&key
    ((:footPose __footPose) (make-array 4 :initial-element 0.0 :element-type :float))
    ((:torsoPose __torsoPose) (make-array 4 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _footPose __footPose)
   (setq _torsoPose __torsoPose)
   self)
  (:footPose
   (&optional __footPose)
   (if __footPose (setq _footPose __footPose)) _footPose)
  (:torsoPose
   (&optional __torsoPose)
   (if __torsoPose (setq _torsoPose __torsoPose)) _torsoPose)
  (:serialization-length
   ()
   (+
    ;; float64[4] _footPose
    (* 8    4)
    ;; float64[4] _torsoPose
    (* 8    4)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[4] _footPose
     (dotimes (i 4)
       (sys::poke (elt _footPose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[4] _torsoPose
     (dotimes (i 4)
       (sys::poke (elt _torsoPose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[4] _footPose
   (dotimes (i (length _footPose))
     (setf (elt _footPose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[4] _torsoPose
   (dotimes (i (length _torsoPose))
     (setf (elt _torsoPose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;;
   self)
  )

(setf (get kuavo_msgs::footPose :md5sum-) "b0acb7ad1ed1ee5a0a630b91b650f49a")
(setf (get kuavo_msgs::footPose :datatype-) "kuavo_msgs/footPose")
(setf (get kuavo_msgs::footPose :definition-)
      "float64[4] footPose # x, y, z, yaw
float64[4] torsoPose # x, y, z, yaw
")



(provide :kuavo_msgs/footPose "b0acb7ad1ed1ee5a0a630b91b650f49a")


