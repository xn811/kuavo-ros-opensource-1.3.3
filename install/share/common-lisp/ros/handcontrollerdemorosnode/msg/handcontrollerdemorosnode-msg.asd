
(cl:in-package :asdf)

(defsystem "handcontrollerdemorosnode-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "armPoseWithTimeStamp" :depends-on ("_package_armPoseWithTimeStamp"))
    (:file "_package_armPoseWithTimeStamp" :depends-on ("_package"))
    (:file "handRotationEular" :depends-on ("_package_handRotationEular"))
    (:file "_package_handRotationEular" :depends-on ("_package"))
    (:file "robotArmPose" :depends-on ("_package_robotArmPose"))
    (:file "_package_robotArmPose" :depends-on ("_package"))
    (:file "robotHandPosition" :depends-on ("_package_robotHandPosition"))
    (:file "_package_robotHandPosition" :depends-on ("_package"))
  ))