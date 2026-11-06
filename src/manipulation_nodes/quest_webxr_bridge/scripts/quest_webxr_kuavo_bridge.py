#!/usr/bin/env python3
"""Quest WebXR bridge with guarded Kuavo v49 staging and handoff."""

import json
import os
import threading
import time

import numpy as np
import rosnode
import rospy
import tf2_ros
from kuavo_msgs.msg import robotHandPosition, sensorsData, twoArmHandPoseCmd
from kuavo_msgs.srv import changeArmCtrlMode
from kuavo_ros_interfaces.msg import robotHeadMotionData
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, String
from std_srvs.srv import SetBool, SetBoolResponse, Trigger, TriggerResponse

from quest_webxr_bridge.arm_safety import (
    RecoveryReadinessGate, adapter_fault_is_recoverable, max_abs_joint_error,
    recovery_target_safe, safety_fault_recovery_pose,
)
from quest_webxr_bridge.bridge_core import (
    ArmRetargeter, HeadRetargeter, PoseStabilityWindow,
    base_alignment_from_head,
)
from quest_webxr_bridge.gesture_control import (
    GestureSafetyController, HUD_CODES, RECOVERY_DETAIL_CODES,
    both_hands_pinching, hand_open_fist_score, palm_up_score, valid_hand,
)
from quest_webxr_bridge.hand_retargeter import FingerRetargeter
from quest_webxr_bridge.math3d import (
    quaternion_xyzw, valid_transform, webxr_hand_frame, webxr_transform,
)
from quest_webxr_bridge.recording_contract import ARM_JOINT_NAMES
from quest_webxr_bridge.webxr_server import WebXRHandServer


def _vector_param(name, default, size):
    value = np.asarray(rospy.get_param(name, default), dtype=float).reshape(-1)
    if value.size != size or not np.all(np.isfinite(value)):
        raise ValueError("{} must contain {} finite numbers".format(name, size))
    return value


class QuestWebXRKuavoBridge:
    WAITING_FOR_START = "WAITING_FOR_START"
    WAITING_FOR_RELEASE = "WAITING_FOR_RELEASE"
    PRECHECK_AUTO_MOTION = "PRECHECK_AUTO_MOTION"
    WAIT_L_REACHED = "WAIT_L_REACHED"
    CALIBRATING_NEUTRAL = "CALIBRATING_NEUTRAL"
    CHECK_IK_HANDOFF = "CHECK_IK_HANDOFF"
    ACTIVE = "ACTIVE"
    PAUSED_HOLD = "PAUSED_HOLD"
    EXIT_CONFIRM_RELEASE = "EXIT_CONFIRM_RELEASE"
    EXIT_CONFIRM_PENDING = "EXIT_CONFIRM_PENDING"
    RECOVERABLE_SAFETY_HOLD = "RECOVERABLE_SAFETY_HOLD"
    RECOVERY_RAMP = "RECOVERY_RAMP"
    SAFETY_FAULT = "AUTO_MOTION_FAULT_HOLD"
    FAULT_RECOVERY_PRECHECK = "FAULT_RECOVERY_PRECHECK"

    def __init__(self):
        self.lock = threading.RLock()
        requested_enable = bool(rospy.get_param("~enable_output", False))
        self.enabled = False
        self.state = (
            self.PRECHECK_AUTO_MOTION if requested_enable else self.WAITING_FOR_START
        )
        self.state_entered = time.monotonic()
        self.fault_reason = None
        self.pending_start_kind = "start"
        self.tracking_timeout = float(rospy.get_param("~tracking_timeout", 0.25))
        self.feedback_timeout = float(rospy.get_param("~feedback_timeout", 0.30))
        self.base_frame = rospy.get_param("~base_frame", "base_link")
        self.position_frames = {
            "left": rospy.get_param("~left_position_frame", "zarm_l6_link"),
            "right": rospy.get_param("~right_position_frame", "zarm_r6_link"),
        }
        self.orientation_frames = {
            "left": rospy.get_param(
                "~left_orientation_frame", "zarm_l7_end_effector"
            ),
            "right": rospy.get_param(
                "~right_orientation_frame", "zarm_r7_end_effector"
            ),
        }
        self.arm_topic = rospy.get_param(
            "~arm_command_topic", "/ik/two_arm_hand_pose_cmd"
        )
        self.hand_topic = rospy.get_param(
            "~hand_command_topic", "/control_robot_hand_position"
        )
        self.arm_frame = int(rospy.get_param("~arm_frame", 2))
        self.enable_arm = bool(rospy.get_param("~enable_arm", True))
        self.enable_hand = bool(rospy.get_param("~enable_hand", True))
        self.enable_head = bool(rospy.get_param("~enable_head", True))
        self.arm_mode_services = list(rospy.get_param(
            "~safe_arm_mode_services",
            ["/arm_traj_change_mode", "/humanoid_change_arm_ctrl_mode"],
        ))
        if not self.arm_mode_services:
            raise ValueError("~safe_arm_mode_services cannot be empty")
        self.selected_arm_mode_service = None
        self.adapter_node = rospy.get_param(
            "~adapter_node", "/quest_webxr_control_contract_adapter"
        )

        axis_mapping = _vector_param(
            "~axis_mapping", [1, 0, 0, 0, 1, 0, 0, 0, 1], 9
        ).reshape(3, 3)
        self.static_axis_mapping = axis_mapping.copy()
        self.arm_retargeter = ArmRetargeter(
            position_scale=_vector_param("~position_scale", [1, 1, 1], 3),
            axis_mapping=axis_mapping,
            max_linear_speed=float(rospy.get_param("~max_linear_speed", 0.60)),
            max_angular_speed=float(rospy.get_param("~max_angular_speed", 1.20)),
            workspace_min=_vector_param("~workspace_min", [0.10, -0.65, -0.25], 3),
            workspace_max=_vector_param("~workspace_max", [0.75, 0.65, 0.65], 3),
            max_input_position_jump=float(
                rospy.get_param("~max_input_position_jump", 0.20)
            ),
            max_input_rotation_jump=float(
                rospy.get_param("~max_input_rotation_jump", 0.80)
            ),
            shoulder_positions={
                "left": _vector_param(
                    "~left_shoulder_position", [-0.017499853, 0.2927, 0.4245], 3
                ),
                "right": _vector_param(
                    "~right_shoulder_position", [-0.017499853, -0.2927, 0.4245], 3
                ),
            },
            min_shoulder_reach=float(
                rospy.get_param("~min_shoulder_reach", 0.15)
            ),
            max_shoulder_reach=float(
                rospy.get_param("~max_shoulder_reach", 0.62)
            ),
            midline_margin=float(rospy.get_param("~midline_margin", 0.05)),
            body_exclusion_front=float(
                rospy.get_param("~body_exclusion_front", 0.18)
            ),
            body_exclusion_half_width=float(
                rospy.get_param("~body_exclusion_half_width", 0.20)
            ),
        )
        self.head_retargeter = HeadRetargeter(
            axis_mapping=axis_mapping,
            yaw_limits=_vector_param("~head_yaw_limits", [-90, 90], 2),
            pitch_limits=_vector_param("~head_pitch_limits", [-20, 30], 2),
            yaw_sign=float(rospy.get_param("~head_yaw_sign", 1.0)),
            pitch_sign=float(rospy.get_param("~head_pitch_sign", 1.0)),
        )
        thumb_aux_dynamic = bool(rospy.get_param("~thumb_aux_dynamic", False))
        self.finger_retargeter = FingerRetargeter(
            thumb_swap=bool(rospy.get_param("~thumb_swap", False)),
            thumb_aux_value=(
                None if thumb_aux_dynamic
                else int(rospy.get_param("~thumb_aux_value", 100))
            ),
            finger_close_denominators=rospy.get_param(
                "~finger_close_denominators", {}
            ),
        )
        neutral_hand = _vector_param(
            "~neutral_hand_position", [0, 0, 0, 0, 0, 0], 6
        )
        if np.any(neutral_hand < 0.0) or np.any(neutral_hand > 100.0):
            raise ValueError("~neutral_hand_position must stay inside [0, 100]")
        self.neutral_hand_command = np.rint(neutral_hand).astype(np.uint8)
        self.calibration_window = PoseStabilityWindow(
            hold_seconds=float(rospy.get_param("~calibration_hold", 1.0)),
            min_samples=int(rospy.get_param("~calibration_min_samples", 30)),
            max_position_spread=float(
                rospy.get_param("~calibration_max_position_spread", 0.015)
            ),
            max_rotation_spread=float(
                rospy.get_param("~calibration_max_rotation_spread", 0.12)
            ),
        )
        self.calibration_prepare_hold = float(
            rospy.get_param("~calibration_prepare_hold", 3.0)
        )
        if self.calibration_prepare_hold < 0.0:
            raise ValueError("~calibration_prepare_hold cannot be negative")
        self.enable_gesture_control = bool(
            rospy.get_param("~enable_gesture_control", True)
        )
        self.gesture = GestureSafetyController(
            enabled=False,
            start_hold=float(rospy.get_param("~gesture_start_hold", 5.0)),
            stop_hold=float(rospy.get_param("~gesture_stop_hold", 3.0)),
            release_hold=float(rospy.get_param("~gesture_release_hold", 1.0)),
            cooldown=float(rospy.get_param("~gesture_cooldown", 2.0)),
            valid_need=int(rospy.get_param("~gesture_valid_frames", 3)),
            invalid_grace=float(rospy.get_param("~gesture_invalid_grace", 0.8)),
            open_ratio=float(rospy.get_param("~gesture_open_ratio", 3.0)),
            fist_ratio=float(rospy.get_param("~gesture_fist_ratio", 2.35)),
            palm_up_dot=float(rospy.get_param("~gesture_palm_up_dot", 0.65)),
        )
        self.pinch_threshold = float(rospy.get_param("~exit_pinch_ratio", 0.20))
        self.pinch_hold = float(rospy.get_param("~exit_pinch_hold", 2.0))
        self.exit_release_hold = float(
            rospy.get_param("~exit_release_hold", 1.0)
        )
        self.exit_fist_hold = float(rospy.get_param("~exit_fist_hold", 3.0))
        self.exit_gesture_t0 = None

        self.safe_lower = _vector_param(
            "~pose_config/limits/preview_lower_deg",
            [-175, -15, -85, -145, -85, -70, -35,
             -175, -115, -85, -145, -85, -35, -35], 14,
        )
        self.safe_upper = _vector_param(
            "~pose_config/limits/preview_upper_deg",
            [85, 115, 85, -5, 85, 35, 35,
             85, 15, 85, -5, 85, 70, 35], 14,
        )
        self.poses = {
            "home": _vector_param(
                "~pose_config/poses/home/nominal_deg",
                [20, 0, 0, -30, 0, 0, 0, 20, 0, 0, -30, 0, 0, 0], 14,
            ),
            "t": _vector_param(
                "~pose_config/poses/t/target_deg",
                [0, 90, 0, -5, 0, 0, 0, 0, -90, 0, -5, 0, 0, 0], 14,
            ),
            "t_bent": _vector_param(
                "~pose_config/poses/t_bent/target_deg",
                [0, 90, 0, -85, 0, 0, 0, 0, -90, 0, -85, 0, 0, 0], 14,
            ),
            "l": _vector_param(
                "~pose_config/poses/l/target_deg",
                [-45.042, 19.388, -30.563, -99.291, 25.290, -10.930, 34,
                 -45.042, -19.388, 30.563, -99.291, -25.290, 10.930, 34], 14,
            ),
        }
        for name, pose in self.poses.items():
            if np.any(pose < self.safe_lower) or np.any(pose > self.safe_upper):
                raise ValueError("pose {} exceeds v49 safe envelope".format(name))
        self.pose_tolerance = float(
            rospy.get_param("~auto_pose_tolerance_deg", 2.0)
        )
        self.pose_hold = float(rospy.get_param("~auto_pose_hold_s", 1.0))
        self.auto_speed = float(rospy.get_param("~auto_joint_speed_deg_s", 5.0))
        self.auto_timeout_margin = float(
            rospy.get_param("~auto_motion_timeout_margin_s", 8.0)
        )
        self.handoff_frames_required = int(
            rospy.get_param("~ik_handoff_valid_frames", 10)
        )
        self.handoff_timeout = float(rospy.get_param("~ik_handoff_timeout_s", 10.0))
        self.recovery_envelope_margin = float(
            rospy.get_param("~recovery_envelope_margin_deg", 0.5)
        )
        self.recovery_candidate_delta = float(
            rospy.get_param("~recovery_candidate_delta_deg", 3.0)
        )
        self.recovery_max_projection = float(
            rospy.get_param("~recovery_max_projection_m", 0.002)
        )
        self.recovery_complete_error = float(
            rospy.get_param("~recovery_complete_error_deg", 3.0)
        )
        # Original 20-degree recovery target-lead guard, kept commented for
        # rollback after the unrestricted low-speed recovery trial:
        # self.recovery_dynamic_follow_error = float(
        #     rospy.get_param("~recovery_dynamic_follow_error_deg", 20.0)
        # )
        recovery_complete_hold = float(
            rospy.get_param("~recovery_complete_hold_s", 0.75)
        )
        # Enter low-speed recovery as soon as enough new safe IK reports have
        # arrived.  This gate deliberately has no stationary hold interval:
        # the operator may keep moving while the recovery limiter follows the
        # live target derived from the original L-pose calibration anchor.
        self.recovery_gate = RecoveryReadinessGate(
            valid_frames=int(rospy.get_param("~recovery_valid_frames", 5)),
            hold_seconds=0.0,
        )
        # The final <=3 degree check has no hidden multi-frame phase: its
        # entire stability interval is the countdown shown in the headset.
        self.recovery_completion_gate = RecoveryReadinessGate(
            valid_frames=1,
            hold_seconds=recovery_complete_hold,
        )
        if (self.recovery_envelope_margin < 0.0 or
                self.recovery_candidate_delta <= 0.0 or
                self.recovery_max_projection < 0.0 or
                self.recovery_complete_error <= 0.0):
            # Original validation clause for the disabled target-lead guard:
            # or self.recovery_dynamic_follow_error <=
            # self.recovery_complete_error
            raise ValueError("recovery safety thresholds are invalid")

        cert_file = os.path.expanduser(rospy.get_param("~cert_file", ""))
        key_file = os.path.expanduser(rospy.get_param("~key_file", ""))
        if not os.path.isfile(cert_file) or not os.path.isfile(key_file):
            raise RuntimeError(
                "WebXR HTTPS requires valid ~cert_file and ~key_file; got {!r}, {!r}".format(
                    cert_file, key_file
                )
            )
        self.webxr = WebXRHandServer(
            host=rospy.get_param("~host", "0.0.0.0"),
            port=int(rospy.get_param("~port", 8012)),
            cert_file=cert_file,
            key_file=key_file,
            fps=int(rospy.get_param("~webxr_fps", 60)),
        )

        self.tf_buffer = tf2_ros.Buffer(cache_time=rospy.Duration(2.0))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.arm_pub = rospy.Publisher(self.arm_topic, twoArmHandPoseCmd, queue_size=1)
        self.hand_pub = rospy.Publisher(self.hand_topic, robotHandPosition, queue_size=1)
        self.mode_pub = rospy.Publisher(
            "/quest_webxr/arm_command_mode", String, queue_size=1, latch=True
        )
        self.hand_follow_pub = rospy.Publisher(
            "/quest_webxr/hand_follow_enabled", Bool, queue_size=1, latch=True
        )
        self.auto_target_pub = rospy.Publisher(
            "/quest_webxr/auto_arm_target", JointState, queue_size=1, latch=True
        )
        self.head_topic = rospy.get_param("~head_command_topic", "/robot_head_motion_data")
        self.head_pub = rospy.Publisher(
            self.head_topic, robotHeadMotionData, queue_size=1, latch=True
        )
        self.status_pub = rospy.Publisher("~status", String, queue_size=1, latch=True)
        self.feedback_sub = rospy.Subscriber(
            "/sensors_data_raw", sensorsData, self._feedback_callback,
            queue_size=1, tcp_nodelay=True,
        )
        self.adapter_status_sub = rospy.Subscriber(
            "/quest_webxr/arm_adapter_status", String,
            self._adapter_status_callback, queue_size=1,
        )
        self.enable_srv = rospy.Service("~set_enabled", SetBool, self._set_enabled)
        self.calibrate_srv = rospy.Service("~recalibrate", Trigger, self._recalibrate)

        self.feedback = None
        self.feedback_time = 0.0
        self.adapter_status = {}
        self.adapter_status_serial = 0
        self.handoff_last_status_serial = -1
        self.last_processed_timestamp = 0.0
        self.last_sample_fresh = False
        self.last_gesture_input_valid = False
        self.last_head_timestamp = 0.0
        self.latest_wrists = None
        self.latest_points = None
        self.latest_head = None
        self.last_finger_command = {
            "left": self.neutral_hand_command.copy(),
            "right": self.neutral_hand_command.copy(),
        }
        self.last_status = None
        self.last_status_publish = 0.0
        self.auto_sequence = []
        self.auto_sequence_kind = None
        self.auto_index = 0
        self.auto_target = None
        self.auto_reached_since = None
        self.auto_deadline = None
        self.alignment_pose_name = "l"
        self.precheck_mode_requested = False
        self.precheck_switched = False
        self.precheck_publishers_checked = False
        self.handoff_valid_frames = 0
        self.alignment_countdown_started = None
        self.recovery_reason = None
        self.recovery_phase = None
        self.recovery_abort_t0 = None
        self.fault_recovery_source_reason = None
        self.hand_follow_enabled = False

        self._publish_adapter_mode("off")
        self._publish_hand_follow(False)
        self._publish_startup_head()
        self.webxr.start()
        rospy.on_shutdown(self.webxr.close)
        update_hz = float(rospy.get_param("~publish_rate", 100.0))
        self.timer = rospy.Timer(rospy.Duration(1.0 / update_hz), self._tick)
        self._publish_status(self.state, force=True)

    def _feedback_callback(self, message):
        values = list(message.joint_data.joint_q)
        if len(values) < 26:
            return
        feedback = np.degrees(np.asarray(values[12:26], dtype=float))
        if np.all(np.isfinite(feedback)):
            with self.lock:
                self.feedback = feedback
                self.feedback_time = time.monotonic()

    def _adapter_status_callback(self, message):
        try:
            status = json.loads(message.data)
        except (TypeError, ValueError):
            return
        with self.lock:
            self.adapter_status = status
            self.adapter_status_serial += 1

    def _publish_startup_head(self):
        message = robotHeadMotionData()
        # Kuavo's native controller convention is +pitch = look down.  The
        # real Quest3 collection helper also uses [yaw=0, pitch=+25] degrees.
        message.joint_data = [0.0, float(rospy.get_param("~startup_head_pitch_deg", 25.0))]
        self.head_pub.publish(message)

    def _publish_adapter_mode(self, mode):
        self.mode_pub.publish(String(data=mode))

    def _publish_hand_follow(self, enabled):
        self.hand_follow_enabled = bool(enabled)
        self.hand_follow_pub.publish(Bool(data=self.hand_follow_enabled))

    def _set_state(self, state):
        self.state = state
        self.state_entered = time.monotonic()
        self._publish_hand_follow(state in (
            self.ACTIVE,
            self.RECOVERABLE_SAFETY_HOLD,
            self.RECOVERY_RAMP,
        ))
        rospy.loginfo("WebXR state -> %s", state)

    def _set_enabled(self, request):
        with self.lock:
            if request.data:
                self.pending_start_kind = "start"
                self._begin_precheck()
                message = "guarded T -> T_BENT -> L startup requested"
            else:
                self._pause("ROS service")
                message = "WebXR output paused; adapter is holding the measured arm pose"
            self._publish_status(self.state, force=True)
        return SetBoolResponse(success=True, message=message)

    def _recalibrate(self, _request):
        with self.lock:
            self.pending_start_kind = "realign"
            self._begin_precheck()
        return TriggerResponse(
            success=True,
            message="guarded move to L and neutral recalibration requested",
        )

    def _change_arm_mode(self, mode):
        errors = []
        candidates = list(self.arm_mode_services)
        if self.selected_arm_mode_service in candidates:
            candidates.remove(self.selected_arm_mode_service)
            candidates.insert(0, self.selected_arm_mode_service)
        for service in candidates:
            try:
                rospy.wait_for_service(service, timeout=0.75)
                response = rospy.ServiceProxy(
                    service, changeArmCtrlMode
                )(control_mode=mode)
                if hasattr(response, "result") and not response.result:
                    raise rospy.ServiceException("service returned result=false")
                self.selected_arm_mode_service = service
                rospy.loginfo("Arm mode %d set through %s", mode, service)
                return True
            except (rospy.ROSException, rospy.ServiceException) as error:
                errors.append("{}: {}".format(service, error))
        rospy.logerr("No usable arm-mode service: %s", "; ".join(errors))
        return False

    def _active_arm_publishers(self):
        try:
            result = rospy.get_master().getSystemState()
            # rosgraph.Master unwraps the XML-RPC status triplet, while some
            # older proxies expose it verbatim. Support both ROS Noetic forms.
            if (len(result) == 3 and isinstance(result[0], int)):
                code, _message, state = result
                if code != 1:
                    return ["ROS_MASTER_QUERY_FAILED"]
            else:
                state = result
            publishers = dict(state[0]).get("/kuavo_arm_traj", [])
        except Exception as error:  # XML-RPC transport errors vary by ROS release.
            rospy.logerr("Could not inspect /kuavo_arm_traj publishers: %s", error)
            return ["ROS_MASTER_QUERY_FAILED"]
        external = []
        for node in publishers:
            if node == self.adapter_node or node.endswith("/" + self.adapter_node.strip("/")):
                continue
            try:
                alive = rosnode.rosnode_ping(node, max_count=1, verbose=False)
            except Exception:
                alive = False
            if alive:
                external.append(node)
        return external

    def _feedback_ready(self):
        return bool(
            self.feedback is not None and
            time.monotonic() - self.feedback_time <= self.feedback_timeout and
            np.all(self.feedback >= self.safe_lower - 0.5) and
            np.all(self.feedback <= self.safe_upper + 0.5)
        )

    def _begin_precheck(self, state=None):
        self.enabled = False
        if state != self.FAULT_RECOVERY_PRECHECK:
            self.fault_recovery_source_reason = None
        self.fault_reason = None
        self.recovery_reason = None
        self.recovery_phase = None
        self.recovery_abort_t0 = None
        self._reset_recovery_gate()
        self.alignment_countdown_started = None
        self.precheck_mode_requested = False
        self.precheck_switched = False
        self.precheck_publishers_checked = False
        self.calibration_window.reset()
        self.arm_retargeter.reset()
        self.head_retargeter.reset()
        self.finger_retargeter.reset()
        self._set_state(state or self.PRECHECK_AUTO_MOTION)

    def _process_precheck(self):
        if os.environ.get("ROBOT_VERSION") != "49":
            self._fault("ROBOT_VERSION_MUST_BE_49")
            return
        if not bool(rospy.get_param("/only_half_up_body", False)):
            self._fault("ONLY_HALF_UP_BODY_REQUIRED")
            return
        if not self._feedback_ready():
            return
        if not self.precheck_publishers_checked:
            external = self._active_arm_publishers()
            if external:
                self._fault("EXTERNAL_ARM_PUBLISHERS: {}".format(",".join(external)))
                return
            self.precheck_publishers_checked = True
        if not self.precheck_mode_requested:
            self._publish_adapter_mode("hold")
            self.precheck_mode_requested = True
            return
        if self.adapter_status.get("mode") != "hold":
            if time.monotonic() - self.state_entered > 3.0:
                self._fault("COMMAND_ADAPTER_DID_NOT_ENTER_HOLD")
            return
        if not self.precheck_switched:
            if not self._change_arm_mode(2):
                self._fault("ARM_MODE_2_SWITCH_FAILED")
                return
            self.precheck_switched = True
        if self.pending_start_kind == "fault_recovery":
            recovery_pose = safety_fault_recovery_pose(
                self.fault_recovery_source_reason
            )
            if recovery_pose is None:
                self._fault("FAULT_NOT_GESTURE_RECOVERABLE")
                return
            self._begin_auto_sequence(
                "fault_recovery", [recovery_pose]
            )
        elif self.pending_start_kind == "realign":
            self._begin_auto_sequence("realign", ["l"])
        else:
            self._begin_auto_sequence("start", ["t", "t_bent", "l"])

    def _pose_state_name(self, kind, pose):
        prefix = "RETURN_" if kind == "exit" else (
            "REALIGN_" if kind == "realign" else ""
        )
        return "{}MOVE_TO_{}".format(prefix, pose.upper())

    def _begin_auto_sequence(self, kind, poses):
        self.auto_sequence_kind = kind
        self.auto_sequence = list(poses)
        if kind != "exit":
            self.alignment_pose_name = self.auto_sequence[-1]
        self.auto_index = 0
        self._start_auto_pose(self.auto_sequence[0])

    def _joint_state(self, position):
        message = JointState()
        message.header.stamp = rospy.Time.now()
        message.header.frame_id = self.base_frame
        message.name = list(ARM_JOINT_NAMES)
        message.position = np.asarray(position, dtype=float).tolist()
        return message

    def _start_auto_pose(self, pose_name):
        target = self.poses[pose_name]
        self.auto_target = target.copy()
        self.auto_reached_since = None
        max_distance = (
            max_abs_joint_error(self.feedback, target)
            if self.feedback is not None else 180.0
        )
        self.auto_deadline = (
            time.monotonic() + max_distance / max(self.auto_speed, 1e-6) +
            self.auto_timeout_margin
        )
        self.auto_target_pub.publish(self._joint_state(target))
        self._publish_adapter_mode("auto")
        self._set_state(self._pose_state_name(self.auto_sequence_kind, pose_name))

    def _process_auto_motion(self):
        # Automatic arm staging never inherits the fist/pinch that selected
        # the transition.  Keep both dexterous hands in their neutral open
        # command while returning to L or exiting to HOME/mode 1.
        self._publish_neutral_hands()
        if (self.adapter_status.get("mode") == "auto" and
                self.adapter_status.get("fault")):
            self._fault("ADAPTER_{}".format(self.adapter_status["fault"]))
            return
        if not self._feedback_ready():
            self.auto_reached_since = None
            if time.monotonic() > self.auto_deadline:
                self._fault("AUTO_MOTION_FEEDBACK_TIMEOUT")
            return
        error = max_abs_joint_error(self.feedback, self.auto_target)
        now = time.monotonic()
        if error <= self.pose_tolerance:
            if self.auto_reached_since is None:
                self.auto_reached_since = now
            elif now - self.auto_reached_since >= self.pose_hold:
                self.auto_index += 1
                if self.auto_index < len(self.auto_sequence):
                    self._start_auto_pose(self.auto_sequence[self.auto_index])
                else:
                    self._finish_auto_sequence()
        else:
            self.auto_reached_since = None
        if now > self.auto_deadline:
            self._fault(
                "AUTO_MOTION_TIMEOUT error={:.2f}deg".format(error)
            )

    def _finish_auto_sequence(self):
        kind = self.auto_sequence_kind
        self._publish_adapter_mode("hold")
        if kind == "exit":
            if not self._change_arm_mode(1):
                self._fault("ARM_MODE_1_SWITCH_FAILED")
                return
            self._publish_adapter_mode("off")
            self.enabled = False
            self.gesture.force_enabled(False, time.monotonic())
            self._set_state(self.WAITING_FOR_START)
            return
        self.calibration_window.reset()
        self.alignment_countdown_started = None
        self._set_state(self.WAIT_L_REACHED)

    def _pause(self, source):
        self.enabled = False
        self.recovery_phase = None
        self.recovery_abort_t0 = None
        self._reset_recovery_gate()
        self._publish_adapter_mode("hold")
        self.gesture.force_enabled(False, time.monotonic())
        self.exit_gesture_t0 = None
        self._set_state(self.PAUSED_HOLD)
        rospy.logwarn("WebXR paused by %s; arm and fingers no longer follow WebXR", source)

    def _begin_recoverable_hold(self, reason):
        """Hold measured motion while safe WebXR/IK candidates are reacquired."""
        now = time.monotonic()
        self.enabled = False
        self.recovery_reason = str(reason)
        self.recovery_phase = "seek_safe"
        self.recovery_abort_t0 = None
        self._reset_recovery_gate()
        self._publish_adapter_mode("hold")
        self.gesture.force_enabled(False, now)
        self._set_state(self.RECOVERABLE_SAFETY_HOLD)
        rospy.logwarn(
            "WebXR recoverable safety hold: %s; move hands back to a safe pose",
            reason,
        )

    def _reset_recovery_gate(self, require_new_status=False):
        self.recovery_gate.reset()
        self.recovery_completion_gate.reset()
        if require_new_status:
            self.recovery_gate.last_serial = self.adapter_status_serial

    def _process_recovery_abort_gesture(self, now, points):
        scores = [
            hand_open_fist_score(points[side]) for side in ("left", "right")
        ]
        both_fist = all(
            score is not None and score < self.gesture.fist_ratio
            for score in scores
        )
        if not both_fist:
            self.recovery_abort_t0 = None
            return False
        if self.recovery_abort_t0 is None:
            self.recovery_abort_t0 = now
            # Starting the explicit abort gesture must never let a recovery
            # ramp continue moving while the operator is deciding to pause.
            # It is also a menu gesture, so do not forward the closed-fist
            # command to the robot fingers.
            self._publish_neutral_hands()
            self._publish_adapter_mode("hold")
            self.recovery_phase = "seek_safe"
            self._set_state(self.RECOVERABLE_SAFETY_HOLD)
            self._reset_recovery_gate(require_new_status=True)
        elapsed = now - self.recovery_abort_t0
        self._update_named_hud(
            "RECOVERY_ABORT_COUNTDOWN",
            self.gesture.stop_hold - elapsed,
            elapsed / max(self.gesture.stop_hold, 1e-6),
        )
        if elapsed >= self.gesture.stop_hold:
            self._pause("two-fist recovery abort gesture")
        return True

    def _recovery_target_safe(self, require_handoff=False,
                              maximum_follow_error=None):
        """Check conditions that permit actual low-speed recovery motion."""
        return recovery_target_safe(
            self.adapter_status,
            feedback_ready=self._feedback_ready(),
            feedback_timeout=self.feedback_timeout,
            ik_timeout=self.tracking_timeout,
            minimum_envelope_margin=self.recovery_envelope_margin,
            constraint_projection=self.arm_retargeter.max_constraint_projection,
            maximum_constraint_projection=self.recovery_max_projection,
            require_handoff=require_handoff,
            maximum_follow_error=maximum_follow_error,
        )

    def _recovery_candidate_safe(self):
        """Require consecutive safe live targets before low-speed pursuit.

        The target may move between reports.  The delta check rejects IK
        branch discontinuities; it is not a stationary-hand requirement.
        Target distance from measured feedback is deliberately unrestricted;
        the recovery limiter alone bounds the physical pursuit speed.
        """
        status = self.adapter_status
        delta = status.get("ik_target_delta_deg")
        return bool(
            self._recovery_target_safe() and
            # Original 20-degree entry guard, kept for rollback:
            # self._recovery_target_safe(
            #     maximum_follow_error=self.recovery_dynamic_follow_error,
            # ) and
            delta is not None and
            float(delta) <= self.recovery_candidate_delta
        )

    def _recovery_blocker(self, require_handoff=False,
                          require_stable=False,
                          maximum_follow_error=None):
        """Return one compact HUD reason for a candidate that is not ready."""
        status = self.adapter_status
        fault = str(status.get("fault") or "")
        fault_details = {
            "FEEDBACK_OUTSIDE_SAFE_ENVELOPE": "FEEDBACK_ENVELOPE",
            "IK_TARGET_OUTSIDE_SAFE_ENVELOPE": "JOINT_LIMIT",
            "IK_TARGET_JUMP": "IK_JUMP",
            "IK_TARGET_STALE": "IK_STALE",
            "RECOVERY_TARGET_LEAD": "IK_DISCONTINUITY",
            "TRACKING_ERROR": "FOLLOW_ERROR",
        }
        if fault in fault_details:
            return RECOVERY_DETAIL_CODES[fault_details[fault]]
        if not self._feedback_ready():
            return RECOVERY_DETAIL_CODES["FEEDBACK"]
        feedback_age = status.get("feedback_age_s")
        if feedback_age is None or float(feedback_age) > self.feedback_timeout:
            return RECOVERY_DETAIL_CODES["FEEDBACK"]
        ik_age = status.get("ik_target_age_s")
        if ik_age is None or float(ik_age) > self.tracking_timeout:
            return RECOVERY_DETAIL_CODES["IK_STALE"]
        if (self.arm_retargeter.max_constraint_projection >
                self.recovery_max_projection):
            return RECOVERY_DETAIL_CODES["WORKSPACE_LIMIT"]
        margin = status.get("ik_envelope_margin_deg")
        if margin is None or float(margin) < self.recovery_envelope_margin:
            return RECOVERY_DETAIL_CODES["JOINT_LIMIT"]
        if maximum_follow_error is not None:
            follow_error = status.get("ik_handoff_error_deg")
            if (follow_error is None or
                    float(follow_error) > float(maximum_follow_error)):
                return RECOVERY_DETAIL_CODES["IK_DISCONTINUITY"]
        if require_stable:
            delta = status.get("ik_target_delta_deg")
            if delta is None or float(delta) > self.recovery_candidate_delta:
                return RECOVERY_DETAIL_CODES["IK_UNSTABLE"]
        if require_handoff and not status.get("ik_handoff_ready", False):
            return RECOVERY_DETAIL_CODES["IK_DISCONTINUITY"]
        if "INPUT_JUMP" in str(self.recovery_reason or ""):
            return RECOVERY_DETAIL_CODES["INPUT_JUMP"]
        return RECOVERY_DETAIL_CODES["NONE"]

    def _handle_tracking_unavailable(self, now, reason):
        """Hold active teleoperation even when no new WebXR frame is available."""
        if self.state == self.ACTIVE:
            self._begin_recoverable_hold(reason)
        elif self.state == self.RECOVERY_RAMP:
            self._begin_recoverable_hold(reason)
        elif self.state == self.RECOVERABLE_SAFETY_HOLD:
            self.recovery_abort_t0 = None
            self._reset_recovery_gate()
            adapter_fault = self.adapter_status.get("fault")
            if adapter_fault and not adapter_fault_is_recoverable(adapter_fault):
                self._fault("ADAPTER_{}".format(adapter_fault))
        self._update_gesture_hud(self.gesture.tracking_invalid(now))

    def _process_recoverable_hold(
            self, now, wrists, points, tracking_valid, fresh):
        if not tracking_valid:
            self.recovery_abort_t0 = None
            self._reset_recovery_gate()
            self._update_gesture_hud(self.gesture.tracking_invalid(now))
            return

        adapter_fault = self.adapter_status.get("fault")
        if adapter_fault and not adapter_fault_is_recoverable(adapter_fault):
            self._fault("ADAPTER_{}".format(adapter_fault))
            return
        if self._process_recovery_abort_gesture(now, points):
            return

        if not self._update_live_fingers(points, fresh):
            return

        if fresh:
            try:
                targets = self.arm_retargeter.update(wrists, now)
            except ValueError as error:
                if self.state == self.RECOVERY_RAMP:
                    self._begin_recoverable_hold(
                        "WEBXR_INPUT_JUMP: {}".format(error)
                    )
                else:
                    self._reset_recovery_gate()
                self._update_named_hud(
                    "RECOVERABLE_SAFETY_HOLD",
                    detail=RECOVERY_DETAIL_CODES["INPUT_JUMP"],
                    show_timer=False,
                )
                return
            if (self.state == self.RECOVERY_RAMP and
                    self.arm_retargeter.max_constraint_projection >
                    self.recovery_max_projection):
                self._begin_recoverable_hold(
                    "RECOVERY_TARGET_UNSAFE"
                )
                self._update_named_hud(
                    "RECOVERABLE_SAFETY_HOLD",
                    detail=RECOVERY_DETAIL_CODES["WORKSPACE_LIMIT"],
                    show_timer=False,
                )
                return
            self.arm_pub.publish(self._arm_message(targets))

        if adapter_fault and self.state == self.RECOVERY_RAMP:
            self._begin_recoverable_hold(
                "ADAPTER_{}".format(adapter_fault)
            )
            self._update_named_hud(
                "RECOVERABLE_SAFETY_HOLD",
                detail=self._recovery_blocker(), show_timer=False,
            )
            return

        if self.recovery_phase == "seek_safe":
            candidate_safe = self._recovery_candidate_safe()
            ready, remaining, progress = self.recovery_gate.update(
                now, self.adapter_status_serial, candidate_safe
            )
            if candidate_safe:
                self._update_named_hud(
                    "RECOVERY_SAFE_HOLD", remaining, progress,
                    show_timer=False,
                )
            else:
                self._update_named_hud(
                    "RECOVERABLE_SAFETY_HOLD", 0.0, progress,
                    detail=self._recovery_blocker(require_stable=True),
                    # Original target-lead HUD blocker, kept for rollback:
                    # detail=self._recovery_blocker(
                    #     require_stable=True,
                    #     maximum_follow_error=self.recovery_dynamic_follow_error,
                    # ),
                    show_timer=False,
                )
            if ready:
                # Keep the original L-pose XR/robot calibration untouched.
                # Recovery follows the continuously updated target produced
                # from that immutable session anchor; it never calibrates at
                # an arbitrary task-space pose.
                self._publish_adapter_mode("recovery")
                self.recovery_phase = "ramp"
                self._reset_recovery_gate()
                self._set_state(self.RECOVERY_RAMP)
                rospy.loginfo(
                    "WebXR recovery is following the original L-pose anchor "
                    "with the low-speed profile"
                )
            return

        if self.recovery_phase != "ramp":
            self._fault("UNKNOWN_RECOVERY_PHASE_{}".format(
                self.recovery_phase
            ))
            return

        motion_safe = self._recovery_target_safe()
        # Original 20-degree ramp guard, kept for rollback:
        # motion_safe = self._recovery_target_safe(
        #     maximum_follow_error=self.recovery_dynamic_follow_error
        # )
        handoff_error = self.adapter_status.get("ik_handoff_error_deg")
        metric = (
            float(handoff_error) if handoff_error is not None else -1.0
        )
        if not motion_safe:
            blocker = self._recovery_blocker()
            # Original target-lead HUD blocker, kept for rollback:
            # blocker = self._recovery_blocker(
            #     maximum_follow_error=self.recovery_dynamic_follow_error
            # )
            self._begin_recoverable_hold(
                "RECOVERY_TARGET_UNSAFE"
            )
            self._update_named_hud(
                "RECOVERABLE_SAFETY_HOLD",
                detail=blocker, show_timer=False,
            )
            return

        recovery_close = bool(
            handoff_error is not None and
            float(handoff_error) <= self.recovery_complete_error
        )
        ready, remaining, progress = self.recovery_completion_gate.update(
            now, self.adapter_status_serial, recovery_close
        )
        timer_running = self.recovery_completion_gate.ready_since is not None
        if recovery_close and timer_running:
            self._update_named_hud(
                "RECOVERY_STABLE", remaining, progress,
                metric=metric, show_timer=True,
            )
        else:
            self._update_named_hud(
                "RECOVERY_SLOW", 0.0, progress, metric=metric,
                show_timer=False,
            )
        if not ready:
            return

        self._publish_adapter_mode("ik")
        self.enabled = True
        self.gesture.force_enabled(True, now)
        self.recovery_reason = None
        self.recovery_phase = None
        self.recovery_abort_t0 = None
        self._reset_recovery_gate()
        self._set_state(self.ACTIVE)
        rospy.loginfo("WebXR safe target reacquired; teleoperation resumed automatically")

    def _fault(self, reason):
        now = time.monotonic()
        self.enabled = False
        self.fault_reason = reason
        self.fault_recovery_source_reason = None
        self.recovery_reason = None
        self.recovery_phase = None
        self.recovery_abort_t0 = None
        self._reset_recovery_gate()
        self._publish_adapter_mode("hold")
        self.gesture.force_enabled(False, now)
        self._set_state(self.SAFETY_FAULT)
        rospy.logerr("WebXR safety hold: %s", reason)

    def _process_safety_fault_gesture(
            self, now, wrists, points, head, fresh):
        """Offer a five-second guarded recovery only for whitelisted faults."""
        recovery_pose = safety_fault_recovery_pose(self.fault_reason)
        if recovery_pose is None:
            self._update_named_hud("SAFETY_FAULT")
            return

        event, hud = self.gesture.update(
            now, wrists, points, fresh=fresh, head=head
        )
        if event == "start":
            self.fault_recovery_source_reason = self.fault_reason
            self.pending_start_kind = "fault_recovery"
            # Recovery precheck and automatic motion never inherit the palms-up
            # hand command.  The gesture controller is explicitly disarmed
            # until calibration and IK handoff have both succeeded.
            self.gesture.force_enabled(False, now)
            self._begin_precheck(self.FAULT_RECOVERY_PRECHECK)
            return
        if hud.get("state") == "START_COUNTDOWN":
            self._update_named_hud(
                "FAULT_RECOVERY_COUNTDOWN",
                hud.get("remaining", 0.0), hud.get("progress", 0.0),
            )
            return
        if hud.get("state") in (
                "TRACKING_INVALID", "COOLDOWN", "RELEASE_TO_REARM"):
            self._update_gesture_hud(hud)
            return
        self._update_named_hud("SAFETY_FAULT_RECOVERABLE")

    def _robot_pose_from_tf(self, side):
        position_transform = self.tf_buffer.lookup_transform(
            self.base_frame, self.position_frames[side],
            rospy.Time(0), rospy.Duration(0.10),
        ).transform
        orientation_transform = self.tf_buffer.lookup_transform(
            self.base_frame, self.orientation_frames[side],
            rospy.Time(0), rospy.Duration(0.10),
        ).transform
        return (
            [position_transform.translation.x, position_transform.translation.y,
             position_transform.translation.z],
            [orientation_transform.rotation.x, orientation_transform.rotation.y,
             orientation_transform.rotation.z, orientation_transform.rotation.w],
        )

    def _try_calibrate(self, wrists, head, landmarks, timestamp):
        try:
            robot_poses = {
                side: self._robot_pose_from_tf(side) for side in ("left", "right")
            }
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException) as error:
            rospy.logwarn_throttle(2.0, "Waiting for robot end-effector TF: %s", error)
            return False
        try:
            base_alignment = base_alignment_from_head(head, self.static_axis_mapping)
        except ValueError as error:
            rospy.logwarn_throttle(2.0, "Waiting for usable HMD direction: %s", error)
            return False
        self.arm_retargeter.set_axis_mapping(base_alignment)
        self.arm_retargeter.calibrate(wrists, robot_poses, timestamp)
        self.head_retargeter.calibrate(head)
        self.finger_retargeter.reset()
        commands = {
            side: self.finger_retargeter.update(side, landmarks[side])
            for side in ("left", "right")
        }
        if any(command is None for command in commands.values()):
            return False
        self.last_finger_command = commands
        self.handoff_valid_frames = 0
        self.handoff_last_status_serial = self.adapter_status_serial
        self._set_state(self.CHECK_IK_HANDOFF)
        return True

    def _arm_message(self, targets):
        message = twoArmHandPoseCmd()
        message.frame = self.arm_frame
        message.use_custom_ik_param = False
        message.joint_angles_as_q0 = False
        params = message.ik_param
        params.major_optimality_tol = 9e-3
        params.major_feasibility_tol = 9e-3
        params.minor_feasibility_tol = 9e-3
        params.major_iterations_limit = 50
        params.oritation_constraint_tol = 19e-3
        params.pos_constraint_tol = 9e-3
        params.pos_cost_weight = 10.0
        for side in ("left", "right"):
            pose = (
                message.hand_poses.left_pose if side == "left"
                else message.hand_poses.right_pose
            )
            pose.pos_xyz = targets[side].position.tolist()
            pose.quat_xyzw = quaternion_xyzw(targets[side].rotation).tolist()
            pose.elbow_pos_xyz = [0.0, 0.0, 0.0]
            pose.joint_angles = [0.0] * 7
        message.hand_poses.header.stamp = rospy.Time.now()
        message.hand_poses.header.frame_id = self.base_frame
        return message

    def _publish_hands(self, finger_commands):
        message = robotHandPosition()
        message.header.stamp = rospy.Time.now()
        message.left_hand_position = [int(v) for v in finger_commands["left"]]
        message.right_hand_position = [int(v) for v in finger_commands["right"]]
        self.hand_pub.publish(message)

    def _update_live_fingers(self, points, fresh):
        """Update and publish live finger targets for active/recovery states."""
        if fresh:
            commands = {
                side: self.finger_retargeter.update(side, points[side])
                for side in ("left", "right")
            }
            if any(command is None for command in commands.values()):
                return False
            self.last_finger_command = commands
        if self.enable_hand:
            self._publish_hands(self.last_finger_command)
        return True

    def _publish_neutral_hands(self):
        if not self.enable_hand:
            return
        commands = {
            "left": self.neutral_hand_command.copy(),
            "right": self.neutral_hand_command.copy(),
        }
        self.last_finger_command = commands
        self._publish_hands(commands)

    def _publish_head(self, head):
        yaw, pitch = self.head_retargeter.update(head)
        message = robotHeadMotionData()
        message.joint_data = [yaw, pitch]
        self.head_pub.publish(message)

    def _tracking_valid(self, wrists, points, head, head_age):
        return bool(
            head is not None and head_age <= self.tracking_timeout and
            valid_transform(head) and
            all(valid_hand(
                wrists[side], points[side],
                self.gesture.hand_size_min, self.gesture.hand_size_max,
            ) for side in ("left", "right"))
        )

    def _process_pause_gestures(self, now, wrists, points, head, fresh):
        pinching = both_hands_pinching(points, self.pinch_threshold)
        if pinching:
            # Pinch has explicit priority in the pause menu.  A pinching hand
            # can still look open to the four-fingertip start detector, so do
            # not allow the same frames to accumulate a realign countdown.
            self.gesture.cancel_hold()
            if self.exit_gesture_t0 is None:
                self.exit_gesture_t0 = now
            elapsed = now - self.exit_gesture_t0
            self._update_named_hud(
                "EXIT_PINCH_COUNTDOWN", self.pinch_hold - elapsed,
                elapsed / max(self.pinch_hold, 1e-6),
            )
            if elapsed >= self.pinch_hold:
                self.exit_gesture_t0 = None
                self._set_state(self.EXIT_CONFIRM_RELEASE)
            return

        self.exit_gesture_t0 = None
        event, hud = self.gesture.update(
            now, wrists, points, fresh=fresh, head=head
        )
        if event == "start":
            self.pending_start_kind = "realign"
            self._set_state(self.WAITING_FOR_RELEASE)
            return
        if hud.get("state") == "START_COUNTDOWN":
            self._update_named_hud(
                "REALIGN_COUNTDOWN",
                hud.get("remaining", 0.0), hud.get("progress", 0.0),
            )
            return
        if self.gesture.release_pending:
            self._update_gesture_hud(hud)
            return
        if hud.get("state") in ("TRACKING_INVALID", "COOLDOWN"):
            self._update_gesture_hud(hud)
            return
        self._update_named_hud("PAUSED_HOLD")

    def _process_exit_confirmation(self, now, points):
        if self.state == self.EXIT_CONFIRM_RELEASE:
            pinching = both_hands_pinching(points, self.pinch_threshold)
            if pinching:
                self.exit_gesture_t0 = None
                self._update_named_hud("EXIT_CONFIRM_RELEASE", self.exit_release_hold)
                return
            if self.exit_gesture_t0 is None:
                self.exit_gesture_t0 = now
            elapsed = now - self.exit_gesture_t0
            self._update_named_hud(
                "EXIT_CONFIRM_RELEASE", self.exit_release_hold - elapsed,
                elapsed / max(self.exit_release_hold, 1e-6),
            )
            if elapsed >= self.exit_release_hold:
                self.exit_gesture_t0 = None
                self._set_state(self.EXIT_CONFIRM_PENDING)
            return
        both_fist = all(
            hand_open_fist_score(points[side]) is not None and
            hand_open_fist_score(points[side]) < self.gesture.fist_ratio
            for side in ("left", "right")
        )
        if not both_fist:
            self.exit_gesture_t0 = None
            self._update_named_hud("EXIT_FIST_COUNTDOWN", self.exit_fist_hold)
            return
        if self.exit_gesture_t0 is None:
            self.exit_gesture_t0 = now
        elapsed = now - self.exit_gesture_t0
        self._update_named_hud(
            "EXIT_FIST_COUNTDOWN", self.exit_fist_hold - elapsed,
            elapsed / max(self.exit_fist_hold, 1e-6),
        )
        if elapsed >= self.exit_fist_hold:
            self.exit_gesture_t0 = None
            self._begin_auto_sequence("exit", ["l", "t_bent", "t", "home"])

    def _tick(self, _event):
        with self.lock:
            if not self.webxr.is_alive():
                self._fault("WEBXR_SERVER_FAILED")
                self._publish_status(self.state)
                return
            if self.state in (
                    self.PRECHECK_AUTO_MOTION,
                    self.FAULT_RECOVERY_PRECHECK):
                self._process_precheck()
                self._update_named_hud(
                    "FAULT_RECOVERY_PRECHECK"
                    if self.state == self.FAULT_RECOVERY_PRECHECK
                    else "AUTOMATIC_MOTION"
                )
                self._publish_status(self.state)
                return
            if "MOVE_TO_" in self.state:
                self._process_auto_motion()
                self._update_named_hud("AUTOMATIC_MOTION")
                self._publish_status(self.state)
                return
            if (self.state == self.SAFETY_FAULT and
                    safety_fault_recovery_pose(self.fault_reason) is None):
                self._update_named_hud("SAFETY_FAULT")
                self._publish_status(self.state)
                return

            now = time.monotonic()
            sample = self.webxr.sample()
            if sample is None:
                self.last_sample_fresh = False
                if self.state == self.SAFETY_FAULT:
                    self._update_gesture_hud(
                        self.gesture.tracking_invalid(now)
                    )
                    self._publish_status(self.state)
                    return
                self._handle_tracking_unavailable(now, "WEBXR_TRACKING_MISSING")
                status = (
                    self.state if self.state in (
                        self.RECOVERABLE_SAFETY_HOLD,
                        self.RECOVERY_RAMP,
                        self.PAUSED_HOLD,
                    ) else "WAITING_FOR_WEBXR"
                )
                self._publish_status(status)
                return
            age = now - sample["timestamp"]
            if age > self.tracking_timeout:
                self.last_sample_fresh = False
                if self.state == self.SAFETY_FAULT:
                    self._update_gesture_hud(
                        self.gesture.tracking_invalid(now)
                    )
                    self._publish_status(self.state, age)
                    return
                self._handle_tracking_unavailable(now, "WEBXR_TRACKING_STALE")
                status = (
                    self.state if self.state in (
                        self.RECOVERABLE_SAFETY_HOLD,
                        self.RECOVERY_RAMP,
                        self.PAUSED_HOLD,
                    ) else "TRACKING_STALE"
                )
                self._publish_status(status, age)
                return
            fresh = sample["timestamp"] > self.last_processed_timestamp
            self.last_sample_fresh = fresh
            if fresh:
                try:
                    left_wrist, left_points = webxr_hand_frame(
                        sample["left_hand"], sample["left_landmarks"]
                    )
                    right_wrist, right_points = webxr_hand_frame(
                        sample["right_hand"], sample["right_landmarks"]
                    )
                except (TypeError, ValueError, np.linalg.LinAlgError):
                    self._handle_tracking_unavailable(
                        now, "WEBXR_TRACKING_INVALID"
                    )
                    self._publish_status(self.state, age)
                    return
                wrists = {"left": left_wrist, "right": right_wrist}
                if not all(valid_transform(wrist) for wrist in wrists.values()):
                    self._handle_tracking_unavailable(
                        now, "WEBXR_TRACKING_INVALID"
                    )
                    self._publish_status(self.state, age)
                    return
                self.latest_wrists = wrists
                self.latest_points = {"left": left_points, "right": right_points}
                self.last_processed_timestamp = sample["timestamp"]

            if self.latest_wrists is None or self.latest_points is None:
                return
            wrists = self.latest_wrists
            points = self.latest_points
            head = None
            head_age = float("inf")
            if sample["head_timestamp"] > 0.0:
                head_age = now - sample["head_timestamp"]
                try:
                    head = webxr_transform(sample["head"])
                except (TypeError, ValueError, np.linalg.LinAlgError):
                    head = None
            tracking_valid = self._tracking_valid(
                wrists, points, head, head_age
            )
            self.last_gesture_input_valid = tracking_valid

            if self.state == self.SAFETY_FAULT:
                if not tracking_valid:
                    self._update_gesture_hud(
                        self.gesture.tracking_invalid(now)
                    )
                else:
                    self._process_safety_fault_gesture(
                        now, wrists, points, head, fresh
                    )
                self._publish_status(self.state, age)
                return

            if self.state in (
                    self.RECOVERABLE_SAFETY_HOLD, self.RECOVERY_RAMP):
                self._process_recoverable_hold(
                    now, wrists, points, tracking_valid, fresh
                )
                self._publish_status(self.state, age)
                return

            if self.state == self.WAITING_FOR_START:
                if not tracking_valid:
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                event, hud = self.gesture.update(
                    now, wrists, points, fresh=fresh, head=head
                )
                self._update_gesture_hud(hud)
                if event == "start":
                    self.pending_start_kind = "start"
                    self._set_state(self.WAITING_FOR_RELEASE)
                self._publish_status(self.state, age)
                return

            if self.state == self.WAITING_FOR_RELEASE:
                if not tracking_valid:
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                _event, hud = self.gesture.update(
                    now, wrists, points, fresh=fresh, head=head
                )
                self._update_gesture_hud(hud)
                if not self.gesture.release_pending:
                    self._begin_precheck()
                return

            if self.state == self.PAUSED_HOLD:
                if not tracking_valid:
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                self._process_pause_gestures(now, wrists, points, head, fresh)
                return

            if self.state in (self.EXIT_CONFIRM_RELEASE, self.EXIT_CONFIRM_PENDING):
                if not tracking_valid:
                    self.exit_gesture_t0 = None
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                self._process_exit_confirmation(now, points)
                return

            if self.state == self.WAIT_L_REACHED:
                if not tracking_valid:
                    self.alignment_countdown_started = None
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                if self.alignment_countdown_started is None:
                    self.alignment_countdown_started = now
                elapsed = now - self.alignment_countdown_started
                remaining = max(0.0, self.calibration_prepare_hold - elapsed)
                self._update_named_hud(
                    ("ALIGN_T_BENT_POSE"
                     if self.alignment_pose_name == "t_bent"
                     else "ALIGN_L_POSE"), remaining,
                    elapsed / max(self.calibration_prepare_hold, 1e-6),
                )
                if elapsed >= self.calibration_prepare_hold and fresh:
                    self.calibration_window.reset()
                    self.alignment_countdown_started = None
                    self._set_state(self.CALIBRATING_NEUTRAL)
                return

            if self.state == self.CALIBRATING_NEUTRAL:
                if not tracking_valid:
                    self.calibration_window.reset()
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                if fresh:
                    self.calibration_window.add(now, wrists, head, points)
                remaining = max(
                    0.0,
                    self.calibration_window.hold_seconds - self.calibration_window.duration,
                )
                self._update_named_hud(
                    "CALIBRATING_NEUTRAL", remaining,
                    self.calibration_window.duration /
                    max(self.calibration_window.hold_seconds, 1e-6),
                )
                if self.calibration_window.ready:
                    averaged = self.calibration_window.average()
                    if not self._try_calibrate(
                        averaged[0], averaged[1], averaged[2], now
                    ):
                        self._publish_status("WAITING_FOR_ROBOT_TF", age)
                return

            if self.state == self.CHECK_IK_HANDOFF:
                if not tracking_valid:
                    self.handoff_valid_frames = 0
                    self._update_gesture_hud(self.gesture.tracking_invalid(now))
                    return
                targets = self.arm_retargeter.update(wrists, now)
                self.arm_pub.publish(self._arm_message(targets))
                self._publish_hands(self.last_finger_command)
                if self.adapter_status.get("fault"):
                    self._fault("ADAPTER_{}".format(self.adapter_status["fault"]))
                    return
                if self.adapter_status_serial != self.handoff_last_status_serial:
                    ready = bool(self.adapter_status.get("ik_handoff_ready", False))
                    self.handoff_valid_frames = (
                        self.handoff_valid_frames + 1 if ready else 0
                    )
                    self.handoff_last_status_serial = self.adapter_status_serial
                self._update_named_hud("IK_HANDOFF_CHECK")
                if self.handoff_valid_frames >= self.handoff_frames_required:
                    self._publish_adapter_mode("ik")
                    self.enabled = True
                    self.gesture.force_enabled(True, now)
                    self.fault_recovery_source_reason = None
                    self._set_state(self.ACTIVE)
                elif now - self.state_entered > self.handoff_timeout:
                    self._fault(
                        "IK_HANDOFF_DISCONTINUITY error={}deg".format(
                            self.adapter_status.get("ik_handoff_error_deg")
                        )
                    )
                return

            if self.state != self.ACTIVE:
                return
            if self.adapter_status.get("fault"):
                adapter_fault = self.adapter_status["fault"]
                if adapter_fault_is_recoverable(adapter_fault):
                    self._begin_recoverable_hold(
                        "ADAPTER_{}".format(adapter_fault)
                    )
                else:
                    self._fault("ADAPTER_{}".format(adapter_fault))
                return
            if not tracking_valid:
                self._handle_tracking_unavailable(
                    now, "WEBXR_TRACKING_INVALID"
                )
                self._publish_status(self.state, age)
                return
            event, hud = self.gesture.update(
                now, wrists, points, fresh=fresh, head=head
            )
            self._update_gesture_hud(hud)
            if event == "stop":
                self._pause("two-fist stop gesture")
                return
            if not self._update_live_fingers(points, fresh):
                return
            if self.enable_arm:
                try:
                    targets = self.arm_retargeter.update(wrists, now)
                except ValueError as error:
                    self._begin_recoverable_hold(
                        "WEBXR_INPUT_JUMP: {}".format(error)
                    )
                    return
                self.arm_pub.publish(self._arm_message(targets))
            if (self.enable_head and sample["head_timestamp"] > self.last_head_timestamp):
                self._publish_head(head)
                self.last_head_timestamp = sample["head_timestamp"]
            self._publish_status(self.ACTIVE, age)

    def _update_named_hud(self, state, remaining=0.0, progress=0.0,
                          detail=0, metric=-1.0, show_timer=None):
        hud = {
            "code": HUD_CODES[state], "state": state,
            "remaining": max(0.0, float(remaining)),
            "progress": min(1.0, max(0.0, float(progress))),
            "enabled": self.enabled,
            "detail": int(detail),
            "metric": float(metric),
        }
        if show_timer is not None:
            hud["show_timer"] = bool(show_timer)
        self._update_gesture_hud(hud)

    def _update_gesture_hud(self, hud):
        self.last_gesture_hud = hud
        legacy_timed_codes = {
            HUD_CODES[name] for name in (
                "START_COUNTDOWN", "STOP_COUNTDOWN", "RELEASE_TO_REARM",
                "COOLDOWN", "CALIBRATING_NEUTRAL", "ALIGN_L_POSE",
                "ALIGN_T_BENT_POSE", "FAULT_RECOVERY_COUNTDOWN",
                "EXIT_PINCH_COUNTDOWN", "EXIT_CONFIRM_RELEASE",
                "EXIT_FIST_COUNTDOWN", "RECOVERY_ABORT_COUNTDOWN",
                "REALIGN_COUNTDOWN",
            )
        }
        self.webxr.set_hud(
            hud["code"], hud.get("remaining", 0.0), hud.get("progress", 0.0),
            hud.get("enabled", self.enabled),
            show_timer=hud.get("show_timer", hud["code"] in legacy_timed_codes),
            detail=hud.get("detail", 0), metric=hud.get("metric", -1.0),
        )

    def _publish_status(self, state, age=None, force=False):
        now = time.monotonic()
        if not force and state == self.last_status and now - self.last_status_publish < 1.0:
            return
        payload = {
            "state": state,
            "enabled": self.enabled,
            "fault": self.fault_reason,
            "recovery_reason": self.recovery_reason,
            "recovery_phase": self.recovery_phase,
            "recovery_safe_reports": self.recovery_gate.count,
            "recovery_constraint_projection_m": (
                None if not np.isfinite(
                    self.arm_retargeter.max_constraint_projection
                ) else self.arm_retargeter.max_constraint_projection
            ),
            "tracking_age_s": age,
            "feedback_age_s": (
                None if self.feedback_time <= 0.0 else now - self.feedback_time
            ),
            "feedback_fresh": self._feedback_ready(),
            "adapter": self.adapter_status,
            "arm_mode_service": self.selected_arm_mode_service,
            "auto_sequence": self.auto_sequence_kind,
            "fault_recovery_source": self.fault_recovery_source_reason,
            "alignment_pose": self.alignment_pose_name,
            "auto_pose": (
                None if not self.auto_sequence or self.auto_index >= len(self.auto_sequence)
                else self.auto_sequence[self.auto_index]
            ),
            "auto_target_error_deg": (
                None if self.feedback is None or self.auto_target is None
                else max_abs_joint_error(self.feedback, self.auto_target)
            ),
            "calibration_samples": self.calibration_window.sample_count,
            "calibration_duration_s": self.calibration_window.duration,
            "calibrated": self.arm_retargeter.calibrated,
            "gesture_state": getattr(self, "last_gesture_hud", {}).get("state"),
            "gesture_input_valid": self.last_gesture_input_valid,
            "gesture_sample_fresh": self.last_sample_fresh,
            "arm_topic": self.arm_topic,
            "head_topic": self.head_topic,
            "base_frame": self.base_frame,
        }
        self.status_pub.publish(String(data=json.dumps(payload, sort_keys=True)))
        self.last_status = state
        self.last_status_publish = now


def main():
    rospy.init_node("quest_webxr_kuavo_bridge")
    try:
        QuestWebXRKuavoBridge()
        rospy.spin()
    except (RuntimeError, ValueError) as error:
        rospy.logfatal("Quest WebXR bridge startup failed: %s", error)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
