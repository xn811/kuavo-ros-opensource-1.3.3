from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np

from .math3d import limit_rotation_step, project_rotation


def base_alignment_from_head(head, initial_mapping=None):
    """Return a rotation that aligns the operator's horizontal forward to Base +X.

    ``head`` is already expressed in the bridge's Z-up WebXR convention.  The
    returned matrix maps vectors from that convention into ``base_link``.  Only
    yaw is calibrated so gravity remains shared by WebXR and the robot.
    """
    initial = project_rotation(
        np.eye(3) if initial_mapping is None else initial_mapping
    )
    rotation = project_rotation(np.asarray(head, dtype=float).reshape(4, 4)[:3, :3])
    forward = initial @ rotation[:, 0]
    forward[2] = 0.0
    norm = float(np.linalg.norm(forward))
    if norm < 1e-6:
        raise ValueError("head forward is vertical; cannot align WebXR yaw to base_link")
    forward /= norm
    yaw = float(np.arctan2(forward[1], forward[0]))
    cosine, sine = np.cos(-yaw), np.sin(-yaw)
    yaw_correction = np.array([
        [cosine, -sine, 0.0],
        [sine, cosine, 0.0],
        [0.0, 0.0, 1.0],
    ])
    return project_rotation(yaw_correction @ initial)


def _rotation_distance(a, b):
    relative = project_rotation(a).T @ project_rotation(b)
    cosine = np.clip((np.trace(relative) - 1.0) * 0.5, -1.0, 1.0)
    return float(np.arccos(cosine))


class PoseStabilityWindow:
    """Collect a stable multi-frame neutral pose before enabling robot output."""

    def __init__(self, hold_seconds=1.0, min_samples=30,
                 max_position_spread=0.015, max_rotation_spread=0.12):
        self.hold_seconds = float(hold_seconds)
        self.min_samples = int(min_samples)
        self.max_position_spread = float(max_position_spread)
        self.max_rotation_spread = float(max_rotation_spread)
        self._samples = []

    def reset(self):
        self._samples = []

    @property
    def sample_count(self):
        return len(self._samples)

    @property
    def duration(self):
        if len(self._samples) < 2:
            return 0.0
        return max(0.0, self._samples[-1][0] - self._samples[0][0])

    def add(self, timestamp, wrists, head, landmarks=None):
        timestamp = float(timestamp)
        sample = (
            timestamp,
            {side: np.asarray(wrists[side], dtype=float).reshape(4, 4).copy()
             for side in ("left", "right")},
            np.asarray(head, dtype=float).reshape(4, 4).copy(),
            None if landmarks is None else {
                side: np.asarray(landmarks[side], dtype=float).reshape(25, 3).copy()
                for side in ("left", "right")
            },
        )
        self._samples.append(sample)
        cutoff = timestamp - self.hold_seconds
        while self._samples and self._samples[0][0] < cutoff:
            self._samples.pop(0)
        return self.ready

    @property
    def ready(self):
        if self.sample_count < self.min_samples or self.duration < self.hold_seconds * 0.95:
            return False
        for group in ([sample[2] for sample in self._samples],) + tuple(
            [sample[1][side] for sample in self._samples] for side in ("left", "right")
        ):
            mean_position = np.mean([pose[:3, 3] for pose in group], axis=0)
            mean_rotation = project_rotation(np.mean([pose[:3, :3] for pose in group], axis=0))
            if max(np.linalg.norm(pose[:3, 3] - mean_position) for pose in group) > self.max_position_spread:
                return False
            if max(_rotation_distance(mean_rotation, pose[:3, :3]) for pose in group) > self.max_rotation_spread:
                return False
        return True

    @staticmethod
    def _average_pose(poses):
        result = np.eye(4)
        result[:3, 3] = np.mean([pose[:3, 3] for pose in poses], axis=0)
        result[:3, :3] = project_rotation(
            np.mean([pose[:3, :3] for pose in poses], axis=0)
        )
        return result

    def average(self):
        if not self.ready:
            raise RuntimeError("calibration stability window is not ready")
        wrists = {
            side: self._average_pose([sample[1][side] for sample in self._samples])
            for side in ("left", "right")
        }
        head = self._average_pose([sample[2] for sample in self._samples])
        landmarks = None
        if all(sample[3] is not None for sample in self._samples):
            landmarks = {
                side: np.mean([sample[3][side] for sample in self._samples], axis=0)
                for side in ("left", "right")
            }
        return wrists, head, landmarks


@dataclass
class HandFrame:
    wrist: np.ndarray
    landmarks: np.ndarray
    valid: bool = True


@dataclass
class HandTrackingSample:
    timestamp: float
    hands: Dict[str, HandFrame]


@dataclass
class ArmTarget:
    position: np.ndarray
    rotation: np.ndarray


class ArmRetargeter:
    """Calibration-relative WebXR wrist to robot base-frame target mapping."""

    def __init__(
        self,
        position_scale=(1.55, 1.20, 1.10),
        axis_mapping=None,
        max_linear_speed=0.60,
        max_angular_speed=1.20,
        workspace_min=(0.10, -0.65, -0.25),
        workspace_max=(0.75, 0.65, 0.65),
        max_input_position_jump=0.20,
        max_input_rotation_jump=0.80,
        shoulder_positions=None,
        min_shoulder_reach=0.15,
        max_shoulder_reach=0.62,
        midline_margin=0.05,
        body_exclusion_front=0.18,
        body_exclusion_half_width=0.20,
    ):
        self.position_scale = np.asarray(position_scale, dtype=float).reshape(3)
        self.axis_mapping = project_rotation(
            np.eye(3) if axis_mapping is None else axis_mapping
        )
        self.max_linear_speed = float(max_linear_speed)
        self.max_angular_speed = float(max_angular_speed)
        self.workspace_min = np.asarray(workspace_min, dtype=float).reshape(3)
        self.workspace_max = np.asarray(workspace_max, dtype=float).reshape(3)
        self.max_input_position_jump = float(max_input_position_jump)
        self.max_input_rotation_jump = float(max_input_rotation_jump)
        default_shoulders = {
            "left": (-0.017499853, 0.2927, 0.4245),
            "right": (-0.017499853, -0.2927, 0.4245),
        }
        shoulder_positions = default_shoulders if shoulder_positions is None else shoulder_positions
        self.shoulder_positions = {
            side: np.asarray(shoulder_positions[side], dtype=float).reshape(3)
            for side in ("left", "right")
        }
        self.min_shoulder_reach = float(min_shoulder_reach)
        self.max_shoulder_reach = float(max_shoulder_reach)
        self.midline_margin = float(midline_margin)
        self.body_exclusion_front = float(body_exclusion_front)
        self.body_exclusion_half_width = float(body_exclusion_half_width)
        if not 0.0 <= self.min_shoulder_reach < self.max_shoulder_reach:
            raise ValueError("shoulder reach bounds are invalid")
        self._xr_reference = {}
        self._robot_reference = {}
        self._last_target = {}
        self._last_xr_wrist = {}
        self._constraint_projection = {}
        self._last_timestamp: Optional[float] = None

    @property
    def calibrated(self):
        return all(side in self._xr_reference for side in ("left", "right"))

    @property
    def constraint_projection(self):
        """Cartesian distance each raw target was moved by safety constraints."""
        return dict(self._constraint_projection)

    @property
    def max_constraint_projection(self):
        if not all(side in self._constraint_projection for side in ("left", "right")):
            return float("inf")
        return max(self._constraint_projection.values())

    def reset(self):
        self._xr_reference.clear()
        self._robot_reference.clear()
        self._last_target.clear()
        self._last_xr_wrist.clear()
        self._constraint_projection.clear()
        self._last_timestamp = None

    def set_axis_mapping(self, axis_mapping):
        self.axis_mapping = project_rotation(axis_mapping)

    def _constrain_position(self, side, position):
        """Project an R6 target into conservative v49 Cartesian safety bounds."""
        position = np.clip(
            np.asarray(position, dtype=float).reshape(3),
            self.workspace_min, self.workspace_max,
        )
        sign = 1.0 if side == "left" else -1.0
        position[1] = sign * max(sign * position[1], self.midline_margin)
        if (position[0] < self.body_exclusion_front and
                abs(position[1]) < self.body_exclusion_half_width):
            position[1] = sign * self.body_exclusion_half_width

        shoulder = self.shoulder_positions[side]
        offset = position - shoulder
        reach = float(np.linalg.norm(offset))
        if reach < 1e-8:
            offset = np.array([1.0, 0.0, 0.0])
            reach = 1.0
        bounded_reach = float(np.clip(
            reach, self.min_shoulder_reach, self.max_shoulder_reach
        ))
        if abs(bounded_reach - reach) > 1e-9:
            position = shoulder + offset * (bounded_reach / reach)
        return np.clip(position, self.workspace_min, self.workspace_max)

    def calibrate(self, xr_wrists, robot_poses, timestamp):
        for side in ("left", "right"):
            xr = np.asarray(xr_wrists[side], dtype=float).reshape(4, 4)
            position, quaternion = robot_poses[side]
            robot = np.eye(4)
            robot[:3, 3] = np.asarray(position, dtype=float).reshape(3)
            from .math3d import rotation_from_quaternion_xyzw
            robot[:3, :3] = rotation_from_quaternion_xyzw(quaternion)
            self._xr_reference[side] = xr.copy()
            self._robot_reference[side] = robot
            self._last_target[side] = ArmTarget(robot[:3, 3].copy(), robot[:3, :3].copy())
            self._last_xr_wrist[side] = xr.copy()
            self._constraint_projection[side] = 0.0
        self._last_timestamp = float(timestamp)

    def update(self, xr_wrists, timestamp):
        if not self.calibrated:
            raise RuntimeError("arm retargeter is not calibrated")
        dt = np.clip(float(timestamp) - float(self._last_timestamp), 1.0 / 240.0, 0.1)
        targets = {}
        for side in ("left", "right"):
            xr = np.asarray(xr_wrists[side], dtype=float).reshape(4, 4)
            previous_xr = self._last_xr_wrist[side]
            position_jump = float(np.linalg.norm(
                xr[:3, 3] - previous_xr[:3, 3]
            ))
            rotation_jump = _rotation_distance(
                previous_xr[:3, :3], xr[:3, :3]
            )
            if position_jump > self.max_input_position_jump:
                raise ValueError(
                    "{} wrist position jumped {:.3f} m".format(side, position_jump)
                )
            if rotation_jump > self.max_input_rotation_jump:
                raise ValueError(
                    "{} wrist rotation jumped {:.3f} rad".format(side, rotation_jump)
                )
            xr0 = self._xr_reference[side]
            robot0 = self._robot_reference[side]
            delta_world = xr[:3, 3] - xr0[:3, 3]
            raw_position = (
                robot0[:3, 3] +
                self.axis_mapping @ (self.position_scale * delta_world)
            )
            position = self._constrain_position(side, raw_position)
            self._constraint_projection[side] = float(
                np.linalg.norm(position - raw_position)
            )

            # Use a world-frame wrist rotation delta, map that delta into Base,
            # then apply it to the Base-frame robot reference.  The former
            # local-delta/post-multiply form was only correct for identity
            # calibration attitudes and could rotate about the wrong axis.
            world_rotation_delta = xr[:3, :3] @ xr0[:3, :3].T
            mapped_rotation = (
                self.axis_mapping @ world_rotation_delta @ self.axis_mapping.T
            )
            rotation = project_rotation(mapped_rotation @ robot0[:3, :3])
            previous = self._last_target[side]
            max_step = self.max_linear_speed * dt
            delta = position - previous.position
            norm = float(np.linalg.norm(delta))
            if norm > max_step > 0.0:
                position = previous.position + delta * (max_step / norm)
            rotation = limit_rotation_step(
                previous.rotation, rotation, self.max_angular_speed * dt
            )
            target = ArmTarget(position, rotation)
            self._last_target[side] = target
            self._last_xr_wrist[side] = xr.copy()
            targets[side] = target
        self._last_timestamp = float(timestamp)
        return targets


class HeadRetargeter:
    """Map a calibration-relative WebXR HMD rotation to Kuavo yaw/pitch degrees."""

    def __init__(self, axis_mapping=None, yaw_limits=(-90.0, 90.0),
                 pitch_limits=(-20.0, 30.0), yaw_sign=1.0, pitch_sign=1.0):
        self.axis_mapping = project_rotation(
            np.eye(3) if axis_mapping is None else axis_mapping
        )
        self.yaw_limits = np.asarray(yaw_limits, dtype=float).reshape(2)
        self.pitch_limits = np.asarray(pitch_limits, dtype=float).reshape(2)
        self.yaw_sign = float(yaw_sign)
        self.pitch_sign = float(pitch_sign)
        self._reference = None

    @property
    def calibrated(self):
        return self._reference is not None

    def reset(self):
        self._reference = None

    def calibrate(self, head):
        self._reference = project_rotation(np.asarray(head, dtype=float)[:3, :3])

    def update(self, head):
        if not self.calibrated:
            raise RuntimeError("head retargeter is not calibrated")
        current = project_rotation(np.asarray(head, dtype=float)[:3, :3])
        relative = self._reference.T @ current
        relative = self.axis_mapping @ relative @ self.axis_mapping.T
        # In the converted Z-up convention +X is headset forward, +Y is left.
        forward = relative[:, 0]
        yaw = np.degrees(np.arctan2(forward[1], forward[0])) * self.yaw_sign
        pitch = np.degrees(np.arctan2(
            forward[2], np.hypot(forward[0], forward[1])
        )) * self.pitch_sign
        yaw = float(np.clip(yaw, self.yaw_limits[0], self.yaw_limits[1]))
        pitch = float(np.clip(pitch, self.pitch_limits[0], self.pitch_limits[1]))
        return round(yaw, 2), round(pitch, 2)
