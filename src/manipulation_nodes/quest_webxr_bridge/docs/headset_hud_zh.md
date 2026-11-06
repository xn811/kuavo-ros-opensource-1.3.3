# Quest 3 头显 HUD 中文说明

本文说明 `quest_webxr_bridge` 当前版本在 Quest 3 沉浸模式中显示的全部 HUD
文字，以及每个状态下操作员应该做什么。以后修改 HUD code、英文文字或状态机时，必须
同步更新本文的完整对照和流程说明。

3D HUD 英文文字来自 `src/quest_webxr_bridge/webxr_server.py`，浏览器 DOM HUD
文字来自 `src/quest_webxr_bridge/head_pose_client.js`，状态编号来自
`src/quest_webxr_bridge/gesture_control.py`。若本文与运行画面不一致，应以代码和
`/quest_webxr_kuavo_bridge/status` 的实时状态为准。

## 1. HUD 状态完整对照

| Code | 头显英文 | 中文含义 | 进入原因与操作方法 |
| ---: | --- | --- | --- |
| 0 | `WAITING FOR BOTH HANDS` | 等待双手 | 系统还没有取得连续有效的双手和头部追踪。把双手放在 Quest 摄像头视野内并保持稳定，不要做启动手势。 |
| 1 | `OPEN HANDS + PALMS UP \| HOLD 5s` | 双手张开、掌心向上，保持 5 秒 | 双手追踪已经有效，系统等待启动手势。双手张开且掌心向上，连续保持 5 秒；任一只手丢失或姿势中断都会暂停或重置计时。 |
| 2 | `STARTING` | 正在进行启动倒计时 | 启动手势已经被识别。继续保持双手张开、掌心向上，直到倒计时结束。 |
| 3 | `ACTIVE \| TWO FISTS: HOLD 3s TO PAUSE` | 遥操已接管；双手握拳 3 秒可暂停 | 此状态允许正常实时跟随；可恢复限制和低速恢复阶段还有各自受限的跟随行为。需要暂停时双手握拳并连续保持 3 秒。 |
| 4 | `STOPPING` | 正在进行暂停倒计时 | 双手握拳暂停手势已经被识别。继续握拳直到倒计时结束；这只会进入暂停保持，不是完全退出。 |
| 5 | `RELEASE GESTURE TO RE-ARM` | 释放刚才的手势，解除防重复触发保护 | 启动或暂停手势刚刚触发。完全离开刚才的掌心向上或握拳姿势，并连续保持释放状态 1 秒。追踪丢失不算释放。 |
| 6 | `SAFETY COOLDOWN` | 防误触冷却中 | 一次手势命令触发后进入冷却期。等待倒计时结束，不要反复做命令手势。 |
| 7 | `TRACKING UNSTABLE \| TIMER PAUSED` | 追踪不稳定，手势计时暂停 | 双手、手部点位或头部姿态无效，或者数据已过期。让双手重新进入视野并保持稳定；恢复连续有效帧后状态机会继续。若发生在 `ACTIVE`，系统会立即进入可恢复保持，防止机器人继续使用旧目标。 |
| 8 | `HOLD A NEUTRAL POSE \| CALIBRATING` | 保持中立姿势，正在标定 | 系统正在采集稳定标定窗口。正常启动及普通故障恢复时对齐当前倾斜 L；`AUTO_MOTION_TIMEOUT` 恢复时对齐 T_BENT。双手张开，头部、手腕和手指保持不动，直到标定完成。 |
| 9 | `ROBOT AUTO-ALIGNING \| KEEP CLEAR` | 机器人正在自动对齐，请保持安全距离 | 机器人正在执行 `T -> T_BENT -> L`、重新回到 L、超时后退回 T_BENT，或执行退出返回路径。不要用手接触机器人，不要进入工作空间，不要启动其他手臂发布节点。 |
| 10 | `MATCH ROBOT L POSE \| CALIBRATION IN` | 与机器人 L 型姿势对齐，标定即将开始 | 机器人已经到达 L 型。将双臂对齐机器人姿势并保持稳定；连续有效追踪启动 3 秒准备倒计时，倒计时结束后才进入正式标定。追踪失效会重置倒计时。 |
| 11 | `CHECKING IK HANDOFF CONTINUITY` | 正在检查 IK 接管连续性 | 正常启动或普通恢复时继续保持 L 型；`AUTO_MOTION_TIMEOUT` 恢复时继续保持 T_BENT。通过多帧检查后进入 `ACTIVE`。普通 LIMIT 自动恢复不会重新标定，也不会进入此状态。 |
| 12 | `PAUSED \| PALMS UP: REALIGN \| PINCH: EXIT` | 已暂停保持；掌心向上可重新对齐，双手捏合可请求完全退出 | 手臂保持暂停时的安全位置，WebXR 手臂和手指输出关闭。要继续遥操，双手张开、掌心向上保持 5 秒；要完全退出，双手拇指和食指同时捏合并保持 2 秒。 |
| 13 | `HOLD BOTH PINCHES TO REQUEST FULL EXIT` | 保持双手捏合，请求完全退出 | 已在暂停状态检测到双手 pinch。继续保持到倒计时结束；这里只进入二次确认，不会立即让机器人回 HOME。 |
| 14 | `RELEASE BOTH PINCHES` | 释放双手捏合手势 | 完全离开双手 pinch，并连续保持释放状态 1 秒，随后进入握拳最终确认。 |
| 15 | `TWO FISTS: CONFIRM FULL EXIT` | 双手握拳，确认完全退出 | 双手握拳并保持 3 秒才会确认退出。确认后机器人执行 `当前保持姿态 -> L -> T_BENT -> T -> HOME`，最后切换到安全模式。 |
| 16 | `SAFETY HOLD \| CHECK TERMINAL` | 不可通过手势恢复的安全保持，请检查终端 | 桥接检测到不在手势恢复白名单内的硬故障，已关闭 WebXR 跟随并请求适配器保持。反馈丢失、控制模式失败、发布者冲突等故障仍锁存，必须检查终端，不能用手势强行移动。 |
| 17 | `SAFETY LIMIT \| MOVE HANDS BACK \| FISTS: PAUSE`，末尾附简短原因 | 触发可恢复安全限制；退回双手，或握拳进入暂停 | 机器人手臂保持真实反馈位置；有效追踪时手指可继续跟随，系统继续后台试算。原因后缀见下表。此状态不显示秒数。 |
| 18 | `SAFE TARGET \| STARTING SLOW RECOVERY` | 已找到安全目标，正在启动低速恢复 | 当前目标仍按首次 L 型锚点计算。系统累计 5 个新的连续安全报告后直接切入低速动态跟随；不显示倒计时，也不要求操作者保持静止。条件失效立即回到 code 17。 |
| 19 | `TWO FISTS: ABORT RECOVERY` | 双手握拳，主动放弃自动恢复 | LIMIT 或低速恢复过程中检测到双手握拳。继续保持 3 秒会进入普通 `PAUSED`；提前松开会取消退出暂停，并重新寻找安全手位。 |
| 20 | `RECOVERING SLOWLY \| ERROR x.x deg` | 正在动态低速跟随，显示当前最大关节误差 | 系统从实测关节位置使用 `5°/s`、`10°/s²` 恢复档，持续追赶按首次 L 型锚点计算的实时安全目标，手指继续实时跟随。这里显示的是实时误差，不是完成时间，因此不显示倒计时；操作者可以继续移动。目标越限、被工作空间投影或追踪失效时会立即回到 code 17 并保持，但不会改变锚点。试验版本已停用原来的 `20°` 目标领先拒绝；实际下发命令通过 `12°` 反馈背压避免接触时越积越远。 |
| 21 | `RECOVERING SLOWLY \| STABLE` | 已进入最终稳定窗口 | 真实反馈与目标进入 `3°` 以内，并且其他安全条件继续成立后，才显示 `0.75 s` 最终稳定倒计时；通过后切换到 code 3 `ACTIVE`。 |
| 22 | `PALMS UP \| RETURN TO L` | 双手张开、掌心向上，正在确认返回 L 型 | 只在 `PAUSED_HOLD` 中显示。连续保持启动手势 5 秒，HUD 显示实时剩余时间；与 pinch 完全退出倒计时互斥。完成后先要求释放手势，再执行自动回 L。 |
| 23 | `SAFETY HOLD \| PALMS UP: RECOVER` | 当前硬故障允许手势请求恢复 | 机器人保持原位，WebXR 输出仍关闭。双手张开、掌心向上连续保持 5 秒可进入故障恢复预检；这不是直接清除故障或直接接管。 |
| 24 | `PALMS UP \| SAFETY RECOVERY` | 硬故障恢复手势倒计时 | 继续保持双手张开、掌心向上。姿势中断或追踪失效会停止并重置倒计时。 |
| 25 | `CHECKING FAULT RECOVERY SAFETY` | 正在执行故障恢复预检 | 系统检查真实反馈、关节安全包络、唯一命令发布者、适配器保持状态和手臂模式；任一条件失败都会重新进入锁存 Safety Hold。 |
| 26 | `MATCH ROBOT T_BENT POSE \| CALIBRATION IN` | 与机器人 T_BENT 姿势对齐，标定即将开始 | 仅用于 `AUTO_MOTION_TIMEOUT` 的手势恢复。机器人已低速退回 T_BENT；操作者模仿当前机器人 T_BENT，双手张开并保持稳定，准备倒计时结束后在该姿势建立本次标定锚点。 |

浏览器 DOM HUD 的 0–16 使用中文：依次为“正在等待双手追踪”“准备启动，双手张开、掌心向上保持 5 秒”“启动控制”“控制中，双手握拳保持 3 秒可暂停”“结束控制”“请松开手势，防止重复触发”“防误触冷却”“追踪不稳定，计时已暂停”“保持自然中立位，正在标定”“机器人正在执行安全对齐动作，请勿靠近”“请与机器人 L 型姿势对齐并保持不动”“正在检查 IK 接管连续性”“已暂停并保持，掌心向上 5 秒重新对齐；双手捏合 2 秒完全结束”“继续捏合以请求完全结束”“请松开捏合手势”“双手握拳确认完全结束”“安全保护已触发，机器人保持当前位置，请在终端检查故障”。17–26 使用上表的英文；两种显示都可能附加倒计时、原因或误差。

code 17 的原因后缀如下：

| 后缀 | 含义 |
| --- | --- |
| `TRACKING` | 追踪不可用或不稳定 |
| `INPUT JUMP` | WebXR 输入跳变 |
| `JOINT LIMIT` | IK 目标超出关节安全范围 |
| `IK JUMP` | 连续 IK 候选跳变 |
| `IK STALE` | IK 目标过期 |
| `WORKSPACE LIMIT` | 工作空间边界限制 |
| `IK UNSTABLE` | IK 候选尚不稳定 |
| `IK DISCONTINUITY` | IK 候选不连续 |
| `FEEDBACK` | 关节反馈异常 |
| `ARM LAG` | 手臂跟随误差持续过大 |
| `JOINT BUFFER` | 反馈进入软限位缓冲区 |

只有确实处于连续保持窗口的状态才会在文字后附加剩余秒数；寻找安全解、检查
IK 连续性和机器人低速移动本身不显示倒计时。HUD 颜色含义如下：绿色表示已进入遥操，
蓝色表示对齐、标定或接管检查，黄色表示需要操作员确认或正在自动运动，红色表示追踪
异常、最终退出确认或硬安全故障。橙黄色的可恢复安全限制表示机器人已停止，但仍允许
操作者通过退回双手恢复。

## 2. 正常启动流程

```text
等待双手（0）
  -> 准备启动（1）
  -> 启动倒计时（2）
  -> 释放手势（5）
  -> 冷却/启动前检查（6/9）
  -> T -> T_BENT -> L 自动动作（9）
  -> 对齐 L 型和 3 秒准备倒计时（10）
  -> 中立位标定（8）
  -> IK 接管连续性检查（11）
  -> ACTIVE（3）
```

`ROBOT AUTO-ALIGNING` 显示期间，头显手势不会直接驱动手臂和手指。每个自动姿态都要
经过真实关节反馈到位确认，不能只根据固定时间跳到下一段。

## 3. 暂停、重新对齐与完全退出

在 `ACTIVE` 中双手握拳 3 秒会进入 `PAUSED`。暂停时：

- 手臂保持安全位置；
- WebXR 手臂和手指跟随关闭；
- 普通握拳不会直接执行回零。
- 暂停菜单中的两个计时器互斥：pinch 优先用于完全退出；没有 pinch 时，张手掌心向上
  才累计回 L 倒计时。两者都会在头显内显示实时剩余时间。

重新对齐流程：

```text
PAUSED（12）
  -> 双手张开、掌心向上 5 秒（22）
  -> 释放 1 秒
  -> 自动回到 L 型（9）
  -> 对齐和标定（10、8）
  -> IK 接管检查（11）
  -> ACTIVE（3）
```

完全退出流程：

```text
PAUSED（12）
  -> 双手 pinch 2 秒（13）
  -> 释放 pinch 1 秒（14）
  -> 双手握拳 3 秒（15）
  -> L -> T_BENT -> T -> HOME（9）
  -> 等待下一次启动（1）
```

自动回 L 和完全退出的自动关节路径都会持续发送
`neutral_hand_position: [0, 0, 0, 0, 0, 0]`，因此机器人手指会自然张开，不会把
用于暂停、pinch 或最终确认的手形保留到 L 型或模式 1。该命令仍通过唯一的桥接适配器
发布，不增加第二个 `/control_robot_hand_position` 发布源。

## 4. Tracking Unstable、可恢复限制与硬 Safety Hold

`TRACKING UNSTABLE` 是可恢复的追踪状态：

- 手势计时暂停或清零；
- 无有效新目标时不继续刷新 WebXR IK；
- 若发生在 `ACTIVE`，适配器立即以真实关节反馈进入手臂保持；有有效手部追踪时手指仍实时跟随，追踪失效后由输入超时停止刷新；
- 双手和头部恢复后，通过与其他可恢复限制相同的安全候选检查自动继续；
- 它不是完全退出，也不是机器人急停。

`SAFETY LIMIT` 是可恢复保持：

- 机器人立即切到基于新鲜真实反馈的保持模式；
- 若真实关节仅越过带 `5°` 余量的软件预览包络、但仍在 URDF 机械硬限位内，HUD 显示
  `JOINT BUFFER`。适配器从真实反馈播种，以保持档 `5°/s`、`10°/s²` 退回最近的软件
  包络边界；目标命令本身仍不允许越过软件包络；
- 手臂不再接受危险候选；手部追踪有效时，手指仍按实时人手更新；
- WebXR 追踪和 IK 后台试算继续运行；
- 把双手缓慢退回安全区域后，候选必须连续稳定、没有 WebXR 跳变、距离关节安全
  包络至少 `0.5°`，且没有被工作空间、中线、躯干禁区或肩部可达半径强行投影；
- 所有候选始终使用本次遥操首次 L 型标定建立的人手/机器人锚点。LIMIT 恢复不会调用
  标定，不会把当前手位绑定到机器人保持位，也不会在任务空间内建立新锚点；
- 连续 5 次新安全报告后，适配器从实测关节位置立即以 `5°/s`、`10°/s²` 进入动态
  低速跟随。不要求额外静止保持，操作者可以继续移动双手；
- 低速跟随期间操作者可以继续平缓移动。目标新鲜、位于关节包络且未被工作空间投影时
  持续跟随；试验阶段不再限制实时 IK 目标与实测关节之间的距离，机器人始终通过
  `5°/s`、`10°/s²` 限速器低速追赶，同时保留原 L 型锚点；原 `20°` 目标领先保护仍以
  注释形式保留在代码中，等待仿真验证后决定删除或恢复；
- 恢复目标本身可以离真实关节任意远，但适配器只把真实反馈前方最多 `12°` 的局部目标
  交给低速限速器。接触阻挡时，命令不会继续积累成远离机器人的姿态；障碍解除或人手
  改回安全位置后，仍沿首次 L 型锚点继续追赶；
- `ACTIVE` 中反馈与已经限速的命令持续相差超过 `45° / 1.0 s` 时，不再进入不可恢复
  的硬 Safety Hold，而是进入同一套软 LIMIT。该检测仍保留，用于停止当前手臂追赶；
- 反馈与实时目标进入 `3°` 以内并再次稳定 `0.75 s` 后自动恢复正常遥操速度；目标移动
  使误差重新超过 `3°` 时只重置最终倒计时，不中断仍然安全的低速跟随，也不需要 pinch；
- 只有从暂停状态主动执行“掌心向上 -> 回 L 型 -> 重新对齐和标定”，或者重启本次
  遥操会话时，才允许建立新锚点；
- 不再因固定时长自动转入 `PAUSED`。只要真实反馈新鲜、底层控制正常，就持续保持并
  继续影子解算；双手握拳 3 秒可主动进入 `PAUSED`。这组双拳是菜单手势，不会下发为
  机器人握拳；开始识别时机器人手指先回到自然张开命令。

`SAFETY HOLD` 是硬桥接故障状态。白名单内故障允许操作员请求一次受保护的恢复：

- WebXR 输出被关闭；
- 适配器切换到保持模式；
- 白名单内显示 code 23；双手张开、掌心向上保持 5 秒后进入 code 25 预检；
- `IK_HANDOFF_DISCONTINUITY`，以及在硬故障阶段出现的
  `ADAPTER_IK_TARGET_JUMP`、`ADAPTER_IK_TARGET_OUTSIDE_SAFE_ENVELOPE`、
  `ADAPTER_IK_TARGET_STALE`、`ADAPTER_RECOVERY_TARGET_LEAD`、
  `ADAPTER_TRACKING_ERROR`、`ADAPTER_FEEDBACK_OUTSIDE_SAFE_ENVELOPE`，预检通过后低速回到当前
  倾斜 L，再按 L 对齐、标定和检查 IK 接管；
- `AUTO_MOTION_TIMEOUT` 预检通过后不再重试可能受阻的 L，而是低速退回 T_BENT，显示
  code 26，并在 T_BENT 对齐、标定和检查 IK 接管；
- `AUTO_MOTION_FEEDBACK_TIMEOUT`、真实反馈过期、控制模式切换失败、其他活动手臂发布者、
  适配器不能进入保持等故障不在白名单内，仍显示 code 16 并锁存；
- 手势只请求预检，不会绕过反馈、控制权、关节包络或 IK 首帧连续性检查；
- 真正危险时仍应使用机器人现场急停，不能把软件保持当作急停替代品。

白名单硬故障恢复流程：

```text
SAFETY HOLD（23）
  -> 双手张开、掌心向上 5 秒（24）
  -> 故障恢复预检（25）
  -> 普通白名单故障：倾斜 L -> 对齐 L（10）
  -> AUTO_MOTION_TIMEOUT：T_BENT -> 对齐 T_BENT（26）
  -> 中立位标定（8）
  -> IK 接管检查（11）
  -> ACTIVE（3）
```

## 5. 安全状态检查方法

先读取桥接状态：

```bash
rostopic echo -n 1 /quest_webxr_kuavo_bridge/status
```

重点查看：

- `state`：可恢复限制为 `RECOVERABLE_SAFETY_HOLD`，低速接管为
  `RECOVERY_RAMP`，硬故障通常为
  `AUTO_MOTION_FAULT_HOLD`；
- `fault`：桥接层锁存的具体原因；
- `recovery_reason`：进入可恢复保持的原因；
- `recovery_phase`：`seek_safe` 或 `ramp`；
- `recovery_safe_reports`：已经连续通过的安全适配器报告数量；
- `recovery_constraint_projection_m`：原始目标被笛卡尔安全边界修正的距离；恢复要求
  不超过 `0.002 m`；
- `adapter.fault`：命令适配器报告的错误；
- `feedback_age_s`：真实关节反馈是否过期；
- `adapter.ik_target_age_s`：IK 目标是否过期；
- `adapter.ik_target_delta_deg`：连续 IK 候选的最大关节变化；
- `adapter.tracking_error_deg`：反馈与受限命令的最大关节误差；
- `adapter.feedback_inside_safe_envelope`：真实反馈是否已回到软件预览包络（含 `0.5°`
  反馈容差）；
- `adapter.feedback_inside_hard_envelope`：真实反馈是否仍在 URDF 机械硬限位内；
- `adapter.feedback_envelope_violation_deg`：真实反馈越过软件包络的最大角度；
- `auto_pose` 和 `auto_target_error_deg`：自动动作卡在哪个姿态及误差。

可恢复原因包括：

- `IK_TARGET_OUTSIDE_SAFE_ENVELOPE`；
- `IK_TARGET_JUMP`；
- 由连续拒绝安全候选造成的 `IK_TARGET_STALE`；
- `TRACKING_ERROR`：反馈与已经限速的命令持续相差超过 `45° / 1.0 s`；
- `FEEDBACK_OUTSIDE_SAFE_ENVELOPE`：反馈进入软件包络与 URDF 硬限位之间的 `5°`
  缓冲区；先由保持档低速退回边界，再继续原 L 型锚点下的影子 IK 恢复；
- `WEBXR_INPUT_JUMP`；
- `WEBXR_TRACKING_MISSING`、`WEBXR_TRACKING_STALE` 或
  `WEBXR_TRACKING_INVALID`。

这些状态不要做 pinch；把双手退回安全区域。code 18 表示连续安全报告正在满足，
不显示倒计时且不要求保持静止；code 20 显示低速恢复的实时关节误差，code 21 只在
最终稳定窗口中显示倒计时。
若明确不再继续本次恢复，双手握拳 3 秒进入 code 12。

不在手势恢复白名单内、必须检查终端的硬故障包括：

- 真实关节反馈过期、包含非有限值，或越过 URDF 机械硬限位（
  `FEEDBACK_OUTSIDE_HARD_LIMITS`）；仅越过软件预览包络现在属于可恢复软 LIMIT；
- 自动动作或非活动阶段出现、且未进入软 LIMIT 流程的命令跟随异常；
- 自动动作期间反馈消失；
- WebXR 服务退出；
- `/kuavo_arm_traj` 存在其他活动发布者；
- 手臂模式切换失败。

自动姿态本身超时和 IK 接管首帧不连续已进入受保护的手势恢复白名单，但只有预检全部
通过才会运动；它们仍会记录在 `fault` 和终端日志中。

硬 Safety Hold 可从终端显式重新开始安全启动路径，或请求回到 L 型重新标定；执行前必须先
确认故障原因已经消失、机器人周围安全、真实反馈正常：

```bash
# 重新走 T -> T_BENT -> L 启动路径
rosservice call /quest_webxr_kuavo_bridge/set_enabled "data: true"

# 请求回到 L 型并重新标定
rosservice call /quest_webxr_kuavo_bridge/recalibrate
```

这些服务不是机器人急停复位，也不能消除机械碰撞、底层控制器故障或硬件报警。若原因
不清楚，应停止本轮测试并检查终端日志，不要反复调用服务强行恢复。

## 6. 状态来源

- HUD 英文文本：`src/quest_webxr_bridge/webxr_server.py`
- HUD code 和基础手势计时：`src/quest_webxr_bridge/gesture_control.py`
- 启动、暂停、退出与 Safety Hold 状态机：
  `scripts/quest_webxr_kuavo_bridge.py`
- 唯一手臂输出、反馈检查、关节包络和关节限速：
  `scripts/quest_webxr_control_contract_adapter.py`
- 默认阈值：`config/default.yaml`
