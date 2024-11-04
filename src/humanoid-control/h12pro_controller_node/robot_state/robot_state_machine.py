import json
import robot_state.before_callback as before_callback
from transitions import Machine
from utils.utils import read_json_file

robot_state_config = read_json_file("robot_state/robot_state.json")

states = robot_state_config["states"]
transitions = robot_state_config["transitions"]


class RobotStateMachine(object):
    def __init__(self, **kwargs):
        self.machine = Machine(model=self, **kwargs)
        self.kuavo_pid = None
        self.setup_transitions()

    def setup_transitions(self):
        """
        Setup transitions, register before callback from external module
        """
        for transition in transitions:
            source = transition["source"]
            dest = transition["dest"]
            trigger = transition["trigger"]
            callback = getattr(before_callback, transition["before"], None)
            if callback:
                self.machine.add_transition(
                    trigger=trigger,
                    source=source,
                    dest=dest,
                    before=callback,
                )


robot_state_machine = RobotStateMachine(
    states=states,
    initial="initial",
    send_event=True,
    auto_transitions=False,
)
