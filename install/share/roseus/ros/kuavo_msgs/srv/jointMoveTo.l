;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::jointMoveTo)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'jointMoveTo (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::JOINTMOVETO")
  (make-package "KUAVO_MSGS::JOINTMOVETO"))
(unless (find-package "KUAVO_MSGS::JOINTMOVETOREQUEST")
  (make-package "KUAVO_MSGS::JOINTMOVETOREQUEST"))
(unless (find-package "KUAVO_MSGS::JOINTMOVETORESPONSE")
  (make-package "KUAVO_MSGS::JOINTMOVETORESPONSE"))

(in-package "ROS")





(defclass kuavo_msgs::jointMoveToRequest
  :super ros::object
  :slots (_goal_position _speed _dt ))

(defmethod kuavo_msgs::jointMoveToRequest
  (:init
   (&key
    ((:goal_position __goal_position) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:speed __speed) 0.0)
    ((:dt __dt) 0.0)
    )
   (send-super :init)
   (setq _goal_position __goal_position)
   (setq _speed (float __speed))
   (setq _dt (float __dt))
   self)
  (:goal_position
   (&optional __goal_position)
   (if __goal_position (setq _goal_position __goal_position)) _goal_position)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:dt
   (&optional __dt)
   (if __dt (setq _dt __dt)) _dt)
  (:serialization-length
   ()
   (+
    ;; float64[] _goal_position
    (* 8    (length _goal_position)) 4
    ;; float64 _speed
    8
    ;; float64 _dt
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _goal_position
     (write-long (length _goal_position) s)
     (dotimes (i (length _goal_position))
       (sys::poke (elt _goal_position i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dt
       (sys::poke _dt (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _goal_position
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _goal_position (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _goal_position i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64 _speed
     (setq _speed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dt
     (setq _dt (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass kuavo_msgs::jointMoveToResponse
  :super ros::object
  :slots (_success _message ))

(defmethod kuavo_msgs::jointMoveToResponse
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

(defclass kuavo_msgs::jointMoveTo
  :super ros::object
  :slots ())

(setf (get kuavo_msgs::jointMoveTo :md5sum-) "61bc968af7a59106f6f5092f42d53578")
(setf (get kuavo_msgs::jointMoveTo :datatype-) "kuavo_msgs/jointMoveTo")
(setf (get kuavo_msgs::jointMoveTo :request) kuavo_msgs::jointMoveToRequest)
(setf (get kuavo_msgs::jointMoveTo :response) kuavo_msgs::jointMoveToResponse)

(defmethod kuavo_msgs::jointMoveToRequest
  (:response () (instance kuavo_msgs::jointMoveToResponse :init)))

(setf (get kuavo_msgs::jointMoveToRequest :md5sum-) "61bc968af7a59106f6f5092f42d53578")
(setf (get kuavo_msgs::jointMoveToRequest :datatype-) "kuavo_msgs/jointMoveToRequest")
(setf (get kuavo_msgs::jointMoveToRequest :definition-)
      "float64[] goal_position
float64 speed
float64 dt
---
bool success
string message

")

(setf (get kuavo_msgs::jointMoveToResponse :md5sum-) "61bc968af7a59106f6f5092f42d53578")
(setf (get kuavo_msgs::jointMoveToResponse :datatype-) "kuavo_msgs/jointMoveToResponse")
(setf (get kuavo_msgs::jointMoveToResponse :definition-)
      "float64[] goal_position
float64 speed
float64 dt
---
bool success
string message

")



(provide :kuavo_msgs/jointMoveTo "61bc968af7a59106f6f5092f42d53578")


