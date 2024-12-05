import time
import os
import pwd
import signal
import yaml
from SimpleSDK import RUIWOTools

ruiwo = RUIWOTools()
config_file = 'config.yaml'

def get_home_path():
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user:
        try:
            pw = pwd.getpwnam(sudo_user)
            path = os.path.join(pw.pw_dir, ".config/lejuconfig")
            return path
        except KeyError:
            pass
    else:
        uid = os.getuid()
        try:
            pw = pwd.getpwuid(uid)
            path = os.path.join(pw.pw_dir, ".config/lejuconfig")
            return path
        except KeyError:
            pass
    return ""

def get_dev_id(config):
    DEV_IDs = [config['address'][f'Left_joint_arm_{i+1}'] for i in range(6)]
    DEV_IDs += [config['address'][f'Right_joint_arm_{i+1}'] for i in range(6)]
    DEV_IDs += [config['address']['Head_joint_low'] ]
    DEV_IDs += [config['address']['Head_joint_high'] ]
    return DEV_IDs

def save_zero_positions(config, zero_positions):
    config['zero_position']['Left_joint_arm'] = zero_positions[:6]
    config['zero_position']['Right_joint_arm'] = zero_positions[6:12]
    return config

def signal_handler(sig, frame):
    motor_set(1, joint_address_list)
    print("\n[RUIWO motor]:Close Canbus:", ruiwo.close_canbus())
    print('Exiting gracefully.')
    exit(0)

def motor_set(mode, joint_address_list):
    if mode == 0:
        for address in joint_address_list:
            state_mode = ruiwo.enter_motor_state(address)
            if isinstance(state_mode, list):
                print("[RUIWO motor]:ID:", address, "Enable: [Succeed]")
            else:
                print("[RUIWO motor]:ID:", address, "Enable: [", state_mode, "]")
            time.sleep(0.05)
    else:
        for address in joint_address_list:
            state = ruiwo.enter_reset_state(address)
            if isinstance(state, list):
                print("[RUIWO motor]:ID:", address, "Disable: [Succeed]")
            else:
                print("[RUIWO motor]:ID:", address, "Disable: [", state, "]")
            time.sleep(0.05)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    path = get_home_path()
    print(f"[RUIWO motor]:config.yaml path: {path}")
    if not path:
        print("Failed to get home path.")
        exit(1)
    config_path = os.path.join(path, config_file)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    # 多圈编码器模式
    try:
        multi_turn_encoder_mode = config['Multi-turn_Encoder_mode']
    except KeyError:
        multi_turn_encoder_mode = False
    if not multi_turn_encoder_mode:
        print("请先在配置文件里面打开多圈编码器模式。")
        exit(1)

    joint_address_list = get_dev_id(config)

    open_canbus = ruiwo.open_canbus()
    if not open_canbus:
        print("[RUIWO motor]:Canbus status: [", open_canbus, "]")
        exit(1)
    print("[RUIWO motor]:Canbus status: [", open_canbus, "]")

    zero_positions = []
    for address in joint_address_list:
        state = ruiwo.enter_motor_state(address)
        if isinstance(state, list):
            zero_positions.append(state[1])  # Assuming state[1] is the position
            print(f"[RUIWO motor]:ID: {address} Current position: {state[1]}")
        else:
            print(f"[RUIWO motor]:ID: {address} Failed to get position: {state}")
            zero_positions.append(0.0)

    with open(config_path, 'r') as file:
        config_lines = file.readlines()

    zero_position_start_idx = None
    for i, line in enumerate(config_lines):
        if 'zero_position:' in line:
            zero_position_start_idx = i
            break

    if zero_position_start_idx is not None:
        left_arm_start_idx = None
        right_arm_start_idx = None
        Head_joint_start_idx = None
        for i in range(zero_position_start_idx, len(config_lines)):
            if 'Left_joint_arm' in config_lines[i]:
                left_arm_start_idx = i
            elif 'Right_joint_arm' in config_lines[i]:
                right_arm_start_idx = i
            elif 'Head_joint' in config_lines[i]:
                Head_joint_start_idx = i

        if left_arm_start_idx is not None:
            config_lines[left_arm_start_idx + 1] = f"  - [{', '.join(f'{pos:.10f}' for pos in zero_positions[:6])}]\n"
        
        if right_arm_start_idx is not None:
            config_lines[right_arm_start_idx + 1] = f"  - [{', '.join(f'{pos:.10f}' for pos in zero_positions[6:12])}]\n"

        if Head_joint_start_idx is not None:
            config_lines[Head_joint_start_idx + 1] = f"  - [{', '.join(f'{pos:.10f}' for pos in zero_positions[12:14])}]\n"


    with open(config_path, 'w') as file:
        file.writelines(config_lines)

    print("[RUIWO motor]:Zero positions saved to config.yaml")

    # Disable motors
    motor_set(1, joint_address_list)

    ruiwo.close_canbus()
    print("[RUIWO motor]:Canbus status: [ Close ]")
    exit(0)
