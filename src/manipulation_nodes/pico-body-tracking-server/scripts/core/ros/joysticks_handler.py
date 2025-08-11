import enum
import time
from typing import Callable, Set
from kuavo_msgs.msg import JoySticks

class ButtonState(enum.Enum):
    IDLE = "IDLE"                   # 空闲
    PRESSED = "PRESSED"             # 点按
    PRESSING = "PRESSING"           # 按压中但未达到触发长按
    LONG_PRESSED = "LONG_PRESSED"   # 长按

class JoySticksHandler:
    def __init__(self) -> None:
        self.btn_names = ['X', 'Y', 'A', 'B']
        self.btn_pressed_time = {btn: 0.0 for btn in self.btn_names}
        self.btn_last_seq = {btn: 0 for btn in self.btn_names}
        self.btn_reported_state = {btn: None for btn in self.btn_names}  # Track last reported state
        self.LONG_PRESS_THRESHOLD = 0.5  # 长按阈值秒
        self.callbacks = {}

    def update(self, joy: JoySticks):
        key_combination = self._handle_buttons(joy)

        # if key_combination:
        #     color_map = {
        #         'IDLE': '\033[90m',             # 灰色
        #         'PRESSED': '\033[92m',          # 绿色
        #         'PRESSING': '\033[93m',         # 黄色
        #         'LONG_PRESSED': '\033[91m'      # 红色
        #     }
        #     colored_keys = []
        #     for key in key_combination:
        #         btn_name, state = key.split('_', 1)
        #         color = color_map.get(state, '\033[0m')
        #         colored_keys.append(f"{color}{key}\033[0m")
        #     print(f"Key combination: {', '.join(colored_keys)}")

        self._handle_key_combination_callback(key_combination, joy)

    def add_callback(self, name: str, key_combination: Set[str], callback: Callable[..., None]) -> None:
        if name in self.callbacks:
            print(f"\033[91mname: {name} already exists\033[0m")
        self.callbacks[name] = (key_combination, callback)

    def remove_callback(self, name: str) -> None:
        if name in self.callbacks:
            del self.callbacks[name]
        else:
            print(f"\033[91mname: {name} not found\033[0m")

    def _handle_buttons(self, joy: JoySticks) -> Set[str]:
        btn_seq = {
            'X': joy.left_first_button_pressed,
            'Y': joy.left_second_button_pressed,
            'A': joy.right_first_button_pressed,
            'B': joy.right_second_button_pressed
        }

        current_time = time.time()
        key_combination = set()

        for btn in self.btn_names:
            is_pressed = btn_seq[btn] == 1
            was_pressed = self.btn_last_seq[btn] == 1

            if is_pressed and not was_pressed:
                # Rising edge
                self.btn_pressed_time[btn] = current_time
                self.btn_reported_state[btn] = None

            elif not is_pressed and was_pressed:
                # Falling edge
                duration = current_time - self.btn_pressed_time[btn]
                if self.btn_reported_state[btn] is None:
                    if duration >= self.LONG_PRESS_THRESHOLD:
                        key_combination.add(f"{btn}_{ButtonState.LONG_PRESSED.value}")
                    else:
                        key_combination.add(f"{btn}_{ButtonState.PRESSED.value}")
                self.btn_pressed_time[btn] = 0.0
                self.btn_reported_state[btn] = None
                self.btn_last_seq[btn] = btn_seq[btn]
                continue

            elif is_pressed:
                # Holding state
                duration = current_time - self.btn_pressed_time[btn]
                if duration < self.LONG_PRESS_THRESHOLD:
                    key_combination.add(f"{btn}_{ButtonState.PRESSING.value}")
                elif duration >= self.LONG_PRESS_THRESHOLD and self.btn_reported_state[btn] is None:
                    key_combination.add(f"{btn}_{ButtonState.LONG_PRESSED.value}")
                    self.btn_reported_state[btn] = ButtonState.LONG_PRESSED

            else:
                key_combination.add(f"{btn}_{ButtonState.IDLE.value}")

            self.btn_last_seq[btn] = btn_seq[btn]

        return key_combination

    def _handle_key_combination_callback(self, key_combination: Set[str], joy: JoySticks) -> None:
        for name, (expected_keys, callback) in self.callbacks.items():
            if expected_keys == key_combination:
            # if expected_keys.issubset(key_combination):
                callback(key_combination, joy)
                break

if __name__ == "__main__":
    import rospy
    rospy.init_node("joy_button_handler")

    joy_button_handler = JoySticksHandler()

    def sub_callback(joy: JoySticks) -> None:
        joy_button_handler.update(joy)

    def callback1(keys: Set[str], joy: JoySticks) -> None:
        print(f"\033[91mcallback1: {keys}\033[0m")

    def callback2(keys: Set[str], joy: JoySticks) -> None:
        print(f"\033[91mcallback2: {keys}\033[0m")

    rospy.Subscriber("/pico/joy", JoySticks, sub_callback)
    joy_button_handler.add_callback("callback1", {"X_PRESSED", "Y_PRESSED"}, callback1)
    joy_button_handler.add_callback("callback2", {"Y_PRESSED"}, callback2)
    rospy.spin()