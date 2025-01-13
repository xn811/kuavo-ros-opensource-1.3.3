## 说明

  - 关于启动`load_kuavo_mujoco_sim.launch`及`load_kuavo_real.launch`时，参数`joystick_type`的选择说明

### 对于仿真
  - **参数的选择**：`load_kuavo_mujoco_sim.launch` 文件启动时参数 `joystick_type` 可选择 `h12` `bt2` `bt2pro` `sim` 分别对应h12遥控器，bt2遥控器，bt2pro遥控器和键盘控制。
    - 这里默认参数为`sim`，如果直接运行会弹出新终端用来从键盘输入运动控制指令。
    - 如果启动该launch文件时`joystick_type`参数选择了`h12`或`bt2`，可以新开一个终端，依次执行`cd kuavo-ros-control`，`sudo su`,`source devel/setup.bash`,`python3 src/kuavo_sdk/scripts/keyboard_control/robot_keyboard_control.py`，在此终端中也可以用键盘输入运动控制指令，此时遥控器和键盘均奏效。
    - 如果启动该launch文件时`joystick_type`参数选择了`bt2pro`，就不能使用键盘控制，因为json配置文件中按键映射不一致会导致键盘控制实失效，只能用遥控器控制。
  - **注意**：
    - 在`joystick_type`参数选择`sim`或选择`bt2`遥控器后新开终端运行键盘控制脚本时，机器人运动控制指令（线速度角速度）是以恒定的加速度变换（即在按动键盘后机器人运动会有一定滞后性，需要时间来把速度加到指定值）。
    - 在`joystick_type`参数选择`h12`遥控器后新开终端运行键盘控制脚本时，不会出现上一条描述的现象，这是因为`joystick_type`参数选择的不同，在launch文件内调用其他的launch文件运行的节点不同，对输入的运动控制指令的处理方式也不同导致的。

### 对于实机
  - **参数的选择**： `load_kuavo_real.launch` 文件启动时参数 `joystick_type` 可选择 `h12` `bt2` `bt2pro` `sim` 分别对应h12遥控器，bt2遥控器，bt2pro遥控器和键盘控制。
    - 这里默认参数为`bt2`，如果启动该launch文件时`joystick_type`参数选择了`h12`或`bt2`，可以新开一个终端，依次执行`cd kuavo-ros-control`，`sudo su`,`source devel/setup.bash`,`python3 src/kuavo_sdk/scripts/keyboard_control/robot_keyboard_control.py`，在此终端中也可以用键盘输入运动控制指令，此时遥控器和键盘均奏效。
    - 如果启动launch文件时`joystick_type`参数选择了`sim`，会弹出新终端用来从键盘输入运动控制指令。
    - 如果启动该launch文件时`joystick_type`参数选择了`bt2pro`，就不能使用键盘控制，因为json配置文件中按键映射不一致会导致键盘控制实失效，只能用遥控器控制。
  - **注意**：
    - 在`joystick_type`参数选择`sim`或选择`bt2`遥控器后新开终端运行键盘控制脚本时，机器人运动控制指令（线速度角速度）是以恒定的加速度变换（即在按动键盘后机器人运动会有一定滞后性，需要时间来把速度加到指定值）。
    - 在`joystick_type`参数选择`h12`遥控器后新开终端运行键盘控制脚本时，不会出现上一条描述的现象，这是因为`joystick_type`参数选择的不同，在launch文件内调用其他的launch文件运行的节点不同，对输入的运动控制指令的处理方式也不同导致的。
  - **特别**：
    - 当`joystick_type`参数不是`sim`时，不论使用上述哪种方式启动键盘控制，都不要在机器人身上插着北通手柄的接受器。