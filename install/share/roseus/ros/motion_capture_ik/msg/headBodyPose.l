;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::headBodyPose)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'headBodyPose (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::HEADBODYPOSE")
  (make-package "MOTION_CAPTURE_IK::HEADBODYPOSE"))

(in-package "ROS")
;;//! \htmlinclude headBodyPose.msg.html


(defclass motion_capture_ik::headBodyPose
  :super ros::object
  :slots (_head_pitch _head_yaw _body_roll _body_pitch _body_yaw _body_x _body_y _body_height ))

(defmethod motion_capture_ik::headBodyPose
  (:init
   (&key
    ((:head_pitch __head_pitch) 0.0)
    ((:head_yaw __head_yaw) 0.0)
    ((:body_roll __body_roll) 0.0)
    ((:body_pitch __body_pitch) 0.0)
    ((:body_yaw __body_yaw) 0.0)
    ((:body_x __body_x) 0.0)
    ((:body_y __body_y) 0.0)
    ((:body_height __body_height) 0.0)
    )
   (send-super :init)
   (setq _head_pitch (float __head_pitch))
   (setq _head_yaw (float __head_yaw))
   (setq _body_roll (float __body_roll))
   (setq _body_pitch (float __body_pitch))
   (setq _body_yaw (float __body_yaw))
   (setq _body_x (float __body_x))
   (setq _body_y (float __body_y))
   (setq _body_height (float __body_height))
   self)
  (:head_pitch
   (&optional __head_pitch)
   (if __head_pitch (setq _head_pitch __head_pitch)) _head_pitch)
  (:head_yaw
   (&optional __head_yaw)
   (if __head_yaw (setq _head_yaw __head_yaw)) _head_yaw)
  (:body_roll
   (&optional __body_roll)
   (if __body_roll (setq _body_roll __body_roll)) _body_roll)
  (:body_pitch
   (&optional __body_pitch)
   (if __body_pitch (setq _body_pitch __body_pitch)) _body_pitch)
  (:body_yaw
   (&optional __body_yaw)
   (if __body_yaw (setq _body_yaw __body_yaw)) _body_yaw)
  (:body_x
   (&optional __body_x)
   (if __body_x (setq _body_x __body_x)) _body_x)
  (:body_y
   (&optional __body_y)
   (if __body_y (setq _body_y __body_y)) _body_y)
  (:body_height
   (&optional __body_height)
   (if __body_height (setq _body_height __body_height)) _body_height)
  (:serialization-length
   ()
   (+
    ;; float64 _head_pitch
    8
    ;; float64 _head_yaw
    8
    ;; float64 _body_roll
    8
    ;; float64 _body_pitch
    8
    ;; float64 _body_yaw
    8
    ;; float64 _body_x
    8
    ;; float64 _body_y
    8
    ;; float64 _body_height
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _head_pitch
       (sys::poke _head_pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _head_yaw
       (sys::poke _head_yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_roll
       (sys::poke _body_roll (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_pitch
       (sys::poke _body_pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_yaw
       (sys::poke _body_yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_x
       (sys::poke _body_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_y
       (sys::poke _body_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _body_height
       (sys::poke _body_height (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _head_pitch
     (setq _head_pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _head_yaw
     (setq _head_yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_roll
     (setq _body_roll (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_pitch
     (setq _body_pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_yaw
     (setq _body_yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_x
     (setq _body_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_y
     (setq _body_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _body_height
     (setq _body_height (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get motion_capture_ik::headBodyPose :md5sum-) "86a58d9f885335d8a0b389ace07ba692")
(setf (get motion_capture_ik::headBodyPose :datatype-) "motion_capture_ik/headBodyPose")
(setf (get motion_capture_ik::headBodyPose :definition-)
      "# head (rad)
float64 head_pitch
float64 head_yaw
# body (rad)
float64 body_roll
float64 body_pitch
float64 body_yaw

float64 body_x
float64 body_y
float64 body_height
")



(provide :motion_capture_ik/headBodyPose "86a58d9f885335d8a0b389ace07ba692")


