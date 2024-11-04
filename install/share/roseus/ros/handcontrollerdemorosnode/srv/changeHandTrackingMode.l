;; Auto-generated. Do not edit!


(when (boundp 'handcontrollerdemorosnode::changeHandTrackingMode)
  (if (not (find-package "HANDCONTROLLERDEMOROSNODE"))
    (make-package "HANDCONTROLLERDEMOROSNODE"))
  (shadow 'changeHandTrackingMode (find-package "HANDCONTROLLERDEMOROSNODE")))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODE")
  (make-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODE"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODEREQUEST")
  (make-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODEREQUEST"))
(unless (find-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODERESPONSE")
  (make-package "HANDCONTROLLERDEMOROSNODE::CHANGEHANDTRACKINGMODERESPONSE"))

(in-package "ROS")





(defclass handcontrollerdemorosnode::changeHandTrackingModeRequest
  :super ros::object
  :slots (_enable ))

(defmethod handcontrollerdemorosnode::changeHandTrackingModeRequest
  (:init
   (&key
    ((:enable __enable) nil)
    )
   (send-super :init)
   (setq _enable __enable)
   self)
  (:enable
   (&optional (__enable :null))
   (if (not (eq __enable :null)) (setq _enable __enable)) _enable)
  (:serialization-length
   ()
   (+
    ;; bool _enable
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _enable
       (if _enable (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _enable
     (setq _enable (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass handcontrollerdemorosnode::changeHandTrackingModeResponse
  :super ros::object
  :slots (_result ))

(defmethod handcontrollerdemorosnode::changeHandTrackingModeResponse
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

(defclass handcontrollerdemorosnode::changeHandTrackingMode
  :super ros::object
  :slots ())

(setf (get handcontrollerdemorosnode::changeHandTrackingMode :md5sum-) "29d58f387352c15c4e4f5763022ae875")
(setf (get handcontrollerdemorosnode::changeHandTrackingMode :datatype-) "handcontrollerdemorosnode/changeHandTrackingMode")
(setf (get handcontrollerdemorosnode::changeHandTrackingMode :request) handcontrollerdemorosnode::changeHandTrackingModeRequest)
(setf (get handcontrollerdemorosnode::changeHandTrackingMode :response) handcontrollerdemorosnode::changeHandTrackingModeResponse)

(defmethod handcontrollerdemorosnode::changeHandTrackingModeRequest
  (:response () (instance handcontrollerdemorosnode::changeHandTrackingModeResponse :init)))

(setf (get handcontrollerdemorosnode::changeHandTrackingModeRequest :md5sum-) "29d58f387352c15c4e4f5763022ae875")
(setf (get handcontrollerdemorosnode::changeHandTrackingModeRequest :datatype-) "handcontrollerdemorosnode/changeHandTrackingModeRequest")
(setf (get handcontrollerdemorosnode::changeHandTrackingModeRequest :definition-)
      "bool enable
---
bool result

")

(setf (get handcontrollerdemorosnode::changeHandTrackingModeResponse :md5sum-) "29d58f387352c15c4e4f5763022ae875")
(setf (get handcontrollerdemorosnode::changeHandTrackingModeResponse :datatype-) "handcontrollerdemorosnode/changeHandTrackingModeResponse")
(setf (get handcontrollerdemorosnode::changeHandTrackingModeResponse :definition-)
      "bool enable
---
bool result

")



(provide :handcontrollerdemorosnode/changeHandTrackingMode "29d58f387352c15c4e4f5763022ae875")


