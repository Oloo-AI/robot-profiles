# Contributing / 贡献指南

## English

### Adding a new robot profile

1. Fork and clone this repo. Pick an `id` for your robot: lowercase, `^[a-z0-9_]+$`,
   matching (where one exists) the lerobot `RobotConfig`/`TeleoperatorConfig`
   registered type name, e.g. `koch_follower`.
2. Create `profiles/<id>/` and, at minimum, `profiles/<id>/profile.json` following
   `schema/robot-profile-v2.schema.json`. The schema doc-comments and the two
   reference implementations (`profiles/so101_follower/`, `profiles/so101_leader/`)
   are the best examples to copy from.
3. Decide your `support_status` honestly:
   - **`verified_hw`** — you ran this profile against real hardware end-to-end
     (connect → calibrate → teleop/record) and it worked.
   - **`verified_mock`** — you've only validated it against Oloo Studio's mock
     motor bus (or transcribed it carefully from a working lerobot config) but
     haven't confirmed it on physical hardware yet.
   - **`planned`** — you don't have hardware or haven't built the full profile
     yet. A stub with just `id`/`name`/`kind`/`dof`/`bus`/`support_status`/
     `lerobot_type` is enough — no thumbnail or full actuator table required.
     This is what powers the "coming soon" gallery cards.
4. If you're not writing a `planned` stub, also add:
   - `README.md` with a **Source** section (where the motor table / URDF /
     calibration numbers came from, upstream repo + commit if you have it) and
     a **License** section (the license governing that upstream hardware
     description — this repo's own `LICENSE` covers the profile.json/README
     text, not necessarily the vendor's mesh/URDF).
   - `thumbnail.webp`, ≤100 KB, roughly 512×512, transparent or light
     background. If you can't render one (no CAD/URDF, or the render pipeline
     fails), ship a clean SVG line-art placeholder instead and say so in the
     README with a `TODO: replace with a real render/photo`.
   - If you have a URDF: put it under `profiles/<id>/urdf/robot.urdf` with
     meshes in `profiles/<id>/urdf/meshes/` (small meshes only — for large
     mesh sets, host them as a GitHub Release asset and point
     `kinematics.urdf.mesh_archive_url` at it instead), plus a `NOTICE.md`
     documenting the upstream source/license/any modifications, following the
     pattern in `profiles/so101_follower/urdf/NOTICE.md`.
5. Only allowed file extensions are accepted anywhere under `profiles/`:
   `.json .webp .png .urdf .stl .dae .glb .md`. This is a hard rule — the
   registry only ever ships data, never executable code (see **Data-only
   safety** in the root README).
6. Run `python scripts/validate.py` locally. Fix everything it flags.
7. Do **not** hand-edit `index.json`. It's generated:
   ```sh
   pip install -r scripts/requirements.txt
   python scripts/build_index.py --write
   ```
   Commit the result alongside your profile changes. CI re-generates it and
   fails the PR if your committed copy doesn't match (see
   `.github/workflows/validate.yml`).
8. Open a PR using the template — fill in the profile checklist.

### Updating an existing profile

Same rules apply. If you're promoting a `planned` stub to `verified_mock` or
`verified_hw`, fill in the full schema (buses/actuators/calibration/features/
kinematics/safety/capabilities) — the stub's minimal fields aren't enough once
`support_status` leaves `planned`.

If you're widening a safety-relevant field (`safety.*`, `actuators[].limits`),
say so explicitly in the PR description — reviewers treat those changes with
extra scrutiny, since Oloo Studio never silently adopts a wider limit on an
already-active robot (see the root README's **Data-only safety** section).

### Local validation reference

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/validate.py            # schema + semantic + file-allowlist checks
python scripts/build_index.py --write # regenerate index.json
python scripts/validate.py --check-index  # confirm index.json is in sync
```

---

## 中文

### 新增一个机器人 profile

1. Fork 并 clone 本仓库。给你的机器人起一个 `id`：小写，`^[a-z0-9_]+$`，
   尽量与 lerobot 里对应的 `RobotConfig`/`TeleoperatorConfig` 注册名一致，
   例如 `koch_follower`。
2. 新建 `profiles/<id>/`，至少要有 `profiles/<id>/profile.json`，
   按 `schema/robot-profile-v2.schema.json` 填写。schema 里的字段注释和两个
   参考实现（`profiles/so101_follower/`、`profiles/so101_leader/`）是最好的模板。
3. 如实标注 `support_status`：
   - **`verified_hw`**：你在真实硬件上完整跑通过（连接→校准→遥操/采集）。
   - **`verified_mock`**：只在 Oloo Studio 的 mock 总线上验证过（或从一份能跑的
     lerobot config 仔细转写而来），还没有在真机上确认。
   - **`planned`**：你手头没有这个机型的硬件，或者还没做完整 profile。
     只填 `id`/`name`/`kind`/`dof`/`bus`/`support_status`/`lerobot_type` 这个最小
     stub 即可，不需要缩略图或完整电机表 —— 这就是画廊里「计划中」卡片的数据来源。
4. 如果不是 `planned` stub，还需要：
   - `README.md`，含 **来源** 小节（电机表/URDF/校准数值出自哪里，上游仓库 +
     commit（如有））和 **许可** 小节（这份硬件描述本身的许可 —— 本仓库自己的
     `LICENSE` 只覆盖 profile.json/README 文字，不一定覆盖厂商的网格/URDF）。
   - `thumbnail.webp`，≤100 KB，约 512×512，透明或浅色背景。渲染不出来（没有
     CAD/URDF，或渲染流程失败）就用干净的 SVG 线框占位，并在 README 里标注
     `TODO: 换成真实渲染图/实物照片`。
   - 如果有 URDF：放在 `profiles/<id>/urdf/robot.urdf`，网格放
     `profiles/<id>/urdf/meshes/`（只放小网格 —— 大网格集合改用 GitHub Release
     附件托管，`kinematics.urdf.mesh_archive_url` 指过去），再加一份
     `NOTICE.md` 记录上游来源/许可/改动说明，参考
     `profiles/so101_follower/urdf/NOTICE.md` 的写法。
5. `profiles/` 下任何位置只允许这些扩展名：
   `.json .webp .png .urdf .stl .dae .glb .md`。这是硬规则 ——
   注册表**只下发数据，永不下发可执行代码**（见根 README「数据-only 安全声明」）。
6. 本地跑一遍 `python scripts/validate.py`，把报出来的问题都改掉。
7. **不要手改** `index.json`，它是生成出来的：
   ```sh
   pip install -r scripts/requirements.txt
   python scripts/build_index.py --write
   ```
   把结果和你的 profile 改动一起提交。CI 会重新生成一份并跟你提交的对比，
   不一致就直接挂掉（见 `.github/workflows/validate.yml`）。
8. 用模板开 PR，把「Profile checklist」勾完。

### 更新已有 profile

规则同上。如果是把一个 `planned` stub 升级成 `verified_mock` 或 `verified_hw`，
要把完整 schema（buses/actuators/calibration/features/kinematics/safety/
capabilities）填全 —— 一旦 `support_status` 离开 `planned`，stub 的最小字段集
就不够用了。

如果你在放宽安全相关字段（`safety.*`、`actuators[].limits`），
请在 PR 描述里明确写出来 —— 审核会额外仔细看这类改动，因为 Oloo Studio
**绝不会对正在使用的机器人静默套用一个变宽的限位**（见根 README
「数据-only 安全声明」）。
