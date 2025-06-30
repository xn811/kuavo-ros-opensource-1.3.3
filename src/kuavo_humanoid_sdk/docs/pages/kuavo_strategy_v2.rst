.. _kuavo-strategy-v2:

***************
策略模块 v2
***************

概述
==========================
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2

策略模块 v2 是 kuavo_humanoid_sdk 的升级版本，提供了更模块化和事件驱动的策略编写框架。

核心组件
====================

机器人SDK
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.robot_sdk

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.robot_sdk.RobotSDK
    :members:
    :undoc-members:
    :show-inheritance:

数据类型
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type.Frame
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type.Point
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type.Pose
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type.Tag
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.data_type.Transform3D
    :members:
    :undoc-members:
    :show-inheritance:

事件系统
====================

基础事件
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.base_event

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.base_event.EventStatus
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.base_event.BaseEvent
    :members:
    :undoc-members:
    :show-inheritance:

移动操作事件
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.mobile_manipulate

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.mobile_manipulate.head_events.EventPercep
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.mobile_manipulate.head_events.EventHeadMoveKeyPoint
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.mobile_manipulate.walk_events.EventWalkToPose
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.common.events.mobile_manipulate.arm_events.EventArmMoveKeyPoint
    :members:
    :undoc-members:
    :show-inheritance:

工具类
====================

日志工具
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.utils

.. autoclass:: kuavo_humanoid_sdk.kuavo_strategy_v2.utils.logger_setup.Logger
    :members:
    :undoc-members:
    :show-inheritance:

策略函数
====================

箱子抓取策略
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.search_tag_with_head

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.walk_approach_target_with_perception_loop

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.move_arm_and_backward

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.grab_box_and_backward

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.place_box_and_backward

.. autofunction:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.strategy.return_to_idle

配置模块
====================

仿真配置
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.configs.config_sim

.. automodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.configs.config_sim
    :members:
    :undoc-members:
    :show-inheritance:

实物配置
------------------------
.. currentmodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.configs.config_real

.. automodule:: kuavo_humanoid_sdk.kuavo_strategy_v2.pick_place_box.configs.config_real
    :members:
    :undoc-members:
    :show-inheritance:

使用示例
============

以下是一个使用策略模块 v2 的基本示例:

仿真运行
--------------

准备
^^^^^^^^^^^^

在运行仿真场景前需要确保配置正确。

编译
^^^^^^^^^^^^

确保所有相关功能包已编译:

.. code-block:: bash

    catkin build kuavo_humanoid_sdk

运行
^^^^^^^^^^^^

启动仿真环境:

.. code-block:: bash

    # 启动仿真场景
    source devel/setup.bash
    roslaunch kuavo_humanoid_sdk start_simulation.launch

运行搬箱子示例:

.. code-block:: bash

    cd src/kuavo_humanoid_sdk/examples/strategies_v2
    python3 grasp_box_example_v2.py --sim

实物运行
--------------

准备
^^^^^^^^^^^^

确保所有硬件连接正确，并已进行必要的标定。

**零点标定** !! 非常重要 !!

执行零点标定工具:

.. code-block:: bash

    sudo su
    ./scripts/joint_cali/One_button_start.sh

目录结构
============

.. toctree::
   :maxdepth: 2
   :caption: 目录

文件
----

- why_v2.md: 解释为什么使用 v2 版本。
- README.md: 项目的简要介绍。

目录
----

- **pick_place_box**: 包含与抓取和放置相关的策略。
- **resource**: 存储资源文件。
- **utils**: 实用工具和辅助函数。
- **common**: 通用模块和共享代码。
- **log**: 日志文件和记录。
