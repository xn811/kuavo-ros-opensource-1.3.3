;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::changeHandArmPosesByConfigName)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'changeHandArmPosesByConfigName (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAME")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAME"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAMEREQUEST")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAMEREQUEST"))
(unless (find-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAMERESPONSE")
  (make-package "H12PRO_CONTROLLER_NODE::CHANGEHANDARMPOSESBYCONFIGNAMERESPONSE"))

(in-package "ROS")





(defclass h12pro_controller_node::changeHandArmPosesByConfigNameRequest
  :super ros::object
  :slots (_config_name ))

(defmethod h12pro_controller_node::changeHandArmPosesByConfigNameRequest
  (:init
   (&key
    ((:config_name __config_name) "")
    )
   (send-super :init)
   (setq _config_name (string __config_name))
   self)
  (:config_name
   (&optional __config_name)
   (if __config_name (setq _config_name __config_name)) _config_name)
  (:serialization-length
   ()
   (+
    ;; string _config_name
    4 (length _config_name)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _config_name
       (write-long (length _config_name) s) (princ _config_name s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _config_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _config_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass h12pro_controller_node::changeHandArmPosesByConfigNameResponse
  :super ros::object
  :slots (_result ))

(defmethod h12pro_controller_node::changeHandArmPosesByConfigNameResponse
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

(defclass h12pro_controller_node::changeHandArmPosesByConfigName
  :super ros::object
  :slots ())

(setf (get h12pro_controller_node::changeHandArmPosesByConfigName :md5sum-) "981617b9cc6699ade1d3c011b67988a7")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigName :datatype-) "h12pro_controller_node/changeHandArmPosesByConfigName")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigName :request) h12pro_controller_node::changeHandArmPosesByConfigNameRequest)
(setf (get h12pro_controller_node::changeHandArmPosesByConfigName :response) h12pro_controller_node::changeHandArmPosesByConfigNameResponse)

(defmethod h12pro_controller_node::changeHandArmPosesByConfigNameRequest
  (:response () (instance h12pro_controller_node::changeHandArmPosesByConfigNameResponse :init)))

(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameRequest :md5sum-) "981617b9cc6699ade1d3c011b67988a7")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameRequest :datatype-) "h12pro_controller_node/changeHandArmPosesByConfigNameRequest")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameRequest :definition-)
      "string config_name
---
bool result

")

(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameResponse :md5sum-) "981617b9cc6699ade1d3c011b67988a7")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameResponse :datatype-) "h12pro_controller_node/changeHandArmPosesByConfigNameResponse")
(setf (get h12pro_controller_node::changeHandArmPosesByConfigNameResponse :definition-)
      "string config_name
---
bool result

")



(provide :h12pro_controller_node/changeHandArmPosesByConfigName "981617b9cc6699ade1d3c011b67988a7")


