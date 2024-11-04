;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::setHwIntialState)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'setHwIntialState (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::SETHWINTIALSTATE")
  (make-package "KUAVO_MSGS::SETHWINTIALSTATE"))
(unless (find-package "KUAVO_MSGS::SETHWINTIALSTATEREQUEST")
  (make-package "KUAVO_MSGS::SETHWINTIALSTATEREQUEST"))
(unless (find-package "KUAVO_MSGS::SETHWINTIALSTATERESPONSE")
  (make-package "KUAVO_MSGS::SETHWINTIALSTATERESPONSE"))

(in-package "ROS")





(defclass kuavo_msgs::setHwIntialStateRequest
  :super ros::object
  :slots (_q_intial _v_intial ))

(defmethod kuavo_msgs::setHwIntialStateRequest
  (:init
   (&key
    ((:q_intial __q_intial) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:v_intial __v_intial) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _q_intial __q_intial)
   (setq _v_intial __v_intial)
   self)
  (:q_intial
   (&optional __q_intial)
   (if __q_intial (setq _q_intial __q_intial)) _q_intial)
  (:v_intial
   (&optional __v_intial)
   (if __v_intial (setq _v_intial __v_intial)) _v_intial)
  (:serialization-length
   ()
   (+
    ;; float64[] _q_intial
    (* 8    (length _q_intial)) 4
    ;; float64[] _v_intial
    (* 8    (length _v_intial)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _q_intial
     (write-long (length _q_intial) s)
     (dotimes (i (length _q_intial))
       (sys::poke (elt _q_intial i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _v_intial
     (write-long (length _v_intial) s)
     (dotimes (i (length _v_intial))
       (sys::poke (elt _v_intial i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _q_intial
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_intial (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_intial i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _v_intial
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _v_intial (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _v_intial i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(defclass kuavo_msgs::setHwIntialStateResponse
  :super ros::object
  :slots (_success _message ))

(defmethod kuavo_msgs::setHwIntialStateResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass kuavo_msgs::setHwIntialState
  :super ros::object
  :slots ())

(setf (get kuavo_msgs::setHwIntialState :md5sum-) "5289a64acc27422c552070b8181b8118")
(setf (get kuavo_msgs::setHwIntialState :datatype-) "kuavo_msgs/setHwIntialState")
(setf (get kuavo_msgs::setHwIntialState :request) kuavo_msgs::setHwIntialStateRequest)
(setf (get kuavo_msgs::setHwIntialState :response) kuavo_msgs::setHwIntialStateResponse)

(defmethod kuavo_msgs::setHwIntialStateRequest
  (:response () (instance kuavo_msgs::setHwIntialStateResponse :init)))

(setf (get kuavo_msgs::setHwIntialStateRequest :md5sum-) "5289a64acc27422c552070b8181b8118")
(setf (get kuavo_msgs::setHwIntialStateRequest :datatype-) "kuavo_msgs/setHwIntialStateRequest")
(setf (get kuavo_msgs::setHwIntialStateRequest :definition-)
      "float64[] q_intial  
float64[] v_intial  
---
bool success
string message

")

(setf (get kuavo_msgs::setHwIntialStateResponse :md5sum-) "5289a64acc27422c552070b8181b8118")
(setf (get kuavo_msgs::setHwIntialStateResponse :datatype-) "kuavo_msgs/setHwIntialStateResponse")
(setf (get kuavo_msgs::setHwIntialStateResponse :definition-)
      "float64[] q_intial  
float64[] v_intial  
---
bool success
string message

")



(provide :kuavo_msgs/setHwIntialState "5289a64acc27422c552070b8181b8118")


