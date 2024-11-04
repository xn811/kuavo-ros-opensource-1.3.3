;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::jointBezierTrajectory)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'jointBezierTrajectory (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::JOINTBEZIERTRAJECTORY")
  (make-package "KUAVO_ROS_INTERFACES::JOINTBEZIERTRAJECTORY"))

(in-package "ROS")
;;//! \htmlinclude jointBezierTrajectory.msg.html


(defclass kuavo_ros_interfaces::jointBezierTrajectory
  :super ros::object
  :slots (_bezier_curve_points ))

(defmethod kuavo_ros_interfaces::jointBezierTrajectory
  (:init
   (&key
    ((:bezier_curve_points __bezier_curve_points) ())
    )
   (send-super :init)
   (setq _bezier_curve_points __bezier_curve_points)
   self)
  (:bezier_curve_points
   (&rest __bezier_curve_points)
   (if (keywordp (car __bezier_curve_points))
       (send* _bezier_curve_points __bezier_curve_points)
     (progn
       (if __bezier_curve_points (setq _bezier_curve_points (car __bezier_curve_points)))
       _bezier_curve_points)))
  (:serialization-length
   ()
   (+
    ;; kuavo_ros_interfaces/bezierCurveCubicPoint[] _bezier_curve_points
    (apply #'+ (send-all _bezier_curve_points :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; kuavo_ros_interfaces/bezierCurveCubicPoint[] _bezier_curve_points
     (write-long (length _bezier_curve_points) s)
     (dolist (elem _bezier_curve_points)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; kuavo_ros_interfaces/bezierCurveCubicPoint[] _bezier_curve_points
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _bezier_curve_points (let (r) (dotimes (i n) (push (instance kuavo_ros_interfaces::bezierCurveCubicPoint :init) r)) r))
     (dolist (elem- _bezier_curve_points)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get kuavo_ros_interfaces::jointBezierTrajectory :md5sum-) "734a11eb72071b59bdbb297c6a53338c")
(setf (get kuavo_ros_interfaces::jointBezierTrajectory :datatype-) "kuavo_ros_interfaces/jointBezierTrajectory")
(setf (get kuavo_ros_interfaces::jointBezierTrajectory :definition-)
      "kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points
================================================================================
MSG: kuavo_ros_interfaces/bezierCurveCubicPoint
# [x, y] x is time, y is value

float64[] end_point
float64[] left_control_point
float64[] right_control_point
")



(provide :kuavo_ros_interfaces/jointBezierTrajectory "734a11eb72071b59bdbb297c6a53338c")


