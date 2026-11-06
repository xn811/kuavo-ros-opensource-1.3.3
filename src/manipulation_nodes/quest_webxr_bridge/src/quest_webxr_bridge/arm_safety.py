"""ROS-free joint-command safety primitives for Kuavo WebXR control.

Angles, angular velocities and angular accelerations in this module use
degrees.  This matches the public ``/kuavo_arm_traj`` contract used by
``ik_ros_uni.py`` and keeps the limiter independent from ROS messages.
"""

import numpy as np


RECOVERABLE_ADAPTER_FAULTS = frozenset((
    "FEEDBACK_OUTSIDE_SAFE_ENVELOPE",
    "IK_TARGET_JUMP",
    "IK_TARGET_OUTSIDE_SAFE_ENVELOPE",
    "IK_TARGET_STALE",
    "RECOVERY_TARGET_LEAD",
    "TRACKING_ERROR",
))


def safety_fault_recovery_pose(fault):
    """Return the guarded calibration pose for a gesture-recoverable hard fault.

    Active-teleoperation adapter faults normally use the live shadow-IK
    recovery path.  The same narrowly classified faults can, however, become a
    latched ``SAFETY_FAULT`` while checking the first IK handoff.  Those faults
    restart from the configured L calibration pose.  An automatic-motion
    timeout is treated separately: it retreats to the already validated
    T_BENT clearance pose and calibrates there instead of retrying a possibly
    obstructed L target.
    """
    reason = str(fault or "")
    if reason.startswith("AUTO_MOTION_TIMEOUT"):
        return "t_bent"
    if reason.startswith("IK_HANDOFF_DISCONTINUITY"):
        return "l"
    if reason.startswith("ADAPTER_"):
        adapter_fault = reason[len("ADAPTER_"):]
        if adapter_fault_is_recoverable(adapter_fault):
            return "l"
    return None


def adapter_fault_is_recoverable(fault):
    """Return whether an adapter fault may recover from safe WebXR backtracking."""
    return str(fault or "") in RECOVERABLE_ADAPTER_FAULTS


def envelope_margin(target, lower, upper):
    """Return the smallest target distance to a joint envelope, in degrees."""
    target = np.asarray(target, dtype=float).reshape(-1)
    lower = np.asarray(lower, dtype=float).reshape(-1)
    upper = np.asarray(upper, dtype=float).reshape(-1)
    if (target.shape != lower.shape or target.shape != upper.shape or
            not np.all(np.isfinite(target + lower + upper))):
        raise ValueError("target and envelope must be finite matching vectors")
    return float(np.min(np.minimum(target - lower, upper - target)))


def recovery_target_safe(
        status, feedback_ready, feedback_timeout, ik_timeout,
        minimum_envelope_margin, constraint_projection,
        maximum_constraint_projection, require_handoff=False,
        maximum_follow_error=None):
    """Return whether a live IK target may be followed during recovery.

    Target-to-target delta is deliberately not part of this predicate.  A
    valid moving target may keep changing while the recovery limiter follows
    it slowly.  Raw IK jumps remain rejected by the adapter; this predicate
    additionally bounds how far the live target may lead measured joints.
    """
    feedback_age = status.get("feedback_age_s")
    ik_age = status.get("ik_target_age_s")
    margin = status.get("ik_envelope_margin_deg")
    try:
        safe = bool(
            not status.get("fault") and
            feedback_ready and
            feedback_age is not None and
            float(feedback_age) <= float(feedback_timeout) and
            ik_age is not None and
            float(ik_age) <= float(ik_timeout) and
            margin is not None and
            float(margin) >= float(minimum_envelope_margin) and
            float(constraint_projection) <=
            float(maximum_constraint_projection)
        )
        if require_handoff:
            safe = safe and bool(status.get("ik_handoff_ready", False))
        if maximum_follow_error is not None:
            follow_error = status.get("ik_handoff_error_deg")
            safe = bool(
                safe and follow_error is not None and
                float(follow_error) <= float(maximum_follow_error)
            )
        return safe
    except (TypeError, ValueError):
        return False


def feedback_bounded_target(target, feedback, lower, upper, maximum_lead):
    """Bound a command target around fresh measured feedback.

    This is command backpressure, not a rejection of a distant IK target.  The
    live IK target may remain arbitrarily far away while recovery follows it;
    only the next command presented to the low-speed limiter is kept within a
    per-joint lead of measured motion.  If contact prevents a joint from
    moving, commanded motion therefore cannot accumulate far beyond it.
    """
    target = np.asarray(target, dtype=float).reshape(-1)
    feedback = np.asarray(feedback, dtype=float).reshape(-1)
    lower = np.asarray(lower, dtype=float).reshape(-1)
    upper = np.asarray(upper, dtype=float).reshape(-1)
    lead = np.asarray(maximum_lead, dtype=float).reshape(-1)
    if lead.size == 1:
        lead = np.repeat(lead, target.size)
    vectors = (target, feedback, lower, upper, lead)
    if (any(vector.shape != target.shape for vector in vectors) or
            not all(np.all(np.isfinite(vector)) for vector in vectors) or
            np.any(lower >= upper) or np.any(lead <= 0.0)):
        raise ValueError(
            "target, feedback, envelope and positive lead must be finite "
            "matching vectors"
        )
    local_lower = np.maximum(lower, feedback - lead)
    local_upper = np.minimum(upper, feedback + lead)
    return np.clip(target, local_lower, local_upper)


class RecoveryReadinessGate:
    """Require fresh consecutive safe adapter reports before automatic resume."""

    def __init__(self, valid_frames, hold_seconds):
        self.valid_frames = int(valid_frames)
        self.hold_seconds = float(hold_seconds)
        if self.valid_frames <= 0 or self.hold_seconds < 0.0:
            raise ValueError("recovery gate thresholds must be non-negative")
        self.reset()

    def reset(self):
        self.count = 0
        self.last_serial = None
        self.ready_since = None

    def update(self, now, serial, valid):
        now = float(now)
        if not valid:
            self.reset()
            return False, 0.0, 0.0
        if serial != self.last_serial:
            self.last_serial = serial
            self.count += 1
        frame_progress = min(1.0, self.count / float(self.valid_frames))
        if self.count < self.valid_frames:
            self.ready_since = None
            return False, 0.0, frame_progress
        if self.ready_since is None:
            self.ready_since = now
        elapsed = max(0.0, now - self.ready_since)
        remaining = max(0.0, self.hold_seconds - elapsed)
        if elapsed + 1e-9 >= self.hold_seconds:
            remaining = 0.0
        hold_progress = (
            1.0 if self.hold_seconds <= 0.0
            else min(1.0, elapsed / self.hold_seconds)
        )
        return elapsed + 1e-9 >= self.hold_seconds, remaining, hold_progress


class ArmCommandLimiter:
    """Apply target-envelope validation and joint velocity/acceleration limits.

    ``lower``/``upper`` are the conservative command envelope.  Optional
    ``feedback_lower``/``feedback_upper`` bounds are the mechanical envelope
    from which measured joints may be seeded.  Keeping the two envelopes
    separate lets a joint that has drifted through the conservative margin
    return at the configured low-speed profile without ever accepting an
    out-of-envelope command target.
    """

    def __init__(self, lower, upper, velocity, acceleration,
                 feedback_lower=None, feedback_upper=None):
        self.lower = self._vector(lower, "lower")
        self.upper = self._vector(upper, "upper")
        self.velocity_limit = self._positive_vector(velocity, "velocity")
        self.acceleration_limit = self._positive_vector(
            acceleration, "acceleration"
        )
        if np.any(self.lower >= self.upper):
            raise ValueError("every lower joint limit must be below its upper limit")
        self.feedback_lower = (
            self.lower.copy() if feedback_lower is None else
            self._vector(feedback_lower, "feedback_lower")
        )
        self.feedback_upper = (
            self.upper.copy() if feedback_upper is None else
            self._vector(feedback_upper, "feedback_upper")
        )
        if (self.feedback_lower.size != self.lower.size or
                self.feedback_upper.size != self.lower.size):
            raise ValueError("feedback envelopes must match the target envelope")
        if (np.any(self.feedback_lower >= self.feedback_upper) or
                np.any(self.feedback_lower > self.lower) or
                np.any(self.feedback_upper < self.upper)):
            raise ValueError(
                "feedback envelope must contain the complete target envelope"
            )
        self.position = None
        self.velocity = np.zeros(self.lower.size, dtype=float)

    @staticmethod
    def _vector(value, name):
        vector = np.asarray(value, dtype=float).reshape(-1)
        if vector.size == 0 or not np.all(np.isfinite(vector)):
            raise ValueError("{} must be a finite, non-empty vector".format(name))
        return vector

    def _positive_vector(self, value, name):
        vector = self._vector(value, name)
        if vector.size == 1:
            vector = np.repeat(vector, self.lower.size)
        if vector.size != self.lower.size or np.any(vector <= 0.0):
            raise ValueError(
                "{} must contain one or {} positive values".format(
                    name, self.lower.size
                )
            )
        return vector

    @property
    def joint_count(self):
        return self.lower.size

    def validate(self, target, tolerance=1e-6):
        target = self._vector(target, "target")
        if target.size != self.joint_count:
            raise ValueError("target must contain {} joints".format(self.joint_count))
        if (np.any(target < self.lower - tolerance) or
                np.any(target > self.upper + tolerance)):
            bad = np.where(
                (target < self.lower - tolerance) |
                (target > self.upper + tolerance)
            )[0]
            raise ValueError(
                "target exceeds safe joint envelope at zero-based joints {}".format(
                    bad.tolist()
                )
            )
        return target

    def validate_feedback(self, position, tolerance=0.5):
        position = self._vector(position, "feedback position")
        if position.size != self.joint_count:
            raise ValueError(
                "feedback position must contain {} joints".format(
                    self.joint_count
                )
            )
        if (np.any(position < self.feedback_lower - tolerance) or
                np.any(position > self.feedback_upper + tolerance)):
            bad = np.where(
                (position < self.feedback_lower - tolerance) |
                (position > self.feedback_upper + tolerance)
            )[0]
            raise ValueError(
                "feedback exceeds mechanical joint envelope at zero-based "
                "joints {}".format(bad.tolist())
            )
        return position

    def seed(self, position, tolerance=0.5):
        # Seed from measured feedback, including the conservative margin, but
        # never from beyond the mechanical feedback envelope.  Do not clip to
        # the target envelope here: step() must bring the command back through
        # that margin under the configured velocity/acceleration limits.
        position = self.validate_feedback(position, tolerance=tolerance)
        self.position = np.clip(
            position, self.feedback_lower, self.feedback_upper
        )
        self.velocity = np.zeros(self.joint_count, dtype=float)
        return self.position.copy()

    def set_profile(self, velocity, acceleration):
        self.velocity_limit = self._positive_vector(velocity, "velocity")
        self.acceleration_limit = self._positive_vector(
            acceleration, "acceleration"
        )

    def step(self, target, dt):
        target = self.validate(target)
        dt = float(dt)
        if not np.isfinite(dt) or dt <= 0.0:
            raise ValueError("dt must be positive and finite")
        dt = min(dt, 0.05)
        if self.position is None:
            raise RuntimeError("limiter must be seeded from fresh feedback")

        error = target - self.position
        direction = np.sign(error)
        # A braking bound prevents the acceleration-limited velocity from
        # carrying a joint through its target on the following cycles.
        braking_velocity = np.sqrt(
            np.maximum(0.0, 2.0 * self.acceleration_limit * np.abs(error))
        )
        desired_velocity = direction * np.minimum(
            self.velocity_limit, braking_velocity
        )
        velocity_delta = np.clip(
            desired_velocity - self.velocity,
            -self.acceleration_limit * dt,
            self.acceleration_limit * dt,
        )
        next_velocity = np.clip(
            self.velocity + velocity_delta,
            -self.velocity_limit,
            self.velocity_limit,
        )
        step = next_velocity * dt
        overshoot = np.abs(step) >= np.abs(error)
        next_position = self.position + step
        next_position[overshoot] = target[overshoot]
        next_velocity[overshoot] = 0.0

        self.position = np.clip(
            next_position, self.feedback_lower, self.feedback_upper
        )
        self.velocity = next_velocity
        return self.position.copy(), self.velocity.copy()


def max_abs_joint_error(a, b):
    """Return the largest absolute joint-space error in degrees."""
    left = np.asarray(a, dtype=float).reshape(-1)
    right = np.asarray(b, dtype=float).reshape(-1)
    if left.shape != right.shape or not np.all(np.isfinite(left + right)):
        raise ValueError("joint vectors must be finite and have matching shapes")
    return float(np.max(np.abs(left - right)))
