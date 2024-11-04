;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::controlEndHand)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'controlEndHand (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHAND")
  (make-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHAND"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHANDREQUEST")
  (make-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHANDREQUEST"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHANDRESPONSE")
  (make-package "HANDCONTROLLERDEMOROSNODE::CONTROLENDHANDRESPONSE"))

(in-package "ROS")





(defclass handcontrollerdemorosnode::controlEndHandRequest
  :super ros::object
  :slots (_left_hand_position _right_hand_position ))

(defmethod handcontrollerdemorosnode::controlEndHandRequest
  (:init
   (&key
    ((:left_hand_position __left_hand_position) (make-array 0 :initial-element 0 :element-type :char))
    ((:right_hand_position __right_hand_position) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _left_hand_position __left_hand_position)
   (setq _right_hand_position __right_hand_position)
   self)
  (:left_hand_position
   (&optional __left_hand_position)
   (if __left_hand_position (setq _left_hand_position __left_hand_position)) _left_hand_position)
  (:right_hand_position
   (&optional __right_hand_position)
   (if __right_hand_position (setq _right_hand_position __right_hand_position)) _right_hand_position)
  (:serialization-length
   ()
   (+
    ;; uint8[] _left_hand_position
    (* 1    (length _left_hand_position)) 4
    ;; uint8[] _right_hand_position
    (* 1    (length _right_hand_position)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _left_hand_position
     (write-long (length _left_hand_position) s)
     (princ _left_hand_position s)
     ;; uint8[] _right_hand_position
     (write-long (length _right_hand_position) s)
     (princ _right_hand_position s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _left_hand_position
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _left_hand_position (make-array n :element-type :char))
     (replace _left_hand_position buf :start2 ptr-) (incf ptr- n))
   ;; uint8[] _right_hand_position
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _right_hand_position (make-array n :element-type :char))
     (replace _right_hand_position buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(defclass handcontrollerdemorosnode::controlEndHandResponse
  :super ros::object
  :slots (_result ))

(defmethod handcontrollerdemorosnode::controlEndHandResponse
  (:init
   (&key
    ((:result __result) nil)
    )
   (send-super :init)
   (setq _result __result)
   self)
  (:result
   (&optional (__result :null))
   (if (not (eq __result :null)) (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; bool _result
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _result
       (if _result (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _result
     (setq _result (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass handcontrollerdemorosnode::controlEndHand
  :super ros::object
  :slots ())

(setf (get handcontrollerdemorosnode::controlEndHand :md5sum-) "741989817a59889e258aa9e94c7ada8a")
(setf (get handcontrollerdemorosnode::controlEndHand :datatype-) "handcontrollerdemorosnode/controlEndHand")
(setf (get handcontrollerdemorosnode::controlEndHand :request) handcontrollerdemorosnode::controlEndHandRequest)
(setf (get handcontrollerdemorosnode::controlEndHand :response) handcontrollerdemorosnode::controlEndHandResponse)

(defmethod handcontrollerdemorosnode::controlEndHandRequest
  (:response () (instance handcontrollerdemorosnode::controlEndHandResponse :init)))

(setf (get handcontrollerdemorosnode::controlEndHandRequest :md5sum-) "741989817a59889e258aa9e94c7ada8a")
(setf (get handcontrollerdemorosnode::controlEndHandRequest :datatype-) "handcontrollerdemorosnode/controlEndHandRequest")
(setf (get handcontrollerdemorosnode::controlEndHandRequest :definition-)
      "uint8[] left_hand_position
uint8[] right_hand_position
---
bool result

")

(setf (get handcontrollerdemorosnode::controlEndHandResponse :md5sum-) "741989817a59889e258aa9e94c7ada8a")
(setf (get handcontrollerdemorosnode::controlEndHandResponse :datatype-) "handcontrollerdemorosnode/controlEndHandResponse")
(setf (get handcontrollerdemorosnode::controlEndHandResponse :definition-)
      "uint8[] left_hand_position
uint8[] right_hand_position
---
bool result

")



(provide :handcontrollerdemorosnode/controlEndHand "741989817a59889e258aa9e94c7ada8a")


