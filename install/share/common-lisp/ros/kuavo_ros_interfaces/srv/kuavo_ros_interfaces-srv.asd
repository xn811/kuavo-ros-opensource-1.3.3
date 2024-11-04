
(cl:in-package :asdf)

(defsystem "kuavo_ros_interfaces-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :kuavo_ros_interfaces-msg
)
  :components ((:file "_package")
    (:file "ocs2ChangeArmCtrlMode" :depends-on ("_package_ocs2ChangeArmCtrlMode"))
    (:file "_package_ocs2ChangeArmCtrlMode" :depends-on ("_package"))
    (:file "planArmTrajectoryBezierCurve" :depends-on ("_package_planArmTrajectoryBezierCurve"))
    (:file "_package_planArmTrajectoryBezierCurve" :depends-on ("_package"))
    (:file "stopPlanArmTrajectory" :depends-on ("_package_stopPlanArmTrajectory"))
    (:file "_package_stopPlanArmTrajectory" :depends-on ("_package"))
  ))