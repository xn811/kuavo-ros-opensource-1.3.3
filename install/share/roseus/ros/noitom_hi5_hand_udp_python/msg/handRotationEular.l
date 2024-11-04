;; Auto-generated. Do not edit!


(when (boundp 'noitom_hi5_hand_udp_python::handRotationEular)
  (if (not (find-package "NOITOM_HI5_HAND_UDP_PYTHON"))
    (make-package "NOITOM_HI5_HAND_UDP_PYTHON"))
  (shadow 'handRotationEular (find-package "NOITOM_HI5_HAND_UDP_PYTHON")))
(unless (find-package "NOITOM_HI5_HAND_UDP_PYTHON::HANDROTATIONEULAR")
  (make-package "NOITOM_HI5_HAND_UDP_PYTHON::HANDROTATIONEULAR"))

(in-package "ROS")
;;//! \htmlinclude handRotationEular.msg.html


(defclass noitom_hi5_hand_udp_python::handRotationEular
  :super ros::object
  :slots (_eulerAngles ))

(defmethod noitom_hi5_hand_udp_python::handRotationEular
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
    ;; noitom_hi5_hand_udp_python/Vector4[] _eulerAngles
    (apply #'+ (send-all _eulerAngles :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; noitom_hi5_hand_udp_python/Vector4[] _eulerAngles
     (write-long (length _eulerAngles) s)
     (dolist (elem _eulerAngles)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; noitom_hi5_hand_udp_python/Vector4[] _eulerAngles
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _eulerAngles (let (r) (dotimes (i n) (push (instance noitom_hi5_hand_udp_python::Vector4 :init) r)) r))
     (dolist (elem- _eulerAngles)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get noitom_hi5_hand_udp_python::handRotationEular :md5sum-) "75ea7fdfd1913bbabb0a96c424b42024")
(setf (get noitom_hi5_hand_udp_python::handRotationEular :datatype-) "noitom_hi5_hand_udp_python/handRotationEular")
(setf (get noitom_hi5_hand_udp_python::handRotationEular :definition-)
      "noitom_hi5_hand_udp_python/Vector4[] eulerAngles

================================================================================
MSG: noitom_hi5_hand_udp_python/Vector4
float32 x
float32 y
float32 z
float32 w
")



(provide :noitom_hi5_hand_udp_python/handRotationEular "75ea7fdfd1913bbabb0a96c424b42024")


