;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::changeArmCtrlMode)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'changeArmCtrlMode (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODE")
  (make-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODE"))
(unless (find-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODEREQUEST")
  (make-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODEREQUEST"))
(unless (find-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODERESPONSE")
  (make-package "MOTION_CAPTURE_IK::CHANGEARMCTRLMODERESPONSE"))

(in-package "ROS")





(defclass motion_capture_ik::changeArmCtrlModeRequest
  :super ros::object
  :slots (_control_mode ))

(defmethod motion_capture_ik::changeArmCtrlModeRequest
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

(defclass motion_capture_ik::changeArmCtrlModeResponse
  :super ros::object
  :slots (_result _mode _message ))

(defmethod motion_capture_ik::changeArmCtrlModeResponse
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

(defclass motion_capture_ik::changeArmCtrlMode
  :super ros::object
  :slots ())

(setf (get motion_capture_ik::changeArmCtrlMode :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get motion_capture_ik::changeArmCtrlMode :datatype-) "motion_capture_ik/changeArmCtrlMode")
(setf (get motion_capture_ik::changeArmCtrlMode :request) motion_capture_ik::changeArmCtrlModeRequest)
(setf (get motion_capture_ik::changeArmCtrlMode :response) motion_capture_ik::changeArmCtrlModeResponse)

(defmethod motion_capture_ik::changeArmCtrlModeRequest
  (:response () (instance motion_capture_ik::changeArmCtrlModeResponse :init)))

(setf (get motion_capture_ik::changeArmCtrlModeRequest :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get motion_capture_ik::changeArmCtrlModeRequest :datatype-) "motion_capture_ik/changeArmCtrlModeRequest")
(setf (get motion_capture_ik::changeArmCtrlModeRequest :definition-)
      "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control 
---
bool result
int32 mode 
string message


")

(setf (get motion_capture_ik::changeArmCtrlModeResponse :md5sum-) "8a8d154c05ee16e8f5d2b72d9bb51026")
(setf (get motion_capture_ik::changeArmCtrlModeResponse :datatype-) "motion_capture_ik/changeArmCtrlModeResponse")
(setf (get motion_capture_ik::changeArmCtrlModeResponse :definition-)
      "int32 control_mode # 0: keep pose, 1: auto_swing_arm, 2: external_control 
---
bool result
int32 mode 
string message


")



(provide :motion_capture_ik/changeArmCtrlMode "8a8d154c05ee16e8f5d2b72d9bb51026")


