import json
import serial
import serial.tools.list_ports


def read_json_file(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def map_value(value, O_min, O_max, N_min, N_max):
    return (value - O_min) * (N_max - N_min) / (O_max - O_min) + N_min


def find_and_send():
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        if "CP2102 USB to UART Bridge Controller" in port.description:
            print("设备: {}".format(port.device))
            print("名称: {}".format(port.name))
            print("描述: {}".format(port.description))
            print("物理位置: {}".format(port.location))
            print("制造商: {}".format(port.manufacturer))
            print("串口号: {}".format(port.serial_number))
            return port
    return 0


def open_serial_port(serial_port):
    try:
        ser = serial.Serial(serial_port.device, baudrate=9600, timeout=1)
        print(f"已成功打开串口 {serial_port.device}")
        return ser
    except Exception as e:
        print(f"ERROR: 打开串口 {serial_port.device} 时出错：{e}")
        return None


def send_data_to_port(ser, data):
    try:
        ser.write(data)

    except Exception as e:
        print(f"发送数据到串口时出错：{e}")
