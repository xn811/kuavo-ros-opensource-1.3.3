import rospy
import rospkg
import os
import pwd
import sys
import asyncio
import signal
import json
from queue import Queue
from dataclasses import dataclass
from typing import Any, Union, Dict
import websockets
import threading
import time
import math
from utils import calculate_file_md5, frames_to_custom_action_data, get_start_end_frame_time, frames_to_custom_action_data_ocs2
import shutil
import rosnode
from kuavo_ros_interfaces.srv import planArmTrajectoryBezierCurve, stopPlanArmTrajectory, planArmTrajectoryBezierCurveRequest, ocs2ChangeArmCtrlMode
from kuavo_ros_interfaces.msg import planArmState, jointBezierTrajectory, bezierCurveCubicPoint, robotHeadMotionData
from kuavo_msgs.msg import robotHandPosition
from std_srvs.srv import Trigger
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from kuavo_msgs.msg import sensorsData
# Replace multiprocessing values with simple variables
plan_arm_state_progress = 0
plan_arm_state_status = False
response_queue = Queue()
active_threads: Dict[websockets.WebSocketServerProtocol, threading.Event] = {}
ACTION_FILE_FOLDER = "~/.config/lejuconfig/action_files"
g_robot_type = ""
ocs2_current_joint_state = []
robot_version = (int)(os.environ.get("ROBOT_VERSION", "45"))

if robot_version >= 40:
    joint_names = [
        "l_arm_pitch",
        "l_arm_roll",
        "l_arm_yaw",
        "l_forearm_pitch",
        "l_hand_yaw",
        "l_hand_pitch",
        "l_hand_roll",
        "r_arm_pitch",
        "r_arm_roll",
        "r_arm_yaw",
        "r_forearm_pitch",
        "r_hand_yaw",
        "r_hand_pitch",
        "r_hand_roll",
    ]
else:
    joint_names = [
        "zarm_l1_link", "zarm_l2_link", "zarm_l3_link", "zarm_l4_link",
        "zarm_r1_link", "zarm_r2_link", "zarm_r3_link", "zarm_r4_link",
    ]
ocs2_joint_state = JointState()
ocs2_hand_state = robotHandPosition()
ocs2_head_state = robotHeadMotionData()
robot_settings = {
    "kuavo":{
        "plan_arm_trajectory_bezier_service_name": "/plan_arm_trajectory_bezier_curve",
        "stop_plan_arm_trajectory_service_name": "/stop_plan_arm_trajectory",
        "arm_traj_state_topic_name": "/robot_plan_arm_state",
    },
    "ocs2":{
        "plan_arm_trajectory_bezier_service_name": "/bezier/plan_arm_trajectory",
        "stop_plan_arm_trajectory_service_name": "/bezier/stop_plan_arm_trajectory",
        "arm_traj_state_topic_name": "/bezier/arm_traj_state",
    }
}

def call_change_arm_ctrl_mode_service(arm_ctrl_mode):
    result = True
    service_name = "humanoid_change_arm_ctrl_mode"
    try:
        rospy.wait_for_service(service_name, timeout=0.5)
        change_arm_ctrl_mode = rospy.ServiceProxy(
            "humanoid_change_arm_ctrl_mode", ocs2ChangeArmCtrlMode
        )
        change_arm_ctrl_mode(control_mode=arm_ctrl_mode)
        rospy.loginfo("Service call successful")
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s", e)
        result = False
    except rospy.ROSException:
        rospy.logerr(f"Service {service_name} not available")
        result = False
    finally:
        return result

def sensors_data_callback(msg):
    global current_arm_joint_state
    global robot_version
    if robot_version >= 40:
        current_arm_joint_state = msg.joint_data.joint_q[12:26]
        current_arm_joint_state = [round(pos, 2) for pos in current_arm_joint_state]
        current_arm_joint_state.extend([0] * 14)
    elif robot_version >= 10 and robot_version < 30:
        current_arm_joint_state = msg.joint_data.joint_q[12:20]
        current_arm_joint_state = [round(pos, 2) for pos in current_arm_joint_state]
        current_arm_joint_state.extend([0] * 8)

def traj_callback(msg):
    global ocs2_joint_state
    global robot_version
    if len(msg.points) == 0:
        return
    point = msg.points[0]
    
    if robot_version >= 40:
        ocs2_joint_state.name = joint_names
        ocs2_joint_state.position = [math.degrees(pos) for pos in point.positions[:14]]
        ocs2_joint_state.velocity = [math.degrees(vel) for vel in point.velocities[:14]]
        ocs2_joint_state.effort = [0] * 14
        ocs2_hand_state.left_hand_position = [int(math.degrees(pos)) for pos in point.positions[14:20]]
        ocs2_hand_state.right_hand_position = [int(math.degrees(pos)) for pos in point.positions[20:26]]
        ocs2_head_state.joint_data = [math.degrees(pos) for pos in point.positions[26:]]

    elif robot_version >= 10 and robot_version < 30:
        ocs2_joint_state.name = joint_names
        ocs2_joint_state.position = [math.degrees(pos) for pos in point.positions[:8]]
        ocs2_joint_state.velocity = [math.degrees(vel) for vel in point.velocities[:8]]
        ocs2_joint_state.effort = [0] * 8


kuavo_arm_traj_pub = None
control_hand_pub = None
control_head_pub = None
update_h12_config_pub = None

def timer_callback(event):
    global kuavo_arm_traj_pub, control_hand_pub, control_head_pub
    if g_robot_type == "ocs2" and len(ocs2_joint_state.position) > 0 and plan_arm_state_status is False:
        kuavo_arm_traj_pub.publish(ocs2_joint_state)
        control_hand_pub.publish(ocs2_hand_state)
        control_head_pub.publish(ocs2_head_state)

def init_publishers():
    global kuavo_arm_traj_pub, control_hand_pub, control_head_pub
    kuavo_arm_traj_pub = rospy.Publisher('/kuavo_arm_traj', JointState, queue_size=1, tcp_nodelay=True)
    control_hand_pub = rospy.Publisher('/control_robot_hand_position', robotHandPosition, queue_size=1, tcp_nodelay=True)
    control_head_pub = rospy.Publisher('/robot_head_motion_data', robotHeadMotionData, queue_size=1, tcp_nodelay=True)

async def init_ros_node():
    print("Initializing ROS node")
    rospy.init_node("arm_action_server", anonymous=True, disable_signals=True)
    robot_plan_arm_state_topic_name = robot_settings[g_robot_type]["arm_traj_state_topic_name"]
    rospy.Subscriber(robot_plan_arm_state_topic_name, planArmState, plan_arm_state_callback)
    rospy.Subscriber('/bezier/arm_traj', JointTrajectory, traj_callback, queue_size=1, tcp_nodelay=True)
    # rospy.Subscriber('/humanoid_mpc_observation', mpc_observation, mpc_obs_callback)
    rospy.Subscriber('/sensors_data_raw', sensorsData, sensors_data_callback, queue_size=1, tcp_nodelay=True)
    
    init_publishers()
    
    # Create a timer that calls timer_callback every 10ms (100Hz)
    rospy.Timer(rospy.Duration(0.01), timer_callback)

    print("ROS node initialized")

def create_bezier_request(action_data, start_frame_time, end_frame_time):
    req = planArmTrajectoryBezierCurveRequest()
    for key, value in action_data.items():
        msg = jointBezierTrajectory()
        for frame in value:
            point = bezierCurveCubicPoint()
            point.end_point, point.left_control_point, point.right_control_point = frame
            msg.bezier_curve_points.append(point)
        req.multi_joint_bezier_trajectory.append(msg)
    req.start_frame_time = start_frame_time
    req.end_frame_time = end_frame_time
    if robot_version >= 40:
        req.joint_names = ["l_arm_pitch", "l_arm_roll", "l_arm_yaw", "l_forearm_pitch", "l_hand_yaw", "l_hand_pitch", "l_hand_roll", "r_arm_pitch", "r_arm_roll", "r_arm_yaw", "r_forearm_pitch", "r_hand_yaw", "r_hand_pitch", "r_hand_roll"]
    else:
        req.joint_names = ["zarm_l1_link", "zarm_l2_link", "zarm_l3_link", "zarm_l4_link", "zarm_r1_link", "zarm_r2_link", "zarm_r3_link", "zarm_r4_link"]
    return req

def plan_arm_trajectory_bezier_curve_client(req):
    service_name = robot_settings[g_robot_type]["plan_arm_trajectory_bezier_service_name"]
    rospy.wait_for_service(service_name)
    try:
        plan_service = rospy.ServiceProxy(service_name, planArmTrajectoryBezierCurve)
        res = plan_service(req)
        return res.success
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
        return False

def stop_plan_arm_trajectory_client():
    service_name = robot_settings[g_robot_type]["stop_plan_arm_trajectory_service_name"]
    rospy.wait_for_service(service_name)
    try:
        if g_robot_type == "ocs2":
            stop_service = rospy.ServiceProxy(service_name, Trigger)
        else:
            stop_service = rospy.ServiceProxy(service_name, stopPlanArmTrajectory)

        stop_service()
        return
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
        return False
@dataclass
class Payload:
    cmd: str
    data: dict

@dataclass
class Response:
    payload: Any
    target: Union[str, websockets.WebSocketServerProtocol]

def plan_arm_state_callback(msg: planArmState):
    global plan_arm_state_progress, plan_arm_state_status
    plan_arm_state_progress = msg.progress
    plan_arm_state_status = msg.is_finished


def update_preview_progress(response: Response, stop_event: threading.Event):
    payload = response.payload
    update_interval = 0.001 
    global plan_arm_state_progress, plan_arm_state_status
    last_progress = None
    last_status = None
    
    while not stop_event.is_set():
        current_progress = plan_arm_state_progress
        current_status = plan_arm_state_status

        if current_progress != last_progress or current_status != last_status:
            last_progress = current_progress
            last_status = current_status
            
            payload.data["progress"] = current_progress
            payload.data["status"] = 0 if current_status else 1
            response_queue.put(response)
            
            if current_status:
                return
        
        time.sleep(update_interval)

async def websocket_message_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    cmd = data.get("cmd", "")
    cmd_handler = f"{cmd}_handler"
    if cmd_handler in globals() and callable(globals()[cmd_handler]):
        await globals()[cmd_handler](websocket, data)
    else:
        print(f"Unknown command: {cmd}")
        error_payload = Payload(
            cmd="error", data={"message": f"Unknown command: {cmd}"}
        )
        error_response = Response(payload=error_payload, target=websocket)
        response_queue.put(error_response)


async def broadacast_handler(websocket: websockets.WebSocketServerProtocol, data: dict):
    payload = Payload(
        cmd="broadcast",
        data={"code": 0, "message": "Broadcast message"},
    )
    response = Response(
        payload=payload,
        target="all",
    )

    response_queue.put(response)


async def preview_action_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    global g_robot_type
    print(g_robot_type)
    # Cancel existing thread for this client if it exists
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]

    payload = Payload(
        cmd="preview_action", data={"code": 0, "status": 0, "progress": 0}
    )

    data = data["data"]
    print(f"received message data: {data}")

    action_filename = data["action_filename"]
    global ACTION_FILE_FOLDER
    action_file_path = os.path.expanduser(f"{ACTION_FILE_FOLDER}/{action_filename}")
    if not os.path.exists(action_file_path):
        print(f"Action file not found: {action_file_path}")
        payload.data["code"] = 1
        response = Response(payload=payload, target=websocket)
        response_queue.put(response)
        return

    if calculate_file_md5(action_file_path) != data["action_file_MD5"]:
        print(f"Action file MD5 mismatch: {action_file_path}")
        payload.data["code"] = 2
        response = Response(payload=payload, target=websocket)
        response_queue.put(response)
        return

    start_frame_time, end_frame_time = get_start_end_frame_time(action_file_path)

    if g_robot_type == "ocs2":
        action_frames = frames_to_custom_action_data_ocs2(action_file_path, start_frame_time, current_arm_joint_state)
        end_frame_time += 1
        call_change_arm_ctrl_mode_service(2)
    else:
        action_frames = frames_to_custom_action_data(action_file_path)

    req = create_bezier_request(action_frames, start_frame_time, end_frame_time)
    plan_arm_trajectory_bezier_curve_client(req)
    time.sleep(0.5)
    # If valid, create initial response
    response = Response(
        payload=payload,
        target=websocket,
    )

    # Create a new stop event for this thread
    stop_event = threading.Event()
    active_threads[websocket] = stop_event

    # Start a thread to update the progress
    thread = threading.Thread(
        target=update_preview_progress, args=(response, stop_event)
    )
    print("Starting thread to update progress")
    thread.start()


async def stop_preview_action_handler(websocket: websockets.WebSocketServerProtocol, data: dict):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]
    
    payload = Payload(
        cmd="stop_preview_action", data={"code":0}
    )
    response = Response(
        payload=payload,
        target=websocket,
    )
    stop_plan_arm_trajectory_client()
    response_queue.put(response)


async def get_robot_info_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):

    robot_version = rospy.get_param('robot_version')
    payload = Payload(
        cmd="get_robot_info", 
        data={
            "code": 0, 
            "robot_type": robot_version,
            "music_folder_path": MUSIC_FILE_FOLDER,
            "maps_folder_path": MAP_FILE_FOLDER,
            "h12_config_path": H12_CONFIG_PATH
        }
    )

    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

# 传入脚本名称或者脚本路径来运行目标脚本。
async def execute_python_script_handler(
        websocket: websockets.WebSocketServerProtocol, data: dict
):
    payload = Payload(
        cmd="execute_python_script", data={"code": 0, "message": "Python script executed successfully"}
    )

    print(f"received execute_python_script data: {data}")
    data = data["data"]
    action_data = data.get("action_data")
    scripts_name = data.get("scripts_name")
    if action_data == "start_action":
        try:
            if not scripts_name:
                payload.data["code"] = 1
                payload.data["message"] = "scripts_name parameter not provided"
            else:
                # 如果scripts_name是绝对路径，直接使用；否则认为是相对UPLOAD_FILES_FOLDER目录的路径
                # 处理脚本路径中的"~"等转义符
                scripts_name_expanded = os.path.expanduser(scripts_name)
                if os.path.isabs(scripts_name_expanded):
                    script_path = scripts_name_expanded
                else:
                    # 默认脚本目录为UPLOAD_FILES_FOLDER
                    global UPLOAD_FILES_FOLDER
                    script_path = os.path.join(UPLOAD_FILES_FOLDER, scripts_name_expanded)
                print(f"script_path: {script_path}")
                if not os.path.isfile(script_path):
                    payload.data["code"] = 2
                    payload.data["message"] = f"Script file does not exist: {script_path}"
                else:
                    # 后台执行python脚本
                    try:
                        # 使用subprocess.Popen后台执行，不等待脚本结束
                        process = subprocess.Popen(
                            ["python3", script_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            encoding='utf-8'
                        )
                        payload.data["code"] = 0
                        payload.data["message"] = f"Python script started in background: {scripts_name}"
                    except Exception as e:
                        payload.data["code"] = 3
                        payload.data["message"] = f"Failed to start Python script in background: {scripts_name}, error: {str(e)}"
        except Exception as e:
            payload.data["code"] = 4
            payload.data["message"] = f"Exception occurred while executing script: {str(e)}"
    elif action_data == "stop_action":
        # 查找scripts_name对应的进程并kill掉
        try:
            if not scripts_name:
                payload.data["code"] = 1
                payload.data["message"] = "scripts_name parameter not provided, cannot stop process"
            else:
                # 处理脚本路径中的"~"等转义符
                scripts_name_expanded = os.path.expanduser(scripts_name)
                # 只取文件名部分，防止路径影响
                script_basename = os.path.basename(scripts_name_expanded)
                # 使用pgrep查找所有python3进程中包含该脚本名的进程
                # 只查找python3进程，避免误杀
                # 获取所有python3进程
                ps = subprocess.Popen(['ps', '-eo', 'pid,cmd'], stdout=subprocess.PIPE, text=True)
                output, _ = ps.communicate()
                killed = False
                for line in output.splitlines():
                    if 'python3' in line and script_basename in line:
                        try:
                            pid = int(line.strip().split()[0])
                            if pid == os.getpid():
                                continue  # 不杀掉自己
                            os.kill(pid, signal.SIGTERM)
                            killed = True
                            print(f"Killed process: {pid} ({line})")
                        except Exception as e:
                            print(f"Failed to kill process: {e}")
                if killed:
                    payload.data["code"] = 0
                    payload.data["message"] = f"Tried to kill all python3 processes containing script name {script_basename}"
                else:
                    payload.data["code"] = 2
                    payload.data["message"] = f"No python3 process found containing script name {script_basename}"
        except Exception as e:
            payload.data["code"] = 3
            payload.data["message"] = f"Exception occurred while stopping script process: {str(e)}"

    response = Response(payload=payload, target=websocket)
    response_queue.put(response)

async def get_robot_status_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    payload = Payload(
        cmd="get_robot_status", data={"code": 0, "isrun": True}
    )

    if not active_threads:
        payload.data["isrun"] = False
        print("No activate threads")
    else:
        for key, value in active_threads.items():
            print(f"Key: {key}, Value: {value}")

    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)


async def run_node_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]

    payload = Payload(
        cmd="run_node", data={"code": 0, "msg": "msg"}
    )

    data = data["data"]
    print(f"received message data: {data}")
    execute_path = data["path"]

    response = Response(
        payload=payload,
        target=websocket,
    )

    # Create a new stop event for this thread
    stop_event = threading.Event()

    # Start a thread to update the progress
    thread = threading.Thread(
        target=execute_command_progress, args=(websocket, response, stop_event, execute_path, False, None)  # 明确传递None作为parameters
    )
    print("Starting thread to update progress")
    thread.start()


def execute_command_progress(websocket: websockets.WebSocketServerProtocol, response: Response, stop_event: threading.Event, execute_path, use_ros_env: bool = False, parameters: dict = None):
    payload = response.payload
    update_interval = 0.001 

    if not os.path.exists(execute_path):
        payload.data["code"] = 1
        payload.data["msg"] = "File not found."
        response_queue.put(response)
        return

    py_exe = sys.executable
    command_list = [py_exe, execute_path]
    
    if parameters:
        for key, value in parameters.items():
            if isinstance(value, bool):
                if value:
                    command_list.append(f"{key}")
                    command_list.append(str(value))
            else:
                command_list.append(f"{key}")
                command_list.append(str(value))
    
    # 当需要加载 ros 环境时，动态查找工作空间路径
    if use_ros_env:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 向上查找直到找到包含devel/setup.bash的目录
        workspace_path = None
        search_dir = current_dir
        while search_dir != '/':
            setup_bash_path = os.path.join(search_dir, 'devel', 'setup.bash')
            if os.path.exists(setup_bash_path):
                workspace_path = search_dir
                break
            search_dir = os.path.dirname(search_dir)
        
        if workspace_path:
            # 使用bash -c来执行source命令和Python脚本
            setup_bash_path = os.path.join(workspace_path, 'devel', 'setup.bash')
            if parameters:
                args_str = ' '.join(command_list[2:])
                command_list = ['bash', '-c', f'source {setup_bash_path} && {py_exe} {execute_path} {args_str}']
            else:
                command_list = ['bash', '-c', f'source {setup_bash_path} && {py_exe} {execute_path}']
            print(f"Found workspace at: {workspace_path}")
        else:
            print("Warning: Could not find ROS workspace")
    
    print(f"Executing command: {command_list}")
    global process
    try: 
        env = os.environ.copy()
        process = subprocess.Popen(command_list, env=env)
    except Exception as e:
        print("An error occurred while trying to execute the command:")
        print(e)
        payload.data["code"] = 1
        payload.data["msg"] = "Command execution failed."
        response_queue.put(response)
        print("Command execution failed.")   
    else:
        active_threads[websocket] = stop_event
        payload.data["code"] = 0
        payload.data["msg"] = "Command executed successfully."
        response_queue.put(response)
        
    while not stop_event.is_set():
        time.sleep(update_interval)

def monitor_and_stop(process):
    global should_stop, terminate_process_result
    terminate_process_result = False
    while True:
        time.sleep(1)
        if should_stop:
            print("Kill the target process")
            process.terminate()
            try:
                process.wait(timeout=3)
                terminate_process_result = True
            except subprocess.TimeoutExpired:
                print("Forced kill the target process")
                process.kill()
                try:
                    process.wait(timeout=2)
                    terminate_process_result = True
                except subprocess.TimeoutExpired:
                    terminate_process_result = False
            break

async def stop_run_node_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]
    
    payload = Payload(
        cmd="stop_run_node", data={"code":0}
    )

    global process, should_stop, terminate_process_result
    monitor_thread = threading.Thread(target=monitor_and_stop, args=(process,))
    monitor_thread.start()
    should_stop = True
    monitor_thread.join()
    print("terminate_process_result: ", terminate_process_result)
    
    if not terminate_process_result:
        payload.data["code"] = 1

    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

async def execute_demo_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]

    payload = Payload(
        cmd="execute_demo", data={"code": 0, "msg": "Demo execution started"}
    )

    data = data["data"]
    print(f"received demo execution data: {data}")
    demo_name = data["demo_name"]
    parameters = data.get("parameters", {})
    
    # 构建demo脚本路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建demo脚本路径：demo_name_demo/main.py
    execute_path = os.path.join(current_dir, f"{demo_name}_demo", "main.py")

    response = Response(
        payload=payload,
        target=websocket,
    )

    # 创建新的停止事件
    stop_event = threading.Event()

    thread = threading.Thread(
        target=execute_command_progress, 
        args=(websocket, response, stop_event, execute_path, True, parameters)
    )
    print("Starting thread to execute demo")
    thread.start()

async def stop_execute_demo_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]
    
    payload = Payload(
        cmd="stop_execute_demo", data={"code":0}
    )

    global process, should_stop, terminate_process_result
    monitor_thread = threading.Thread(target=monitor_and_stop, args=(process,))
    monitor_thread.start()
    should_stop = True
    monitor_thread.join()
    print("terminate_process_result: ", terminate_process_result)
    
    if not terminate_process_result:
        payload.data["code"] = 1
        payload.data["msg"] = "Failed to stop demo execution"

    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

async def load_map_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]
    payload = Payload(
        cmd="load_map", data={"code":0}
    )
    data = data["data"]
    map_name = data["map_name"]
    try:
        service_name = '/load_map'
        rospy.wait_for_service(service_name,timeout=3.0)
        load_map_client = rospy.ServiceProxy(service_name, LoadMap)

        # request
        req = LoadMapRequest()
        req.map_name = map_name
        
        # response  
        res = load_map_client(req)
        if res.success:
            if  download_map_file(map_name):
                payload.data["code"] = 0
                payload.data["msg"] = "Map loaded successfully"
                payload.data["map_path"] = MAP_FILE_FOLDER +"/"+ map_name+".png"
            else:
                payload.data["code"] = 1
                payload.data["msg"] = "Map loaded successfully, but failed to download map file"

    except rospy.ServiceException as e:
        payload.data["code"] = 2
        payload.data["msg"] = f"Service `load_map` call failed: {e}"
    except rospy.ROSException as e:
        payload.data["code"] = 2
        payload.data["msg"] = f"Service `load_map` call failed: {e}"
    except Exception as e:
        payload.data["code"] = 2
        payload.data["msg"] = f"Service `load_map` call failed: {e}"
    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)
    
async def init_localization_by_pose_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    payload = Payload(
        cmd="init_localization_by_pose", data={"code":0}
    )

    data = data["data"]
    print(f"received init localization by pose data: {data}")
    x = data["x"]
    y = data["y"]
    z = data["z"]
    roll = data["roll"]
    pitch = data["pitch"]
    yaw = data["yaw"]
    
    try:
        service_name = 'set_initialpose'
        rospy.wait_for_service(service_name,timeout=3.0)
        init_localization_by_pose_client = rospy.ServiceProxy(service_name, SetInitialPose) 

        # 将 roll pitch yaw 转换为四元数
        orientation = tf.transformations.quaternion_from_euler(yaw, pitch, roll)

        # request
        req = SetInitialPoseRequest()
        req.initial_pose.header.frame_id = "map"
        req.initial_pose.header.stamp = rospy.Time.now()
        req.initial_pose.pose.pose.position.x = x
        req.initial_pose.pose.pose.position.y = y
        req.initial_pose.pose.pose.position.z = z
        req.initial_pose.pose.pose.orientation.x = orientation[0]
        req.initial_pose.pose.pose.orientation.y = orientation[1]
        req.initial_pose.pose.pose.orientation.z = orientation[2]
        req.initial_pose.pose.pose.orientation.w = orientation[3]
        
        # response
        res = init_localization_by_pose_client(req)
        if res.success:
            payload.data["code"] = 0
            payload.data["msg"] = "Localization initialized successfully"
        else:
            payload.data["code"] = 1
            payload.data["msg"] = "Failed to initialize localization"
    except rospy.ServiceException as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Service `init_localization_by_pose` call failed: {e}"
    except rospy.ROSException as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Service `init_localization_by_pose` call failed: {e}"  
    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

def download_map_file(map_name: str = ""):
    # 将地图文件下载到本地指定路径
    # 订阅一次/map话题，将得到的map数据保存为png格式

    """
    订阅一次/map话题，将地图数据保存为png格式图片
    """
    global MAP_FILE_FOLDER
    try:
        msg = rospy.wait_for_message('/map', OccupancyGrid)
        width = msg.info.width
        height = msg.info.height
        data = np.array(msg.data, dtype=np.int8).reshape((height, width))

        # 映射到图像灰度：0=白色，100=黑色，-1=灰色
        img = np.zeros((height, width), dtype=np.uint8)
        img[data == -1] = 128
        img[data == 0] = 255
        img[data == 100] = 0
        # 可选：线性插值灰度（处理 0~100 范围的值）
        mask = (data > 0) & (data < 100)
        img[mask] = 255 - (data[mask] * 255 // 100)

        # OpenCV 默认原点在左上，而 ROS 地图原点通常在左下 → 上下翻转图像
        img = cv2.flip(img, 0)

        # 保存为 PNG
        cv2.imwrite(MAP_FILE_FOLDER+"/"+map_name+".png", img)
        rospy.loginfo(f"地图已保存为 {MAP_FILE_FOLDER}/{map_name}.png")
        return True
    except Exception as e:
        rospy.logerr(f"Failed to download map file: {e}")
        return False


async def get_robot_position_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    payload = Payload(
        cmd="get_robot_position", data={"code":0}
    )
    try:
        # 获取base_link在map坐标系下的位置
        listener = tf.TransformListener()
        listener.waitForTransform("map", "base_link", rospy.Time(0), rospy.Duration(2.0))
        (trans, rot) = listener.lookupTransform("map", "base_link", rospy.Time(0))
        # trans为(x, y, z)
        x, y, z = trans

        # 获取地图信息
        map_msg = rospy.wait_for_message('/map', OccupancyGrid, timeout=2.0)
        origin = map_msg.info.origin
        resolution = map_msg.info.resolution
        width = map_msg.info.width
        height = map_msg.info.height

        # 这里的origin_grid_x和origin_grid_y表示map坐标系下(0,0)点在栅格坐标系下的坐标
        # 也就是map坐标系的(0,0)点对应的像素点
        origin_x = origin.position.x
        origin_y = origin.position.y

        origin_grid_x = int((0.0 - origin_x) / resolution)
        origin_grid_y = int((0.0 - origin_y) / resolution)

        origin_grid_y =  height - 1 - origin_grid_y

        # 将base_link的map坐标转换为栅格坐标
        grid_x = int((x - origin_x) / resolution)
        grid_y = int((y - origin_y) / resolution)

        # 转换为PNG图片上的像素坐标
        # PNG图片通过cv2.flip(img, 0)上下翻转，所以Y坐标需要转换
        png_x = grid_x
        png_y = height - 1 - grid_y

        payload.data["position"] = {
            "png_x": png_x,  # PNG图片上的X像素坐标
            "png_y": png_y,  # PNG图片上的Y像素坐标
            "origin_grid_x": origin_grid_x,  # 地图原点在栅格坐标系下的X
            "origin_grid_y": origin_grid_y,  # 地图原点在栅格坐标系下的Y
        }
        payload.data["msg"] = "Get robot position successfully"
    except Exception as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Failed to get robot position: {e}"
    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

async def get_all_maps_handler(
    websocket: websockets.WebSocketServerProtocol, data: dict
):
    payload = Payload(
        cmd="get_all_maps", data={"code":0}
    )
    try:
        service_name = 'get_all_maps'
        rospy.wait_for_service(service_name,timeout=3.0)
        get_all_maps_client = rospy.ServiceProxy(service_name, GetAllMaps)  
        
        # request   
        req = GetAllMapsRequest()

        # response
        res = get_all_maps_client(req)
        payload.data["maps"] = res.maps
        payload.data["msg"] = "Get all maps successfully"
    except rospy.ServiceException as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Service `get_all_maps` call failed: {e}"
    except rospy.ROSException as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Service `get_all_maps` call failed: {e}"
    except Exception as e:
        payload.data["code"] = 1
        payload.data["msg"] = f"Service `get_all_maps` call failed: {e}"
    response = Response(
        payload=payload,
        target=websocket,
    )
    response_queue.put(response)

# Add a function to clean up when a websocket connection is closed
def cleanup_websocket(websocket: websockets.WebSocketServerProtocol):
    if websocket in active_threads:
        active_threads[websocket].set()
        del active_threads[websocket]

# Add a new function to set the robot type
def set_robot_type(robot_type: str):
    global g_robot_type
    g_robot_type = robot_type

def set_folder_path(action_file_folder: str, upload_folder: str, map_file_folder: str):
    global ACTION_FILE_FOLDER, UPLOAD_FILES_FOLDER, MAP_FILE_FOLDER
    ACTION_FILE_FOLDER = action_file_folder
    UPLOAD_FILES_FOLDER = upload_folder
    MAP_FILE_FOLDER = map_file_folder
