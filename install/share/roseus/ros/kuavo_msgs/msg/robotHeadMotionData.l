;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::robotHeadMotionData)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'robotHeadMotionData (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::ROBOTHEADMOTIONDATA")
  (make-package "KUAVO_MSGS::ROBOTHEADMOTIONDATA"))

(in-package "ROS")
;;//! \htmlinclude robotHeadMotionData.msg.html


(defclass kuavo_msgs::robotHeadMotionData
  :super ros::object
  :slots (_joint_data ))

(defmethod kuavo_msgs::robotHeadMotionData
  (:init
   (&key
    ((:joint_data __joint_data) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _joint_data __joint_data)
   self)
  (:joint_data
   (&optional __joint_data)
   (if __joint_data (setq _joint_data __joint_data)) _joint_data)
  (:serialization-length
   ()
   (+
    ;; float64[] _joint_data
    (* 8    (length _joint_data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _joint_data
     (write-long (length _joint_data) s)
     (dotimes (i (length _joint_data))
       (sys::poke (elt _joint_data i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _joint_data
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_data (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_data i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get kuavo_msgs::robotHeadMotionData :md5sum-) "400001e7cf73111efbced59084cb481a")
(setf (get kuavo_msgs::robotHeadMotionData :datatype-) "kuavo_msgs/robotHeadMotionData")
(setf (get kuavo_msgs::robotHeadMotionData :definition-)
      "# robotHeadMotionData.msg
# 
# - joint_data[0] : yaw,   [-30, 30]
# - joint_data[1] : pitch, [-25, 25]
#
# - [-8.000000, 0.000000]

float64[] joint_data

")



(provide :kuavo_msgs/robotHeadMotionData "400001e7cf73111efbced59084cb481a")


