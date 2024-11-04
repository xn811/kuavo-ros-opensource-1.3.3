;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::planArmState)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'planArmState (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::PLANARMSTATE")
  (make-package "KUAVO_ROS_INTERFACES::PLANARMSTATE"))

(in-package "ROS")
;;//! \htmlinclude planArmState.msg.html


(defclass kuavo_ros_interfaces::planArmState
  :super ros::object
  :slots (_progress _is_finished ))

(defmethod kuavo_ros_interfaces::planArmState
  (:init
   (&key
    ((:progress __progress) 0)
    ((:is_finished __is_finished) nil)
    )
   (send-super :init)
   (setq _progress (round __progress))
   (setq _is_finished __is_finished)
   self)
  (:progress
   (&optional __progress)
   (if __progress (setq _progress __progress)) _progress)
  (:is_finished
   (&optional (__is_finished :null))
   (if (not (eq __is_finished :null)) (setq _is_finished __is_finished)) _is_finished)
  (:serialization-length
   ()
   (+
    ;; int32 _progress
    4
    ;; bool _is_finished
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _progress
       (write-long _progress s)
     ;; bool _is_finished
       (if _is_finished (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _progress
     (setq _progress (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; bool _is_finished
     (setq _is_finished (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get kuavo_ros_interfaces::planArmState :md5sum-) "0743feb5221b176f512f6ea58920b201")
(setf (get kuavo_ros_interfaces::planArmState :datatype-) "kuavo_ros_interfaces/planArmState")
(setf (get kuavo_ros_interfaces::planArmState :definition-)
      "int32 progress
bool is_finished
")



(provide :kuavo_ros_interfaces/planArmState "0743feb5221b176f512f6ea58920b201")


