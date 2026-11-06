import numpy as np


def _signed_angle(a, b, axis):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    axis = np.asarray(axis, dtype=float)
    a /= max(np.linalg.norm(a), 1e-9)
    b /= max(np.linalg.norm(b), 1e-9)
    axis /= max(np.linalg.norm(axis), 1e-9)
    return float(np.arctan2(np.dot(axis, np.cross(a, b)), np.dot(a, b)))


def _norm01(value, open_value, closed_value):
    denominator = float(closed_value - open_value)
    if abs(denominator) < 1e-8:
        return 0.0
    return float(np.clip((value - open_value) / denominator, 0.0, 1.0))


class FingerRetargeter:
    """Retarget xteleop's 25 WebXR landmarks to Kuavo's six hand channels."""

    _CLOSE_CHANNEL_NAMES = ("thumb", "index", "middle", "ring", "pinky")

    def __init__(
            self, thumb_swap=False, thumb_aux_value=100,
            finger_close_denominators=None):
        self.thumb_swap = bool(thumb_swap)
        self.thumb_aux_value = None if thumb_aux_value is None else int(
            np.clip(thumb_aux_value, 0, 100)
        )
        configured = dict(finger_close_denominators or {})
        unknown = set(configured) - set(self._CLOSE_CHANNEL_NAMES)
        if unknown:
            raise ValueError(
                "unknown finger close denominator(s): {}".format(
                    ", ".join(sorted(unknown))
                )
            )
        denominators = {
            name: float(configured.get(name, 1.0))
            for name in self._CLOSE_CHANNEL_NAMES
        }
        if any(
                not np.isfinite(value) or value <= 0.0
                for value in denominators.values()):
            raise ValueError(
                "finger close denominators must be finite and greater than zero"
            )
        self.thumb_close_denominator = denominators["thumb"]
        self.finger_close_denominators = np.array([
            denominators["index"], denominators["middle"],
            denominators["ring"], denominators["pinky"],
        ], dtype=float)
        self._states = {"left": {}, "right": {}}

    def reset(self):
        self._states = {"left": {}, "right": {}}

    def update(self, side, landmarks):
        points = np.asarray(landmarks, dtype=float)
        if points.shape != (25, 3) or not np.all(np.isfinite(points)):
            return None
        wrist = points[0]
        hand_size = float(np.max(np.linalg.norm(points - wrist, axis=1)))
        if not 0.08 <= hand_size <= 0.35:
            return None
        palm_size = float(np.linalg.norm(points[10] - wrist))
        if palm_size < 0.025:
            return None

        thumb_mcp, thumb_ip, thumb_tip = points[2], points[3], points[4]
        index_root, index_tip = points[5], points[9]
        middle_root, middle_tip = points[10], points[14]
        ring_tip = points[19]
        little_root, little_tip = points[20], points[24]

        # Original palm normal (landmarks 0-5-20), kept for easy rollback:
        # x_axis = index_root - wrist
        # palm_vec = little_root - wrist

        # Trial palm normal (landmarks 0-10-20): wrist, middle root, little root.
        x_axis = middle_root - wrist
        palm_vec = little_root - wrist
        if np.linalg.norm(x_axis) < 1e-7 or np.linalg.norm(palm_vec) < 1e-7:
            return None
        x_axis /= np.linalg.norm(x_axis)
        z_axis = np.cross(x_axis, palm_vec)
        if np.linalg.norm(z_axis) < 1e-7:
            return None
        z_axis /= np.linalg.norm(z_axis)

        thumb_vector = thumb_tip - wrist
        thumb_vector /= max(np.linalg.norm(thumb_vector), 1e-9)
        thumb_abduction = float(np.dot(thumb_vector, z_axis))

        # Original p2-p3-p4 signed-angle thumb bend implementation, kept for
        # easy rollback after the p2-p4 distance trial:
        # thumb_back = thumb_ip - thumb_mcp
        # thumb_front = thumb_tip - thumb_ip

        # Trial thumb bend feature: the p2-p4 chord becomes shorter as the
        # distal thumb folds.  Normalize by the two intervening bone lengths
        # so the feature is independent of operator/Quest hand scale.
        thumb_chain_length = (
            np.linalg.norm(thumb_ip - thumb_mcp)
            + np.linalg.norm(thumb_tip - thumb_ip)
        )
        if thumb_chain_length < 1e-7:
            return None
        thumb_bend_ratio = float(np.clip(
            np.linalg.norm(thumb_tip - thumb_mcp) / thumb_chain_length,
            0.0,
            1.0,
        ))

        state = self._states[side]
        if "thumb_abduction_open" not in state:
            state["thumb_abduction_open"] = thumb_abduction
            # Original p2-p3-p4 signed-angle calibration, kept for rollback:
            # thumb_bend_axis = np.cross(thumb_back, thumb_front)
            # if np.linalg.norm(thumb_bend_axis) < 1e-6:
            #     thumb_bend_axis = z_axis.copy()
            # state["thumb_bend_axis"] = (
            #     thumb_bend_axis / np.linalg.norm(thumb_bend_axis)
            # )
            # state["thumb_bend_open"] = _signed_angle(
            #     thumb_back, thumb_front, state["thumb_bend_axis"]
            # )
        if "thumb_bend_ratio_open" not in state:
            state["thumb_bend_ratio_open"] = thumb_bend_ratio

        # Original p2-p3-p4 signed-angle measurement, kept for rollback:
        # thumb_bend = _signed_angle(
        #     thumb_back, thumb_front, state["thumb_bend_axis"]
        # )

        abduction_delta = 0.35 if side == "right" else -0.45
        thumb_rotation_close = _norm01(
            thumb_abduction,
            state["thumb_abduction_open"],
            state["thumb_abduction_open"] + abduction_delta,
        )
        # Original p2-p3-p4 signed-angle mapping, kept for rollback:
        # thumb_bend_close = _norm01(
        #     thumb_bend,
        #     state["thumb_bend_open"],
        #     state["thumb_bend_open"] - 0.85,
        # )

        # A 0.12 reduction from the calibrated open chord ratio is the first
        # trial range.  Closing shortens the chord, so _norm01 handles a
        # decreasing open-to-closed interval here.
        thumb_bend_ratio_closed = max(
            state["thumb_bend_ratio_open"] - 0.12,
            0.0,
        )
        thumb_bend_close = _norm01(
            thumb_bend_ratio,
            state["thumb_bend_ratio_open"],
            thumb_bend_ratio_closed,
        )
        # Scale only semantic thumb flexion.  Thumb abduction/opposition remains
        # untouched regardless of the published thumb channel order.
        thumb_bend_close = float(np.clip(
            thumb_bend_close / self.thumb_close_denominator, 0.0, 1.0
        ))

        fingertip_ratios = np.array([
            np.linalg.norm(index_tip - wrist) / palm_size,
            np.linalg.norm(middle_tip - wrist) / palm_size,
            np.linalg.norm(ring_tip - wrist) / palm_size,
            np.linalg.norm(little_tip - wrist) / palm_size,
        ])
        if "finger_open_ratios" not in state:
            # The neutral calibration pose is the per-operator open reference.
            # Ratios remove Quest skeleton/hand-size differences while fixed
            # closed ratios retain a usable range before a fist is observed.
            state["finger_open_ratios"] = fingertip_ratios.copy()
        closed_ratios = np.array([1.35, 1.35, 1.30, 1.20])
        open_ratios = np.maximum(
            state["finger_open_ratios"], closed_ratios + 0.35
        )
        finger_close = np.clip(
            (open_ratios - fingertip_ratios) / (open_ratios - closed_ratios),
            0.0, 1.0,
        )
        finger_close = np.clip(
            finger_close / self.finger_close_denominators, 0.0, 1.0
        )

        thumb_channels = np.array([thumb_rotation_close, thumb_bend_close])
        if self.thumb_swap:
            thumb_channels = thumb_channels[::-1]
        if self.thumb_aux_value is None:
            thumb_primary, thumb_aux = thumb_channels
        else:
            # Reference task1 bags use [thumb_close, 100, index, middle,
            # ring, pinky].  Combine the two tracked thumb motions into the
            # primary close channel and keep thumb_aux at the recorded value.
            thumb_primary = float(np.max(thumb_channels))
            thumb_aux = self.thumb_aux_value / 100.0
        raw = np.concatenate(([thumb_primary, thumb_aux], finger_close))

        previous = state.get("filtered")
        if previous is None:
            filtered = raw
        else:
            # Opening is deliberately faster than closing, matching xteleop.
            beta = np.where(raw < previous, 0.98, np.array([0.65, 0.55, 0.75, 0.75, 0.75, 0.75]))
            filtered = previous + beta * (raw - previous)
        state["filtered"] = np.clip(filtered, 0.0, 1.0)
        return np.rint(state["filtered"] * 100.0).astype(np.uint8)
