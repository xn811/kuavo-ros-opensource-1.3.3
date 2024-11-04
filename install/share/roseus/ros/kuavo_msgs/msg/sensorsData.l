;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::sensorsData)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'sensorsData (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::SENSORSDATA")
  (make-package "KUAVO_MSGS::SENSORSDATA"))

(in-package "ROS")
;;//! \htmlinclude sensorsData.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass kuavo_msgs::sensorsData
  :super ros::object
  :slots (_header _sensor_time _joint_data _imu_data _end_effector_data ))

(defmethod kuavo_msgs::sensorsData
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:sensor_time __sensor_time) (instance ros::time :init))
    ((:joint_data __joint_data) (instance kuavo_msgs::jointData :init))
    ((:imu_data __imu_data) (instance kuavo_msgs::imuData :init))
    ((:end_effector_data __end_effector_data) (instance kuavo_msgs::endEffectorData :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _sensor_time __sensor_time)
   (setq _joint_data __joint_data)
   (setq _imu_data __imu_data)
   (setq _end_effector_data __end_effector_data)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:sensor_time
   (&optional __sensor_time)
   (if __sensor_time (setq _sensor_time __sensor_time)) _sensor_time)
  (:joint_data
   (&rest __joint_data)
   (if (keywordp (car __joint_data))
       (send* _joint_data __joint_data)
     (progn
       (if __joint_data (setq _joint_data (car __joint_data)))
       _joint_data)))
  (:imu_data
   (&rest __imu_data)
   (if (keywordp (car __imu_data))
       (send* _imu_data __imu_data)
     (progn
       (if __imu_data (setq _imu_data (car __imu_data)))
       _imu_data)))
  (:end_effector_data
   (&rest __end_effector_data)
   (if (keywordp (car __end_effector_data))
       (send* _end_effector_data __end_effector_data)
     (progn
       (if __end_effector_data (setq _end_effector_data (car __end_effector_data)))
       _end_effector_data)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; time _sensor_time
    8
    ;; kuavo_msgs/jointData _joint_data
    (send _joint_data :serialization-length)
    ;; kuavo_msgs/imuData _imu_data
    (send _imu_data :serialization-length)
    ;; kuavo_msgs/endEffectorData _end_effector_data
    (send _end_effector_data :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; time _sensor_time
       (write-long (send _sensor_time :sec) s) (write-long (send _sensor_time :nsec) s)
     ;; kuavo_msgs/jointData _joint_data
       (send _joint_data :serialize s)
     ;; kuavo_msgs/imuData _imu_data
       (send _imu_data :serialize s)
     ;; kuavo_msgs/endEffectorData _end_effector_data
       (send _end_effector_data :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; time _sensor_time
     (send _sensor_time :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _sensor_time :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; kuavo_msgs/jointData _joint_data
     (send _joint_data :deserialize buf ptr-) (incf ptr- (send _joint_data :serialization-length))
   ;; kuavo_msgs/imuData _imu_data
     (send _imu_data :deserialize buf ptr-) (incf ptr- (send _imu_data :serialization-length))
   ;; kuavo_msgs/endEffectorData _end_effector_data
     (send _end_effector_data :deserialize buf ptr-) (incf ptr- (send _end_effector_data :serialization-length))
   ;;
   self)
  )

(setf (get kuavo_msgs::sensorsData :md5sum-) "54439d3ac2ef33d46fd7cf6d324860c3")
(setf (get kuavo_msgs::sensorsData :datatype-) "kuavo_msgs/sensorsData")
(setf (get kuavo_msgs::sensorsData :definition-)
      "std_msgs/Header header
time sensor_time
kuavo_msgs/jointData joint_data
kuavo_msgs/imuData imu_data
kuavo_msgs/endEffectorData end_effector_data

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: kuavo_msgs/jointData
float64[] joint_q  
float64[] joint_v  
float64[] joint_vd    
float64[] joint_current  

================================================================================
MSG: kuavo_msgs/imuData
geometry_msgs/Vector3 gyro    #陀螺仪数据
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

================================================================================
MSG: kuavo_msgs/endEffectorData
string[] name  
float64[] position
float64[] velocity  
float64[] effort

")



(provide :kuavo_msgs/sensorsData "54439d3ac2ef33d46fd7cf6d324860c3")


