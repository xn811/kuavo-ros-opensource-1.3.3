"""xteleop-style, two-hand gesture arming for the WebXR bridge.

This module is deliberately ROS-free so the safety state machine can be unit
tested without a robot or a Quest headset.
"""

import numpy as np


HUD_CODES = {
    "WAITING_FOR_TRACKING": 0,
    "READY_TO_START": 1,
    "START_COUNTDOWN": 2,
    "ACTIVE": 3,
    "STOP_COUNTDOWN": 4,
    "RELEASE_TO_REARM": 5,
    "COOLDOWN": 6,
    "TRACKING_INVALID": 7,
    "CALIBRATING_NEUTRAL": 8,
    "AUTOMATIC_MOTION": 9,
    "ALIGN_L_POSE": 10,
    "IK_HANDOFF_CHECK": 11,
    "PAUSED_HOLD": 12,
    "EXIT_PINCH_COUNTDOWN": 13,
    "EXIT_CONFIRM_RELEASE": 14,
    "EXIT_FIST_COUNTDOWN": 15,
    "SAFETY_FAULT": 16,
    "RECOVERABLE_SAFETY_HOLD": 17,
    "RECOVERY_SAFE_HOLD": 18,
    "RECOVERY_ABORT_COUNTDOWN": 19,
    "RECOVERY_SLOW": 20,
    "RECOVERY_STABLE": 21,
    "REALIGN_COUNTDOWN": 22,
    "SAFETY_FAULT_RECOVERABLE": 23,
    "FAULT_RECOVERY_COUNTDOWN": 24,
    "FAULT_RECOVERY_PRECHECK": 25,
    "ALIGN_T_BENT_POSE": 26,
}


# Compact recovery blockers shown after ``SAFETY LIMIT``.  Keep these numeric
# values stable because they cross the ROS/WebXR multiprocessing boundary.
RECOVERY_DETAIL_CODES = {
    "NONE": 0,
    "TRACKING": 1,
    "INPUT_JUMP": 2,
    "JOINT_LIMIT": 3,
    "IK_JUMP": 4,
    "IK_STALE": 5,
    "WORKSPACE_LIMIT": 6,
    "IK_UNSTABLE": 7,
    "IK_DISCONTINUITY": 8,
    "FEEDBACK": 9,
    "FOLLOW_ERROR": 10,
    "FEEDBACK_ENVELOPE": 11,
}

RECOVERY_DETAIL_TEXT = {
    RECOVERY_DETAIL_CODES["NONE"]: "",
    RECOVERY_DETAIL_CODES["TRACKING"]: "TRACKING",
    RECOVERY_DETAIL_CODES["INPUT_JUMP"]: "INPUT JUMP",
    RECOVERY_DETAIL_CODES["JOINT_LIMIT"]: "JOINT LIMIT",
    RECOVERY_DETAIL_CODES["IK_JUMP"]: "IK JUMP",
    RECOVERY_DETAIL_CODES["IK_STALE"]: "IK STALE",
    RECOVERY_DETAIL_CODES["WORKSPACE_LIMIT"]: "WORKSPACE LIMIT",
    RECOVERY_DETAIL_CODES["IK_UNSTABLE"]: "IK UNSTABLE",
    RECOVERY_DETAIL_CODES["IK_DISCONTINUITY"]: "IK DISCONTINUITY",
    RECOVERY_DETAIL_CODES["FEEDBACK"]: "FEEDBACK",
    RECOVERY_DETAIL_CODES["FOLLOW_ERROR"]: "ARM LAG",
    RECOVERY_DETAIL_CODES["FEEDBACK_ENVELOPE"]: "JOINT BUFFER",
}


def hand_open_fist_score(points):
    """Return xteleop's mean four-fingertip distance / palm-size score."""
    points = np.asarray(points, dtype=float)
    if points.shape != (25, 3) or not np.all(np.isfinite(points)):
        return None
    palm_size = float(np.linalg.norm(points[10] - points[0]))
    if palm_size < 1e-6:
        return None
    tip_distance = np.mean([
        np.linalg.norm(points[index] - points[0]) for index in (9, 14, 19, 24)
    ])
    return float(tip_distance / palm_size)


def thumb_index_pinch_score(points):
    """Return thumb-tip/index-tip distance normalized by palm size."""
    points = np.asarray(points, dtype=float)
    if points.shape != (25, 3) or not np.all(np.isfinite(points)):
        return None
    palm_size = float(np.linalg.norm(points[10] - points[0]))
    if palm_size < 1e-6:
        return None
    return float(np.linalg.norm(points[4] - points[9]) / palm_size)


def both_hands_pinching(points, threshold=0.20):
    """Detect xteleop-style simultaneous thumb/index pinches."""
    scores = [thumb_index_pinch_score(points[side]) for side in ("left", "right")]
    return all(score is not None and score < float(threshold) for score in scores)


def valid_hand(wrist, points, hand_size_min=0.030, hand_size_max=0.35):
    points = np.asarray(points, dtype=float)
    wrist = np.asarray(wrist, dtype=float)
    if points.shape != (25, 3) or wrist.shape != (4, 4):
        return False
    if not np.all(np.isfinite(points)) or not np.all(np.isfinite(wrist)):
        return False
    if abs(float(np.linalg.det(wrist[:3, :3]))) < 1e-6:
        return False
    palm_size = float(np.linalg.norm(points[10] - points[0]))
    spread = float(np.max(np.linalg.norm(points - points[0], axis=1)))
    epsilon = 0.003
    return bool(
        hand_size_min - epsilon <= palm_size <= hand_size_max
        and spread >= hand_size_min - epsilon
    )


_R_FIX_LEFT = np.array([[0.0, 0.0, 1.0],
                        [1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0]])
_R_FIX_RIGHT = np.diag([1.0, 1.0, -1.0]) @ _R_FIX_LEFT


def palm_up_score(wrist, side, head=None):
    """Return the xteleop palm-axis dot product with world up.

    This reproduces xteleop's head-relative wrist transform, per-side R_fix,
    palm axis 0, and opposite left/right command_palm_sign values.
    """
    wrist = np.asarray(wrist, dtype=float)
    if wrist.shape != (4, 4) or not np.all(np.isfinite(wrist)):
        return None
    rotation = wrist[:3, :3]
    if head is not None:
        head = np.asarray(head, dtype=float)
        if head.shape != (4, 4) or not np.all(np.isfinite(head)):
            return None
        rotation = head[:3, :3].T @ rotation
    mapping = _R_FIX_LEFT if side == "left" else _R_FIX_RIGHT
    fixed = mapping @ rotation @ mapping.T
    sign = 1.0 if side == "left" else -1.0
    normal = sign * fixed[:, 0]
    norm = float(np.linalg.norm(normal))
    if norm < 1e-8:
        return None
    return float(normal[2] / norm)


class GestureSafetyController:
    """Continuous-hold start/stop gestures with xteleop anti-retrigger guards."""

    def __init__(
        self,
        enabled=False,
        start_hold=5.0,
        stop_hold=3.0,
        release_hold=1.0,
        cooldown=2.0,
        valid_need=3,
        invalid_grace=0.8,
        open_ratio=3.0,
        fist_ratio=2.35,
        palm_up_dot=0.65,
        hand_size_min=0.030,
        hand_size_max=0.35,
    ):
        self.enabled = bool(enabled)
        self.start_hold = float(start_hold)
        self.stop_hold = float(stop_hold)
        self.release_hold = float(release_hold)
        self.cooldown = float(cooldown)
        self.valid_need = int(valid_need)
        self.invalid_grace = float(invalid_grace)
        self.open_ratio = float(open_ratio)
        self.fist_ratio = float(fist_ratio)
        self.palm_up_dot = float(palm_up_dot)
        self.hand_size_min = float(hand_size_min)
        self.hand_size_max = float(hand_size_max)
        self.valid_count = 0
        self.invalid_since = None
        self.hold_kind = None
        self.hold_t0 = None
        self.release_kind = None
        self.release_clear_t0 = None
        self.cooldown_until = 0.0

    def force_enabled(self, enabled, now):
        self.enabled = bool(enabled)
        self.hold_kind = None
        self.hold_t0 = None
        self.release_kind = None
        self.release_clear_t0 = None
        self.cooldown_until = float(now) + 0.2

    @property
    def release_pending(self):
        return self.release_kind is not None

    def _clear_hold(self):
        self.hold_kind = None
        self.hold_t0 = None

    def cancel_hold(self):
        """Cancel an in-progress start/stop hold without arming a command.

        PAUSED_HOLD gives the full-exit pinch gesture priority over the
        palms-up realignment gesture.  This public helper prevents time spent
        pinching from remaining in the realignment countdown.
        """
        self._clear_hold()

    def tracking_invalid(self, now):
        now = float(now)
        if self.invalid_since is None:
            self.invalid_since = now
        if now - self.invalid_since >= self.invalid_grace:
            self._clear_hold()
            self.valid_count = 0
        return self._hud("TRACKING_INVALID", 0.0, 0.0)

    def _hud(self, state, remaining=0.0, progress=0.0):
        return {
            "code": HUD_CODES[state],
            "state": state,
            "remaining": max(0.0, float(remaining)),
            "progress": min(1.0, max(0.0, float(progress))),
            "enabled": self.enabled,
        }

    def _gesture_flags(self, wrists, points, head):
        scores = {
            side: hand_open_fist_score(points[side]) for side in ("left", "right")
        }
        both_open = all(
            scores[side] is not None and scores[side] > self.open_ratio
            for side in ("left", "right")
        )
        both_fist = all(
            scores[side] is not None and scores[side] < self.fist_ratio
            for side in ("left", "right")
        )
        both_palms_up = all(
            palm_up_score(wrists[side], side, head) is not None
            and palm_up_score(wrists[side], side, head) > self.palm_up_dot
            for side in ("left", "right")
        )
        return both_open and both_palms_up, both_fist

    def update(self, now, wrists, points, fresh=True, head=None):
        """Return ``(event, hud)`` where event is ``start``, ``stop`` or None."""
        now = float(now)
        head_valid = (
            head is None or (
                np.asarray(head).shape == (4, 4)
                and np.all(np.isfinite(head))
                and abs(float(np.linalg.det(np.asarray(head)[:3, :3]))) > 1e-6
            )
        )
        input_valid = head_valid and all(
            valid_hand(
                wrists[side], points[side], self.hand_size_min, self.hand_size_max
            )
            for side in ("left", "right")
        )
        if not input_valid:
            if fresh:
                self.valid_count = max(0, self.valid_count - 1)
            return None, self.tracking_invalid(now)
        if fresh:
            self.valid_count += 1
        if self.valid_count < self.valid_need:
            # A valid recovery frame must survive long enough to accumulate
            # ``valid_need`` consecutive samples. Calling tracking_invalid()
            # here would clear the new count immediately whenever the prior
            # dropout had already exceeded invalid_grace.
            self.invalid_since = None
            return None, self._hud("TRACKING_INVALID", 0.0, 0.0)
        self.invalid_since = None

        start_gesture, stop_gesture = self._gesture_flags(wrists, points, head)

        # After either command, the triggering pose must be left continuously
        # before any future command can arm. Tracking loss never counts as a
        # release because this block is reached only for valid input.
        if self.release_kind is not None:
            still_held = start_gesture if self.release_kind == "start" else stop_gesture
            if still_held:
                self.release_clear_t0 = None
                remaining = self.release_hold
            else:
                if self.release_clear_t0 is None:
                    self.release_clear_t0 = now
                elapsed = now - self.release_clear_t0
                remaining = max(0.0, self.release_hold - elapsed)
                if elapsed >= self.release_hold:
                    self.release_kind = None
                    self.release_clear_t0 = None
            return None, self._hud(
                "RELEASE_TO_REARM", remaining,
                1.0 - remaining / max(self.release_hold, 1e-6),
            )

        if now < self.cooldown_until:
            remaining = self.cooldown_until - now
            return None, self._hud(
                "COOLDOWN", remaining, 1.0 - remaining / max(self.cooldown, 1e-6)
            )

        kind = "stop" if self.enabled else "start"
        detected = stop_gesture if self.enabled else start_gesture
        hold_time = self.stop_hold if self.enabled else self.start_hold
        if not detected:
            self._clear_hold()
            state = "ACTIVE" if self.enabled else "READY_TO_START"
            return None, self._hud(state)

        if self.hold_kind != kind or self.hold_t0 is None:
            self.hold_kind = kind
            self.hold_t0 = now
        elapsed = max(0.0, now - self.hold_t0)
        remaining = max(0.0, hold_time - elapsed)
        state = "STOP_COUNTDOWN" if kind == "stop" else "START_COUNTDOWN"
        if elapsed < hold_time:
            return None, self._hud(state, remaining, elapsed / max(hold_time, 1e-6))

        self.enabled = kind == "start"
        self._clear_hold()
        self.release_kind = kind
        self.release_clear_t0 = None
        self.cooldown_until = now + self.cooldown
        return kind, self._hud("RELEASE_TO_REARM", self.release_hold, 0.0)
