;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::gaitTimeName)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'gaitTimeName (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::GAITTIMENAME")
  (make-package "KUAVO_MSGS::GAITTIMENAME"))

(in-package "ROS")
;;//! \htmlinclude gaitTimeName.msg.html


(defclass kuavo_msgs::gaitTimeName
  :super ros::object
  :slots (_start_time _gait_name ))

(defmethod kuavo_msgs::gaitTimeName
  (:init
   (&key
    ((:start_time __start_time) 0.0)
    ((:gait_name __gait_name) "")
    )
   (send-super :init)
   (setq _start_time (float __start_time))
   (setq _gait_name (string __gait_name))
   self)
  (:start_time
   (&optional __start_time)
   (if __start_time (setq _start_time __start_time)) _start_time)
  (:gait_name
   (&optional __gait_name)
   (if __gait_name (setq _gait_name __gait_name)) _gait_name)
  (:serialization-length
   ()
   (+
    ;; float32 _start_time
    4
    ;; string _gait_name
    4 (length _gait_name)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _start_time
       (sys::poke _start_time (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; string _gait_name
       (write-long (length _gait_name) s) (princ _gait_name s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _start_time
     (setq _start_time (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; string _gait_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _gait_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get kuavo_msgs::gaitTimeName :md5sum-) "c694c8dbb2e8c9d73614407bfe314692")
(setf (get kuavo_msgs::gaitTimeName :datatype-) "kuavo_msgs/gaitTimeName")
(setf (get kuavo_msgs::gaitTimeName :definition-)
      "float32 start_time
string  gait_name

")



(provide :kuavo_msgs/gaitTimeName "c694c8dbb2e8c9d73614407bfe314692")


