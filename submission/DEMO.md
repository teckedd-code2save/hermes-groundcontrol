# GroundControl for Hermes — real product demo

[Watch the approved 81-second video](https://github.com/teckedd-code2save/hermes-groundcontrol/releases/download/v0.2.0/GroundControl-Hermes-Product-Demo.mp4).

The video records actual Hermes Desktop interaction with DeepSeek V4 Pro, the `groundcontrol:operate` skill and GroundControl's native MCP connection. Every application pixel comes from the original window recording. Editorial captions and crops improve readability; waiting time is cut. The configuration excerpt is placed before the capability explanation for narrative order. No reconstructed interface or fixture result appears.

| Time | Demonstrated use |
| --- | --- |
| 0:03–0:18 | Load the skill and list four granted deployments with `deployment.list`. |
| 0:18–0:36 | Run `deployment.health` for all four and compare runtime health with public endpoint response. |
| 0:36–0:52 | Use `deployment.inspect` and `deployment.logs` to investigate one workload and its three latest deployment records. |
| 0:52–1:06 | Use `deployment.config.check` to check two configuration keys without revealing their values. |
| 1:06–1:16 | Explain supported operations from inspected capabilities; no operation is executed. |

Eight real MCP calls cover five tool types. The investigation finds a workload whose public endpoint responds with HTTP 200 while research containers are exited/unhealthy. Historical deployment records and configuration presence help narrow the inquiry; they do not establish a current root cause, validate credentials or prove an authenticated customer journey.

The operator explicitly approved read-only access to the four workloads. No write operation or `operation.get` call was made. Executing a change requires an exact authorized workload/action and effective approval controls. The demo does not claim all runtimes support the same operations.

The export is H.264 High Level 4.1, yuv420p, 1920×1080, 30 fps, fast-start MP4, 81 seconds, silent with captions. Full decoding passed. Real browser playback reached 81/81 seconds with `ended=true` and no media error. SHA-256: `9d4c23b82c97af93e9ce29a08c759d2e86a78742832ab7f16ed9e48fec8ddc5f`.

The earlier caption-rendered acceptance video is superseded and is not the challenge demo. `demo-capture.json` is historical acceptance evidence only; it must not be used to reconstruct or claim a live UI.
