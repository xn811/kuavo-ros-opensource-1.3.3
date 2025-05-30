.. _examples:

************
使用示例
************
.. include:: components/tips_launch_kuavo.rst

机器人信息
===========
这个示例展示了如何获取机器人的基本信息。

.. literalinclude:: ../../examples/atomic_skills/robot_info_example.py
  :language: python

基础机器人控制
==============
这个示例展示了如何初始化 SDK 并控制机器人的运动。

.. literalinclude:: ../../examples/atomic_skills/motion_example.py
  :language: python

末端执行器控制
==============

LejuClaw 夹爪
--------------
这个示例展示了如何控制夹爪，包括位置、速度和力矩控制。

.. literalinclude:: ../../examples/atomic_skills/lejuclaw_example.py
  :language: python

Qiangnao 灵巧手
----------------
这个示例展示了如何控制灵巧手/触觉灵巧手。

.. literalinclude:: ../../examples/atomic_skills/dexhand_example.py
  :language: python

手臂控制
========
这个示例展示了如何控制机器人手臂运动，包括轨迹控制和目标姿态控制。

.. literalinclude:: ../../examples/atomic_skills/ctrl_arm_example.py
  :language: python

正向和逆向运动学控制
====================
这个示例展示了如何使用正向运动学 (FK) 从关节角度计算末端执行器位置，以及如何使用逆向运动学 (IK) 计算实现所需末端执行器姿态所需的关节角度。

.. literalinclude:: ../../examples/atomic_skills/arm_ik_example.py
  :language: python

头部控制
========
这个示例展示了如何控制机器人头部运动，包括点头 (pitch) 和摇头 (yaw) 运动。

.. literalinclude:: ../../examples/atomic_skills/ctrl_head_example.py
  :language: python

单步控制
========
这个示例展示了如何逐步控制机器人的运动，包括单脚的放置和轨迹控制。

.. literalinclude:: ../../examples/atomic_skills/step_control_example.py
  :language: python