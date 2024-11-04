;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::bezierCurveCubicPoint)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'bezierCurveCubicPoint (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::BEZIERCURVECUBICPOINT")
  (make-package "KUAVO_ROS_INTERFACES::BEZIERCURVECUBICPOINT"))

(in-package "ROS")
;;//! \htmlinclude bezierCurveCubicPoint.msg.html


(defclass kuavo_ros_interfaces::bezierCurveCubicPoint
  :super ros::object
  :slots (_end_point _left_control_point _right_control_point ))

(defmethod kuavo_ros_interfaces::bezierCurveCubicPoint
  (:init
   (&key
    ((:end_point __end_point) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:left_control_point __left_control_point) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:right_control_point __right_control_point) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _end_point __end_point)
   (setq _left_control_point __left_control_point)
   (setq _right_control_point __right_control_point)
   self)
  (:end_point
   (&optional __end_point)
   (if __end_point (setq _end_point __end_point)) _end_point)
  (:left_control_point
   (&optional __left_control_point)
   (if __left_control_point (setq _left_control_point __left_control_point)) _left_control_point)
  (:right_control_point
   (&optional __right_control_point)
   (if __right_control_point (setq _right_control_point __right_control_point)) _right_control_point)
  (:serialization-length
   ()
   (+
    ;; float64[] _end_point
    (* 8    (length _end_point)) 4
    ;; float64[] _left_control_point
    (* 8    (length _left_control_point)) 4
    ;; float64[] _right_control_point
    (* 8    (length _right_control_point)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _end_point
     (write-long (length _end_point) s)
     (dotimes (i (length _end_point))
       (sys::poke (elt _end_point i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _left_control_point
     (write-long (length _left_control_point) s)
     (dotimes (i (length _left_control_point))
       (sys::poke (elt _left_control_point i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _right_control_point
     (write-long (length _right_control_point) s)
     (dotimes (i (length _right_control_point))
       (sys::poke (elt _right_control_point i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _end_point
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _end_point (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _end_point i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _left_control_point
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _left_control_point (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _left_control_point i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _right_control_point
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _right_control_point (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _right_control_point i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get kuavo_ros_interfaces::bezierCurveCubicPoint :md5sum-) "4262726b7e41e02a58fb5df3475aa027")
(setf (get kuavo_ros_interfaces::bezierCurveCubicPoint :datatype-) "kuavo_ros_interfaces/bezierCurveCubicPoint")
(setf (get kuavo_ros_interfaces::bezierCurveCubicPoint :definition-)
      "# [x, y] x is time, y is value

float64[] end_point
float64[] left_control_point
float64[] right_control_point
")



(provide :kuavo_ros_interfaces/bezierCurveCubicPoint "4262726b7e41e02a58fb5df3475aa027")


