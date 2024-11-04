
(cl:in-package :asdf)

(defsystem "kuavo_ros_interfaces-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "armTargetPoses" :depends-on ("_package_armTargetPoses"))
    (:file "_package_armTargetPoses" :depends-on ("_package"))
    (:file "bezierCurveCubicPoint" :depends-on ("_package_bezierCurveCubicPoint"))
    (:file "_package_bezierCurveCubicPoint" :depends-on ("_package"))
    (:file "jointBezierTrajectory" :depends-on ("_package_jointBezierTrajectory"))
    (:file "_package_jointBezierTrajectory" :depends-on ("_package"))
    (:file "planArmState" :depends-on ("_package_planArmState"))
    (:file "_package_planArmState" :depends-on ("_package"))
    (:file "robotHandPosition" :depends-on ("_package_robotHandPosition"))
    (:file "_package_robotHandPosition" :depends-on ("_package"))
    (:file "robotHeadMotionData" :depends-on ("_package_robotHeadMotionData"))
    (:file "_package_robotHeadMotionData" :depends-on ("_package"))
  ))