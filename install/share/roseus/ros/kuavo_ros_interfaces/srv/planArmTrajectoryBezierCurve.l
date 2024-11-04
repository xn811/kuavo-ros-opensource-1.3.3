;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::planArmTrajectoryBezierCurve)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'planArmTrajectoryBezierCurve (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVE")
  (make-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVE"))
(unless (find-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVEREQUEST")
  (make-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVEREQUEST"))
(unless (find-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVERESPONSE")
  (make-package "KUAVO_ROS_INTERFACES::PLANARMTRAJECTORYBEZIERCURVERESPONSE"))

(in-package "ROS")





(defclass kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest
  :super ros::object
  :slots (_multi_joint_bezier_trajectory _start_frame_time _end_frame_time _joint_names ))

(defmethod kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest
  (:init
   (&key
    ((:multi_joint_bezier_trajectory __multi_joint_bezier_trajectory) ())
    ((:start_frame_time __start_frame_time) 0.0)
    ((:end_frame_time __end_frame_time) 0.0)
    ((:joint_names __joint_names) (let (r) (dotimes (i 0) (push "" r)) r))
    )
   (send-super :init)
   (setq _multi_joint_bezier_trajectory __multi_joint_bezier_trajectory)
   (setq _start_frame_time (float __start_frame_time))
   (setq _end_frame_time (float __end_frame_time))
   (setq _joint_names __joint_names)
   self)
  (:multi_joint_bezier_trajectory
   (&rest __multi_joint_bezier_trajectory)
   (if (keywordp (car __multi_joint_bezier_trajectory))
       (send* _multi_joint_bezier_trajectory __multi_joint_bezier_trajectory)
     (progn
       (if __multi_joint_bezier_trajectory (setq _multi_joint_bezier_trajectory (car __multi_joint_bezier_trajectory)))
       _multi_joint_bezier_trajectory)))
  (:start_frame_time
   (&optional __start_frame_time)
   (if __start_frame_time (setq _start_frame_time __start_frame_time)) _start_frame_time)
  (:end_frame_time
   (&optional __end_frame_time)
   (if __end_frame_time (setq _end_frame_time __end_frame_time)) _end_frame_time)
  (:joint_names
   (&optional __joint_names)
   (if __joint_names (setq _joint_names __joint_names)) _joint_names)
  (:serialization-length
   ()
   (+
    ;; kuavo_ros_interfaces/jointBezierTrajectory[] _multi_joint_bezier_trajectory
    (apply #'+ (send-all _multi_joint_bezier_trajectory :serialization-length)) 4
    ;; float64 _start_frame_time
    8
    ;; float64 _end_frame_time
    8
    ;; string[] _joint_names
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _joint_names)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; kuavo_ros_interfaces/jointBezierTrajectory[] _multi_joint_bezier_trajectory
     (write-long (length _multi_joint_bezier_trajectory) s)
     (dolist (elem _multi_joint_bezier_trajectory)
       (send elem :serialize s)
       )
     ;; float64 _start_frame_time
       (sys::poke _start_frame_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _end_frame_time
       (sys::poke _end_frame_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; string[] _joint_names
     (write-long (length _joint_names) s)
     (dolist (elem _joint_names)
       (write-long (length elem) s) (princ elem s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; kuavo_ros_interfaces/jointBezierTrajectory[] _multi_joint_bezier_trajectory
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _multi_joint_bezier_trajectory (let (r) (dotimes (i n) (push (instance kuavo_ros_interfaces::jointBezierTrajectory :init) r)) r))
     (dolist (elem- _multi_joint_bezier_trajectory)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; float64 _start_frame_time
     (setq _start_frame_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _end_frame_time
     (setq _end_frame_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; string[] _joint_names
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_names (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _joint_names i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;;
   self)
  )

(defclass kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse
  :super ros::object
  :slots (_success ))

(defmethod kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse
  (:init
   (&key
    ((:success __success) nil)
    )
   (send-super :init)
   (setq _success __success)
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass kuavo_ros_interfaces::planArmTrajectoryBezierCurve
  :super ros::object
  :slots ())

(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurve :md5sum-) "4dbc940608d7275f775b6fdef47eb369")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurve :datatype-) "kuavo_ros_interfaces/planArmTrajectoryBezierCurve")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurve :request) kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest)
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurve :response) kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse)

(defmethod kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest
  (:response () (instance kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse :init)))

(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest :md5sum-) "4dbc940608d7275f775b6fdef47eb369")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest :datatype-) "kuavo_ros_interfaces/planArmTrajectoryBezierCurveRequest")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveRequest :definition-)
      "kuavo_ros_interfaces/jointBezierTrajectory[] multi_joint_bezier_trajectory
float64 start_frame_time
float64 end_frame_time
string[] joint_names

================================================================================
MSG: kuavo_ros_interfaces/jointBezierTrajectory
kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points
================================================================================
MSG: kuavo_ros_interfaces/bezierCurveCubicPoint
# [x, y] x is time, y is value

float64[] end_point
float64[] left_control_point
---
bool success
")

(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse :md5sum-) "4dbc940608d7275f775b6fdef47eb369")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse :datatype-) "kuavo_ros_interfaces/planArmTrajectoryBezierCurveResponse")
(setf (get kuavo_ros_interfaces::planArmTrajectoryBezierCurveResponse :definition-)
      "kuavo_ros_interfaces/jointBezierTrajectory[] multi_joint_bezier_trajectory
float64 start_frame_time
float64 end_frame_time
string[] joint_names

================================================================================
MSG: kuavo_ros_interfaces/jointBezierTrajectory
kuavo_ros_interfaces/bezierCurveCubicPoint[] bezier_curve_points
================================================================================
MSG: kuavo_ros_interfaces/bezierCurveCubicPoint
# [x, y] x is time, y is value

float64[] end_point
float64[] left_control_point
---
bool success
")



(provide :kuavo_ros_interfaces/planArmTrajectoryBezierCurve "4dbc940608d7275f775b6fdef47eb369")


