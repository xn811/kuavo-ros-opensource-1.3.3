import asyncio
import contextlib
import json
import signal
import time
from multiprocessing import Array, Process, Value
from pathlib import Path

import numpy as np

from quest_webxr_bridge.gesture_control import RECOVERY_DETAIL_TEXT


class WebXRHandServer:
    """Small Vuer server exposing Quest WebXR hand matrices to a ROS process."""

    def __init__(self, host, port, cert_file, key_file, fps=60):
        self.host = host
        self.port = int(port)
        self.cert_file = cert_file
        self.key_file = key_file
        self.fps = int(fps)
        self.left_hand = Array("d", 16, lock=True)
        self.right_hand = Array("d", 16, lock=True)
        self.left_landmarks = Array("d", 75, lock=True)
        self.right_landmarks = Array("d", 75, lock=True)
        self.head = Array("d", 16, lock=True)
        self.last_update = Value("d", 0.0, lock=True)
        self.left_last_update = Value("d", 0.0, lock=True)
        self.right_last_update = Value("d", 0.0, lock=True)
        self.head_last_update = Value("d", 0.0, lock=True)
        self.direct_last_update = Value("d", 0.0, lock=True)
        # 0: none, 1: direct XR frame bridge, 2: Vuer HAND_MOVE fallback.
        self.tracking_source = Value("i", 0, lock=True)
        self.input_source_mask = Value("i", 0, lock=True)
        self.parse_errors = Value("i", 0, lock=True)
        self.hud_code = Value("i", 0, lock=True)
        self.hud_remaining = Value("d", 0.0, lock=True)
        self.hud_progress = Value("d", 0.0, lock=True)
        self.hud_enabled = Value("b", False, lock=True)
        self.hud_show_timer = Value("b", False, lock=True)
        self.hud_detail = Value("i", 0, lock=True)
        self.hud_metric = Value("d", -1.0, lock=True)
        self.process = None

    @staticmethod
    def _parse_side(raw, side):
        values = np.asarray(raw, dtype=float).reshape(-1)
        if values.size < 25 * 16:
            raise ValueError("{} hand expected 400 matrix values, got {}".format(side, values.size))
        wrist = values[:16]
        landmarks = np.empty((25, 3), dtype=float)
        for index in range(25):
            base = index * 16
            landmarks[index] = values[base + 12:base + 15]
        return wrist, landmarks.reshape(-1)

    @classmethod
    def parse_payload(cls, value):
        if all(key in value for key in ("leftHand", "rightHand", "leftLandmarks", "rightLandmarks")):
            return (
                np.asarray(value["leftHand"], dtype=float).reshape(16),
                np.asarray(value["rightHand"], dtype=float).reshape(16),
                np.asarray(value["leftLandmarks"], dtype=float).reshape(75),
                np.asarray(value["rightLandmarks"], dtype=float).reshape(75),
            )
        if all(key in value for key in ("left", "right", "leftState", "rightState")):
            left_hand, left_points = cls._parse_side(value["left"], "left")
            right_hand, right_points = cls._parse_side(value["right"], "right")
            return left_hand, right_hand, left_points, right_points
        raise KeyError("unsupported HAND_MOVE payload")

    def _run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        from vuer import Vuer
        from vuer.schemas import Billboard, DefaultScene, Hands, Text
        from aiohttp import WSMsgType, web
        from aiohttp.hdrs import UPGRADE

        app = Vuer(
            host=self.host,
            port=self.port,
            cert=self.cert_file,
            key=self.key_file,
            queries=dict(grid=False),
            queue_len=3,
        )

        # Vuer's CAMERA_MOVE represents the rendered viewport rather than a
        # guaranteed physical HMD pose. Inject a tiny client that observes the
        # active WebXR session's viewer pose, matching xteleop's head bridge.
        vuer_socket_index = app.socket_index
        script_path = Path(__file__).with_name("head_pose_client.js")

        async def socket_index(request):
            if request.headers.get(UPGRADE, "").lower().strip() == "websocket":
                return await vuer_socket_index(request)
            index_path = Path(app.client_root) / "index.html"
            html = index_path.read_text(encoding="utf-8")
            html = html.replace(
                "<head>", '<head><script src="/teleop_head_pose.js?v=5"></script>', 1
            )
            return web.Response(text=html, content_type="text/html",
                                headers={"Cache-Control": "no-store"})

        async def head_pose_script(_request):
            return web.Response(text=script_path.read_text(encoding="utf-8"),
                                content_type="application/javascript",
                                headers={"Cache-Control": "no-store"})

        async def head_pose_websocket(request):
            websocket = web.WebSocketResponse(heartbeat=15.0)
            await websocket.prepare(request)
            async def stream_hud():
                previous = None
                while not websocket.closed:
                    payload = {
                        "type": "HUD_STATUS",
                        "code": int(self.hud_code.value),
                        "remaining": float(self.hud_remaining.value),
                        "progress": float(self.hud_progress.value),
                        "enabled": bool(self.hud_enabled.value),
                        "show_timer": bool(self.hud_show_timer.value),
                        "detail": int(self.hud_detail.value),
                        "metric": float(self.hud_metric.value),
                    }
                    signature = (
                        payload["code"], round(payload["remaining"], 1),
                        round(payload["progress"], 2), payload["enabled"],
                        payload["show_timer"], payload["detail"],
                        round(payload["metric"], 1),
                    )
                    if signature != previous:
                        await websocket.send_json(payload)
                        previous = signature
                    await asyncio.sleep(0.05)

            sender = asyncio.create_task(stream_hud())
            try:
                async for message in websocket:
                    if message.type != WSMsgType.TEXT:
                        continue
                    try:
                        payload = json.loads(message.data)
                        matrix = np.asarray(payload.get("matrix"), dtype=float)
                        if payload.get("type") != "HEAD_POSE" or matrix.shape != (16,):
                            continue
                        matrix_4x4 = matrix.reshape(4, 4, order="F")
                        if (not np.all(np.isfinite(matrix_4x4)) or
                                abs(np.linalg.det(matrix_4x4[:3, :3])) < 1e-6):
                            continue
                        self.head[:] = matrix
                        self.head_last_update.value = time.monotonic()
                        self.input_source_mask.value = int(
                            payload.get("input_source_mask", 0)
                        )

                        # Follow controller-to-hand transitions directly from
                        # the active XRSession. This is a fallback for Vuer
                        # releases that keep stale hand sources in HAND_MOVE.
                        update_time = time.monotonic()
                        direct_sides = 0
                        for side in ("left", "right"):
                            if side not in payload:
                                continue
                            hand, points = self._parse_side(payload[side], side)
                            if not all(np.all(np.isfinite(item))
                                       for item in (hand, points)):
                                raise ValueError(
                                    "non-finite direct WebXR {} hand data".format(side)
                                )
                            getattr(self, "{}_hand".format(side))[:] = hand
                            getattr(self, "{}_landmarks".format(side))[:] = points
                            getattr(self, "{}_last_update".format(side)).value = update_time
                            direct_sides += 1
                        if direct_sides:
                            self.direct_last_update.value = update_time
                            self.tracking_source.value = 1
                        side_times = (
                            float(self.left_last_update.value),
                            float(self.right_last_update.value),
                        )
                        if all(value > 0.0 for value in side_times):
                            self.last_update.value = min(side_times)
                    except (TypeError, ValueError, json.JSONDecodeError):
                        self.parse_errors.value += 1
            finally:
                sender.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await sender
            return websocket

        app.socket_index = socket_index
        app._add_route("/teleop_head_pose.js", head_pose_script)
        app._add_route("/teleop_head_pose", head_pose_websocket)

        @app.add_handler("HAND_MOVE")
        async def on_hand_move(event, _session):
            # The injected XR-frame bridge and Vuer can report the same hands
            # concurrently. Do not let Vuer overwrite fresh direct matrices:
            # mixing both writers can make consecutive-frame validation
            # alternate between coordinate conventions. Vuer remains the
            # fallback whenever the direct path has been silent for 0.5 s.
            if (self.direct_last_update.value > 0.0 and
                    time.monotonic() - self.direct_last_update.value < 0.5):
                return
            value = event.value
            if not isinstance(value, dict):
                return
            # Vuer 0.0.67 emits HAND_MOVE while controllers are active, using
            # None/ExtType placeholders for absent hands. This is an expected
            # input mode rather than a malformed tracking frame.
            if not all(key in value for key in ("left", "right")):
                if not all(key in value for key in (
                        "leftHand", "rightHand", "leftLandmarks", "rightLandmarks")):
                    return
            raw_hands = (
                (value.get("leftHand"), value.get("rightHand"))
                if "leftHand" in value else
                (value.get("left"), value.get("right"))
            )
            if any(raw is None or raw.__class__.__name__ == "ExtType"
                   for raw in raw_hands):
                return
            try:
                left, right, left_points, right_points = self.parse_payload(value)
                if not all(np.all(np.isfinite(item)) for item in (left, right, left_points, right_points)):
                    raise ValueError("non-finite WebXR hand data")
                self.left_hand[:] = left
                self.right_hand[:] = right
                self.left_landmarks[:] = left_points
                self.right_landmarks[:] = right_points
                update_time = time.monotonic()
                self.left_last_update.value = update_time
                self.right_last_update.value = update_time
                self.last_update.value = update_time
                self.tracking_source.value = 2
            except (KeyError, TypeError, ValueError):
                self.parse_errors.value += 1

        @app.spawn(start=False)
        async def main(session):
            session.set @ DefaultScene(frameloop="always")
            session.upsert @ Hands(
                fps=self.fps, stream=True, key="hands", showLeft=False, showRight=False
            )
            labels = {
                0: ("WAITING FOR BOTH HANDS", "white"),
                1: ("OPEN HANDS + PALMS UP  |  HOLD 5s", "white"),
                2: ("STARTING", "#54ff8a"),
                3: ("ACTIVE  |  TWO FISTS: HOLD 3s TO PAUSE", "#54ff8a"),
                4: ("STOPPING", "#ffca58"),
                5: ("RELEASE GESTURE TO RE-ARM", "#ffca58"),
                6: ("SAFETY COOLDOWN", "#ffca58"),
                7: ("TRACKING UNSTABLE  |  TIMER PAUSED", "#ff6b6b"),
                8: ("HOLD A NEUTRAL POSE  |  CALIBRATING", "#54c7ff"),
                9: ("ROBOT AUTO-ALIGNING  |  KEEP CLEAR", "#ffca58"),
                10: ("MATCH ROBOT L POSE  |  CALIBRATION IN", "#54c7ff"),
                11: ("CHECKING IK HANDOFF CONTINUITY", "#54c7ff"),
                12: ("PAUSED  |  PALMS UP: REALIGN  |  PINCH: EXIT", "#ffca58"),
                13: ("HOLD BOTH PINCHES TO REQUEST FULL EXIT", "#ffca58"),
                14: ("RELEASE BOTH PINCHES", "#ffca58"),
                15: ("TWO FISTS: CONFIRM FULL EXIT", "#ff6b6b"),
                16: ("SAFETY HOLD  |  CHECK TERMINAL", "#ff6b6b"),
                17: ("SAFETY LIMIT  |  MOVE HANDS BACK  |  FISTS: PAUSE", "#ffca58"),
                18: ("SAFE TARGET  |  STARTING SLOW RECOVERY", "#54c7ff"),
                19: ("TWO FISTS: ABORT RECOVERY", "#ff6b6b"),
                20: ("RECOVERING SLOWLY", "#54c7ff"),
                21: ("RECOVERING SLOWLY  |  STABLE", "#54c7ff"),
                22: ("PALMS UP  |  RETURN TO L", "#54c7ff"),
                23: ("SAFETY HOLD  |  PALMS UP: RECOVER", "#ffca58"),
                24: ("PALMS UP  |  SAFETY RECOVERY", "#54c7ff"),
                25: ("CHECKING FAULT RECOVERY SAFETY", "#ffca58"),
                26: ("MATCH ROBOT T_BENT POSE  |  CALIBRATION IN", "#54c7ff"),
            }
            while True:
                code = int(self.hud_code.value)
                label, color = labels.get(code, labels[0])
                detail = RECOVERY_DETAIL_TEXT.get(
                    int(self.hud_detail.value), ""
                )
                if code == 17 and detail:
                    label = "{}  |  {}".format(label, detail)
                if (code == 20 and np.isfinite(self.hud_metric.value) and
                        self.hud_metric.value >= 0.0):
                    label = "{}  |  ERROR {:.1f} deg".format(
                        label, self.hud_metric.value
                    )
                if self.hud_show_timer.value:
                    label = "{}  {:.1f}s".format(label, self.hud_remaining.value)
                head = np.asarray(self.head[:], dtype=float).reshape(4, 4, order="F")
                if self.head_last_update.value > 0.0 and np.all(np.isfinite(head)):
                    # Keep the 3D fallback panel one metre in front of the HMD.
                    position = head[:3, 3] + head[:3, :3] @ np.array([0.0, 0.18, -1.0])
                    position = position.tolist()
                else:
                    position = [0.0, 1.45, -1.0]
                session.upsert @ Billboard(
                    Text(
                        label, key="kuavo-gesture-hud-text", color=color,
                        fontSize=0.055, anchorX="center", anchorY="middle",
                        outlineWidth="5%", outlineColor="black",
                    ),
                    key="kuavo-gesture-hud-3d", position=position,
                )
                await asyncio.sleep(0.1)

        app.run()

    def start(self):
        if self.process is not None and self.process.is_alive():
            return
        self.process = Process(target=self._run, name="quest_webxr_vuer")
        self.process.daemon = True
        self.process.start()
        # Import, TLS and bind failures happen in the child process. Do not let
        # the ROS node advertise WAITING_FOR_WEBXR when that child has already
        # exited and no HTTPS endpoint exists.
        time.sleep(0.25)
        if not self.process.is_alive():
            exit_code = self.process.exitcode
            self.process.join(timeout=0.1)
            self.process = None
            raise RuntimeError(
                "WebXR HTTPS server exited during startup (exit code {})".format(
                    exit_code
                )
            )

    def is_alive(self):
        return self.process is not None and self.process.is_alive()

    def close(self):
        if self.process is None:
            return
        self.process.terminate()
        self.process.join(timeout=2.0)
        if self.process.is_alive():
            self.process.kill()
            self.process.join(timeout=1.0)
        self.process = None

    def set_hud(self, code, remaining=0.0, progress=0.0, enabled=False,
                show_timer=False, detail=0, metric=-1.0):
        self.hud_code.value = int(code)
        self.hud_remaining.value = float(remaining)
        self.hud_progress.value = float(progress)
        self.hud_enabled.value = bool(enabled)
        self.hud_show_timer.value = bool(show_timer)
        self.hud_detail.value = int(detail)
        self.hud_metric.value = float(metric)

    def sample(self):
        timestamp = float(self.last_update.value)
        if timestamp <= 0.0:
            return None
        return {
            "timestamp": timestamp,
            "left_hand": np.asarray(self.left_hand[:], dtype=float).reshape(4, 4, order="F"),
            "right_hand": np.asarray(self.right_hand[:], dtype=float).reshape(4, 4, order="F"),
            "left_landmarks": np.asarray(self.left_landmarks[:], dtype=float).reshape(25, 3),
            "right_landmarks": np.asarray(self.right_landmarks[:], dtype=float).reshape(25, 3),
            "head": np.asarray(self.head[:], dtype=float).reshape(4, 4, order="F"),
            "head_timestamp": float(self.head_last_update.value),
        }
