;; Auto-generated. Do not edit!


(when (boundp 'h12pro_controller_node::walkCommand)
  (if (not (find-package "H12PRO_CONTROLLER_NODE"))
    (make-package "H12PRO_CONTROLLER_NODE"))
  (shadow 'walkCommand (find-package "H12PRO_CONTROLLER_NODE")))
(unless (find-package "H12PRO_CONTROLLER_NODE::WALKCOMMAND")
  (make-package "H12PRO_CONTROLLER_NODE::WALKCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude walkCommand.msg.html


(defclass h12pro_controller_node::walkCommand
  :super ros::object
  :slots (_mode _values ))

(defmethod h12pro_controller_node::walkCommand
  (:init
   (&key
    ((:mode __mode) 0)
    ((:values __values) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _mode (round __mode))
   (setq _values __values)
   self)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:values
   (&optional __values)
   (if __values (setq _values __values)) _values)
  (:serialization-length
   ()
   (+
    ;; uint8 _mode
    1
    ;; float64[] _values
    (* 8    (length _values)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _mode
       (write-byte _mode s)
     ;; float64[] _values
     (write-long (length _values) s)
     (dotimes (i (length _values))
       (sys::poke (elt _values i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _mode
     (setq _mode (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; float64[] _values
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _values (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _values i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get h12pro_controller_node::walkCommand :md5sum-) "5b32312c0e7618ca6c317ce9272f2ca7")
(setf (get h12pro_controller_node::walkCommand :datatype-) "h12pro_controller_node/walkCommand")
(setf (get h12pro_controller_node::walkCommand :definition-)
      "# mode: 0->PositionCommand | 1->VelocityCommand
uint8 mode
float64[] values

")



(provide :h12pro_controller_node/walkCommand "5b32312c0e7618ca6c317ce9272f2ca7")


