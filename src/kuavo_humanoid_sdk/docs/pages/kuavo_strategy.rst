.. _kuavo-strategy:
.. include:: components/tips_launch_kuavo.rst

********
策略模块
********
原子技能层级
====================================================
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy

.. autoclass:: kuavo_humanoid_sdk.KuavoRobot
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

.. autoclass:: KuavoRobotVision
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:
    
.. autoclass:: KuavoRobotState
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:


.. autoclass:: KuavoRobotTools
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:
    
基础策略接口
====================
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy.kuavo_strategy.KuavoRobotStrategyBase
    :members:
    :undoc-members:
    :show-inheritance:

箱子抓取策略
====================
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy.grasp_box

箱子信息数据结构
------------------------
.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy.BoxInfo
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

箱子抓取策略类
------------------------
.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy.grasp_box.grasp_box_strategy.KuavoGraspBox
    :members:
    :undoc-members:
    :show-inheritance:

使用示例
============

以下是一个使用箱子抓取策略的基本示例:

.. literalinclude:: ../../examples/strategies/grasp_box_example.py
  :language: python