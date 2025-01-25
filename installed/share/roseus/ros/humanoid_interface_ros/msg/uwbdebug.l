;; Auto-generated. Do not edit!


(when (boundp 'humanoid_interface_ros::uwbdebug)
  (if (not (find-package "HUMANOID_INTERFACE_ROS"))
    (make-package "HUMANOID_INTERFACE_ROS"))
  (shadow 'uwbdebug (find-package "HUMANOID_INTERFACE_ROS")))
(unless (find-package "HUMANOID_INTERFACE_ROS::UWBDEBUG")
  (make-package "HUMANOID_INTERFACE_ROS::UWBDEBUG"))

(in-package "ROS")
;;//! \htmlinclude uwbdebug.msg.html


(defclass humanoid_interface_ros::uwbdebug
  :super ros::object
  :slots (_robot_uwb_cur_x _robot_uwb_cur_y _robot_uwb_cur_angle _robot_uwb_fir_angle _robot_uwb_fir_x _robot_uwb_fir_y _robot_uwb_avr_x _robot_uwb_avr_y ))

(defmethod humanoid_interface_ros::uwbdebug
  (:init
   (&key
    ((:robot_uwb_cur_x __robot_uwb_cur_x) 0.0)
    ((:robot_uwb_cur_y __robot_uwb_cur_y) 0.0)
    ((:robot_uwb_cur_angle __robot_uwb_cur_angle) 0.0)
    ((:robot_uwb_fir_angle __robot_uwb_fir_angle) 0.0)
    ((:robot_uwb_fir_x __robot_uwb_fir_x) 0.0)
    ((:robot_uwb_fir_y __robot_uwb_fir_y) 0.0)
    ((:robot_uwb_avr_x __robot_uwb_avr_x) 0.0)
    ((:robot_uwb_avr_y __robot_uwb_avr_y) 0.0)
    )
   (send-super :init)
   (setq _robot_uwb_cur_x (float __robot_uwb_cur_x))
   (setq _robot_uwb_cur_y (float __robot_uwb_cur_y))
   (setq _robot_uwb_cur_angle (float __robot_uwb_cur_angle))
   (setq _robot_uwb_fir_angle (float __robot_uwb_fir_angle))
   (setq _robot_uwb_fir_x (float __robot_uwb_fir_x))
   (setq _robot_uwb_fir_y (float __robot_uwb_fir_y))
   (setq _robot_uwb_avr_x (float __robot_uwb_avr_x))
   (setq _robot_uwb_avr_y (float __robot_uwb_avr_y))
   self)
  (:robot_uwb_cur_x
   (&optional __robot_uwb_cur_x)
   (if __robot_uwb_cur_x (setq _robot_uwb_cur_x __robot_uwb_cur_x)) _robot_uwb_cur_x)
  (:robot_uwb_cur_y
   (&optional __robot_uwb_cur_y)
   (if __robot_uwb_cur_y (setq _robot_uwb_cur_y __robot_uwb_cur_y)) _robot_uwb_cur_y)
  (:robot_uwb_cur_angle
   (&optional __robot_uwb_cur_angle)
   (if __robot_uwb_cur_angle (setq _robot_uwb_cur_angle __robot_uwb_cur_angle)) _robot_uwb_cur_angle)
  (:robot_uwb_fir_angle
   (&optional __robot_uwb_fir_angle)
   (if __robot_uwb_fir_angle (setq _robot_uwb_fir_angle __robot_uwb_fir_angle)) _robot_uwb_fir_angle)
  (:robot_uwb_fir_x
   (&optional __robot_uwb_fir_x)
   (if __robot_uwb_fir_x (setq _robot_uwb_fir_x __robot_uwb_fir_x)) _robot_uwb_fir_x)
  (:robot_uwb_fir_y
   (&optional __robot_uwb_fir_y)
   (if __robot_uwb_fir_y (setq _robot_uwb_fir_y __robot_uwb_fir_y)) _robot_uwb_fir_y)
  (:robot_uwb_avr_x
   (&optional __robot_uwb_avr_x)
   (if __robot_uwb_avr_x (setq _robot_uwb_avr_x __robot_uwb_avr_x)) _robot_uwb_avr_x)
  (:robot_uwb_avr_y
   (&optional __robot_uwb_avr_y)
   (if __robot_uwb_avr_y (setq _robot_uwb_avr_y __robot_uwb_avr_y)) _robot_uwb_avr_y)
  (:serialization-length
   ()
   (+
    ;; float32 _robot_uwb_cur_x
    4
    ;; float32 _robot_uwb_cur_y
    4
    ;; float32 _robot_uwb_cur_angle
    4
    ;; float32 _robot_uwb_fir_angle
    4
    ;; float32 _robot_uwb_fir_x
    4
    ;; float32 _robot_uwb_fir_y
    4
    ;; float32 _robot_uwb_avr_x
    4
    ;; float32 _robot_uwb_avr_y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _robot_uwb_cur_x
       (sys::poke _robot_uwb_cur_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_cur_y
       (sys::poke _robot_uwb_cur_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_cur_angle
       (sys::poke _robot_uwb_cur_angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_fir_angle
       (sys::poke _robot_uwb_fir_angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_fir_x
       (sys::poke _robot_uwb_fir_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_fir_y
       (sys::poke _robot_uwb_fir_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_avr_x
       (sys::poke _robot_uwb_avr_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _robot_uwb_avr_y
       (sys::poke _robot_uwb_avr_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _robot_uwb_cur_x
     (setq _robot_uwb_cur_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_cur_y
     (setq _robot_uwb_cur_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_cur_angle
     (setq _robot_uwb_cur_angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_fir_angle
     (setq _robot_uwb_fir_angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_fir_x
     (setq _robot_uwb_fir_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_fir_y
     (setq _robot_uwb_fir_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_avr_x
     (setq _robot_uwb_avr_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _robot_uwb_avr_y
     (setq _robot_uwb_avr_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get humanoid_interface_ros::uwbdebug :md5sum-) "a496166c5de3c06085e7947afcc759bc")
(setf (get humanoid_interface_ros::uwbdebug :datatype-) "humanoid_interface_ros/uwbdebug")
(setf (get humanoid_interface_ros::uwbdebug :definition-)
      "# 机器人uwb x,y 轴滤波后的效果
float32 robot_uwb_cur_x
float32 robot_uwb_cur_y
float32 robot_uwb_cur_angle
float32 robot_uwb_fir_angle
float32 robot_uwb_fir_x
float32 robot_uwb_fir_y
float32 robot_uwb_avr_x
float32 robot_uwb_avr_y
")



(provide :humanoid_interface_ros/uwbdebug "a496166c5de3c06085e7947afcc759bc")


