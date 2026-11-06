#!/usr/bin/env python3
"""Single-owner arm/hand output arbiter for the WebXR bridge.

The adapter is the only WebXR node allowed to publish ``/kuavo_arm_traj``.
It arbitrates HOLD, automatic staging poses and live IK, then applies the same
v49 joint envelope and explicit velocity/acceleration limits to every path.
"""

import json
import threading
import time

import numpy as np
import rospy
from kuavo_msgs.msg import robotHandPosition, sensorsData
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, String

from quest_webxr_bridge.arm_safety import (
    ArmCommandLimiter, adapter_fault_is_recoverable, envelope_margin,
    feedback_bounded_target, max_abs_joint_error,
)
from quest_webxr_bridge.recording_contract import ARM_JOINT_NAMES


def _vector_param(name, default, size=14):
    value = np.asarray(rospy.get_param(name, default), dtype=float).reshape(-1)
    if value.size == 1:
        value = np.repeat(value, size)
    if value.size != size or not np.all(np.isfinite(value)):
        raise ValueError("{} must contain one or {} finite values".format(name, size))
    return value


class ControlContractAdapter:
    VALID_MODES = frozenset(("off", "hold", "auto", "recovery", "ik"))

    def __init__(self):
        self._lock = threading.RLock()
        self._mode = "off"
        self._requested_mode = "off"
        self._fault = None
        self._feedback = None
        self._feedback_time = 0.0
        self._auto_target = None
        self._ik_target = None
        self._ik_target_time = 0.0
        self._previous_raw_ik = None
        self._ik_target_delta = None
        self._latest_hand = None
        self._latest_hand_time = 0.0
        self._hand_follow_enabled = False
        self._hold_target = None
        self._last_tick = None
        self._tracking_error_since = None

        lower = _vector_param(
            "~pose_config/limits/preview_lower_deg",
            [-175, -15, -85, -145, -85, -70, -35,
             -175, -115, -85, -145, -85, -35, -35],
        )
        upper = _vector_param(
            "~pose_config/limits/preview_upper_deg",
            [85, 115, 85, -5, 85, 35, 35,
             85, 15, 85, -5, 85, 70, 35],
        )
        hard_lower = _vector_param(
            "~pose_config/limits/hard_lower_deg",
            [-180, -20, -90, -150, -90, -75, -40,
             -180, -120, -90, -150, -90, -40, -40],
        )
        hard_upper = _vector_param(
            "~pose_config/limits/hard_upper_deg",
            [90, 120, 90, 0, 90, 40, 40,
             90, 20, 90, 0, 90, 75, 40],
        )
        if (np.any(hard_lower > lower) or np.any(hard_upper < upper)):
            raise ValueError(
                "mechanical feedback envelope must contain preview envelope"
            )
        self._profiles = {
            "auto": (
                _vector_param("~auto_joint_velocity_deg_s", [5.0]),
                _vector_param("~auto_joint_acceleration_deg_s2", [10.0]),
            ),
            "ik": (
                _vector_param(
                    "~teleop_joint_velocity_deg_s",
                    [25, 30, 30, 40, 45, 45, 45,
                     25, 30, 30, 40, 45, 45, 45],
                ),
                _vector_param(
                    "~teleop_joint_acceleration_deg_s2",
                    [80, 100, 100, 120, 150, 150, 150,
                     80, 100, 100, 120, 150, 150, 150],
                ),
            ),
            "recovery": (
                _vector_param("~recovery_joint_velocity_deg_s", [5.0]),
                _vector_param("~recovery_joint_acceleration_deg_s2", [10.0]),
            ),
            "hold": (
                _vector_param("~hold_joint_velocity_deg_s", [5.0]),
                _vector_param("~hold_joint_acceleration_deg_s2", [10.0]),
            ),
        }
        self._limiter = ArmCommandLimiter(
            lower, upper, self._profiles["hold"][0], self._profiles["hold"][1],
            feedback_lower=hard_lower, feedback_upper=hard_upper,
        )
        self._hard_feedback_tolerance = float(
            rospy.get_param("~feedback_hard_limit_tolerance_deg", 0.25)
        )
        self._safe_feedback_tolerance = float(
            rospy.get_param("~feedback_safe_envelope_tolerance_deg", 0.5)
        )
        if self._hard_feedback_tolerance < 0.0:
            raise ValueError(
                "~feedback_hard_limit_tolerance_deg must be non-negative"
            )
        if self._safe_feedback_tolerance < 0.0:
            raise ValueError(
                "~feedback_safe_envelope_tolerance_deg must be non-negative"
            )
        self._feedback_timeout = float(rospy.get_param("~feedback_timeout", 0.30))
        self._ik_timeout = float(rospy.get_param("~ik_target_timeout", 0.25))
        self._hand_timeout = float(rospy.get_param("~hand_target_timeout", 0.25))
        self._raw_ik_jump_limit = float(
            rospy.get_param("~raw_ik_jump_limit_deg", 25.0)
        )
        self._handoff_limit = float(
            rospy.get_param("~ik_handoff_limit_deg", 12.0)
        )
        # Original 20-degree recovery target-lead guard, kept commented for
        # rollback after the unrestricted low-speed recovery trial:
        # self._recovery_follow_error_limit = float(
        #     rospy.get_param("~recovery_dynamic_follow_error_deg", 20.0)
        # )
        self._tracking_error_limit = float(
            rospy.get_param("~tracking_error_limit_deg", 45.0)
        )
        self._tracking_error_grace = float(
            rospy.get_param("~tracking_error_grace_s", 1.0)
        )
        self._recovery_command_lead = _vector_param(
            "~recovery_command_lead_deg", [12.0]
        )
        if np.any(self._recovery_command_lead <= 0.0):
            raise ValueError("~recovery_command_lead_deg must be positive")
        # Original validation for the disabled target-lead guard:
        # if self._recovery_follow_error_limit <= 0.0:
        #     raise ValueError(
        #         "~recovery_dynamic_follow_error_deg must be positive"
        #     )

        arm_input = rospy.get_param(
            "~arm_input_topic", "/quest_webxr/internal_ik_arm_traj"
        )
        hand_input = rospy.get_param(
            "~hand_input_topic", "/quest_webxr/internal_hand_position"
        )
        arm_output = rospy.get_param("~arm_output_topic", "/kuavo_arm_traj")
        hand_output = rospy.get_param(
            "~hand_output_topic", "/control_robot_hand_position"
        )
        mode_input = rospy.get_param(
            "~mode_input_topic", "/quest_webxr/arm_command_mode"
        )
        hand_follow_input = rospy.get_param(
            "~hand_follow_input_topic", "/quest_webxr/hand_follow_enabled"
        )
        auto_input = rospy.get_param(
            "~auto_input_topic", "/quest_webxr/auto_arm_target"
        )
        feedback_input = rospy.get_param("~feedback_topic", "/sensors_data_raw")

        self._arm_pub = rospy.Publisher(arm_output, JointState, queue_size=2)
        self._hand_pub = rospy.Publisher(hand_output, robotHandPosition, queue_size=2)
        self._status_pub = rospy.Publisher(
            "/quest_webxr/arm_adapter_status", String, queue_size=1, latch=True
        )
        self._subs = [
            rospy.Subscriber(mode_input, String, self._mode_callback, queue_size=1),
            rospy.Subscriber(
                hand_follow_input, Bool, self._hand_follow_callback, queue_size=1
            ),
            rospy.Subscriber(auto_input, JointState, self._auto_callback, queue_size=1),
            rospy.Subscriber(
                hand_input, robotHandPosition, self._hand_callback,
                queue_size=1, tcp_nodelay=True,
            ),
            rospy.Subscriber(
                arm_input, JointState, self._arm_callback,
                queue_size=1, tcp_nodelay=True,
            ),
            rospy.Subscriber(
                feedback_input, sensorsData, self._feedback_callback,
                queue_size=1, tcp_nodelay=True,
            ),
        ]
        rate = float(rospy.get_param("~publish_rate", 100.0))
        self._timer = rospy.Timer(rospy.Duration(1.0 / rate), self._tick)
        self._status_timer = rospy.Timer(rospy.Duration(0.2), self._publish_status)

    def _valid_joint_state(self, message, source):
        if (tuple(message.name) != ARM_JOINT_NAMES or
                len(message.position) != len(ARM_JOINT_NAMES)):
            rospy.logerr_throttle(
                2.0, "%s must be arm_joint_1..arm_joint_14 with 14 positions", source
            )
            return None
        position = np.asarray(message.position, dtype=float)
        if not np.all(np.isfinite(position)):
            rospy.logerr_throttle(2.0, "%s contains non-finite values", source)
            return None
        try:
            return self._limiter.validate(position)
        except ValueError as error:
            rospy.logerr_throttle(2.0, "%s rejected: %s", source, error)
            return None

    def _mode_callback(self, message):
        mode = message.data.strip().lower()
        if mode not in self.VALID_MODES:
            rospy.logerr("Ignoring unknown WebXR arm mode %r", message.data)
            return
        with self._lock:
            self._requested_mode = mode
            if mode == "hold" and adapter_fault_is_recoverable(self._fault):
                # An explicit bridge-issued HOLD acknowledges a recoverable IK
                # fault after the bridge has observed it.  Clearing the narrow
                # recoverable set here also lets the guarded hard-fault path
                # leave CHECK_IK_HANDOFF, precheck ownership, and then command
                # the configured L calibration pose. TRACKING_ERROR is also
                # acknowledged here after it has been reported to the bridge;
                # feedback and limiter faults remain hard failures.
                self._fault = None
                self._tracking_error_since = None
            if mode in ("off", "hold"):
                # A later neutral calibration starts a new IK solution branch;
                # do not compare its first candidate with the pre-pause task.
                self._previous_raw_ik = None
                self._ik_target = None
                self._ik_target_time = 0.0
                self._ik_target_delta = None
            if mode == "off":
                self._mode = "off"
                self._hold_target = None
                self._fault = None

    def _auto_callback(self, message):
        target = self._valid_joint_state(message, "automatic arm target")
        if target is not None:
            with self._lock:
                self._auto_target = target.copy()

    def _arm_callback(self, message):
        target = self._valid_joint_state(message, "WebXR IK arm output")
        if target is None:
            with self._lock:
                self._fault = "IK_TARGET_OUTSIDE_SAFE_ENVELOPE"
                self._ik_target_delta = None
                if self._mode in ("hold", "recovery"):
                    # Forget the rejected branch.  The bridge keeps the
                    # original L-pose anchor, then waits for new safe live
                    # candidates before enabling low-speed pursuit again.
                    self._previous_raw_ik = None
            return
        with self._lock:
            target_delta = (
                0.0 if self._previous_raw_ik is None else
                max_abs_joint_error(target, self._previous_raw_ik)
            )
            self._ik_target_delta = target_delta
            if (self._mode in ("hold", "recovery", "ik") and
                    self._previous_raw_ik is not None and
                    target_delta > self._raw_ik_jump_limit):
                self._fault = "IK_TARGET_JUMP"
                rospy.logerr_throttle(
                    1.0, "Rejecting IK target jump above %.1f deg",
                    self._raw_ik_jump_limit,
                )
                if self._mode in ("hold", "recovery"):
                    self._previous_raw_ik = None
                return
            if (self._mode in ("hold", "recovery") and
                    adapter_fault_is_recoverable(self._fault) and
                    self._fault not in (
                        "FEEDBACK_OUTSIDE_SAFE_ENVELOPE",
                        "RECOVERY_TARGET_LEAD", "TRACKING_ERROR"
                    )):
                # Ordinary recoverable IK faults clear on the next valid
                # target. RECOVERY_TARGET_LEAD is deliberately latched until
                # an explicit bridge-issued HOLD acknowledges it.
                self._fault = None
            self._previous_raw_ik = target.copy()
            self._ik_target = target.copy()
            self._ik_target_time = time.monotonic()

    def _hand_callback(self, message):
        if (len(message.left_hand_position) != 6 or
                len(message.right_hand_position) != 6):
            rospy.logerr_throttle(
                2.0, "WebXR hand command must contain six channels per hand"
            )
            return
        with self._lock:
            self._latest_hand = (
                list(message.left_hand_position), list(message.right_hand_position)
            )
            self._latest_hand_time = time.monotonic()

    def _hand_follow_callback(self, message):
        with self._lock:
            self._hand_follow_enabled = bool(message.data)

    def _feedback_callback(self, message):
        values = list(message.joint_data.joint_q)
        if len(values) < 26:
            rospy.logerr_throttle(2.0, "sensors_data_raw has fewer than 26 joints")
            return
        feedback = np.degrees(np.asarray(values[12:26], dtype=float))
        if not np.all(np.isfinite(feedback)):
            return
        with self._lock:
            self._feedback = feedback
            self._feedback_time = time.monotonic()

    def _enter_requested_mode(self, now):
        if self._requested_mode == self._mode:
            return True
        if self._requested_mode == "off":
            self._mode = "off"
            return True
        if self._feedback is None or now - self._feedback_time > self._feedback_timeout:
            self._fault = "FEEDBACK_STALE"
            return False
        try:
            self._limiter.seed(
                self._feedback, tolerance=self._hard_feedback_tolerance
            )
        except ValueError:
            self._fault = "FEEDBACK_OUTSIDE_HARD_LIMITS"
            return False
        self._mode = self._requested_mode
        feedback_inside_safe = bool(
            np.all(
                self._feedback >=
                self._limiter.lower - self._safe_feedback_tolerance
            ) and
            np.all(
                self._feedback <=
                self._limiter.upper + self._safe_feedback_tolerance
            )
        )
        self._fault = (
            None if feedback_inside_safe else
            "FEEDBACK_OUTSIDE_SAFE_ENVELOPE"
        )
        self._tracking_error_since = None
        self._hold_target = np.clip(
            self._feedback, self._limiter.lower, self._limiter.upper
        )
        velocity, acceleration = self._profiles[
            "ik" if self._mode == "ik" else self._mode
        ]
        self._limiter.set_profile(velocity, acceleration)
        return True

    def _target_for_mode(self, now):
        if self._mode == "hold":
            return self._hold_target
        if self._mode == "auto":
            return self._auto_target
        if self._mode in ("recovery", "ik"):
            if self._ik_target is None or now - self._ik_target_time > self._ik_timeout:
                self._fault = "IK_TARGET_STALE"
                return None
            return self._ik_target
        return None

    def _tick(self, event):
        now = time.monotonic()
        with self._lock:
            if not self._enter_requested_mode(now) or self._mode == "off":
                self._last_tick = now
                return
            feedback_fresh = (
                self._feedback is not None and
                now - self._feedback_time <= self._feedback_timeout
            )
            if not feedback_fresh:
                self._fault = "FEEDBACK_STALE"
                return
            try:
                self._limiter.validate_feedback(
                    self._feedback,
                    tolerance=self._hard_feedback_tolerance,
                )
            except ValueError:
                # Mechanical-limit violations remain hard faults.  They must
                # not be converted into an automatic pursuit command.
                self._fault = "FEEDBACK_OUTSIDE_HARD_LIMITS"
                return
            feedback_inside_safe = bool(
                np.all(
                    self._feedback >=
                    self._limiter.lower - self._safe_feedback_tolerance
                ) and
                np.all(
                    self._feedback <=
                    self._limiter.upper + self._safe_feedback_tolerance
                )
            )
            if (not feedback_inside_safe and
                    self._mode in ("auto", "recovery", "ik")):
                # A real joint crossed only the conservative software margin.
                # Enter a recoverable hold and command the nearest point on
                # that margin.  The hold profile and feedback backpressure
                # below return it slowly; IK targets continue arriving in the
                # background for automatic live recovery afterwards.
                self._fault = "FEEDBACK_OUTSIDE_SAFE_ENVELOPE"
                self._requested_mode = "hold"
                self._mode = "hold"
                self._hold_target = np.clip(
                    self._feedback,
                    self._limiter.lower,
                    self._limiter.upper,
                )
                self._limiter.seed(
                    self._feedback,
                    tolerance=self._hard_feedback_tolerance,
                )
                self._limiter.set_profile(*self._profiles["hold"])
                self._tracking_error_since = None
                return
            target = self._target_for_mode(now)
            if target is None:
                return
            # Original 20-degree recovery target-lead stop, kept commented for
            # rollback. Recovery now pursues any otherwise-safe IK target using
            # the 5 deg/s, 10 deg/s^2 limiter regardless of target distance.
            # if (self._mode == "recovery" and
            #         max_abs_joint_error(self._feedback, target) >
            #         self._recovery_follow_error_limit):
            #     self._fault = "RECOVERY_TARGET_LEAD"
            #     self._requested_mode = "hold"
            #     self._mode = "hold"
            #     self._hold_target = self._feedback.copy()
            #     self._limiter.seed(self._feedback)
            #     self._previous_raw_ik = None
            #     self._ik_target = None
            #     self._ik_target_time = 0.0
            #     self._ik_target_delta = None
            #     return
            step_target = target
            if self._mode in ("hold", "recovery"):
                # A distant live IK target remains valid. Only the command
                # presented to the low-speed limiter is bounded around fresh
                # feedback, so contact cannot make commanded joint motion
                # accumulate arbitrarily far ahead of the real robot.
                if (self._limiter.position is not None and
                        max_abs_joint_error(
                            self._feedback, self._limiter.position
                        ) > float(np.max(self._recovery_command_lead)) + 0.5):
                    self._limiter.seed(
                        self._feedback,
                        tolerance=self._hard_feedback_tolerance,
                    )
                    rospy.logwarn_throttle(
                        1.0,
                        "Recovery command was ahead of feedback; reseeding "
                        "the low-speed limiter from measured joints",
                    )
                step_target = feedback_bounded_target(
                    target, self._feedback,
                    self._limiter.lower, self._limiter.upper,
                    self._recovery_command_lead,
                )
                self._tracking_error_since = None
            elif self._limiter.position is not None:
                tracking_error = max_abs_joint_error(
                    self._feedback, self._limiter.position
                )
                if tracking_error > self._tracking_error_limit:
                    if self._tracking_error_since is None:
                        self._tracking_error_since = now
                    elif now - self._tracking_error_since >= self._tracking_error_grace:
                        self._fault = "TRACKING_ERROR"
                        self._requested_mode = "hold"
                        self._mode = "hold"
                        self._hold_target = self._feedback.copy()
                        self._limiter.seed(self._feedback)
                        return
                else:
                    self._tracking_error_since = None
            if self._last_tick is None:
                dt = max(
                    1e-3,
                    min(0.05, event.current_real.to_sec() - event.last_real.to_sec()),
                )
            else:
                dt = max(1e-3, min(0.05, now - self._last_tick))
            self._last_tick = now
            try:
                position, velocity = self._limiter.step(step_target, dt)
            except (RuntimeError, ValueError) as error:
                self._fault = "LIMITER_REJECTED: {}".format(error)
                return

            stamp = rospy.Time.now()
            arm_out = JointState()
            arm_out.header.stamp = stamp
            arm_out.header.frame_id = "base_link"
            arm_out.name = list(ARM_JOINT_NAMES)
            arm_out.position = position.tolist()
            arm_out.velocity = velocity.tolist()
            arm_out.effort = [0.0] * len(ARM_JOINT_NAMES)
            self._arm_pub.publish(arm_out)

            hand_output_allowed = bool(
                self._mode == "auto" or
                (self._hand_follow_enabled and
                 self._mode in ("hold", "recovery", "ik"))
            )
            if (hand_output_allowed and
                    self._latest_hand is not None and
                    now - self._latest_hand_time <= self._hand_timeout):
                hand_out = robotHandPosition()
                hand_out.header.stamp = stamp
                hand_out.left_hand_position = self._latest_hand[0]
                hand_out.right_hand_position = self._latest_hand[1]
                self._hand_pub.publish(hand_out)

    def _publish_status(self, _event):
        now = time.monotonic()
        with self._lock:
            feedback_age = (
                None if self._feedback_time <= 0.0 else now - self._feedback_time
            )
            ik_age = None if self._ik_target_time <= 0.0 else now - self._ik_target_time
            handoff_error = None
            ik_envelope_margin = None
            if self._feedback is not None and self._ik_target is not None:
                handoff_error = max_abs_joint_error(self._feedback, self._ik_target)
                ik_envelope_margin = envelope_margin(
                    self._ik_target, self._limiter.lower, self._limiter.upper
                )
            feedback_inside_safe = bool(
                self._feedback is not None and
                np.all(
                    self._feedback >=
                    self._limiter.lower - self._safe_feedback_tolerance
                ) and
                np.all(
                    self._feedback <=
                    self._limiter.upper + self._safe_feedback_tolerance
                )
            )
            feedback_inside_hard = False
            feedback_envelope_violation = None
            if self._feedback is not None:
                feedback_inside_hard = bool(
                    np.all(
                        self._feedback >= self._limiter.feedback_lower -
                        self._hard_feedback_tolerance
                    ) and
                    np.all(
                        self._feedback <= self._limiter.feedback_upper +
                        self._hard_feedback_tolerance
                    )
                )
                feedback_envelope_violation = float(np.max(np.maximum(
                    np.maximum(self._limiter.lower - self._feedback, 0.0),
                    np.maximum(self._feedback - self._limiter.upper, 0.0),
                )))
            payload = {
                "mode": self._mode,
                "requested_mode": self._requested_mode,
                "fault": self._fault,
                "hand_follow_enabled": self._hand_follow_enabled,
                "recovery_command_lead_deg": self._recovery_command_lead.tolist(),
                "feedback_age_s": feedback_age,
                "feedback_inside_safe_envelope": feedback_inside_safe,
                "feedback_inside_hard_envelope": feedback_inside_hard,
                "feedback_envelope_violation_deg": (
                    feedback_envelope_violation
                ),
                "ik_target_age_s": ik_age,
                "ik_target_delta_deg": self._ik_target_delta,
                "ik_target_fresh": bool(
                    ik_age is not None and ik_age <= self._ik_timeout
                ),
                "ik_handoff_error_deg": handoff_error,
                "ik_envelope_margin_deg": ik_envelope_margin,
                "ik_handoff_ready": bool(
                    handoff_error is not None and
                    handoff_error <= self._handoff_limit and
                    feedback_age is not None and
                    feedback_age <= self._feedback_timeout and
                    ik_age is not None and ik_age <= self._ik_timeout
                ),
                "tracking_error_deg": (
                    None if self._feedback is None or self._limiter.position is None
                    else max_abs_joint_error(self._feedback, self._limiter.position)
                ),
            }
        self._status_pub.publish(String(data=json.dumps(payload, sort_keys=True)))


def main():
    rospy.init_node("quest_webxr_control_contract_adapter")
    try:
        ControlContractAdapter()
        rospy.spin()
    except (RuntimeError, ValueError) as error:
        rospy.logfatal("WebXR command adapter startup failed: %s", error)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
