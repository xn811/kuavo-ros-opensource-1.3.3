;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::srvChangePhases)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'srvChangePhases (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASES")
  (make-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASES"))
(unless (find-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASESREQUEST")
  (make-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASESREQUEST"))
(unless (find-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASESRESPONSE")
  (make-package "H12PRO_CONTROLLER_NODE::SRVCHANGEPHASESRESPONSE"))

(in-package "ROS")





(defclass h12pro_controller_node::srvChangePhasesRequest
  :super ros::object
  :slots (_masterID _stateReq _subState ))

(defmethod h12pro_controller_node::srvChangePhasesRequest
  (:init
   (&key
    ((:masterID __masterID) 0)
    ((:stateReq __stateReq) "")
    ((:subState __subState) "")
    )
   (send-super :init)
   (setq _masterID (round __masterID))
   (setq _stateReq (string __stateReq))
   (setq _subState (string __subState))
   self)
  (:masterID
   (&optional __masterID)
   (if __masterID (setq _masterID __masterID)) _masterID)
  (:stateReq
   (&optional __stateReq)
   (if __stateReq (setq _stateReq __stateReq)) _stateReq)
  (:subState
   (&optional __subState)
   (if __subState (setq _subState __subState)) _subState)
  (:serialization-length
   ()
   (+
    ;; uint8 _masterID
    1
    ;; string _stateReq
    4 (length _stateReq)
    ;; string _subState
    4 (length _subState)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _masterID
       (write-byte _masterID s)
     ;; string _stateReq
       (write-long (length _stateReq) s) (princ _stateReq s)
     ;; string _subState
       (write-long (length _subState) s) (princ _subState s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _masterID
     (setq _masterID (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _stateReq
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _stateReq (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _subState
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _subState (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass h12pro_controller_node::srvChangePhasesResponse
  :super ros::object
  :slots (_stateRes ))

(defmethod h12pro_controller_node::srvChangePhasesResponse
  (:init
   (&key
    ((:stateRes __stateRes) 0)
    )
   (send-super :init)
   (setq _stateRes (round __stateRes))
   self)
  (:stateRes
   (&optional __stateRes)
   (if __stateRes (setq _stateRes __stateRes)) _stateRes)
  (:serialization-length
   ()
   (+
    ;; int16 _stateRes
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _stateRes
       (write-word _stateRes s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _stateRes
     (setq _stateRes (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(defclass h12pro_controller_node::srvChangePhases
  :super ros::object
  :slots ())

(setf (get h12pro_controller_node::srvChangePhases :md5sum-) "f89a7d7f1ae7501d38174856aa23b24d")
(setf (get h12pro_controller_node::srvChangePhases :datatype-) "h12pro_controller_node/srvChangePhases")
(setf (get h12pro_controller_node::srvChangePhases :request) h12pro_controller_node::srvChangePhasesRequest)
(setf (get h12pro_controller_node::srvChangePhases :response) h12pro_controller_node::srvChangePhasesResponse)

(defmethod h12pro_controller_node::srvChangePhasesRequest
  (:response () (instance h12pro_controller_node::srvChangePhasesResponse :init)))

(setf (get h12pro_controller_node::srvChangePhasesRequest :md5sum-) "f89a7d7f1ae7501d38174856aa23b24d")
(setf (get h12pro_controller_node::srvChangePhasesRequest :datatype-) "h12pro_controller_node/srvChangePhasesRequest")
(setf (get h12pro_controller_node::srvChangePhasesRequest :definition-)
      "uint8 masterID
string stateReq
string subState
---
int16 stateRes

")

(setf (get h12pro_controller_node::srvChangePhasesResponse :md5sum-) "f89a7d7f1ae7501d38174856aa23b24d")
(setf (get h12pro_controller_node::srvChangePhasesResponse :datatype-) "h12pro_controller_node/srvChangePhasesResponse")
(setf (get h12pro_controller_node::srvChangePhasesResponse :definition-)
      "uint8 masterID
string stateReq
string subState
---
int16 stateRes

")



(provide :h12pro_controller_node/srvChangePhases "f89a7d7f1ae7501d38174856aa23b24d")


