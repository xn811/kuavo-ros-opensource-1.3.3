;; Auto-generated. Do not edit!


(when (boundp 'motion_capture_ik::ikSolveParam)
  (if (not (find-package "MOTION_CAPTURE_IK"))
    (make-package "MOTION_CAPTURE_IK"))
  (shadow 'ikSolveParam (find-package "MOTION_CAPTURE_IK")))
(unless (find-package "MOTION_CAPTURE_IK::IKSOLVEPARAM")
  (make-package "MOTION_CAPTURE_IK::IKSOLVEPARAM"))

(in-package "ROS")
;;//! \htmlinclude ikSolveParam.msg.html


(defclass motion_capture_ik::ikSolveParam
  :super ros::object
  :slots (_major_optimality_tol _major_feasibility_tol _minor_feasibility_tol _major_iterations_limit _oritation_constraint_tol _pos_constraint_tol _pos_cost_weight ))

(defmethod motion_capture_ik::ikSolveParam
  (:init
   (&key
    ((:major_optimality_tol __major_optimality_tol) 0.0)
    ((:major_feasibility_tol __major_feasibility_tol) 0.0)
    ((:minor_feasibility_tol __minor_feasibility_tol) 0.0)
    ((:major_iterations_limit __major_iterations_limit) 0.0)
    ((:oritation_constraint_tol __oritation_constraint_tol) 0.0)
    ((:pos_constraint_tol __pos_constraint_tol) 0.0)
    ((:pos_cost_weight __pos_cost_weight) 0.0)
    )
   (send-super :init)
   (setq _major_optimality_tol (float __major_optimality_tol))
   (setq _major_feasibility_tol (float __major_feasibility_tol))
   (setq _minor_feasibility_tol (float __minor_feasibility_tol))
   (setq _major_iterations_limit (float __major_iterations_limit))
   (setq _oritation_constraint_tol (float __oritation_constraint_tol))
   (setq _pos_constraint_tol (float __pos_constraint_tol))
   (setq _pos_cost_weight (float __pos_cost_weight))
   self)
  (:major_optimality_tol
   (&optional __major_optimality_tol)
   (if __major_optimality_tol (setq _major_optimality_tol __major_optimality_tol)) _major_optimality_tol)
  (:major_feasibility_tol
   (&optional __major_feasibility_tol)
   (if __major_feasibility_tol (setq _major_feasibility_tol __major_feasibility_tol)) _major_feasibility_tol)
  (:minor_feasibility_tol
   (&optional __minor_feasibility_tol)
   (if __minor_feasibility_tol (setq _minor_feasibility_tol __minor_feasibility_tol)) _minor_feasibility_tol)
  (:major_iterations_limit
   (&optional __major_iterations_limit)
   (if __major_iterations_limit (setq _major_iterations_limit __major_iterations_limit)) _major_iterations_limit)
  (:oritation_constraint_tol
   (&optional __oritation_constraint_tol)
   (if __oritation_constraint_tol (setq _oritation_constraint_tol __oritation_constraint_tol)) _oritation_constraint_tol)
  (:pos_constraint_tol
   (&optional __pos_constraint_tol)
   (if __pos_constraint_tol (setq _pos_constraint_tol __pos_constraint_tol)) _pos_constraint_tol)
  (:pos_cost_weight
   (&optional __pos_cost_weight)
   (if __pos_cost_weight (setq _pos_cost_weight __pos_cost_weight)) _pos_cost_weight)
  (:serialization-length
   ()
   (+
    ;; float64 _major_optimality_tol
    8
    ;; float64 _major_feasibility_tol
    8
    ;; float64 _minor_feasibility_tol
    8
    ;; float64 _major_iterations_limit
    8
    ;; float64 _oritation_constraint_tol
    8
    ;; float64 _pos_constraint_tol
    8
    ;; float64 _pos_cost_weight
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _major_optimality_tol
       (sys::poke _major_optimality_tol (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _major_feasibility_tol
       (sys::poke _major_feasibility_tol (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _minor_feasibility_tol
       (sys::poke _minor_feasibility_tol (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _major_iterations_limit
       (sys::poke _major_iterations_limit (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _oritation_constraint_tol
       (sys::poke _oritation_constraint_tol (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pos_constraint_tol
       (sys::poke _pos_constraint_tol (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pos_cost_weight
       (sys::poke _pos_cost_weight (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _major_optimality_tol
     (setq _major_optimality_tol (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _major_feasibility_tol
     (setq _major_feasibility_tol (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _minor_feasibility_tol
     (setq _minor_feasibility_tol (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _major_iterations_limit
     (setq _major_iterations_limit (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _oritation_constraint_tol
     (setq _oritation_constraint_tol (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pos_constraint_tol
     (setq _pos_constraint_tol (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pos_cost_weight
     (setq _pos_cost_weight (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get motion_capture_ik::ikSolveParam :md5sum-) "be29d8b02ad14da680464b8c4f590f98")
(setf (get motion_capture_ik::ikSolveParam :datatype-) "motion_capture_ik/ikSolveParam")
(setf (get motion_capture_ik::ikSolveParam :definition-)
      "# snopt params
float64 major_optimality_tol
float64 major_feasibility_tol
float64 minor_feasibility_tol
float64 major_iterations_limit
# constraint and cost params
float64 oritation_constraint_tol
float64 pos_constraint_tol # work when pos_cost_weight > 0.0
float64 pos_cost_weight
")



(provide :motion_capture_ik/ikSolveParam "be29d8b02ad14da680464b8c4f590f98")


