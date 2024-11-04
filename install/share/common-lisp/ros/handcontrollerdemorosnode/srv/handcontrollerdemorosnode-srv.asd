
(cl:in-package :asdf)

(defsystem "handcontrollerdemorosnode-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "changeHandTrackingMode" :depends-on ("_package_changeHandTrackingMode"))
    (:file "_package_changeHandTrackingMode" :depends-on ("_package"))
    (:file "controlEndHand" :depends-on ("_package_controlEndHand"))
    (:file "_package_controlEndHand" :depends-on ("_package"))
    (:file "srvArmIK" :depends-on ("_package_srvArmIK"))
    (:file "_package_srvArmIK" :depends-on ("_package"))
  ))