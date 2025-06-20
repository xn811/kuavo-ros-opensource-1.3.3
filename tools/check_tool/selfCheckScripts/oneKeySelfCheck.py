import subprocess
import sys
import threading
import signal
import os
import rospy
import select

develFound = False
installedFound = False

roslaunch_running = False
h12_msg = False

h12_msg_valid = False
h12_msg = None
current_process = None

# 定义要打印的日志信息列表
target_logs = [
    "IMU 总采样次数: ",
    "数据读取失败次数: ",
    "数据读取成功率: ", 
    "Yaw角漂移检测失败！漂移量：",
    "可能原因：IMU未校准、陀螺仪零偏过大或设备晃动",
    "Yaw角稳定性检测通过！漂移量：",
    "当前IMU（HIPNUC）不支持时间戳，无法统计更新频率.",
    "IMU更新频率统计:",
    "加速度计: 均值=",
    "陀螺仪:   均值=",
    "四元数:   均值=",
    "获取IMU数据更新频率失败!!!",
    "IMU 初始化成功!!!",
    "IMU 初始化失败!!!",
    "末端执行器(灵巧手)初始化成功!!!",
    "末端执行器(灵巧手)初始化失败!!!",
    "电机初始化成功!!!",
    "电机初始化失败!!!",
    "测试手臂电机>>",
    "手臂关节",
    "测试手臂电机失败, 请用户确认相应关节是否使能!!!",
    "测试手臂电机成功!!!",
    "测试腿部电机>>",
    "测试腿部电机失败!!!",
    "测试手臂电机成功!!!",
    "测试手臂电机失败!!!",
    "当前cali位置是否正确，[y/n] 输入[y]进入到准备姿态(执行完后可以输入[x]退出程序)",
    "输入x退出程序：",
    # 新增电机跟随测试相关的关键词
    "正在测试电机对:",
    "左电机误差方差:",
    "右电机误差方差:",
    "相似性：",
    "本轮电机对测试结果：",
    "test complete.",
    "Switching to joint pair",
    "电机对进度:"
]

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建 LidarCheck.py 的绝对路径
OneKeyCheckSalveComputer_path = os.path.join(current_dir, 'OneKeyCheckSlaveComputer.py')

# 反推kuavo-ros-control的路径
kuavo_ros_control_path = os.path.abspath(os.path.join(current_dir, "../../.."))
# 打印kuavo-ros-control的路径
print(f"kuavo-ros-control的路径为: {kuavo_ros_control_path}")

# 获取当前Python脚本所在目录
shell_script_path = os.path.join(current_dir, "compiling_dependent_lib.sh")

# 计算相对路径
launch_path = os.path.join(kuavo_ros_control_path, "hardware_node hardwareSelfCheck.launch")

def print_colored_text(text, color="green", bold=False):
    color_codes = {
        "green": ("32", "92"),
        "yellow": ("33", "93"),
        "red": ("31", "91")
    }
    base_code = "\033["
    if bold:
        base_code += "1;"
    color_code = color_codes.get(color, ("32", "92"))[1]
    print(f"{base_code}{color_code}m{text}\033[0m")

def h12_topic_callback(msg):
    global h12_msg
    global h12_msg_valid
    if h12_msg:
        h12_msg = msg
        channels = msg.channels
        has_non_zero = any(channel != 0 for channel in channels)
        if has_non_zero:
            h12_msg_valid = True
        # else:
            # print(f"收到 /h12pro_channel 话题消息，但消息中的数据全为 0: {msg}")

def h12_remote_control_detection():
    global h12_msg
    global h12_msg_valid

    workspace_path  = "../../../devel/lib/python3/dist-packages"
    if workspace_path not in sys.path:
        sys.path.append(workspace_path)

    # 检查并赋予执行权限（关键修复）
    if not os.access(shell_script_path, os.X_OK):
        os.chmod(shell_script_path, 0o755)
        # print(f"已为 {shell_script_path} 添加执行权限")

    try:
        result = os.system(shell_script_path)
        if result != 0:
            print(f"Error occurred while running the shell script. Return code: {result}")
        from h12pro_controller_node.msg import h12proRemoteControllerChannel
        print("成功导入消息模块")
    except ImportError as e:
        print(f"导入模块时出错: {e}")
        return

    rospy.Subscriber('/h12pro_channel', h12proRemoteControllerChannel, h12_topic_callback)
    start_time = rospy.Time.now()
    h12_msg = True
    while not rospy.is_shutdown() and (rospy.Time.now() - start_time).to_sec() < 0.5:
        
        rospy.rostime.wallsleep(0.1)
    
    h12_msg = False
    if h12_msg_valid:
        print_colored_text(f"收到 /h12pro_channel 话题消息成功", color="green", bold=True)
    else:
        print_colored_text(f"收到 /h12pro_channel 话题消息异常", color="red", bold=True)

def input_thread(process):
    global roslaunch_running
    while process and process.poll() is None:
        try:
            user_input = input().strip()  # 获取输入并清理空格
            if process.stdin:
                # 直接发送原始输入内容
                process.stdin.write(user_input + "\n")
                process.stdin.flush()
                
                # 如果输入x则退出
                if user_input.lower() == 'x':
                    print("收到退出命令，正在结束测试...")
                    roslaunch_running = False
                    break
                    
        except (BrokenPipeError, AttributeError):
            break
        except Exception as e:
            print(f"输入线程错误: {e}", file=sys.stderr)
            break

def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    global current_process, roslaunch_running
    print("\n收到Ctrl+C, 正在关闭程序...")
    if current_process and current_process.poll() is None:
        # 发送退出命令
        if current_process.stdin:
            current_process.stdin.write('x\n')  # 发送退出命令
            current_process.stdin.flush()
        current_process.terminate()  # 发送SIGTERM
        try:
            current_process.wait(timeout=3)  # 等待3秒
        except subprocess.TimeoutExpired:
            current_process.kill()  # 强制终止
    roslaunch_running = False
    rospy.signal_shutdown("Received Ctrl+C")
    sys.exit(0)

def register_signal_handler(process):
    """注册信号处理函数"""
    global current_process
    current_process = process
    handler = lambda sig, frame: signal_handler(sig, frame)
    signal.signal(signal.SIGINT, handler)

def check_package_compiled(package_names):
    global develFound
    global installedFound

    """检查指定的ROS包是否已经编译"""
    # 获取当前脚本所在目录
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # 假设 ROS 工作空间在当前脚本目录的上两级目录
    workspace_root = os.path.abspath(os.path.join(current_script_dir, '..', '..', '..'))
    workspace_setup = os.path.join(workspace_root, 'devel', 'setup.bash')
    if not os.path.exists(workspace_setup):
        print(f"devel路径不存在...")
        print(f"workspace_setup的路径为: {workspace_setup}")
        return False
    
    develFound = False
    installedFound = False

    # 检查包对应的目录是否存在于devel空间中
    for package_name in package_names:
        # 检查包对应的目录是否存在于devel空间中
        package_devel_path = os.path.join(os.path.dirname(workspace_setup), "lib", package_name)
        if not os.path.exists(package_devel_path):
            develFound = False
        else:
            print("find in devel/lib")
            develFound = True
            return develFound

        # 检查installed空间的include目录
        installed_include_path = os.path.join(
            os.path.dirname(os.path.dirname(workspace_setup)), 
            "installed", 
            "share"
        )
        # 检查installed/include/<package_name>是否存在
        package_installed_include_path = os.path.join(installed_include_path, package_name)
        if os.path.exists(package_installed_include_path):
            installedFound = True
            print("find in installed/share")
        else:
            print("can't find in installed/share")
    if not develFound and not installedFound:
        print_colored_text(f"不能在[devel/lib]和[installed/share]找到 {', '.join(package_names)} 的编译包，请先编译这些包。", color="red", bold=True)

    return develFound or installedFound


def run_motor_follow_test():
    global develFound
    global installedFound
    global roslaunch_running 

    package_name_list = [
                    "hardware_node"
                    ]
    if not check_package_compiled(package_name_list):
        return 1
    
    process = None  # 初始化process变量
    try:
        if installedFound:
            print("exe in installed")
            full_command = (
                "cd ../../../installed/bin && "
                f"source {kuavo_ros_control_path}/devel/setup.bash && "
                # f"source {kuavo_ros_control_path}/installed/setup.bash && "
                f"./motorFollowTest"
            )
        elif develFound:
            full_command = (
                "cd ../../../devel/lib/hardware_node && "
                f"source {kuavo_ros_control_path}/devel/setup.bash && "
                f"./motorFollowTest"
            )
        else:
            print_colored_text("未找到编译产物！", color="red", bold=True)
            return 1  # 提前返回，避免后续代码执行

        # 定义输出文件路径
        output_file_path = "./motorTest/motor_follow_output.log"

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # 初始化进度跟踪变量
        current_pair = 0
        total_pairs = 13  # 总共13对电机
        test_results = []
        test_details = []  # 存储每对电机的详细信息
        current_pair_progress = {"left": 0, "right": 0}  # 当前电机对的周期进度
        current_motor_pair = None  # 当前测试的电机对索引
        
        print_colored_text("=== 电机跟随性测试开始 ===", color="green", bold=True)
        print_colored_text(f"总共需要测试 {total_pairs} 对电机", color="blue", bold=True)
        print_colored_text("=" * 50, color="blue")

        # 打开文件以写入模式
        with open(output_file_path, 'w') as output_file:
            # 启动roslaunch
            process = subprocess.Popen(
                ['bash', '-c', full_command],
                stdin=subprocess.PIPE,  # 允许输入
                stdout=subprocess.PIPE,  # 捕获标准输出
                stderr=subprocess.STDOUT,  # 将错误输出合并到标准输出
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True,
            )

            # 注册信号处理
            register_signal_handler(process)
            roslaunch_running = True
            
            # 生成支持点击的超链接
            clickable_link = f"\x1b]8;;file://{output_file_path}\x1b\\{output_file_path}\x1b]8;;\x1b\\"
            print(f"电机跟随性测试已启动，输出已保存到 {clickable_link}")
            print("按Ctrl+C退出，或输入x结束测试...")
            print()

            # 启动输入线程处理用户输入
            motor_thread = threading.Thread(target=input_thread,args=(process,),daemon=True)
            motor_thread.start()

            # 实时监控输出并过滤目标日志
            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    output_file.write(line)
                    output_file.flush()
                    
                    # 检查是否为目标日志信息
                    for target_log in target_logs:
                        if target_log in line:
                            line_stripped = line.strip()
                            
                            # 处理不同的输出类型
                            if "电机对进度:" in line_stripped:
                                # 解析电机对进度
                                try:
                                    # 格式: "电机对进度: 1 | 左周期: 4/10 | 右周期: 6/10"
                                    parts = line_stripped.split("|")
                                    if len(parts) >= 3:
                                        pair_info = parts[0].split(":")
                                        left_info = parts[1].split(":")
                                        right_info = parts[2].split(":")
                                        
                                        pair_num = int(pair_info[1].strip())
                                        left_cycle = int(left_info[1].strip().split("/")[0])
                                        right_cycle = int(right_info[1].strip().split("/")[0])
                                        
                                        # 更新当前电机对进度
                                        current_pair_progress["left"] = left_cycle
                                        current_pair_progress["right"] = right_cycle
                                        
                                        # 计算当前电机对的完成百分比
                                        left_progress = (left_cycle / 10) * 100
                                        right_progress = (right_cycle / 10) * 100
                                        avg_progress = (left_progress + right_progress) / 2
                                        
                                        # 显示当前电机对进度
                                        left_bar = "█" * int(left_progress / 5) + "░" * (20 - int(left_progress / 5))
                                        right_bar = "█" * int(right_progress / 5) + "░" * (20 - int(right_progress / 5))
                                        
                                        print(f"\r🔄 电机对 {pair_num}: 左电机 [{left_bar}] {left_cycle}/10 | 右电机 [{right_bar}] {right_cycle}/10 | 平均: {avg_progress:.1f}%", end="", flush=True)
                                except:
                                    pass
                            
                            elif "Switching to joint pair" in line_stripped:
                                # 这是测试开始的信号，更新进度
                                print()  # 换行，结束当前进度条
                                current_pair += 1
                                progress = (current_pair / total_pairs) * 100
                                progress_bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
                                print_colored_text(f"🔄 开始测试第 {current_pair} 对电机", color="yellow", bold=True)
                                print_colored_text(f"总进度: [{progress_bar}] {progress:.1f}% ({current_pair}/{total_pairs})", color="cyan")
                                # 重置当前电机对进度
                                current_pair_progress = {"left": 0, "right": 0}
                            
                            elif "正在测试电机对:" in line_stripped:
                                # 提取电机对编号并显示
                                try:
                                    parts = line_stripped.split(":")
                                    if len(parts) >= 2:
                                        motor_info = parts[1].strip()
                                        current_motor_pair = motor_info  # 记录当前电机对
                                        print_colored_text(f"📊 分析电机对: {motor_info}", color="blue", bold=True)
                                except:
                                    print_colored_text(f"📊 {line_stripped}", color="blue", bold=True)
                            
                            elif "左电机误差方差:" in line_stripped or "右电机误差方差:" in line_stripped:
                                if "[异常]" in line_stripped:
                                    print_colored_text(f"❌ {line_stripped}", color="red")
                                else:
                                    print_colored_text(f"✅ {line_stripped}", color="green")
                            
                            elif "相似性：" in line_stripped:
                                if "[异常]" in line_stripped:
                                    print_colored_text(f"❌ {line_stripped}", color="red")
                                else:
                                    print_colored_text(f"✅ {line_stripped}", color="green")
                            
                            elif "本轮电机对测试结果：" in line_stripped:
                                if "异常" in line_stripped:
                                    print_colored_text(f"❌ {line_stripped}", color="red", bold=True)
                                    test_results.append("异常")
                                    # 记录异常电机对的详细信息
                                    if current_motor_pair:
                                        test_details.append({
                                            "pair": current_pair,
                                            "motors": current_motor_pair,
                                            "result": "异常"
                                        })
                                else:
                                    print_colored_text(f"✅ {line_stripped}", color="green", bold=True)
                                    test_results.append("正常")
                                    # 记录正常电机对的详细信息
                                    if current_motor_pair:
                                        test_details.append({
                                            "pair": current_pair,
                                            "motors": current_motor_pair,
                                            "result": "正常"
                                        })
                                print()  # 添加空行分隔
                            
                            elif "test complete." in line_stripped:
                                print()  # 确保换行
                                print_colored_text(f"🎉 {line_stripped}", color="green", bold=True)
                                print_colored_text("=" * 50, color="blue")
                                
                                # 显示测试总结
                                print_colored_text("=== 电机跟随性测试总结 ===", color="green", bold=True)
                                normal_count = test_results.count("正常")
                                abnormal_count = test_results.count("异常")
                                print_colored_text(f"总测试对数: {len(test_results)}", color="blue")
                                print_colored_text(f"正常: {normal_count} 对", color="green")
                                print_colored_text(f"异常: {abnormal_count} 对", color="red")
                                
                                if abnormal_count == 0:
                                    print_colored_text("🎉 所有电机对测试通过！", color="green", bold=True)
                                else:
                                    print_colored_text(f"⚠️  有 {abnormal_count} 对电机测试异常，请检查相关电机", color="red", bold=True)
                                    
                                    # 显示异常电机组的详细信息
                                    print_colored_text("\n📋 异常电机组详情:", color="yellow", bold=True)
                                    abnormal_pairs = [detail for detail in test_details if detail["result"] == "异常"]
                                    for i, detail in enumerate(abnormal_pairs, 1):
                                        print_colored_text(f"  {i}. 电机组 {detail['pair']}: 电机 {detail['motors']}", color="red")
                                
                                # 询问用户是否显示图像
                                print_colored_text("=" * 50, color="blue")
                                print_colored_text("📊 测试数据已保存，是否生成波形图像？", color="yellow", bold=True)
                                print_colored_text("图像将显示每对电机的输入信号和响应信号对比", color="cyan")
                                print_colored_text("输入 'y' 生成图像，输入其他键跳过", color="cyan")
                                
                                try:
                                    user_choice = input("请选择 (y/其他): ").strip().lower()
                                    if user_choice == 'y':
                                        print_colored_text("🔄 正在生成波形图像...", color="yellow", bold=True)
                                        
                                        # 切换到motorTest目录
                                        motor_test_dir = os.path.join(current_dir, "motorTest")
                                        if os.path.exists(motor_test_dir):
                                            # 保存当前工作目录
                                            original_cwd = os.getcwd()
                                            try:
                                                # 切换到motorTest目录
                                                os.chdir(motor_test_dir)
                                                
                                                # 运行drawWaveform脚本
                                                draw_waveform_script = os.path.join(motor_test_dir, "drawWaveform.py")
                                                if os.path.exists(draw_waveform_script):
                                                    result = subprocess.run(['python3', draw_waveform_script], 
                                                                          capture_output=True, text=True)
                                                    
                                                    if result.returncode == 0:
                                                        print_colored_text("✅ 波形图像生成成功！", color="green", bold=True)
                                                        print_colored_text("📁 图像保存位置:", color="blue")
                                                        print_colored_text("   - 组合图像: ./motorTest/grouped_images/", color="cyan")
                                                        
                                                        # 检查是否有异常电机，如果有则特别提醒
                                                        if abnormal_count > 0:
                                                            print_colored_text(f"💡 建议查看异常电机的波形图像进行详细分析", color="yellow")
                                                    else:
                                                        print_colored_text("❌ 波形图像生成失败", color="red", bold=True)
                                                        if result.stderr:
                                                            print_colored_text(f"错误信息: {result.stderr}", color="red")
                                                else:
                                                    print_colored_text("❌ 未找到 drawWaveform.py 脚本", color="red", bold=True)
                                            finally:
                                                # 恢复原始工作目录
                                                os.chdir(original_cwd)
                                        else:
                                            print_colored_text("❌ 未找到 motorTest 目录", color="red", bold=True)
                                    else:
                                        print_colored_text("⏭️  跳过图像生成", color="blue")
                                except KeyboardInterrupt:
                                    print_colored_text("\n⏭️  用户取消，跳过图像生成", color="blue")
                                except Exception as e:
                                    print_colored_text(f"❌ 图像生成过程中出错: {e}", color="red", bold=True)
                            
                            else:
                                # 其他目标日志信息
                                print(line_stripped)

            # 等待进程结束
            process.wait()
            print_colored_text("电机跟随性测试已结束", color="green", bold=True)

    except Exception as e:
        print_colored_text(f"发生错误: {e}", color="red", bold=True)
    finally:
        # 确保进程已终止
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=2)
                if process.poll() is None:
                    process.kill()
            except Exception as e:
                print(f"终止进程时出错: {e}")
        roslaunch_running = False


def run_roslaunch():
    global roslaunch_running
    global target_logs
    global develFound
    global installedFound

    package_name_list = [
                    "hardware_node"
                    ]
    if not check_package_compiled(package_name_list):
        return 1
    
    process = None  # 初始化process变量
    try:
        # 构造完整的启动命令
        print("develFound:", develFound)
        if develFound:
            full_command = (
                "source /opt/ros/noetic/setup.bash && "
                f"source {kuavo_ros_control_path}/devel/setup.bash && "
                f"roslaunch hardware_node hardwareSelfCheck.launch"
            )
        elif installedFound:
            full_command = (
                "cd ../../../installed/bin && "
                f"source {kuavo_ros_control_path}/devel/setup.bash && "
                # f"source {kuavo_ros_control_path}/installed/setup.bash && "
                f"./hardwareSelfCheck"
            )
        else:
            print_colored_text("未找到编译产物！", color="red", bold=True)
            return 1  # 提前返回，避免后续代码执行

        # 定义输出文件路径
        output_file_path = "roslaunch_output.log"

        # 打开文件以写入模式
        with open(output_file_path, 'w') as output_file:
            # 启动roslaunch
            process = subprocess.Popen(
                ['bash', '-c', full_command],
                stdin=subprocess.PIPE,  # 允许输入
                stdout=subprocess.PIPE,  # 捕获标准输出
                stderr=subprocess.STDOUT,  # 将错误输出合并到标准输出
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True,
            )

            # 注册信号处理
            register_signal_handler(process)

            # 生成支持点击的超链接
            clickable_link = f"\x1b]8;;file://{output_file_path}\x1b\\{output_file_path}\x1b]8;;\x1b\\"
            print(f"ROS launch已启动，输出已保存到当前路径下 {clickable_link}，你可以点击该链接查看详细信息。按Ctrl+C退出...")
            roslaunch_running = True

            # 启动输入线程
            thread = threading.Thread(target=input_thread, args=(process,), daemon=True)
            thread.start()

            # 监控标准输出
            while process.poll() is None:
                rlist, _, _ = select.select([process.stdout], [], [], 0.1)
                if rlist:
                    line = process.stdout.readline()
                    # 检查是否为目标日志信息
                    for target_log in target_logs:
                        if target_log in line:
                            print(line.strip())
                    # 将所有输出写入日志文件
                    output_file.write(line)
                    output_file.flush()

            # 主线程等待进程结束
            process.wait()

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 确保进程已终止
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=2)
            if process.poll() is None:
                process.kill()
        roslaunch_running = False


if __name__ == "__main__":
    run_flag = True
    rospy.init_node('main_node', anonymous=True)
    while run_flag:
        if not roslaunch_running:
            print("\n请选择要执行的操作:")
            print("1. 下位机检测(启动hardwareSelfCheck.cc程序)")
            print("2. 上位机检测")
            print("3. h12遥控器信号检测")
            print("4. 电机跟随性测试")
            print("0. 退出")
            try:
                choice = input("输入选项: ")

                if choice == '1':
                    run_roslaunch()  # 启动roslaunch（假设其内部有独立的退出逻辑）
                elif choice == '2':
                    subprocess.run(['python3', OneKeyCheckSalveComputer_path])
                elif choice == '3':
                    h12_remote_control_detection()
                elif choice == '4':
                    run_motor_follow_test()
                elif choice == '0':
                    print("退出程序。")
                    run_flag = False
                else:
                    print_colored_text(f"无效的选项，请重新输入...", color="yellow", bold=True)
            except KeyboardInterrupt:
                print("\n收到Ctrl+C，退出程序。")
                run_flag = False
            except Exception as e:
                print_colored_text(f"发生错误: {e}", color="red", bold=True)
                print("返回主菜单...")
