;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::changeTorsoCtrlMode)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'changeTorsoCtrlMode (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::CHANGETORSOCTRLMODE")
  (make-package "KUAVO_MSGS::CHANGETORSOCTRLMODE"))
(unless (find-package "KUAVO_MSGS::CHANGETORSOCTRLMODEREQUEST")
  (make-package "KUAVO_MSGS::CHANGETORSOCTRLMODEREQUEST"))
(unless (find-package "KUAVO_MSGS::CHANGETORSOCTRLMODERESPONSE")
  (make-package "KUAVO_MSGS::CHANGETORSOCTRLMODERESPONSE"))

(in-package "ROS")





(defclass kuavo_msgs::changeTorsoCtrlModeRequest
  :super ros::object
  :slots (_control_mode ))

(defmethod kuavo_msgs::changeTorsoCtrlModeRequest
  (:init
   (&key
    ((:control_mode __control_mode) 0)
    )
   (send-super :init)
   (setq _control_mode (round __control_mode))
   self)
  (:control_mode
   (&optional __control_mode)
   (if __control_mode (setq _control_mode __control_mode)) _control_mode)
  (:serialization-length
   ()
   (+
    ;; int32 _control_mode
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _control_mode
       (write-long _control_mode s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _control_mode
     (setq _control_mode (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass kuavo_msgs::changeTorsoCtrlModeResponse
  :super ros::object
  :slots (_result _mode _message ))

(defmethod kuavo_msgs::changeTorsoCtrlModeResponse
  (:init
   (&key
    ((:result __result) nil)
    ((:mode __mode) 0)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _result __result)
   (setq _mode (round __mode))
   (setq _message (string __message))
   self)
  (:result
   (&optional (__result :null))
   (if (not (eq __result :null)) (setq _result __result)) _result)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _result
    1
    ;; int32 _mode
    4
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _result
       (if _result (write-byte -1 s) (write-byte 0 s))
     ;; int32 _mode
       (write-long _mode s)
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _result
     (setq _result (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _mode
     (setq _mode (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass kuavo_msgs::changeTorsoCtrlMode
  :super ros::object
  :slots ())

(setf (get kuavo_msgs::changeTorsoCtrlMode :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_msgs::changeTorsoCtrlMode :datatype-) "kuavo_msgs/changeTorsoCtrlMode")
(setf (get kuavo_msgs::changeTorsoCtrlMode :request) kuavo_msgs::changeTorsoCtrlModeRequest)
(setf (get kuavo_msgs::changeTorsoCtrlMode :response) kuavo_msgs::changeTorsoCtrlModeResponse)

(defmethod kuavo_msgs::changeTorsoCtrlModeRequest
  (:response () (instance kuavo_msgs::changeTorsoCtrlModeResponse :init)))

(setf (get kuavo_msgs::changeTorsoCtrlModeRequest :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_msgs::changeTorsoCtrlModeRequest :datatype-) "kuavo_msgs/changeTorsoCtrlModeRequest")
(setf (get kuavo_msgs::changeTorsoCtrlModeRequest :definition-)
      "int32 control_mode # 0: control 6dof, 1: control height+yaw+pitch, 2: control control height+pitch 
---
bool result
int32 mode
string message

")

(setf (get kuavo_msgs::changeTorsoCtrlModeResponse :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_msgs::changeTorsoCtrlModeResponse :datatype-) "kuavo_msgs/changeTorsoCtrlModeResponse")
(setf (get kuavo_msgs::changeTorsoCtrlModeResponse :definition-)
      "int32 control_mode # 0: control 6dof, 1: control height+yaw+pitch, 2: control control height+pitch 
---
bool result
int32 mode
string message

")



(provide :kuavo_msgs/changeTorsoCtrlMode "8a8d154c05ee16e8f5d2b72d9bb51026")


