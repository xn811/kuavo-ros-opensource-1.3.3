;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::srvArmIK)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'srvArmIK (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::SRVARMIK")
  (make-package "HANDCONTROLLERDEMOROSNODE::SRVARMIK"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::SRVARMIKREQUEST")
  (make-package "HANDCONTROLLERDEMOROSNODE::SRVARMIKREQUEST"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::SRVARMIKRESPONSE")
  (make-package "HANDCONTROLLERDEMOROSNODE::SRVARMIKRESPONSE"))

(in-package "ROS")



(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))


(defclass handcontrollerdemorosnode::srvArmIKRequest
  :super ros::object
  :slots (_left_arm_pose _right_arm_pose ))

(defmethod handcontrollerdemorosnode::srvArmIKRequest
  (:init
   (&key
    ((:left_arm_pose __left_arm_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:right_arm_pose __right_arm_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _left_arm_pose __left_arm_pose)
   (setq _right_arm_pose __right_arm_pose)
   self)
  (:left_arm_pose
   (&optional __left_arm_pose)
   (if __left_arm_pose (setq _left_arm_pose __left_arm_pose)) _left_arm_pose)
  (:right_arm_pose
   (&optional __right_arm_pose)
   (if __right_arm_pose (setq _right_arm_pose __right_arm_pose)) _right_arm_pose)
  (:serialization-length
   ()
   (+
    ;; float64[] _left_arm_pose
    (* 8    (length _left_arm_pose)) 4
    ;; float64[] _right_arm_pose
    (* 8    (length _right_arm_pose)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _left_arm_pose
     (write-long (length _left_arm_pose) s)
     (dotimes (i (length _left_arm_pose))
       (sys::poke (elt _left_arm_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _right_arm_pose
     (write-long (length _right_arm_pose) s)
     (dotimes (i (length _right_arm_pose))
       (sys::poke (elt _right_arm_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _left_arm_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _left_arm_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _left_arm_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _right_arm_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _right_arm_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _right_arm_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(defclass handcontrollerdemorosnode::srvArmIKResponse
  :super ros::object
  :slots (_joint_state ))

(defmethod handcontrollerdemorosnode::srvArmIKResponse
  (:init
   (&key
    ((:joint_state __joint_state) (instance sensor_msgs::JointState :init))
    )
   (send-super :init)
   (setq _joint_state __joint_state)
   self)
  (:joint_state
   (&rest __joint_state)
   (if (keywordp (car __joint_state))
       (send* _joint_state __joint_state)
     (progn
       (if __joint_state (setq _joint_state (car __joint_state)))
       _joint_state)))
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/JointState _joint_state
    (send _joint_state :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/JointState _joint_state
       (send _joint_state :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/JointState _joint_state
     (send _joint_state :deserialize buf ptr-) (incf ptr- (send _joint_state :serialization-length))
   ;;
   self)
  )

(defclass handcontrollerdemorosnode::srvArmIK
  :super ros::object
  :slots ())

(setf (get handcontrollerdemorosnode::srvArmIK :md5sum-) "2b5b0516bd664187d5eefa858c0bc7ee")
(setf (get handcontrollerdemorosnode::srvArmIK :datatype-) "handcontrollerdemorosnode/srvArmIK")
(setf (get handcontrollerdemorosnode::srvArmIK :request) handcontrollerdemorosnode::srvArmIKRequest)
(setf (get handcontrollerdemorosnode::srvArmIK :response) handcontrollerdemorosnode::srvArmIKResponse)

(defmethod handcontrollerdemorosnode::srvArmIKRequest
  (:response () (instance handcontrollerdemorosnode::srvArmIKResponse :init)))

(setf (get handcontrollerdemorosnode::srvArmIKRequest :md5sum-) "2b5b0516bd664187d5eefa858c0bc7ee")
(setf (get handcontrollerdemorosnode::srvArmIKRequest :datatype-) "handcontrollerdemorosnode/srvArmIKRequest")
(setf (get handcontrollerdemorosnode::srvArmIKRequest :definition-)
      "float64[] left_arm_pose
float64[] right_arm_pose
---
sensor_msgs/JointState joint_state


================================================================================
MSG: sensor_msgs/JointState
# This is a message that holds data to describe the state of a set of torque controlled joints. 
#
# The state of each joint (revolute or prismatic) is defined by:
#  * the position of the joint (rad or m),
#  * the velocity of the joint (rad/s or m/s) and 
#  * the effort that is applied in the joint (Nm or N).
#
# Each joint is uniquely identified by its name
# The header specifies the time at which the joint states were recorded. All the joint states
# in one message have to be recorded at the same time.
#
# This message consists of a multiple arrays, one for each part of the joint state. 
# The goal is to make each of the fields optional. When e.g. your joints have no
# effort associated with them, you can leave the effort array empty. 
#
# All arrays in this message should have the same size, or be empty.
# This is the only way to uniquely associate the joint name with the correct
# states.


Header header

string[] name
float64[] position
float64[] velocity
float64[] effort

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
")

(setf (get handcontrollerdemorosnode::srvArmIKResponse :md5sum-) "2b5b0516bd664187d5eefa858c0bc7ee")
(setf (get handcontrollerdemorosnode::srvArmIKResponse :datatype-) "handcontrollerdemorosnode/srvArmIKResponse")
(setf (get handcontrollerdemorosnode::srvArmIKResponse :definition-)
      "float64[] left_arm_pose
float64[] right_arm_pose
---
sensor_msgs/JointState joint_state


================================================================================
MSG: sensor_msgs/JointState
# This is a message that holds data to describe the state of a set of torque controlled joints. 
#
# The state of each joint (revolute or prismatic) is defined by:
#  * the position of the joint (rad or m),
#  * the velocity of the joint (rad/s or m/s) and 
#  * the effort that is applied in the joint (Nm or N).
#
# Each joint is uniquely identified by its name
# The header specifies the time at which the joint states were recorded. All the joint states
# in one message have to be recorded at the same time.
#
# This message consists of a multiple arrays, one for each part of the joint state. 
# The goal is to make each of the fields optional. When e.g. your joints have no
# effort associated with them, you can leave the effort array empty. 
#
# All arrays in this message should have the same size, or be empty.
# This is the only way to uniquely associate the joint name with the correct
# states.


Header header

string[] name
float64[] position
float64[] velocity
float64[] effort

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
")



(provide :handcontrollerdemorosnode/srvArmIK "2b5b0516bd664187d5eefa858c0bc7ee")


