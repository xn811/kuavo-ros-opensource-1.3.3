
(cl:in-package :asdf)

(defsystem "humanoid_interface_ros-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "uwbdebug" :depends-on ("_package_uwbdebug"))
    (:file "_package_uwbdebug" :depends-on ("_package"))
  ))