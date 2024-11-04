;; Auto-generated. Do not edit!


(when (boundp 'kuavo_msgs::questJoySticks)
  (if (not (find-package "KUAVO_MSGS"))
    (make-package "KUAVO_MSGS"))
  (shadow 'questJoySticks (find-package "KUAVO_MSGS")))
(unless (find-package "KUAVO_MSGS::QUESTJOYSTICKS")
  (make-package "KUAVO_MSGS::QUESTJOYSTICKS"))

(in-package "ROS")
;;//! \htmlinclude questJoySticks.msg.html


(defclass kuavo_msgs::questJoySticks
  :super ros::object
  :slots (_left_x _left_y _left_trigger _left_grip _left_first_button_pressed _left_second_button_pressed _left_first_button_touched _left_second_button_touched _right_x _right_y _right_trigger _right_grip _right_first_button_pressed _right_second_button_pressed _right_first_button_touched _right_second_button_touched ))

(defmethod kuavo_msgs::questJoySticks
  (:init
   (&key
    ((:left_x __left_x) 0.0)
    ((:left_y __left_y) 0.0)
    ((:left_trigger __left_trigger) 0.0)
    ((:left_grip __left_grip) 0.0)
    ((:left_first_button_pressed __left_first_button_pressed) nil)
    ((:left_second_button_pressed __left_second_button_pressed) nil)
    ((:left_first_button_touched __left_first_button_touched) nil)
    ((:left_second_button_touched __left_second_button_touched) nil)
    ((:right_x __right_x) 0.0)
    ((:right_y __right_y) 0.0)
    ((:right_trigger __right_trigger) 0.0)
    ((:right_grip __right_grip) 0.0)
    ((:right_first_button_pressed __right_first_button_pressed) nil)
    ((:right_second_button_pressed __right_second_button_pressed) nil)
    ((:right_first_button_touched __right_first_button_touched) nil)
    ((:right_second_button_touched __right_second_button_touched) nil)
    )
   (send-super :init)
   (setq _left_x (float __left_x))
   (setq _left_y (float __left_y))
   (setq _left_trigger (float __left_trigger))
   (setq _left_grip (float __left_grip))
   (setq _left_first_button_pressed __left_first_button_pressed)
   (setq _left_second_button_pressed __left_second_button_pressed)
   (setq _left_first_button_touched __left_first_button_touched)
   (setq _left_second_button_touched __left_second_button_touched)
   (setq _right_x (float __right_x))
   (setq _right_y (float __right_y))
   (setq _right_trigger (float __right_trigger))
   (setq _right_grip (float __right_grip))
   (setq _right_first_button_pressed __right_first_button_pressed)
   (setq _right_second_button_pressed __right_second_button_pressed)
   (setq _right_first_button_touched __right_first_button_touched)
   (setq _right_second_button_touched __right_second_button_touched)
   self)
  (:left_x
   (&optional __left_x)
   (if __left_x (setq _left_x __left_x)) _left_x)
  (:left_y
   (&optional __left_y)
   (if __left_y (setq _left_y __left_y)) _left_y)
  (:left_trigger
   (&optional __left_trigger)
   (if __left_trigger (setq _left_trigger __left_trigger)) _left_trigger)
  (:left_grip
   (&optional __left_grip)
   (if __left_grip (setq _left_grip __left_grip)) _left_grip)
  (:left_first_button_pressed
   (&optional (__left_first_button_pressed :null))
   (if (not (eq __left_first_button_pressed :null)) (setq _left_first_button_pressed __left_first_button_pressed)) _left_first_button_pressed)
  (:left_second_button_pressed
   (&optional (__left_second_button_pressed :null))
   (if (not (eq __left_second_button_pressed :null)) (setq _left_second_button_pressed __left_second_button_pressed)) _left_second_button_pressed)
  (:left_first_button_touched
   (&optional (__left_first_button_touched :null))
   (if (not (eq __left_first_button_touched :null)) (setq _left_first_button_touched __left_first_button_touched)) _left_first_button_touched)
  (:left_second_button_touched
   (&optional (__left_second_button_touched :null))
   (if (not (eq __left_second_button_touched :null)) (setq _left_second_button_touched __left_second_button_touched)) _left_second_button_touched)
  (:right_x
   (&optional __right_x)
   (if __right_x (setq _right_x __right_x)) _right_x)
  (:right_y
   (&optional __right_y)
   (if __right_y (setq _right_y __right_y)) _right_y)
  (:right_trigger
   (&optional __right_trigger)
   (if __right_trigger (setq _right_trigger __right_trigger)) _right_trigger)
  (:right_grip
   (&optional __right_grip)
   (if __right_grip (setq _right_grip __right_grip)) _right_grip)
  (:right_first_button_pressed
   (&optional (__right_first_button_pressed :null))
   (if (not (eq __right_first_button_pressed :null)) (setq _right_first_button_pressed __right_first_button_pressed)) _right_first_button_pressed)
  (:right_second_button_pressed
   (&optional (__right_second_button_pressed :null))
   (if (not (eq __right_second_button_pressed :null)) (setq _right_second_button_pressed __right_second_button_pressed)) _right_second_button_pressed)
  (:right_first_button_touched
   (&optional (__right_first_button_touched :null))
   (if (not (eq __right_first_button_touched :null)) (setq _right_first_button_touched __right_first_button_touched)) _right_first_button_touched)
  (:right_second_button_touched
   (&optional (__right_second_button_touched :null))
   (if (not (eq __right_second_button_touched :null)) (setq _right_second_button_touched __right_second_button_touched)) _right_second_button_touched)
  (:serialization-length
   ()
   (+
    ;; float32 _left_x
    4
    ;; float32 _left_y
    4
    ;; float32 _left_trigger
    4
    ;; float32 _left_grip
    4
    ;; bool _left_first_button_pressed
    1
    ;; bool _left_second_button_pressed
    1
    ;; bool _left_first_button_touched
    1
    ;; bool _left_second_button_touched
    1
    ;; float32 _right_x
    4
    ;; float32 _right_y
    4
    ;; float32 _right_trigger
    4
    ;; float32 _right_grip
    4
    ;; bool _right_first_button_pressed
    1
    ;; bool _right_second_button_pressed
    1
    ;; bool _right_first_button_touched
    1
    ;; bool _right_second_button_touched
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _left_x
       (sys::poke _left_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _left_y
       (sys::poke _left_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _left_trigger
       (sys::poke _left_trigger (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _left_grip
       (sys::poke _left_grip (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _left_first_button_pressed
       (if _left_first_button_pressed (write-byte -1 s) (write-byte 0 s))
     ;; bool _left_second_button_pressed
       (if _left_second_button_pressed (write-byte -1 s) (write-byte 0 s))
     ;; bool _left_first_button_touched
       (if _left_first_button_touched (write-byte -1 s) (write-byte 0 s))
     ;; bool _left_second_button_touched
       (if _left_second_button_touched (write-byte -1 s) (write-byte 0 s))
     ;; float32 _right_x
       (sys::poke _right_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _right_y
       (sys::poke _right_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _right_trigger
       (sys::poke _right_trigger (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _right_grip
       (sys::poke _right_grip (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _right_first_button_pressed
       (if _right_first_button_pressed (write-byte -1 s) (write-byte 0 s))
     ;; bool _right_second_button_pressed
       (if _right_second_button_pressed (write-byte -1 s) (write-byte 0 s))
     ;; bool _right_first_button_touched
       (if _right_first_button_touched (write-byte -1 s) (write-byte 0 s))
     ;; bool _right_second_button_touched
       (if _right_second_button_touched (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _left_x
     (setq _left_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _left_y
     (setq _left_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _left_trigger
     (setq _left_trigger (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _left_grip
     (setq _left_grip (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _left_first_button_pressed
     (setq _left_first_button_pressed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _left_second_button_pressed
     (setq _left_second_button_pressed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _left_first_button_touched
     (setq _left_first_button_touched (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _left_second_button_touched
     (setq _left_second_button_touched (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _right_x
     (setq _right_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _right_y
     (setq _right_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _right_trigger
     (setq _right_trigger (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _right_grip
     (setq _right_grip (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _right_first_button_pressed
     (setq _right_first_button_pressed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _right_second_button_pressed
     (setq _right_second_button_pressed (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _right_first_button_touched
     (setq _right_first_button_touched (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _right_second_button_touched
     (setq _right_second_button_touched (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get kuavo_msgs::questJoySticks :md5sum-) "c686b65cdd180a9046db651d6492ec65")
(setf (get kuavo_msgs::questJoySticks :datatype-) "kuavo_msgs/questJoySticks")
(setf (get kuavo_msgs::questJoySticks :definition-)
      "float32 left_x
float32 left_y
float32 left_trigger
float32 left_grip
bool left_first_button_pressed
bool left_second_button_pressed
bool left_first_button_touched
bool left_second_button_touched
float32 right_x
float32 right_y
float32 right_trigger
float32 right_grip
bool right_first_button_pressed
bool right_second_button_pressed
bool right_first_button_touched
bool right_second_button_touched

")



(provide :kuavo_msgs/questJoySticks "c686b65cdd180a9046db651d6492ec65")


