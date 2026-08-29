# Oloo Robot Profiles

Public, versioned registry of robot profiles for [Oloo Studio](https://github.com/Oloo-AI/oloo-studio) —
motor tables, buses, calibration schemes, safety limits, and (optionally) a URDF for
each supported robot. Apache-2.0 licensed. Data only — see **Data-only safety** below.

Oloo-AI/robot-profiles 是 [Oloo Studio](https://github.com/Oloo-AI/oloo-studio) 的公开机器人
配置注册表：每个支持的机型一份电机表、总线、校准方案、安全阈值，以及（可选的）URDF。
Apache-2.0 许可。**只有数据** —— 见下方「数据-only 安全声明」。

## What is this? / 这是什么？

Oloo Studio ships with a handful of built-in robot profiles so it always works offline,
then syncs the rest of the gallery from this repo in the background. Every entry here is
plain JSON plus optional images/URDF/meshes — nothing here is ever executed as code.

Oloo Studio 内置几个 profile 保证离线可用，其余机型的画廊在后台从本仓库同步。
这里的每一条都是纯 JSON 加上可选的图片/URDF/网格 —— 任何内容都不会被当作代码执行。

- `schema/robot-profile-v2.schema.json` — the profile schema (JSON Schema, draft 2020-12)
- `schema/index.schema.json` — the generated index's schema
- `profiles/<id>/` — one directory per robot; `profile.json` is the only required file
- `index.json` — **CI-generated, never hand-edited** (`scripts/build_index.py`)
- `scripts/validate.py` — the same checks CI runs, runnable locally
- `scripts/build_index.py` — regenerates `index.json` from `profiles/`

## Adding this registry in Oloo Studio / 如何在 Oloo Studio 里添加本注册表

Oloo Studio already points at `https://raw.githubusercontent.com/Oloo-AI/robot-profiles/main/`
as its default official source (with jsDelivr / mirror fallbacks — see
`docs/design/robot-abstraction.md` §5.3 in `oloo-studio`). To add a *different* registry
(a vendor's own, or a school/lab internal one) or re-point to a fork of this one:

1. Open Oloo Studio → **Settings → Robot Registries**.
2. Add a source: `{ slug, name, base_url, trust: "official" | "third_party" }`. A
   `base_url` must serve `index.json` at its root and every URL inside `index.json`
   is resolved relative to it, so a raw-GitHub URL, a jsDelivr URL, or a mirror all work
   unmodified.
3. Profiles from a `third_party` source are always treated as `support_status: untested`-tier
   by the app's SafetyGuard, regardless of what the profile itself claims — see §5.4 of the
   design doc. Only this repo (or an explicit fork the user trusts) should be marked
   `official`.

在 Oloo Studio 里：**设置 → 机器人注册表**，加一个源
`{slug, name, base_url, trust}`。`base_url` 根目录要能拿到 `index.json`，
里面所有 URL 都是相对这个 base 解析的，所以 GitHub raw / jsDelivr / 镜像都能直接用。
`third_party` 源来的 profile，不管自己声明什么，app 侧的 SafetyGuard 一律按
`untested` 的保守阈值处理（见 `oloo-studio` 设计文档 §5.4）；只有本仓库（或用户明确
信任的 fork）应该标 `official`。

## Contributing a new robot / 贡献新机型

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide and the PR template
(`.github/PULL_REQUEST_TEMPLATE.md`) for the field-by-field checklist. Short version:

完整指南见 [CONTRIBUTING.md](./CONTRIBUTING.md)，逐字段检查表见 PR 模板
(`.github/PULL_REQUEST_TEMPLATE.md`)。简版流程：

1. `profiles/<id>/profile.json` following `schema/robot-profile-v2.schema.json`
   （按 schema 填一份 `profile.json`）
2. `README.md` (Source + License sections), `thumbnail.webp` (≤100 KB, ~512×512) —
   unless it's a `planned` stub （非 `planned` stub 都需要，stub 可以没有）
3. `python scripts/validate.py` passes locally （本地跑通校验）
4. `python scripts/build_index.py --write` and commit the result — never hand-edit
   `index.json` （生成 index.json 一起提交，不要手改）
5. Open a PR — CI re-validates everything and re-checks `index.json` is in sync
   （开 PR，CI 会重新校验并核对 `index.json`）

## Support status definitions / 支持状态定义

Every profile declares `support_status`. Oloo Studio's SafetyGuard uses this to decide
how conservative to be by default (tighter step limits, more confirmation prompts) —
so this field is a safety signal, not just a badge. Be honest.

每个 profile 都要声明 `support_status`。Oloo Studio 的 SafetyGuard 用它决定默认保守
程度（更小的单步限位、更多确认弹窗）—— 这是安全信号，不只是徽章，请如实填写。

| value | meaning | 含义 |
|---|---|---|
| `verified_hw` | Run end-to-end (connect → calibrate → teleop/record) on **real physical hardware**. | 在**真实硬件**上完整跑通过（连接→校准→遥操/采集）。 |
| `verified_mock` | Validated against Oloo Studio's mock motor bus, or carefully transcribed from a working lerobot config — **not yet confirmed on physical hardware**. | 在 Oloo Studio 的 mock 总线上验证过，或从一份能跑的 lerobot config 仔细转写而来 —— **尚未在真机上确认**。 |
| `planned` | Not yet profiled. A minimal stub (`id`/`name`/`kind`/`dof`/`bus`/`support_status`/`lerobot_type`) so the gallery can show a "coming soon" card. | 尚未做出完整 profile，只有最小 stub 字段，让画廊能展示「计划中」卡片。 |

This registry's `support_status` enum (`verified_hw` / `verified_mock` / `planned`) **is**
the app's enum: Oloo Studio stores it verbatim (its older `verified` / `untested` spellings
are migrated to `verified_hw` / `verified_mock` on load). The registry needs to distinguish
"tested on real hardware" from "only tested against the mock bus" so contributors without
hardware can still contribute honestly-labeled profiles; the app's SafetyGuard runs its
conservative thresholds (lower temperature ceiling, halved per-cycle steps) for anything
that is not `verified_hw`, and for every profile from a `third_party` source.

本仓库的 `support_status` 取值（`verified_hw` / `verified_mock` / `planned`）**就是**
应用内部的枚举：Oloo Studio 原样存储（旧写法 `verified` / `untested` 读取时迁移为
`verified_hw` / `verified_mock`）。注册表需要区分「真机测过」和「只在 mock 总线测过」，
这样没有硬件的贡献者也能诚实地贡献 profile；应用侧 SafetyGuard 对非 `verified_hw`
的 profile、以及所有 `third_party` 源的 profile 一律使用保守阈值（温度上限更低、单步减半）。

## Data-only safety / 数据-only 安全声明

This registry is designed so that **nothing it serves can ever be executed as code**:

1. **Allowed file types only**: `.json .webp .png .urdf .stl .dae .glb .md`. Anything
   else is rejected by CI. There is no field anywhere in the schema for a script,
   command, or path that gets interpreted/executed.
2. **Validate before trust**: every file goes through sha256 check → JSON Schema
   validation → semantic cross-reference checks before Oloo Studio's local cache will
   use it. Any single profile failing any step is dropped (and logged), without
   affecting the rest of the registry.
3. **URDF is parsed defensively**: size-capped (URDF ≤2 MB, single mesh ≤10 MB, total
   ≤100 MB per profile), XML parsed with external entities disabled (XXE-safe), and
   `filename` attributes may only be relative paths without `..`.
4. **Untrusted-by-default for third-party sources**: a profile from a non-`official`
   registry source is always treated at `untested`-tier safety thresholds, regardless
   of what it claims about itself.
5. **Never a silent limit widen**: if a profile update changes safety-relevant fields
   (limits, voltage/temperature thresholds) for the robot a user currently has active,
   Oloo Studio shows a field-level diff and requires explicit confirmation before
   switching — it never auto-adopts a wider limit.
6. **Signing is planned, not yet enforced**: `index.json` reserves a slot for a
   detached signature (minisign / sigstore) per §5.4 of the design doc; until that
   ships, every profile is labeled "unverified signature" in the app UI.

本注册表被设计成**任何下发内容都不会被当作代码执行**：

1. **文件类型白名单**：`.json .webp .png .urdf .stl .dae .glb .md`，其它一律被 CI
   拒绝；schema 里任何字段都不能表示一段脚本/命令/会被解释执行的路径。
2. **先校验再信任**：每个文件都要经过 sha256 校验 → JSON Schema 校验 →
   语义交叉校验，Oloo Studio 的本地缓存才会用它；任何一步失败就丢弃这一条
   （并记录），不影响其它 profile。
3. **URDF 防御式解析**：大小上限（单个 URDF ≤2 MB、单个网格 ≤10 MB、
   单个 profile 总量 ≤100 MB），XML 解析禁用外部实体（防 XXE），
   `filename` 只允许相对路径且不含 `..`。
4. **第三方源默认不信任**：非 `official` 源来的 profile，不管自己声明什么，
   一律按 `untested` 级别的安全阈值处理。
5. **绝不静默放宽限位**：如果某次更新改动了用户当前激活机器人的安全相关字段
   （限位、电压/温度阈值），Oloo Studio 会展示字段级 diff 并要求用户确认后
   才切换 —— 不会自动套用一个更宽的限位。
6. **签名功能已预留，尚未强制**：`index.json` 按设计文档 §5.4 预留了分离签名
   （minisign / sigstore）的位置；在签名上线前，应用 UI 会把每个 profile 标注为
   「未签名」。

## License / 许可

This repository (schema, scripts, workflow, profile.json/README text) is licensed
under [Apache-2.0](./LICENSE). Robot hardware descriptions (URDF/meshes) retain their
own upstream license, documented per-profile in that profile's README and, where
applicable, `urdf/NOTICE.md` — check those before redistributing a specific robot's
geometry.

本仓库（schema、脚本、workflow、profile.json/README 文字）采用
[Apache-2.0](./LICENSE) 许可。各机型的硬件描述（URDF/网格）保留各自的上游许可，
记录在对应 profile 的 README 里，以及（如有）`urdf/NOTICE.md`
—— 转发某个机型的几何数据前请先核对那份许可。
