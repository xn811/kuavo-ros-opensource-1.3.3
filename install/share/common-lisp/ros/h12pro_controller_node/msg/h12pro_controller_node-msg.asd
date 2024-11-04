
(cl:in-package :asdf)

(defsystem "h12pro_controller_node-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "ECJointMotordata" :depends-on ("_package_ECJointMotordata"))
    (:file "_package_ECJointMotordata" :depends-on ("_package"))
    (:file "h12proRemoteControllerChannel" :depends-on ("_package_h12proRemoteControllerChannel"))
    (:file "_package_h12proRemoteControllerChannel" :depends-on ("_package"))
    (:file "robotPhase" :depends-on ("_package_robotPhase"))
    (:file "_package_robotPhase" :depends-on ("_package"))
    (:file "robotQVTau" :depends-on ("_package_robotQVTau"))
    (:file "_package_robotQVTau" :depends-on ("_package"))
    (:file "robotTorsoState" :depends-on ("_package_robotTorsoState"))
    (:file "_package_robotTorsoState" :depends-on ("_package"))
    (:file "walkCommand" :depends-on ("_package_walkCommand"))
    (:file "_package_walkCommand" :depends-on ("_package"))
  ))