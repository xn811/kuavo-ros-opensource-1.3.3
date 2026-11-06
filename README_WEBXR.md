# Kuavo v49 普通场景 WebXR 半身遥操

本说明用于 Kuavo ROS Noetic 工作区中的普通 v49 MuJoCo 半身场景。通过 Quest 浏览器手部追踪控制机器人，不包含相机数采或录包流程。咖啡杯场景在后续提交中另有说明。

## 使用前准备

- 将 `quest_webxr_bridge` 放在 `src/manipulation_nodes/quest_webxr_bridge`，并准备好原仓库所需的 ROS Noetic、MuJoCo、Drake 和编译环境。
- Quest 与运行 ROS 的电脑需要网络互通；允许 Quest 访问 TCP 8012。准备 Quest 浏览器信任的 HTTPS 证书和私钥，不要把私钥提交到仓库。
- 下面把工作区路径记作 `KUAVO_WS`。在每个终端将示例路径替换成自己的工作区；如果使用容器，使用容器内的路径。容器名、证书路径和 IP 均以现场配置为准。
- 每个启动仿真或桥接的终端都设置 `ROBOT_VERSION=49`。桥接的动作预检还要求 `/only_half_up_body=true`。

### 首次安装与编译

在已有 Kuavo 依赖的环境中，先按原仓库说明编译基础系统，再编译桥接包。例如：

```bash
export KUAVO_WS=/path/to/kuavo-ros-opensource-1.3.3
cd "$KUAVO_WS"
source /opt/ros/noetic/setup.bash
source installed/setup.bash
export ROBOT_VERSION=49

catkin config -DCMAKE_ASM_COMPILER=/usr/bin/as -DCMAKE_BUILD_TYPE=Release
catkin build humanoid_controllers
python3 -m venv --system-site-packages .venv-webxr
source .venv-webxr/bin/activate
python -m pip install -r src/manipulation_nodes/quest_webxr_bridge/requirements.txt
catkin build quest_webxr_bridge motion_capture_ik
source devel/setup.bash
```

上面使用源码工作区的 `devel` 空间。根据主机环境配置 Drake 的库和 Python 搜索路径；环境依赖以原仓库安装说明为准。

## 终端一：普通 v49 半身仿真

如果使用 Docker，先进入已经配置好的 Kuavo 容器，然后在容器内执行：

```bash
export KUAVO_WS=/path/to/kuavo-ros-opensource-1.3.3
cd "$KUAVO_WS"
source /opt/ros/noetic/setup.bash
source installed/setup.bash
source devel/setup.bash
export ROBOT_VERSION=49

roslaunch humanoid_controllers load_kuavo_mujoco_sim.launch \
  only_half_up_body:=true \
  with_ik:=false with_mm_ik:=false vr_remote_control:=false
```

等待 MuJoCo 加载、机器人稳定且未暂停，保持终端运行。不要同时启动原有 `*_with_vr.launch`、`quest3_node.py` 或另一套 IK/手臂控制源。

## 终端二：WebXR 桥接

进入与终端一相同的 ROS 环境。将证书路径改成实际的绝对路径：

```bash
export KUAVO_WS=/path/to/kuavo-ros-opensource-1.3.3
cd "$KUAVO_WS"
source /opt/ros/noetic/setup.bash
source installed/setup.bash
source devel/setup.bash
source .venv-webxr/bin/activate
export ROBOT_VERSION=49
export WEBXR_PYTHON="$KUAVO_WS/.venv-webxr/bin/python3"

roslaunch quest_webxr_bridge quest_webxr_bridge.launch \
  cert_file:=/absolute/path/to/cert.pem \
  key_file:=/absolute/path/to/key.pem \
  enable_output:=false enable_head:=false \
  start_ik:=true quest_compatible_ik:=true
```

启动时桥接会锁存一次头部 `[0, +25]` 度的低头命令；`enable_head:=false` 关闭之后的头显动态跟随，不取消初始命令。手臂自动动作需要后续启动手势和预检。

在同一 ROS 环境另开终端，可检查：

```bash
rosparam get /only_half_up_body
rostopic info /kuavo_arm_traj
rostopic echo -n 1 /quest_webxr_kuavo_bridge/status
rosnode list | grep -E 'quest_webxr_kuavo_bridge|quest_webxr_control_contract_adapter|ik_ros_uni|arms_ik_node|quest3_node'
```

半身参数应为 `true`。应有桥接器、适配器和一个 `ik_ros_uni`，不要有另一套 `arms_ik_node` 或 `quest3_node`；正式手臂话题应由 WebXR 适配器独占。发现冲突时先停止冲突节点。

## Quest 操作

1. 关闭旧的 WebXR 标签页，在 Quest 浏览器打开 `https://<电脑IP>:8012`，按浏览器提示处理可信证书并允许手部追踪。用手柄点击 **Enter VR**，再切换到手部追踪。
2. 双手进入视野并保持稳定。确认周围安全后，双手张开、掌心向上保持 5 秒，再释放手势 1 秒。
3. 预检通过后机器人依次执行 `T → T_BENT → L`。动作期间保持距离；到达 L 后模仿机器人姿态并保持稳定，等待 3 秒对齐、标定和 IK 连贯性检查。只有显示 `ACTIVE` 后才开始小幅遥操。
4. 先分别小幅验证双手前后、左右、上下、手腕和手指，再进行任务。追踪丢失或安全限制出现时，查看头显和终端状态；不要通过重复手势强行绕过故障。
5. 双手握拳 3 秒暂停。暂停后掌心向上 5 秒可请求回 L 重新标定；完全退出需双手捏合 2 秒、释放 1 秒，再双手握拳 3 秒确认，等待机器人经 L、T_BENT、T 返回 HOME。之后停止桥接和仿真终端。

详细提示、恢复条件与故障处理见 [HUD 说明](src/manipulation_nodes/quest_webxr_bridge/docs/headset_hud_zh.md)。

## 真机限制

当前启动预检对真机同样要求桥接终端 `ROBOT_VERSION=49` 和 `/only_half_up_body=true`。必须由现场人员确认机器人实际的半身控制配置、驱动、反馈、TF、服务和唯一命令源均适用；设置 ROS 参数本身不等于确认真机安全。配置中的跟随误差参数用于 MuJoCo 抓取试验，转移真机前需要重新审查。先完成仿真验证，保留原有保护并确保现场急停可用；此说明不构成真机验证。
