;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::robotArmPose)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'robotArmPose (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::ROBOTARMPOSE")
  (make-package "HANDCONTROLLERDEMOROSNODE::ROBOTARMPOSE"))

(in-package "ROS")
;;//! \htmlinclude robotArmPose.msg.html


(defclass handcontrollerdemorosnode::robotArmPose
  :super ros::object
  :slots (_left_arm_pose _right_arm_pose ))

(defmethod handcontrollerdemorosnode::robotArmPose
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

(setf (get handcontrollerdemorosnode::robotArmPose :md5sum-) "c281ae760454cca592ca88fb5b3b708b")
(setf (get handcontrollerdemorosnode::robotArmPose :datatype-) "handcontrollerdemorosnode/robotArmPose")
(setf (get handcontrollerdemorosnode::robotArmPose :definition-)
      "float64[] left_arm_pose
float64[] right_arm_pose
")



(provide :handcontrollerdemorosnode/robotArmPose "c281ae760454cca592ca88fb5b3b708b")


