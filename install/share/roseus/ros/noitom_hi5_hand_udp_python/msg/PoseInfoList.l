;; Auto-generated. Do not edit!


(when (boundp 'noitom_hi5_hand_udp_python::PoseInfoList)
  (if (not (find-package "NOITOM_HI5_HAND_UDP_PYTHON"))
    (make-package "NOITOM_HI5_HAND_UDP_PYTHON"))
  (shadow 'PoseInfoList (find-package "NOITOM_HI5_HAND_UDP_PYTHON")))
(unless (find-package "NOITOM_HI5_HAND_UDP_PYTHON::POSEINFOLIST")
  (make-package "NOITOM_HI5_HAND_UDP_PYTHON::POSEINFOLIST"))

(in-package "ROS")
;;//! \htmlinclude PoseInfoList.msg.html


(defclass noitom_hi5_hand_udp_python::PoseInfoList
  :super ros::object
  :slots (_timestamp_ms _is_high_confidence _is_hand_tracking _poses ))

(defmethod noitom_hi5_hand_udp_python::PoseInfoList
  (:init
   (&key
    ((:timestamp_ms __timestamp_ms) 0)
    ((:is_high_confidence __is_high_confidence) nil)
    ((:is_hand_tracking __is_hand_tracking) nil)
    ((:poses __poses) ())
    )
   (send-super :init)
   (setq _timestamp_ms (round __timestamp_ms))
   (setq _is_high_confidence __is_high_confidence)
   (setq _is_hand_tracking __is_hand_tracking)
   (setq _poses __poses)
   self)
  (:timestamp_ms
   (&optional __timestamp_ms)
   (if __timestamp_ms (setq _timestamp_ms __timestamp_ms)) _timestamp_ms)
  (:is_high_confidence
   (&optional (__is_high_confidence :null))
   (if (not (eq __is_high_confidence :null)) (setq _is_high_confidence __is_high_confidence)) _is_high_confidence)
  (:is_hand_tracking
   (&optional (__is_hand_tracking :null))
   (if (not (eq __is_hand_tracking :null)) (setq _is_hand_tracking __is_hand_tracking)) _is_hand_tracking)
  (:poses
   (&rest __poses)
   (if (keywordp (car __poses))
       (send* _poses __poses)
     (progn
       (if __poses (setq _poses (car __poses)))
       _poses)))
  (:serialization-length
   ()
   (+
    ;; int64 _timestamp_ms
    8
    ;; bool _is_high_confidence
    1
    ;; bool _is_hand_tracking
    1
    ;; noitom_hi5_hand_udp_python/PoseInfo[] _poses
    (apply #'+ (send-all _poses :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _timestamp_ms
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _timestamp_ms (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _timestamp_ms) (= (length (_timestamp_ms . bv)) 2)) ;; bignum
              (write-long (ash (elt (_timestamp_ms . bv) 0) 0) s)
              (write-long (ash (elt (_timestamp_ms . bv) 1) -1) s))
             ((and (class _timestamp_ms) (= (length (_timestamp_ms . bv)) 1)) ;; big1
              (write-long (elt (_timestamp_ms . bv) 0) s)
              (write-long (if (>= _timestamp_ms 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _timestamp_ms s)(write-long (if (>= _timestamp_ms 0) 0 #xffffffff) s)))
     ;; bool _is_high_confidence
       (if _is_high_confidence (write-byte -1 s) (write-byte 0 s))
     ;; bool _is_hand_tracking
       (if _is_hand_tracking (write-byte -1 s) (write-byte 0 s))
     ;; noitom_hi5_hand_udp_python/PoseInfo[] _poses
     (write-long (length _poses) s)
     (dolist (elem _poses)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _timestamp_ms
#+(or :alpha :irix6 :x86_64)
      (setf _timestamp_ms (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _timestamp_ms (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; bool _is_high_confidence
     (setq _is_high_confidence (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _is_hand_tracking
     (setq _is_hand_tracking (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; noitom_hi5_hand_udp_python/PoseInfo[] _poses
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _poses (let (r) (dotimes (i n) (push (instance noitom_hi5_hand_udp_python::PoseInfo :init) r)) r))
     (dolist (elem- _poses)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get noitom_hi5_hand_udp_python::PoseInfoList :md5sum-) "f56d5e4df1c0e38a423ead4bde9414b3")
(setf (get noitom_hi5_hand_udp_python::PoseInfoList :datatype-) "noitom_hi5_hand_udp_python/PoseInfoList")
(setf (get noitom_hi5_hand_udp_python::PoseInfoList :definition-)
      "int64 timestamp_ms
bool is_high_confidence
bool is_hand_tracking
PoseInfo[] poses
================================================================================
MSG: noitom_hi5_hand_udp_python/PoseInfo
geometry_msgs/Point position
geometry_msgs/Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :noitom_hi5_hand_udp_python/PoseInfoList "f56d5e4df1c0e38a423ead4bde9414b3")


