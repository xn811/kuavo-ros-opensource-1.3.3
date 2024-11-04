;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::h12proRemoteControllerChannel)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'h12proRemoteControllerChannel (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::H12PROREMOTECONTROLLERCHANNEL")
  (make-package "H12PRO_CONTROLLER_NODE::H12PROREMOTECONTROLLERCHANNEL"))

(in-package "ROS")
;;//! \htmlinclude h12proRemoteControllerChannel.msg.html


(defclass h12pro_controller_node::h12proRemoteControllerChannel
  :super ros::object
  :slots (_channels _sbus_state ))

(defmethod h12pro_controller_node::h12proRemoteControllerChannel
  (:init
   (&key
    ((:channels __channels) (make-array 0 :initial-element 0 :element-type :integer))
    ((:sbus_state __sbus_state) 0)
    )
   (send-super :init)
   (setq _channels __channels)
   (setq _sbus_state (round __sbus_state))
   self)
  (:channels
   (&optional __channels)
   (if __channels (setq _channels __channels)) _channels)
  (:sbus_state
   (&optional __sbus_state)
   (if __sbus_state (setq _sbus_state __sbus_state)) _sbus_state)
  (:serialization-length
   ()
   (+
    ;; uint16[] _channels
    (* 2    (length _channels)) 4
    ;; uint8 _sbus_state
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16[] _channels
     (write-long (length _channels) s)
     (dotimes (i (length _channels))
       (write-word (elt _channels i) s)
       )
     ;; uint8 _sbus_state
       (write-byte _sbus_state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16[] _channels
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _channels (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _channels i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;; uint8 _sbus_state
     (setq _sbus_state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get h12pro_controller_node::h12proRemoteControllerChannel :md5sum-) "fbc04b5769be8336707a1083b8b107dd")
(setf (get h12pro_controller_node::h12proRemoteControllerChannel :datatype-) "h12pro_controller_node/h12proRemoteControllerChannel")
(setf (get h12pro_controller_node::h12proRemoteControllerChannel :definition-)
      "uint16[] channels
uint8 sbus_state
")



(provide :h12pro_controller_node/h12proRemoteControllerChannel "fbc04b5769be8336707a1083b8b107dd")


