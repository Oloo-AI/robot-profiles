# SO-101 Leader

## 来源 / Source

- 硬件设计：[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)（`Simulation/SO101/`）
- 电机表来自 lerobot `teleoperators/so_leader/so_leader.py`（与 follower 表逐字节相同）；
  `so100_leader` 作为别名解析到本 profile（见 `profile.json` 的 `aliases`）
- URDF / 网格：与 `../so101_follower/urdf/` 共用同一套文件（同一副物理臂），本 profile 的
  `kinematics.urdf.url` 直接指向那里，不重复存放网格

Source (EN): hardware design by TheRobotStudio (SO-ARM100); motor table from lerobot's
`so_leader` teleoperator class (byte-identical to the follower's table). Shares URDF/mesh
files with `../so101_follower/` since it's physically the same arm.

## 许可 / License

- 本 profile.json / README：Apache-2.0（本仓库整体许可，见根目录 `LICENSE`）
- URDF 与网格：Apache-2.0，版权归 TheRobotStudio（同本仓库根目录 `LICENSE`），
  详见 `../so101_follower/urdf/NOTICE.md`

## 支持状态 / Support status

`support_status: "verified_mock"` — 在 Oloo Studio 的 mock 总线上验证过遥操链路，
**尚未在真实硬件上回归本 profile 的 v2 字段**。真机验证后请改为 `verified_hw` 并补验证记录。

Verified against the mock motor bus; not yet re-confirmed on physical hardware for this
v2-schema transcription. Flip to `verified_hw` once that's done.

## 致谢 / Acknowledgements

TheRobotStudio for the open-hardware SO-ARM100 design, and the lerobot community
(Hugging Face) for the reference motor table and calibration scheme this profile mirrors.
