;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::imuData)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'imuData (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::IMUDATA")
  (make-package "KUAVO_MSGS::IMUDATA"))

(in-package "ROS")
;;//! \htmlinclude imuData.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass kuavo_msgs::imuData
  :super ros::object
  :slots (_gyro _acc _free_acc _quat ))

(defmethod kuavo_msgs::imuData
  (:init
   (&key
    ((:gyro __gyro) (instance geometry_msgs::Vector3 :init))
    ((:acc __acc) (instance geometry_msgs::Vector3 :init))
    ((:free_acc __free_acc) (instance geometry_msgs::Vector3 :init))
    ((:quat __quat) (instance geometry_msgs::Quaternion :init))
    )
   (send-super :init)
   (setq _gyro __gyro)
   (setq _acc __acc)
   (setq _free_acc __free_acc)
   (setq _quat __quat)
   self)
  (:gyro
   (&rest __gyro)
   (if (keywordp (car __gyro))
       (send* _gyro __gyro)
     (progn
       (if __gyro (setq _gyro (car __gyro)))
       _gyro)))
  (:acc
   (&rest __acc)
   (if (keywordp (car __acc))
       (send* _acc __acc)
     (progn
       (if __acc (setq _acc (car __acc)))
       _acc)))
  (:free_acc
   (&rest __free_acc)
   (if (keywordp (car __free_acc))
       (send* _free_acc __free_acc)
     (progn
       (if __free_acc (setq _free_acc (car __free_acc)))
       _free_acc)))
  (:quat
   (&rest __quat)
   (if (keywordp (car __quat))
       (send* _quat __quat)
     (progn
       (if __quat (setq _quat (car __quat)))
       _quat)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Vector3 _gyro
    (send _gyro :serialization-length)
    ;; geometry_msgs/Vector3 _acc
    (send _acc :serialization-length)
    ;; geometry_msgs/Vector3 _free_acc
    (send _free_acc :serialization-length)
    ;; geometry_msgs/Quaternion _quat
    (send _quat :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Vector3 _gyro
       (send _gyro :serialize s)
     ;; geometry_msgs/Vector3 _acc
       (send _acc :serialize s)
     ;; geometry_msgs/Vector3 _free_acc
       (send _free_acc :serialize s)
     ;; geometry_msgs/Quaternion _quat
       (send _quat :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Vector3 _gyro
     (send _gyro :deserialize buf ptr-) (incf ptr- (send _gyro :serialization-length))
   ;; geometry_msgs/Vector3 _acc
     (send _acc :deserialize buf ptr-) (incf ptr- (send _acc :serialization-length))
   ;; geometry_msgs/Vector3 _free_acc
     (send _free_acc :deserialize buf ptr-) (incf ptr- (send _free_acc :serialization-length))
   ;; geometry_msgs/Quaternion _quat
     (send _quat :deserialize buf ptr-) (incf ptr- (send _quat :serialization-length))
   ;;
   self)
  )

(setf (get kuavo_msgs::imuData :md5sum-) "6406067cf839b39a677ae809cd04646a")
(setf (get kuavo_msgs::imuData :datatype-) "kuavo_msgs/imuData")
(setf (get kuavo_msgs::imuData :definition-)
      "geometry_msgs/Vector3 gyro    #陀螺仪数据
geometry_msgs/Vector3 acc     #加速计数据
geometry_msgs/Vector3 free_acc    #无重力加速度数据
geometry_msgs/Quaternion quat    #四元数数据

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

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



(provide :kuavo_msgs/imuData "6406067cf839b39a677ae809cd04646a")


