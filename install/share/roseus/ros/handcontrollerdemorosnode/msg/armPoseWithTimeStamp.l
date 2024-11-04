;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::armPoseWithTimeStamp)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'armPoseWithTimeStamp (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::ARMPOSEWITHTIMESTAMP")
  (make-package "HANDCONTROLLERDEMOROSNODE::ARMPOSEWITHTIMESTAMP"))

(in-package "ROS")
;;//! \htmlinclude armPoseWithTimeStamp.msg.html


(defclass handcontrollerdemorosnode::armPoseWithTimeStamp
  :super ros::object
  :slots (_offset _left_hand_pose _right_hand_pose ))

(defmethod handcontrollerdemorosnode::armPoseWithTimeStamp
  (:init
   (&key
    ((:offset __offset) 0)
    ((:left_hand_pose __left_hand_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:right_hand_pose __right_hand_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _offset (round __offset))
   (setq _left_hand_pose __left_hand_pose)
   (setq _right_hand_pose __right_hand_pose)
   self)
  (:offset
   (&optional __offset)
   (if __offset (setq _offset __offset)) _offset)
  (:left_hand_pose
   (&optional __left_hand_pose)
   (if __left_hand_pose (setq _left_hand_pose __left_hand_pose)) _left_hand_pose)
  (:right_hand_pose
   (&optional __right_hand_pose)
   (if __right_hand_pose (setq _right_hand_pose __right_hand_pose)) _right_hand_pose)
  (:serialization-length
   ()
   (+
    ;; int32 _offset
    4
    ;; float64[] _left_hand_pose
    (* 8    (length _left_hand_pose)) 4
    ;; float64[] _right_hand_pose
    (* 8    (length _right_hand_pose)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _offset
       (write-long _offset s)
     ;; float64[] _left_hand_pose
     (write-long (length _left_hand_pose) s)
     (dotimes (i (length _left_hand_pose))
       (sys::poke (elt _left_hand_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _right_hand_pose
     (write-long (length _right_hand_pose) s)
     (dotimes (i (length _right_hand_pose))
       (sys::poke (elt _right_hand_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _offset
     (setq _offset (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64[] _left_hand_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _left_hand_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _left_hand_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _right_hand_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _right_hand_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _right_hand_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get handcontrollerdemorosnode::armPoseWithTimeStamp :md5sum-) "3404338b5cb042ac3b3cf3de3f0fcb4f")
(setf (get handcontrollerdemorosnode::armPoseWithTimeStamp :datatype-) "handcontrollerdemorosnode/armPoseWithTimeStamp")
(setf (get handcontrollerdemorosnode::armPoseWithTimeStamp :definition-)
      "int32 offset
float64[] left_hand_pose
float64[] right_hand_pose
")



(provide :handcontrollerdemorosnode/armPoseWithTimeStamp "3404338b5cb042ac3b3cf3de3f0fcb4f")


