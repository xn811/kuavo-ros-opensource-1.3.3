import os
import sys
import rospy
import rosbag
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from sensor_msgs.msg import JointState
import argparse
from rich.console import Console
import questionary
from kuavo_msgs.msg import sensorsData
from std_msgs.msg import Bool
import threading
import subprocess
from kuavo_msgs.srv import changeArmCtrlMode, changeArmCtrlModeRequest, changeArmCtrlModeResponse
console = Console()

class TrajectoryValidator:
    def __init__(self):
        self.reference_joint_states = []
        self.actual_joint_states = []
        self.joint_names = []
        self.time_reference = []
        self.time_actual = []
        self.is_recording = False
        self.start_time = None
        self.recording_sub = rospy.Subscriber('/recording_status', Bool, self.recording_callback)
        
        # 增加逆解轨迹相关变量
        self.reference_ik_trajectory = []
        self.actual_ik_trajectory = []
        self.time_reference_ik = []
        self.time_actual_ik = []
        
        # 存储多次运行的实际轨迹数据
        self.multiple_runs_trajectories = []  # 存储每次运行的实际关节状态
        self.multiple_runs_times = []         # 存储每次运行的时间戳
        self.multiple_runs_ik_trajectories = []  # 存储每次运行的逆解轨迹
        self.multiple_runs_ik_times = []         # 存储每次运行的逆解轨迹时间戳
        
    def load_reference_bag(self, reference_bag_path):
        """加载参考轨迹的rosbag文件"""
        console.print(f"[blue]加载参考轨迹: {reference_bag_path}[/blue]")
        try:
            bag = rosbag.Bag(reference_bag_path)
            for topic, msg, t in tqdm(bag.read_messages(topics=['/sensors_data_raw', '/kuavo_arm_traj']), desc="加载参考轨迹"):
                if topic == '/sensors_data_raw':
                    if not self.joint_names and hasattr(msg, 'joint_data') and hasattr(msg.joint_data, 'joint_name'):
                        self.joint_names = msg.joint_data.joint_name
                        console.print(f"[green]成功设置joint_names，共 {len(self.joint_names)} 个关节[/green]")
                    
                    if hasattr(msg, 'joint_data') and hasattr(msg.joint_data, 'joint_q'):
                        # 只关心第12~25个数据（手臂电机数据）
                        arm_joint_data = msg.joint_data.joint_q[12:26]
                        self.reference_joint_states.append(arm_joint_data)
                        self.time_reference.append(t.to_sec())
                elif topic == '/kuavo_arm_traj':
                    # 记录逆解轨迹数据
                    self.reference_ik_trajectory.append(msg)
                    self.time_reference_ik.append(t.to_sec())
            bag.close()
            console.print(f"[green]成功加载参考轨迹，共 {len(self.reference_joint_states)} 个关节数据点[/green]")
            console.print(f"[green]成功加载参考逆解轨迹，共 {len(self.reference_ik_trajectory)} 个数据点[/green]")
            return True
        except Exception as e:
            console.print(f"[red]加载参考轨迹失败: {str(e)}[/red]")
            return False
    
    def recording_callback(self, msg):
        """接收录制状态的回调函数"""
        # 如果录制状态为False（0），等待0.5秒
        self.is_recording = msg.data
        if self.is_recording and not self.start_time:
            self.start_time = rospy.Time.now()
            console.print("[green]开始记录实际关节状态...[/green]")
        elif not self.is_recording:
            console.print("[green]停止记录实际关节状态[/green]")
    
    def joint_state_callback(self, msg):
        """接收实际关节状态的回调函数"""
        if self.is_recording:
            if not self.start_time:
                self.start_time = rospy.Time.now()
            
            current_time = rospy.Time.now()
            elapsed_time = (current_time - self.start_time).to_sec()
            
            # 只关心第12~25个数据（手臂电机数据）
            arm_joint_data = msg.joint_data.joint_q[12:26]
            self.actual_joint_states.append(arm_joint_data)
            self.time_actual.append(elapsed_time)
    
    def ik_trajectory_callback(self, msg):
        """接收实际逆解轨迹的回调函数"""
        if self.is_recording:
            if not self.start_time:
                self.start_time = rospy.Time.now()
            
            current_time = rospy.Time.now()
            elapsed_time = (current_time - self.start_time).to_sec()
            
            self.actual_ik_trajectory.append(msg)
            self.time_actual_ik.append(elapsed_time)

    
    def play_trajectory_bag(self, trajectory_bag_path):
        """播放轨迹指令的rosbag文件"""
        console.print(f"[blue]播放轨迹指令: {trajectory_bag_path}[/blue]")
        
        # 订阅关节状态
        rospy.Subscriber('/sensors_data_raw', sensorsData, self.joint_state_callback)
        # 订阅逆解轨迹
        rospy.Subscriber('/kuavo_arm_traj', JointState, self.ik_trajectory_callback)
        
        # 开始记录
        self.is_recording = False  # 初始状态为不记录
        self.start_time = None
        self.actual_joint_states = []
        self.time_actual = []
        self.actual_ik_trajectory = []
        self.time_actual_ik = []
        
        # 使用subprocess播放rosbag
        try:
            # 启动rosbag播放进程
            process = subprocess.Popen(["rosbag", "play", trajectory_bag_path])
            
            # 等待rosbag开始播放
            console.print("[green]等待rosbag开始播放...[/green]")
            rospy.sleep(0.6)  # 等待rosbag初始化
            
            # 等待rosbag播放完成
            process.wait()
            
            console.print(f"[green]轨迹播放完成，记录了 {len(self.actual_joint_states)} 个实际关节状态[/green]")
            console.print(f"[green]轨迹播放完成，记录了 {len(self.actual_ik_trajectory)} 个实际逆解轨迹点[/green]")
            
            # 保存当前运行的轨迹数据
            if self.actual_joint_states and self.time_actual:
                self.multiple_runs_trajectories.append(self.actual_joint_states.copy())
                self.multiple_runs_times.append(self.time_actual.copy())
                console.print(f"[green]已保存第 {len(self.multiple_runs_trajectories)} 次运行的关节状态数据[/green]")
            
            if self.actual_ik_trajectory and self.time_actual_ik:
                self.multiple_runs_ik_trajectories.append(self.actual_ik_trajectory.copy())
                self.multiple_runs_ik_times.append(self.time_actual_ik.copy())
                console.print(f"[green]已保存第 {len(self.multiple_runs_ik_trajectories)} 次运行的逆解轨迹数据[/green]")
            
            return True
        except Exception as e:
            console.print(f"[red]播放轨迹指令失败: {str(e)}[/red]")
            return False
    
    def calculate_error(self):
        """计算参考轨迹和实际轨迹之间的误差"""
        # 检查是否有数据
        if not self.reference_joint_states:
            console.print("[red]参考轨迹数据为空[/red]")
            return None
        if not self.actual_joint_states:
            console.print("[red]实际轨迹数据为空[/red]")
            return None
        
        # 忽略前100个点
        reference_states = self.reference_joint_states[20:]
        actual_states = self.actual_joint_states[20:]
        
        # 如果数据点数量不一致，自动对齐
        if len(reference_states) != len(actual_states):
            if len(reference_states) < len(actual_states):
                actual_states = actual_states[:len(reference_states)]
            else:
                reference_states = reference_states[:len(actual_states)]
        
        # 检查数据点数量是否仍然有效
        if len(reference_states) == 0 or len(actual_states) == 0:
            console.print("[red]对齐后的数据点数量为0[/red]")
            return None
        
        # 检查关节数量是否一致
        if len(reference_states[0]) != len(actual_states[0]):
            console.print(f"[red]关节数量不一致，参考轨迹: {len(reference_states[0])}, 实际轨迹: {len(actual_states[0])}[/red]")
            return None
        
        # 计算每个位置的平方差误差
        errors = []
        num_joints = len(reference_states[0])
        
        for joint_idx in range(num_joints):
            try:
                ref_positions = [state[joint_idx] for state in reference_states]
                act_positions = [state[joint_idx] for state in actual_states]
                
                # 计算平方差误差
                mse = np.mean([(r - a)**2 for r, a in zip(ref_positions, act_positions)])
                errors.append(mse)
                console.print(f"[green]位置 {joint_idx} 的平方差误差: {mse}[/green]")
            except Exception as e:
                console.print(f"[red]计算位置 {joint_idx} 的误差时出错: {str(e)}[/red]")
                return None
        
        return errors
    
    def calculate_ik_error(self):
        """计算参考逆解轨迹和实际逆解轨迹之间的误差"""
        # 检查是否有数据
        if not self.reference_ik_trajectory:
            console.print("[red]参考逆解轨迹数据为空[/red]")
            return None
        if not self.actual_ik_trajectory:
            console.print("[red]实际逆解轨迹数据为空[/red]")
            return None
        
        reference_ik = self.reference_ik_trajectory[50:]
        actual_ik = self.actual_ik_trajectory[50:]
        
        # 如果数据点数量不一致，自动对齐
        if len(reference_ik) != len(actual_ik):
            if len(reference_ik) < len(actual_ik):
                actual_ik = actual_ik[:len(reference_ik)]
            else:
                reference_ik = reference_ik[:len(actual_ik)]
        
        # 检查数据点数量是否仍然有效
        if len(reference_ik) == 0 or len(actual_ik) == 0:
            console.print("[red]对齐后的逆解数据点数量为0[/red]")
            return None
        
        # 计算每个位置的平方差误差
        errors = []
        
        # 假设JointState消息有position字段
        try:
            for i in range(len(reference_ik[0].position)):
                ref_positions = [msg.position[i] for msg in reference_ik]
                act_positions = [msg.position[i] for msg in actual_ik]
                
                # 计算平方差误差
                mse = np.mean([(r - a)**2 for r, a in zip(ref_positions, act_positions)])
                errors.append(mse)
                console.print(f"[green]逆解轨迹位置 {i} 的平方差误差: {mse}[/green]")
        except Exception as e:
            console.print(f"[red]计算逆解轨迹误差时出错: {str(e)}[/red]")
            return None
        
        return errors
    
    def visualize_comparison(self, errors=None):
        """可视化参考轨迹和多次运行的实际轨迹的比较"""
        if not self.reference_joint_states or not self.multiple_runs_trajectories:
            console.print("[red]没有足够的数据进行可视化[/red]")
            return
        
        # 使用Agg后端，避免Tkinter问题
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from scipy.interpolate import interp1d
        
        # 获取关节数量
        num_joints = len(self.reference_joint_states[0])
        if num_joints == 0:
            console.print("[red]没有关节数据可用于可视化[/red]")
            return
        
        # 忽略前100个数据点
        start_idx = 100
        if len(self.time_reference) <= start_idx:
            console.print("[yellow]数据点不足100个，将使用所有可用数据[/yellow]")
            start_idx = 0
            
        time_reference_filtered = self.time_reference[start_idx:]
        reference_states_filtered = self.reference_joint_states[start_idx:]
        
        # 为每个关节创建一个子图
        fig, axes = plt.subplots(num_joints, 1, figsize=(12, 3*num_joints), sharex=True)
        
        if num_joints == 1:
            axes = [axes]
        
        # 颜色列表，用于区分不同的运行
        colors = ['r', 'g', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink']
        
        for joint_idx in range(num_joints):
            ax = axes[joint_idx]
            
            # 提取该关节的参考位置
            ref_positions = [state[joint_idx] for state in reference_states_filtered]
            
            # 绘制参考轨迹
            ax.plot(time_reference_filtered, ref_positions, 'b-', linewidth=2, label='Reference trajectory')
            
            # 绘制每次运行的实际轨迹
            for run_idx, (run_trajectory, run_times) in enumerate(zip(self.multiple_runs_trajectories, self.multiple_runs_times)):
                if len(run_times) > 1:
                    # 创建插值函数
                    joint_positions = [state[joint_idx] for state in run_trajectory]
                    interp_func = interp1d(run_times, joint_positions, bounds_error=False, fill_value="extrapolate")
                    
                    # 在参考轨迹的时间点上重采样实际轨迹
                    reference_duration = time_reference_filtered[-1] - time_reference_filtered[0]
                    actual_duration = run_times[-1] - run_times[0]
                    
                    # 时间缩放因子
                    scale_factor = actual_duration / reference_duration if reference_duration > 0 else 1.0
                    
                    resampled_positions = []
                    for t in time_reference_filtered:
                        scaled_t = (t - time_reference_filtered[0]) * scale_factor + run_times[0]
                        resampled_positions.append(interp_func(scaled_t))
                    
                    # 绘制实际轨迹
                    color_idx = run_idx % len(colors)
                    ax.plot(time_reference_filtered, resampled_positions, 
                            color=colors[color_idx], linestyle='-', alpha=0.7,
                            label=f'Run {run_idx+1}')
            
            ax.set_title(f'Position {joint_idx}')
            ax.set_ylabel('Position')
            ax.grid(True)
            ax.legend()
        
        if num_joints > 0:
            axes[-1].set_xlabel('Time (s)')
            plt.tight_layout()
            
            # 保存图像
            output_dir = os.path.expanduser("./")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = rospy.Time.now().to_sec()
            output_path = os.path.join(output_dir, f"multiple_runs_comparison_{int(timestamp)}.png")
            plt.savefig(output_path)
            console.print(f"[green]多次运行轨迹比较图已保存至: {output_path}[/green]")
            
            # 关闭图形，避免内存泄漏
            plt.close(fig)
    
    def visualize_ik_comparison(self, errors=None):
        """可视化参考逆解轨迹和实际逆解轨迹的比较"""
        if not self.reference_ik_trajectory or not self.actual_ik_trajectory:
            console.print("[red]没有足够的逆解轨迹数据进行可视化[/red]")
            return
        
        # 对实际轨迹进行时间对齐和重采样
        from scipy.interpolate import interp1d
        
        if len(self.time_actual_ik) > 1 and len(self.reference_ik_trajectory[0].position) > 0:
            # 创建插值函数
            interp_funcs = []
            for joint_idx in range(len(self.actual_ik_trajectory[0].position)):
                joint_positions = [msg.position[joint_idx] for msg in self.actual_ik_trajectory]
                interp_funcs.append(interp1d(self.time_actual_ik, joint_positions, 
                                            bounds_error=False, fill_value="extrapolate"))
            
            # 在参考轨迹的时间点上重采样实际轨迹
            resampled_actual = []
            reference_duration = self.time_reference_ik[-1] - self.time_reference_ik[0]
            actual_duration = self.time_actual_ik[-1] - self.time_actual_ik[0]
            
            # 时间缩放因子
            scale_factor = actual_duration / reference_duration if reference_duration > 0 else 1.0
            
            for t in self.time_reference_ik:
                scaled_t = (t - self.time_reference_ik[0]) * scale_factor + self.time_actual_ik[0]
                joint_positions = [func(scaled_t) for func in interp_funcs]
                resampled_actual.append(joint_positions)
            
            # 获取关节数量
            num_joints = len(self.actual_ik_trajectory[0].position)
            if num_joints == 0:
                console.print("[red]没有逆解轨迹数据可用于可视化[/red]")
                return
            

            start_idx = 20
            if len(self.time_reference_ik) <= start_idx:
                console.print("[yellow]数据点不足50个，将使用所有可用数据[/yellow]")
                start_idx = 0
                
            time_reference_ik_filtered = self.time_reference_ik[start_idx:]
            reference_ik_trajectory_filtered = self.reference_ik_trajectory[start_idx:]
            resampled_actual_filtered = resampled_actual[start_idx:]
            
            # 为每个关节创建一个子图
            fig, axes = plt.subplots(num_joints, 1, figsize=(12, 3*num_joints), sharex=True)
            
            if num_joints == 1:
                axes = [axes]
            
            for joint_idx in range(num_joints):
                ax = axes[joint_idx]
                
                # 提取该关节的参考位置和实际位置
                ref_positions = [msg.position[joint_idx] for msg in reference_ik_trajectory_filtered]
                act_positions = [pos[joint_idx] for pos in resampled_actual_filtered]
                
                # 绘制参考轨迹和实际轨迹
                ax.plot(time_reference_ik_filtered, ref_positions, 'b-', label='Reference inverse solution trajectory')
                ax.plot(time_reference_ik_filtered, act_positions, 'r-', label='Actual inverse solution trajectory')
                
                # 添加误差信息（如果有）
                if errors and joint_idx < len(errors):
                    ax.set_title(f'IK Position {joint_idx} (MSE: {errors[joint_idx]:.4f})')
                else:
                    ax.set_title(f'IK Position {joint_idx}')
                
                ax.set_ylabel('Position')
                ax.grid(True)
                ax.legend()
            
            if num_joints > 0:
                axes[-1].set_xlabel('Time (s)')
                plt.tight_layout()
                
                # 保存图像
                output_dir = os.path.expanduser("./")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                timestamp = rospy.Time.now().to_sec()
                output_path = os.path.join(output_dir, f"ik_trajectory_comparison_{int(timestamp)}.png")
                plt.savefig(output_path)
                console.print(f"[green]逆解轨迹比较图已保存至: {output_path}[/green]")
                
                # 显示图像
                plt.show()
        else:
            console.print("[red]实际逆解轨迹数据点不足，无法进行可视化[/red]")
    
    def visualize_multiple_runs_comparison(self):
        """可视化多次运行的逆解轨迹与参考轨迹的比较"""
        if not self.reference_ik_trajectory or not self.multiple_runs_ik_trajectories:
            console.print("[red]没有足够的逆解轨迹数据进行多次运行比较可视化[/red]")
            return
        
        # 使用Agg后端，避免Tkinter问题
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from scipy.interpolate import interp1d
        
        # 获取关节数量
        num_joints = len(self.reference_ik_trajectory[0].position)
        if num_joints == 0:
            console.print("[red]没有逆解轨迹数据可用于可视化[/red]")
            return
        
        # 忽略前50个数据点
        start_idx = 50
        if len(self.time_reference_ik) <= start_idx:
            console.print("[yellow]数据点不足50个，将使用所有可用数据[/yellow]")
            start_idx = 0
            
        time_reference_ik_filtered = self.time_reference_ik[start_idx:]
        reference_ik_trajectory_filtered = self.reference_ik_trajectory[start_idx:]
        
        # 为每个关节创建一个子图
        fig, axes = plt.subplots(num_joints, 1, figsize=(12, 3*num_joints), sharex=True)
        
        if num_joints == 1:
            axes = [axes]
        
        # 颜色列表，用于区分不同的运行
        colors = ['r', 'g', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink']
        
        for joint_idx in range(num_joints):
            ax = axes[joint_idx]
            
            # 提取该关节的参考位置
            ref_positions = [msg.position[joint_idx] for msg in reference_ik_trajectory_filtered]
            
            # 绘制参考轨迹
            ax.plot(time_reference_ik_filtered, ref_positions, 'b-', linewidth=2, label='Reference trajectory')
            
            # 绘制每次运行的实际轨迹
            for run_idx, (run_trajectory, run_times) in enumerate(zip(self.multiple_runs_ik_trajectories, self.multiple_runs_ik_times)):
                if len(run_times) > 1:
                    # 创建插值函数
                    joint_positions = [msg.position[joint_idx] for msg in run_trajectory]
                    interp_func = interp1d(run_times, joint_positions, bounds_error=False, fill_value="extrapolate")
                    
                    # 在参考轨迹的时间点上重采样实际轨迹
                    reference_duration = time_reference_ik_filtered[-1] - time_reference_ik_filtered[0]
                    actual_duration = run_times[-1] - run_times[0]
                    
                    # 时间缩放因子
                    scale_factor = actual_duration / reference_duration if reference_duration > 0 else 1.0
                    
                    resampled_positions = []
                    for t in time_reference_ik_filtered:
                        scaled_t = (t - time_reference_ik_filtered[0]) * scale_factor + run_times[0]
                        resampled_positions.append(interp_func(scaled_t))
                    
                    # 绘制实际轨迹
                    color_idx = run_idx % len(colors)
                    ax.plot(time_reference_ik_filtered, resampled_positions, 
                            color=colors[color_idx], linestyle='-', alpha=0.7,
                            label=f'Run {run_idx+1}')
            
            ax.set_title(f'IK Position {joint_idx}')
            ax.set_ylabel('Position')
            ax.grid(True)
            ax.legend()
        
        if num_joints > 0:
            axes[-1].set_xlabel('Time (s)')
            plt.tight_layout()
            
            # 保存图像
            output_dir = os.path.expanduser("./")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = rospy.Time.now().to_sec()
            output_path = os.path.join(output_dir, f"multiple_runs_ik_comparison_{int(timestamp)}.png")
            plt.savefig(output_path)
            console.print(f"[green]多次运行逆解轨迹比较图已保存至: {output_path}[/green]")
            
            # 显示图像
            plt.show()

def select_rosbag_file(base_dir, message):
    """选择rosbag文件"""
    if not os.path.exists(base_dir):
        console.print(f"[red]目录不存在: {base_dir}[/red]")
        return None
    
    subfolders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    if not subfolders:
        console.print("[red]没有找到子文件夹[/red]")
        return None
    
    selected_folder = questionary.select("请选择一个子文件夹", choices=subfolders).ask()
    if selected_folder is None:
        return None
    
    folder_path = os.path.join(base_dir, selected_folder)
    rosbag_files = [file for file in os.listdir(folder_path) if file.endswith(".bag")]
    if not rosbag_files:
        console.print(f"[red]在选定的文件夹中没有找到rosbag文件[/red]")
        return None
    
    selected_rosbag = questionary.select(message, choices=rosbag_files).ask()
    if selected_rosbag is None:
        return None
    
    return os.path.join(folder_path, selected_rosbag)

def main():
    rospy.init_node('trajectory_validator', anonymous=True)
    
    validator = TrajectoryValidator()
    
    # 选择rosbag文件
    rosbag_log_save_path = os.path.expanduser("./")
    
    # 选择参考轨迹rosbag
    reference_bag_path = select_rosbag_file(rosbag_log_save_path, "请选择包含标准电机位置的参考rosbag文件")
    if not reference_bag_path:
        return
    
    # 加载参考轨迹
    if not validator.load_reference_bag(reference_bag_path):
        return
    
    # 选择轨迹指令rosbag
    trajectory_bag_path = select_rosbag_file(rosbag_log_save_path, "请选择包含VR路径指令的rosbag文件")
    if not trajectory_bag_path:
        return
    
    # 运行5次并记录数据
    console.print("[blue]将进行5次轨迹运行并记录数据...[/blue]")
    for run in range(5):
        # 调用服务将控制模式设置为1（VR控制模式）
        try:
           # 创建服务代理
            arm_traj_change_mode_client = rospy.ServiceProxy("/arm_traj_change_mode", changeArmCtrlMode)

            # 创建请求对象
            request1 = changeArmCtrlModeRequest()
            request1.control_mode = 1  # 设置控制模式

            # 调用服务并获取响应
            response = arm_traj_change_mode_client(request1)
            # 创建请求对象
            rospy.sleep(2)
            request2 = changeArmCtrlModeRequest()
            request2.control_mode = 2  # 设置控制模式
            
            # 调用服务并获取响应
            response2 = arm_traj_change_mode_client(request2)
            rospy.sleep(2)
        except rospy.ROSException as e:
            console.print(f"[red]无法连接到控制模式服务: {e}[/red]")
        except rospy.ServiceException as e:
            console.print(f"[red]调用控制模式服务失败: {e}[/red]")
        console.print(f"[blue]开始第 {run+1} 次运行...[/blue]")
        
        
        if not validator.play_trajectory_bag(trajectory_bag_path):
            console.print(f"[red]第 {run+1} 次运行失败，跳过[/red]")
            continue
        console.print(f"[green]第 {run+1} 次运行完成[/green]")
        # 等待一段时间再进行下一次运行
        rospy.sleep(1.0)
    
    # 计算关节误差
    errors = validator.calculate_error()
    if errors:
        console.print("[green]关节轨迹误差计算完成[/green]")
        
        # 显示每个位置的误差
        console.print("[blue]各关节位置的平方差误差 (MSE):[/blue]")
        total_error = 0.0
        for idx, error in enumerate(errors):
            console.print(f"  位置 {idx}: {error:.4f}")
            total_error += error
        
        # 计算平均误差
        avg_error = total_error / len(errors)
        console.print(f"[blue]平均关节误差: {avg_error:.4f}[/blue]")
        
        # 根据误差判断动作是否标准
        threshold = 0.0025  # 平方差阈值 (0.05的平方)
        if avg_error < threshold:
            console.print("[green]关节动作执行标准！误差在可接受范围内。[/green]")
        else:
            console.print("[yellow]关节动作执行不够标准，误差超过阈值。[/yellow]")
        
        # 可视化比较
        validator.visualize_comparison(errors)
    else:
        console.print("[red]无法计算关节轨迹误差[/red]")
    
    # 计算逆解轨迹误差
    ik_errors = validator.calculate_ik_error()
    if ik_errors:
        console.print("[green]逆解轨迹误差计算完成[/green]")
        
        # 显示每个位置的误差
        console.print("[blue]各逆解位置的平方差误差 (MSE):[/blue]")
        total_error = 0.0
        for idx, error in enumerate(ik_errors):
            console.print(f"  逆解位置 {idx}: {error:.4f}")
            total_error += error
        
        # 计算平均平方差误差
        avg_error = total_error / len(ik_errors)
        console.print(f"[blue]平均逆解平方差误差: {avg_error:.4f}[/blue]")
        
        # 根据平方差误差判断逆解是否标准
        threshold = 0.0025  # 平方差阈值 (0.05的平方)
        if avg_error < threshold:
            console.print("[green]逆解轨迹执行标准！平方差误差在可接受范围内。[/green]")
        else:
            console.print("[yellow]逆解轨迹执行不够标准，平方差误差超过阈值。[/yellow]")
        
        # 可视化比较
        validator.visualize_ik_comparison(ik_errors)
    else:
        console.print("[red]无法计算逆解轨迹误差[/red]")

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        console.print("[yellow]程序被用户中断[/yellow]")
