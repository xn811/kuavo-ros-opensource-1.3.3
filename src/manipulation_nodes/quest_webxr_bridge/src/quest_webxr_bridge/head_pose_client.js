// Observe Vuer's existing immersive WebXR session and stream the physical HMD
// pose. This deliberately does not create a second XR session.
(() => {
  // Quest3's source loop is capped at 100 Hz. XR requestAnimationFrame may run
  // at 72/90 Hz, so this cap preserves every physical display frame available.
  const SEND_INTERVAL_MS = 1000 / 100;
  const HAND_JOINT_KEYS = [
    "wrist",
    "thumb-metacarpal", "thumb-phalanx-proximal",
    "thumb-phalanx-distal", "thumb-tip",
    "index-finger-metacarpal", "index-finger-phalanx-proximal",
    "index-finger-phalanx-intermediate", "index-finger-phalanx-distal",
    "index-finger-tip",
    "middle-finger-metacarpal", "middle-finger-phalanx-proximal",
    "middle-finger-phalanx-intermediate", "middle-finger-phalanx-distal",
    "middle-finger-tip",
    "ring-finger-metacarpal", "ring-finger-phalanx-proximal",
    "ring-finger-phalanx-intermediate", "ring-finger-phalanx-distal",
    "ring-finger-tip",
    "pinky-finger-metacarpal", "pinky-finger-phalanx-proximal",
    "pinky-finger-phalanx-intermediate", "pinky-finger-phalanx-distal",
    "pinky-finger-tip",
  ];
  let socket = null;
  const sessionStates = new WeakMap();

  const hud = document.createElement("div");
  hud.id = "kuavo-gesture-hud";
  hud.style.cssText = [
    "position:fixed", "left:50%", "top:12%", "transform:translateX(-50%)",
    "z-index:2147483647", "min-width:420px", "padding:18px 28px",
    "border-radius:18px", "background:rgba(0,0,0,.72)",
    "border:2px solid rgba(255,255,255,.72)", "color:white",
    "font:600 24px/1.35 system-ui,sans-serif", "text-align:center",
    "pointer-events:none", "white-space:pre-line"
  ].join(";");
  hud.textContent = "正在等待双手追踪…";
  document.documentElement.appendChild(hud);

  const HUD_TEXT = {
    0: ["正在等待双手追踪…", "#ffffff"],
    1: ["准备启动\n双手张开、掌心向上保持 5 秒", "#ffffff"],
    2: ["启动控制", "#54ff8a"],
    3: ["控制中\n双手握拳保持 3 秒可暂停", "#54ff8a"],
    4: ["结束控制", "#ffca58"],
    5: ["请松开手势，防止重复触发", "#ffca58"],
    6: ["防误触冷却", "#ffca58"],
    7: ["追踪不稳定，计时已暂停", "#ff6b6b"],
    8: ["保持自然中立位，正在标定", "#54c7ff"],
    9: ["机器人正在执行安全对齐动作\n请勿靠近", "#ffca58"],
    10: ["请与机器人 L 型姿势对齐并保持不动", "#54c7ff"],
    11: ["正在检查 IK 接管连续性", "#54c7ff"],
    12: ["已暂停并保持\n掌心向上 5 秒重新对齐；双手捏合 2 秒完全结束", "#ffca58"],
    13: ["继续捏合以请求完全结束", "#ffca58"],
    14: ["请松开捏合手势", "#ffca58"],
    15: ["双手握拳确认完全结束", "#ff6b6b"],
    16: ["安全保护已触发，机器人保持当前位置\n请在终端检查故障", "#ff6b6b"],
    17: ["SAFETY LIMIT | MOVE HANDS BACK | FISTS: PAUSE", "#ffca58"],
    18: ["SAFE TARGET | STARTING SLOW RECOVERY", "#54c7ff"],
    19: ["TWO FISTS: ABORT RECOVERY", "#ff6b6b"],
    20: ["RECOVERING SLOWLY", "#54c7ff"],
    21: ["RECOVERING SLOWLY | STABLE", "#54c7ff"],
    22: ["PALMS UP | RETURN TO L", "#54c7ff"],
    23: ["SAFETY HOLD | PALMS UP: RECOVER", "#ffca58"],
    24: ["PALMS UP | SAFETY RECOVERY", "#54c7ff"],
    25: ["CHECKING FAULT RECOVERY SAFETY", "#ffca58"],
    26: ["MATCH ROBOT T_BENT POSE | CALIBRATION IN", "#54c7ff"],
  };

  const RECOVERY_DETAIL = {
    0: "", 1: "TRACKING", 2: "INPUT JUMP", 3: "JOINT LIMIT",
    4: "IK JUMP", 5: "IK STALE", 6: "WORKSPACE LIMIT",
    7: "IK UNSTABLE", 8: "IK DISCONTINUITY", 9: "FEEDBACK",
    10: "ARM LAG", 11: "JOINT BUFFER",
  };

  function updateHud(payload) {
    const entry = HUD_TEXT[payload.code] || HUD_TEXT[0];
    let text = entry[0];
    const detail = RECOVERY_DETAIL[Number(payload.detail || 0)] || "";
    if (payload.code === 17 && detail) text += ` | ${detail}`;
    const metric = Number(payload.metric);
    if (payload.code === 20 && Number.isFinite(metric) && metric >= 0) {
      text += ` | ERROR ${metric.toFixed(1)} deg`;
    }
    const seconds = Number(payload.remaining || 0);
    hud.textContent = payload.show_timer ? `${text}\n${seconds.toFixed(1)} s` : text;
    hud.style.borderColor = entry[1];
    hud.style.color = entry[1];
  }

  function send(payload) {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(payload));
    }
  }

  function connect() {
    if (socket && (socket.readyState === WebSocket.OPEN ||
                   socket.readyState === WebSocket.CONNECTING)) {
      return;
    }
    const url = new URL("/teleop_head_pose", window.location.href);
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
    socket = new WebSocket(url);
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === "HUD_STATUS") updateHud(payload);
      } catch (error) {
        console.warn("[Kuavo HUD] invalid status", error);
      }
    };
    socket.onclose = () => {
      socket = null;
      window.setTimeout(connect, 1000);
    };
  }

  function readHand(frame, referenceSpace, hand) {
    if (!hand) return null;
    const matrices = [];
    for (const jointName of HAND_JOINT_KEYS) {
      const jointSpace = hand.get(jointName);
      if (!jointSpace) return null;
      const pose = frame.getJointPose(jointSpace, referenceSpace);
      if (!pose) return null;
      matrices.push(...pose.transform.matrix);
    }
    return matrices;
  }

  function sendPose(timeMs, frame, state, session) {
    if (!state.referenceSpace) {
      return;
    }
    // XR frame timestamps may restart when a new immersive session is
    // entered. Keep throttling state per session so re-entering VR cannot
    // suppress head/hand frames until the previous timestamp is reached.
    if (timeMs < state.lastSentMs) {
      state.lastSentMs = -Infinity;
    }
    if (timeMs - state.lastSentMs < SEND_INTERVAL_MS) {
      return;
    }
    const pose = frame.getViewerPose(state.referenceSpace);
    if (!pose || !socket || socket.readyState !== WebSocket.OPEN) {
      return;
    }
    state.lastSentMs = timeMs;
    const payload = {
      type: "HEAD_POSE",
      timestamp_ms: timeMs,
      matrix: Array.from(pose.transform.matrix),
      input_source_mask: 0,
    };

    // The session may be entered with controllers and switch to hands later.
    // Read the live input-source list on every XR frame so the bridge follows
    // that transition even if Vuer's HAND_MOVE component keeps stale sources.
    for (const inputSource of session.inputSources || []) {
      if (!["left", "right"].includes(inputSource.handedness)) {
        continue;
      }
      const sideBit = inputSource.handedness === "left" ? 1 : 2;
      payload.input_source_mask |= inputSource.hand ? sideBit << 2 : sideBit;
      if (!inputSource.hand) continue;
      const hand = readHand(frame, state.referenceSpace, inputSource.hand);
      if (hand) payload[inputSource.handedness] = hand;
    }
    send(payload);
  }

  function observeSession(session) {
    let state = sessionStates.get(session);
    if (state) {
      return state;
    }
    state = { referenceSpace: null, lastSentMs: -Infinity };
    sessionStates.set(session, state);
    connect();
    session.requestReferenceSpace("local-floor")
      .catch(() => session.requestReferenceSpace("local"))
      .then((space) => { state.referenceSpace = space; })
      .catch((error) => console.warn("[WebXR head] reference space unavailable", error));
    return state;
  }

  function patchSessionFrameLoop() {
    const prototype = window.XRSession && window.XRSession.prototype;
    if (!prototype || prototype.__kuavoHeadPosePatched) {
      return Boolean(prototype);
    }
    const originalRequestAnimationFrame = prototype.requestAnimationFrame;
    if (typeof originalRequestAnimationFrame !== "function") {
      return false;
    }
    prototype.__kuavoHeadPosePatched = true;
    prototype.requestAnimationFrame = function(callback) {
      const session = this;
      const state = observeSession(session);
      return originalRequestAnimationFrame.call(session, (timeMs, frame) => {
        try {
          sendPose(timeMs, frame, state, session);
        } catch (error) {
          console.warn("[WebXR head] pose read failed", error);
        }
        callback(timeMs, frame);
      });
    };
    return true;
  }

  if (!navigator.xr || !navigator.xr.requestSession) {
    return;
  }
  connect();
  if (!patchSessionFrameLoop()) {
    const retryPatch = () => {
      if (!patchSessionFrameLoop()) {
        window.setTimeout(retryPatch, 500);
      }
    };
    window.setTimeout(retryPatch, 500);
  }
  const originalRequestSession = navigator.xr.requestSession.bind(navigator.xr);
  navigator.xr.requestSession = async (mode, options) => {
    let sessionOptions = options;
    if (mode === "immersive-vr" || mode === "immersive-ar") {
      sessionOptions = Object.assign({}, options || {});
      const optional = new Set(sessionOptions.optionalFeatures || []);
      optional.add("dom-overlay");
      sessionOptions.optionalFeatures = Array.from(optional);
      sessionOptions.domOverlay = {root: hud};
    }
    let session;
    try {
      session = await originalRequestSession(mode, sessionOptions);
    } catch (error) {
      // Older Quest Browser versions may reject the DOM-overlay dictionary.
      // Retry without it so HUD support can never prevent entering WebXR.
      if (error && error.name === "NotAllowedError") throw error;
      session = await originalRequestSession(mode, options);
    }
    if (mode === "immersive-vr" || mode === "immersive-ar") {
      observeSession(session);
    }
    return session;
  };
})();
