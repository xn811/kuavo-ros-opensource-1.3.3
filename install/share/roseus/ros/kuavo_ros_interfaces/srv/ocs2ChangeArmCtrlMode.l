;; Auto-generated. Do not edit!


(when (boundp 'kuavo_ros_interfaces::ocs2ChangeArmCtrlMode)
  (if (not (find-package "KUAVO_ROS_INTERFACES"))
    (make-package "KUAVO_ROS_INTERFACES"))
  (shadow 'ocs2ChangeArmCtrlMode (find-package "KUAVO_ROS_INTERFACES")))
(unless (find-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODE")
  (make-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODE"))
(unless (find-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODEREQUEST")
  (make-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODEREQUEST"))
(unless (find-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODERESPONSE")
  (make-package "KUAVO_ROS_INTERFACES::OCS2CHANGEARMCTRLMODERESPONSE"))

(in-package "ROS")





(defclass kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest
  :super ros::object
  :slots (_control_mode ))

(defmethod kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest
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

(defclass kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse
  :super ros::object
  :slots (_result _mode _message ))

(defmethod kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse
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

(defclass kuavo_ros_interfaces::ocs2ChangeArmCtrlMode
  :super ros::object
  :slots ())

(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlMode :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlMode :datatype-) "kuavo_ros_interfaces/ocs2ChangeArmCtrlMode")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlMode :request) kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest)
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlMode :response) kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse)

(defmethod kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest
  (:response () (instance kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse :init)))

(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest :datatype-) "kuavo_ros_interfaces/ocs2ChangeArmCtrlModeRequest")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeRequest :definition-)
      "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control 
---
bool result
int32 mode 
string message


")

(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse :datatype-) "kuavo_ros_interfaces/ocs2ChangeArmCtrlModeResponse")
(setf (get kuavo_ros_interfaces::ocs2ChangeArmCtrlModeResponse :definition-)
      "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control 
---
bool result
int32 mode 
string message


")



(provide :kuavo_ros_interfaces/ocs2ChangeArmCtrlMode "8a8d154c05ee16e8f5d2b72d9bb51026")


