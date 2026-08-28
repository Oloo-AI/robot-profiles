# SO-101 Follower

## 来源 / Source

- 硬件设计：[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)（`Simulation/SO101/`）
- 电机表来自 lerobot `robots/so_follower/so_follower.py`（与 `so100_follower` 完全一致，`so100_*` 作为
  别名解析到本 profile，见 `profile.json` 的 `aliases`）
- URDF / 网格：本目录 `urdf/`，从 `Oloo-AI/oloo-studio`
  （`packages/oloo/src/oloo/assets/robots/so101/`）复制而来 —— `oloo-studio` 是私有仓库，
  为了让 profile 的 `kinematics.urdf.url` 能被公开抓取，把这份已获授权的资产镜像到本公开仓库。
  详见 `urdf/NOTICE.md`。

Source (EN): hardware design by TheRobotStudio (SO-ARM100), motor table from lerobot's
`so_follower` robot class. URDF/meshes are mirrored here from Oloo-AI/oloo-studio (private)
so this public registry entry can serve a fetchable `kinematics.urdf.url` — see `urdf/NOTICE.md`
for the full provenance and mesh-decimation notes.

## 许可 / License

- 本 profile.json / README：Apache-2.0（本仓库整体许可，见根目录 `LICENSE`）
- URDF 与网格：Apache-2.0，版权归 TheRobotStudio（同本仓库根目录 `LICENSE`），机型描述有精简/重导出，
  几何近似，仅用于可视化，不用于制造或精密仿真（见 `urdf/NOTICE.md`）

## 支持状态 / Support status

`support_status: "verified_mock"` — 在 Oloo Studio 的 mock 总线上验证过完整链路
（连接、校准向导、遥操、采集），**尚未在真实 SO-101 硬件上跑通本 profile 的 v2 字段**
（电机表/校准范式本身在 Oloo 的 SO-101 MVP 上已用真机验证多时，但这份 registry v2 schema
的转写还没有配一次真机回归）。真机验证后请把这个字段改成 `verified_hw` 并在这里补一句
验证记录（日期 + 验证人 + 固件/kit 版本）。

Verified against Oloo Studio's mock motor bus end-to-end; the underlying SO-101 motor
table/calibration scheme has extensive real-hardware mileage in Oloo's MVP, but this specific
v2-schema transcription has not yet been re-confirmed against physical hardware. Flip to
`verified_hw` once that regression is done.

## 致谢 / Acknowledgements

TheRobotStudio for the open-hardware SO-ARM100 design, and the lerobot community
(Hugging Face) for the reference motor table and calibration scheme this profile mirrors.
