
(cl:in-package :asdf)

(defsystem "noitom_hi5_hand_udp_python-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "JoySticks" :depends-on ("_package_JoySticks"))
    (:file "_package_JoySticks" :depends-on ("_package"))
    (:file "PoseInfo" :depends-on ("_package_PoseInfo"))
    (:file "_package_PoseInfo" :depends-on ("_package"))
    (:file "PoseInfoList" :depends-on ("_package_PoseInfoList"))
    (:file "_package_PoseInfoList" :depends-on ("_package"))
    (:file "QuaternionArray" :depends-on ("_package_QuaternionArray"))
    (:file "_package_QuaternionArray" :depends-on ("_package"))
    (:file "Vector4" :depends-on ("_package_Vector4"))
    (:file "_package_Vector4" :depends-on ("_package"))
    (:file "handRotation" :depends-on ("_package_handRotation"))
    (:file "_package_handRotation" :depends-on ("_package"))
    (:file "handRotationEular" :depends-on ("_package_handRotationEular"))
    (:file "_package_handRotationEular" :depends-on ("_package"))
  ))