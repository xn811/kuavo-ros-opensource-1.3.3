;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::changeArmCtrlMode)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'changeArmCtrlMode (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODE")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODE"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODEREQUEST")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODEREQUEST"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODERESPONSE")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEARMCTRLMODERESPONSE"))

(in-package "ROS")





(defclass h12pro_controller_node::changeArmCtrlModeRequest
  :super ros::object
  :slots (_control_mode ))

(defmethod h12pro_controller_node::changeArmCtrlModeRequest
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

(defclass h12pro_controller_node::changeArmCtrlModeResponse
  :super ros::object
  :slots (_result ))

(defmethod h12pro_controller_node::changeArmCtrlModeResponse
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

(defclass h12pro_controller_node::changeArmCtrlMode
  :super ros::object
  :slots ())

(setf (get h12pro_controller_node::changeArmCtrlMode :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeArmCtrlMode :datatype-) "h12pro_controller_node/changeArmCtrlMode")
(setf (get h12pro_controller_node::changeArmCtrlMode :request) h12pro_controller_node::changeArmCtrlModeRequest)
(setf (get h12pro_controller_node::changeArmCtrlMode :response) h12pro_controller_node::changeArmCtrlModeResponse)

(defmethod h12pro_controller_node::changeArmCtrlModeRequest
  (:response () (instance h12pro_controller_node::changeArmCtrlModeResponse :init)))

(setf (get h12pro_controller_node::changeArmCtrlModeRequest :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeArmCtrlModeRequest :datatype-) "h12pro_controller_node/changeArmCtrlModeRequest")
(setf (get h12pro_controller_node::changeArmCtrlModeRequest :definition-)
      "bool control_mode
---
bool result


")

(setf (get h12pro_controller_node::changeArmCtrlModeResponse :md5sum-) "f89438f9d6f48f748eabe64775a22261")
(setf (get h12pro_controller_node::changeArmCtrlModeResponse :datatype-) "h12pro_controller_node/changeArmCtrlModeResponse")
(setf (get h12pro_controller_node::changeArmCtrlModeResponse :definition-)
      "bool control_mode
---
bool result


")



(provide :h12pro_controller_node/changeArmCtrlMode "f89438f9d6f48f748eabe64775a22261")


