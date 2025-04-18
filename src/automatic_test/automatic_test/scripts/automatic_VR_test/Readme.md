# VR 测试说明文档
## 动作录制
- 启动机器人仿真，启动 VR
```bash
   source ~/kuavo-ros-control/devel/setup.bash
   roslaunch humanoid_controllers load_kuavo_mujoco_sim.launch 
   roslaunch noitom_hi5_hand_udp_python launch_quest3_ik.launch 
```
- 接入 VR 解锁手臂
- 运行程序，开始录制：
```python
    python3 record_bag.py
```
- 执行待测试动作，大约在 5 秒以内
- 录制完毕后，录制的 rosbag 文件在以下目录，同时脚本也会有输出：
```bash
   ~/rosbag_records/session_2025*.bag
```
## bag 拆分
- 将录制的 bag 拆分成两个待使用的bag：
1. 包含实际参考的逆解轨迹以及电机值的 bag：
```bash
    session_2025*_group1.bag
```
2. 包含 VR 发布的末端的姿态和手肘的姿态的骨骼信息
```bash
    session_2025*_group2.bag
```
- 拷贝待拆分的 rosbag 文件到当前目录：
```bash
    cp ~/rosbag_records/session_2025*.bag ./
```
- 运行脚本自动拆分
``` bash
    ./filter_bag.sh session_2025*.bag
```
- 拆分出来后的 rosbag 包保存在当前目录
## 运行测试
- 新建一个文件夹，存放 rosbag 文件
```bash
    mkdir VR_action
```
- 将 rosbag 放入其中
```bash
    mv session_2025*_group*.bag VR_action
```
- 执行 VR_test.py 文件，并选择需要执行动作的 bag 子目录
```bash
    先加载参考轨迹，选择后缀为 _group1.bag
    再加载动作轨迹，选择后缀为 _group2.bag
```
- 等待结果的计算
## 误差计算方法
1. 逆解的逐关节误差：
- 比较每一个关节的每一个逆解结果，两个值作差值，将整个逆解结果的差值进行求平方差，给出阈值，并且对比是否合格。
2. 机器人实际运动关节对比：
- 由于每一次的运动，逆解并不一定是唯一解。因此还读取了实际的关节电机读数，可参考电机是否达到目标位置。若达到目标位置，则可以认为此次测试通过。
## 阈值
- 当前测试还未能测试出较好的阈值结果，需要多测试和验证才能给出。