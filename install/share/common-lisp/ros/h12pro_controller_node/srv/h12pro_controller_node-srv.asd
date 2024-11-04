
(cl:in-package :asdf)

(defsystem "h12pro_controller_node-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "changeAMBACCtrlMode" :depends-on ("_package_changeAMBACCtrlMode"))
    (:file "_package_changeAMBACCtrlMode" :depends-on ("_package"))
    (:file "changeArmCtrlMode" :depends-on ("_package_changeArmCtrlMode"))
    (:file "_package_changeArmCtrlMode" :depends-on ("_package"))
    (:file "changeHandArmPosesByConfigName" :depends-on ("_package_changeHandArmPosesByConfigName"))
    (:file "_package_changeHandArmPosesByConfigName" :depends-on ("_package"))
    (:file "srvChangePhases" :depends-on ("_package_srvChangePhases"))
    (:file "_package_srvChangePhases" :depends-on ("_package"))
    (:file "srvClearPositionCMD" :depends-on ("_package_srvClearPositionCMD"))
    (:file "_package_srvClearPositionCMD" :depends-on ("_package"))
    (:file "srvchangeCtlMode" :depends-on ("_package_srvchangeCtlMode"))
    (:file "_package_srvchangeCtlMode" :depends-on ("_package"))
  ))