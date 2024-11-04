;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::robotPhase)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'robotPhase (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::ROBOTPHASE")
  (make-package "H12PRO_CONTROLLER_NODE::ROBOTPHASE"))

(in-package "ROS")
;;//! \htmlinclude robotPhase.msg.html


(defclass h12pro_controller_node::robotPhase
  :super ros::object
  :slots (_mainPhase _subPhase ))

(defmethod h12pro_controller_node::robotPhase
  (:init
   (&key
    ((:mainPhase __mainPhase) 0)
    ((:subPhase __subPhase) 0)
    )
   (send-super :init)
   (setq _mainPhase (round __mainPhase))
   (setq _subPhase (round __subPhase))
   self)
  (:mainPhase
   (&optional __mainPhase)
   (if __mainPhase (setq _mainPhase __mainPhase)) _mainPhase)
  (:subPhase
   (&optional __subPhase)
   (if __subPhase (setq _subPhase __subPhase)) _subPhase)
  (:serialization-length
   ()
   (+
    ;; uint8 _mainPhase
    1
    ;; uint8 _subPhase
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _mainPhase
       (write-byte _mainPhase s)
     ;; uint8 _subPhase
       (write-byte _subPhase s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _mainPhase
     (setq _mainPhase (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _subPhase
     (setq _subPhase (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get h12pro_controller_node::robotPhase :md5sum-) "26cd19545acfae4dd7729b92456b2c32")
(setf (get h12pro_controller_node::robotPhase :datatype-) "h12pro_controller_node/robotPhase")
(setf (get h12pro_controller_node::robotPhase :definition-)
      "uint8 mainPhase
uint8 subPhase
")



(provide :h12pro_controller_node/robotPhase "26cd19545acfae4dd7729b92456b2c32")


