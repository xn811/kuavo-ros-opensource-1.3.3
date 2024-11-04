;; Auto-generated. Do not edit!


(when (boundp 'noitom_hi5_hand_udp_python::PoseInfo)
  (if (not (find-package "NOITOM_HI5_HAND_UDP_PYTHON"))
    (make-package "NOITOM_HI5_HAND_UDP_PYTHON"))
  (shadow 'PoseInfo (find-package "NOITOM_HI5_HAND_UDP_PYTHON")))
(unless (find-package "NOITOM_HI5_HAND_UDP_PYTHON::POSEINFO")
  (make-package "NOITOM_HI5_HAND_UDP_PYTHON::POSEINFO"))

(in-package "ROS")
;;//! \htmlinclude PoseInfo.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass noitom_hi5_hand_udp_python::PoseInfo
  :super ros::object
  :slots (_position _orientation ))

(defmethod noitom_hi5_hand_udp_python::PoseInfo
  (:init
   (&key
    ((:position __position) (instance geometry_msgs::Point :init))
    ((:orientation __orientation) (instance geometry_msgs::Quaternion :init))
    )
   (send-super :init)
   (setq _position __position)
   (setq _orientation __orientation)
   self)
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Point _position
    (send _position :serialization-length)
    ;; geometry_msgs/Quaternion _orientation
    (send _orientation :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Point _position
       (send _position :serialize s)
     ;; geometry_msgs/Quaternion _orientation
       (send _orientation :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Point _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; geometry_msgs/Quaternion _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;;
   self)
  )

(setf (get noitom_hi5_hand_udp_python::PoseInfo :md5sum-) "e45d45a5a1ce597b249e23fb30fc871f")
(setf (get noitom_hi5_hand_udp_python::PoseInfo :datatype-) "noitom_hi5_hand_udp_python/PoseInfo")
(setf (get noitom_hi5_hand_udp_python::PoseInfo :definition-)
      "geometry_msgs/Point position
geometry_msgs/Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :noitom_hi5_hand_udp_python/PoseInfo "e45d45a5a1ce597b249e23fb30fc871f")


