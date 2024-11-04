;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::armTargetPoses)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'armTargetPoses (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::ARMTARGETPOSES")
  (make-package "KUAVO_MSGS::ARMTARGETPOSES"))

(in-package "ROS")
;;//! \htmlinclude armTargetPoses.msg.html


(defclass kuavo_msgs::armTargetPoses
  :super ros::object
  :slots (_times _values ))

(defmethod kuavo_msgs::armTargetPoses
  (:init
   (&key
    ((:times __times) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:values __values) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _times __times)
   (setq _values __values)
   self)
  (:times
   (&optional __times)
   (if __times (setq _times __times)) _times)
  (:values
   (&optional __values)
   (if __values (setq _values __values)) _values)
  (:serialization-length
   ()
   (+
    ;; float64[] _times
    (* 8    (length _times)) 4
    ;; float64[] _values
    (* 8    (length _values)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _times
     (write-long (length _times) s)
     (dotimes (i (length _times))
       (sys::poke (elt _times i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _values
     (write-long (length _values) s)
     (dotimes (i (length _values))
       (sys::poke (elt _values i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _times
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _times (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _times i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _values
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _values (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _values i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get kuavo_msgs::armTargetPoses :md5sum-) "267055a1a7e685e90c17a3ebf7a8a26c")
(setf (get kuavo_msgs::armTargetPoses :datatype-) "kuavo_msgs/armTargetPoses")
(setf (get kuavo_msgs::armTargetPoses :definition-)
      "# times: times series
# values: values matrix
float64[] times
float64[] values

")



(provide :kuavo_msgs/armTargetPoses "267055a1a7e685e90c17a3ebf7a8a26c")


