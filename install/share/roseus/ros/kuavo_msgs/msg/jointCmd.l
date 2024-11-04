;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::jointCmd)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'jointCmd (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::JOINTCMD")
  (make-package "KUAVO_MSGS::JOINTCMD"))

(in-package "ROS")
;;//! \htmlinclude jointCmd.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass kuavo_msgs::jointCmd
  :super ros::object
  :slots (_header _joint_q _joint_v _tau _tau_max _tau_ratio _joint_kp _joint_kd _control_modes ))

(defmethod kuavo_msgs::jointCmd
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:joint_q __joint_q) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_v __joint_v) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:tau __tau) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:tau_max __tau_max) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:tau_ratio __tau_ratio) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_kp __joint_kp) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_kd __joint_kd) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:control_modes __control_modes) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _header __header)
   (setq _joint_q __joint_q)
   (setq _joint_v __joint_v)
   (setq _tau __tau)
   (setq _tau_max __tau_max)
   (setq _tau_ratio __tau_ratio)
   (setq _joint_kp __joint_kp)
   (setq _joint_kd __joint_kd)
   (setq _control_modes __control_modes)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:joint_q
   (&optional __joint_q)
   (if __joint_q (setq _joint_q __joint_q)) _joint_q)
  (:joint_v
   (&optional __joint_v)
   (if __joint_v (setq _joint_v __joint_v)) _joint_v)
  (:tau
   (&optional __tau)
   (if __tau (setq _tau __tau)) _tau)
  (:tau_max
   (&optional __tau_max)
   (if __tau_max (setq _tau_max __tau_max)) _tau_max)
  (:tau_ratio
   (&optional __tau_ratio)
   (if __tau_ratio (setq _tau_ratio __tau_ratio)) _tau_ratio)
  (:joint_kp
   (&optional __joint_kp)
   (if __joint_kp (setq _joint_kp __joint_kp)) _joint_kp)
  (:joint_kd
   (&optional __joint_kd)
   (if __joint_kd (setq _joint_kd __joint_kd)) _joint_kd)
  (:control_modes
   (&optional __control_modes)
   (if __control_modes (setq _control_modes __control_modes)) _control_modes)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64[] _joint_q
    (* 8    (length _joint_q)) 4
    ;; float64[] _joint_v
    (* 8    (length _joint_v)) 4
    ;; float64[] _tau
    (* 8    (length _tau)) 4
    ;; float64[] _tau_max
    (* 8    (length _tau_max)) 4
    ;; float64[] _tau_ratio
    (* 8    (length _tau_ratio)) 4
    ;; float64[] _joint_kp
    (* 8    (length _joint_kp)) 4
    ;; float64[] _joint_kd
    (* 8    (length _joint_kd)) 4
    ;; int32[] _control_modes
    (* 4    (length _control_modes)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64[] _joint_q
     (write-long (length _joint_q) s)
     (dotimes (i (length _joint_q))
       (sys::poke (elt _joint_q i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_v
     (write-long (length _joint_v) s)
     (dotimes (i (length _joint_v))
       (sys::poke (elt _joint_v i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _tau
     (write-long (length _tau) s)
     (dotimes (i (length _tau))
       (sys::poke (elt _tau i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _tau_max
     (write-long (length _tau_max) s)
     (dotimes (i (length _tau_max))
       (sys::poke (elt _tau_max i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _tau_ratio
     (write-long (length _tau_ratio) s)
     (dotimes (i (length _tau_ratio))
       (sys::poke (elt _tau_ratio i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_kp
     (write-long (length _joint_kp) s)
     (dotimes (i (length _joint_kp))
       (sys::poke (elt _joint_kp i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_kd
     (write-long (length _joint_kd) s)
     (dotimes (i (length _joint_kd))
       (sys::poke (elt _joint_kd i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; int32[] _control_modes
     (write-long (length _control_modes) s)
     (dotimes (i (length _control_modes))
       (write-long (elt _control_modes i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64[] _joint_q
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_q (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_q i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_v
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_v (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_v i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _tau
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tau (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _tau i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _tau_max
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tau_max (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _tau_max i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _tau_ratio
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tau_ratio (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _tau_ratio i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_kp
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_kp (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_kp i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_kd
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_kd (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_kd i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; int32[] _control_modes
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _control_modes (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _control_modes i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get kuavo_msgs::jointCmd :md5sum-) "9ed16f87b9f90b25cdeeb417f3c21f9e")
(setf (get kuavo_msgs::jointCmd :datatype-) "kuavo_msgs/jointCmd")
(setf (get kuavo_msgs::jointCmd :definition-)
      "std_msgs/Header header
float64[] joint_q  
float64[] joint_v  
float64[] tau  
float64[] tau_max
float64[] tau_ratio  
float64[] joint_kp  
float64[] joint_kd
int32[] control_modes  

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



(provide :kuavo_msgs/jointCmd "9ed16f87b9f90b25cdeeb417f3c21f9e")


