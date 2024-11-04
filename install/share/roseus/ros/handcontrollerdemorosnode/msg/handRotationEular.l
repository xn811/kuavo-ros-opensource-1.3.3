;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::handRotationEular)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'handRotationEular (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::HANDROTATIONEULAR")
  (make-package "HANDCONTROLLERDEMOROSNODE::HANDROTATIONEULAR"))

(in-package "ROS")
;;//! \htmlinclude handRotationEular.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass handcontrollerdemorosnode::handRotationEular
  :super ros::object
  :slots (_eulerAngles ))

(defmethod handcontrollerdemorosnode::handRotationEular
  (:init
   (&key
    ((:eulerAngles __eulerAngles) ())
    )
   (send-super :init)
   (setq _eulerAngles __eulerAngles)
   self)
  (:eulerAngles
   (&rest __eulerAngles)
   (if (keywordp (car __eulerAngles))
       (send* _eulerAngles __eulerAngles)
     (progn
       (if __eulerAngles (setq _eulerAngles (car __eulerAngles)))
       _eulerAngles)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Vector3[] _eulerAngles
    (apply #'+ (send-all _eulerAngles :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Vector3[] _eulerAngles
     (write-long (length _eulerAngles) s)
     (dolist (elem _eulerAngles)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Vector3[] _eulerAngles
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _eulerAngles (let (r) (dotimes (i n) (push (instance geometry_msgs::Vector3 :init) r)) r))
     (dolist (elem- _eulerAngles)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get handcontrollerdemorosnode::handRotationEular :md5sum-) "6f24fd3e9eed11c525f6da164f46e8b2")
(setf (get handcontrollerdemorosnode::handRotationEular :datatype-) "handcontrollerdemorosnode/handRotationEular")
(setf (get handcontrollerdemorosnode::handRotationEular :definition-)
      "geometry_msgs/Vector3[] eulerAngles

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
")



(provide :handcontrollerdemorosnode/handRotationEular "6f24fd3e9eed11c525f6da164f46e8b2")


