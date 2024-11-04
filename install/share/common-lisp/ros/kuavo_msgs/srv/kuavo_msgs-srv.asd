
(cl:in-package :asdf)

(defsystem "kuavo_msgs-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :kuavo_msgs-msg
)
  :components ((:file "_package")
    (:file "changeArmCtrlMode" :depends-on ("_package_changeArmCtrlMode"))
    (:file "_package_changeArmCtrlMode" :depends-on ("_package"))
    (:file "changeTorsoCtrlMode" :depends-on ("_package_changeTorsoCtrlMode"))
    (:file "_package_changeTorsoCtrlMode" :depends-on ("_package"))
    (:file "jointMoveTo" :depends-on ("_package_jointMoveTo"))
    (:file "_package_jointMoveTo" :depends-on ("_package"))
    (:file "setHwIntialState" :depends-on ("_package_setHwIntialState"))
    (:file "_package_setHwIntialState" :depends-on ("_package"))
    (:file "singleStepControl" :depends-on ("_package_singleStepControl"))
    (:file "_package_singleStepControl" :depends-on ("_package"))
  ))