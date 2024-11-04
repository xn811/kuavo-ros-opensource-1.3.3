;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::changeAMBACCtrlMode)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'changeAMBACCtrlMode (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODE")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODE"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODEREQUEST")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODEREQUEST"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODERESPONSE")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEAMBACCTRLMODERESPONSE"))

(in-package "ROS")





(defclass h12pro_controller_node::changeAMBACCtrlModeRequest
  :super ros::object
  :slots (_control_mode ))

(defmethod h12pro_controller_node::changeAMBACCtrlModeRequest
  (:init
   (&key
    ((:control_mode __control_mode) nil)
    )
   (send-super :init)
   (setq _control_mode __control_mode)
   self)
  (:control_mode
   (&optional (__control_mode :null))
   (if (not (eq __control_mode :null)) (setq _control_mode __control_mode)) _control_mode)
  (:serialization-length
   ()
   (+
    ;; bool _control_mode
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _control_mode
       (if _control_mode (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _control_mode
     (setq _control_mode (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass h12pro_controller_node::changeAMBACCtrlModeResponse
  :super ros::object
  :slots (_result ))

(defmethod h12pro_controller_node::changeAMBACCtrlModeResponse
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

(defclass h12pro_controller_node::changeAMBACCtrlMode
  :super ros::object
  :slots ())

(setf (get h12pro_controller_node::changeAMBACCtrlMode :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeAMBACCtrlMode :datatype-) "h12pro_controller_node/changeAMBACCtrlMode")
(setf (get h12pro_controller_node::changeAMBACCtrlMode :request) h12pro_controller_node::changeAMBACCtrlModeRequest)
(setf (get h12pro_controller_node::changeAMBACCtrlMode :response) h12pro_controller_node::changeAMBACCtrlModeResponse)

(defmethod h12pro_controller_node::changeAMBACCtrlModeRequest
  (:response () (instance h12pro_controller_node::changeAMBACCtrlModeResponse :init)))

(setf (get h12pro_controller_node::changeAMBACCtrlModeRequest :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeAMBACCtrlModeRequest :datatype-) "h12pro_controller_node/changeAMBACCtrlModeRequest")
(setf (get h12pro_controller_node::changeAMBACCtrlModeRequest :definition-)
      "bool control_mode
---
bool result


")

(setf (get h12pro_controller_node::changeAMBACCtrlModeResponse :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeAMBACCtrlModeResponse :datatype-) "h12pro_controller_node/changeAMBACCtrlModeResponse")
(setf (get h12pro_controller_node::changeAMBACCtrlModeResponse :definition-)
      "bool control_mode
---
bool result


")



(provide :h12pro_controller_node/changeAMBACCtrlMode "f89438f9d6f48f748eabe64775a22261")


