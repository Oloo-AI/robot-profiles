#!/usr/bin/env python3
"""CI validation for Oloo-AI/robot-profiles.

Checks (see docs/design/robot-abstraction.md §5.2 in Oloo-AI/oloo-studio):
1. Every profiles/*/profile.json validates against schema/robot-profile-v2.schema.json.
2. Directory name == profile.json's `id`; all ids are globally unique (including aliases).
3. thumbnail.webp exists, is a WebP file, and is <=100 KB (required unless
   support_status == "planned", which is a stub with no thumbnail by design).
   hero.webp, if present, is <=400 KB.
4. README.md exists and contains a "来源"/"Source" and a "许可"/"License" section
   (required unless support_status == "planned"). If urdf/ exists, urdf/NOTICE.md
   is required.
5. Semantic cross-references: actuators[].bus all resolve to buses[].id; features
   observation.state/action entries reference existing actuators; kinematics.urdf
   joint_map keys are actuator names; `bus` (protocol list) is consistent with
   buses[].protocol when both are present.
6. Registry-wide file-type allowlist (data-only guarantee, §5.4): every tracked
   file under profiles/ has an extension in the allowlist; URDF/mesh size caps.

Usage: python scripts/validate.py [--check-index]
  --check-index   also regenerate index.json in memory and diff against the
                   committed one (fails if they differ / it's missing).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import jsonschema

import registry_lib as lib


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_schema(profile_dir: Path, doc: dict, validator: jsonschema.Draft202012Validator, errors: list[str]) -> None:
    for err in validator.iter_errors(doc):
        path = "/".join(str(p) for p in err.path) or "<root>"
        fail(errors, f"{profile_dir.name}/profile.json: schema error at {path}: {err.message}")


def check_id_matches_dir(profile_dir: Path, doc: dict, errors: list[str]) -> None:
    pid = doc.get("id")
    if pid != profile_dir.name:
        fail(errors, f"{profile_dir.name}: profile.json id={pid!r} does not match directory name")
    if pid is not None and not lib.ID_PATTERN.match(pid):
        fail(errors, f"{profile_dir.name}: id {pid!r} does not match ^[a-z0-9_]+$")


def check_thumbnail(profile_dir: Path, doc: dict, errors: list[str]) -> None:
    planned = doc.get("support_status") == "planned"
    thumb = profile_dir / "thumbnail.webp"
    if not thumb.exists():
        if not planned:
            fail(errors, f"{profile_dir.name}: missing required thumbnail.webp (support_status={doc.get('support_status')!r})")
        return
    if planned:
        # Not an error for a planned stub to have a thumbnail, but unusual; allow it.
        pass
    data = thumb.read_bytes()
    if data[8:12] != b"WEBP":
        fail(errors, f"{profile_dir.name}/thumbnail.webp: not a valid WebP file")
    if len(data) > lib.MAX_THUMBNAIL_BYTES:
        fail(errors, f"{profile_dir.name}/thumbnail.webp: {len(data)} bytes exceeds {lib.MAX_THUMBNAIL_BYTES} byte limit")

    hero = profile_dir / "hero.webp"
    if hero.exists():
        hdata = hero.read_bytes()
        if hdata[8:12] != b"WEBP":
            fail(errors, f"{profile_dir.name}/hero.webp: not a valid WebP file")
        if len(hdata) > lib.MAX_HERO_BYTES:
            fail(errors, f"{profile_dir.name}/hero.webp: {len(hdata)} bytes exceeds {lib.MAX_HERO_BYTES} byte limit")


def check_readme(profile_dir: Path, doc: dict, errors: list[str]) -> None:
    planned = doc.get("support_status") == "planned"
    readme = profile_dir / "README.md"
    if not readme.exists():
        if not planned:
            fail(errors, f"{profile_dir.name}: missing required README.md (support_status={doc.get('support_status')!r})")
        return
    text = readme.read_text(encoding="utf-8")
    has_source = ("来源" in text) or ("Source" in text) or ("## source" in text.lower())
    has_license = ("许可" in text) or ("License" in text) or ("## license" in text.lower())
    if not has_source:
        fail(errors, f"{profile_dir.name}/README.md: missing a 来源/Source section")
    if not has_license:
        fail(errors, f"{profile_dir.name}/README.md: missing a 许可/License section")

    urdf_dir = profile_dir / "urdf"
    if urdf_dir.exists() and not (urdf_dir / "NOTICE.md").exists():
        fail(errors, f"{profile_dir.name}/urdf/: NOTICE.md is required when urdf/ is present")


def check_semantic(profile_dir: Path, doc: dict, errors: list[str]) -> None:
    if doc.get("support_status") == "planned":
        return
    bus_ids = {b["id"] for b in doc.get("buses", [])}
    actuator_names = {a["name"] for a in doc.get("actuators", [])}

    for a in doc.get("actuators", []):
        if a.get("bus") not in bus_ids:
            fail(errors, f"{profile_dir.name}: actuators[{a.get('name')}].bus={a.get('bus')!r} not found in buses[].id")

    features = doc.get("features", {})
    for section in ("observation.state", "action"):
        for ref in features.get(section, []):
            if ref.get("actuator") not in actuator_names:
                fail(errors, f"{profile_dir.name}: features.{section} references unknown actuator {ref.get('actuator')!r}")

    urdf = doc.get("kinematics", {}).get("urdf") or {}
    joint_map = urdf.get("joint_map") or {}
    for key in joint_map:
        if key not in actuator_names:
            fail(errors, f"{profile_dir.name}: kinematics.urdf.joint_map key {key!r} is not an actuator name")

    declared_bus = doc.get("bus")
    if declared_bus is not None:
        derived = sorted({b["protocol"] for b in doc.get("buses", [])})
        if sorted(set(declared_bus)) != derived:
            fail(
                errors,
                f"{profile_dir.name}: top-level bus={declared_bus!r} inconsistent with "
                f"buses[].protocol={derived!r}",
            )


def check_file_allowlist(profile_dir: Path, errors: list[str]) -> None:
    total_mesh_bytes = 0
    for path in profile_dir.rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext not in lib.ALLOWED_EXTENSIONS:
            fail(errors, f"{path.relative_to(lib.REPO_ROOT)}: extension {ext!r} not in registry allowlist {sorted(lib.ALLOWED_EXTENSIONS)}")
            continue
        size = path.stat().st_size
        if ext == ".urdf" and size > lib.MAX_URDF_BYTES:
            fail(errors, f"{path.relative_to(lib.REPO_ROOT)}: {size} bytes exceeds {lib.MAX_URDF_BYTES} byte URDF limit")
        if ext in (".stl", ".dae", ".glb"):
            if size > lib.MAX_MESH_BYTES:
                fail(errors, f"{path.relative_to(lib.REPO_ROOT)}: {size} bytes exceeds {lib.MAX_MESH_BYTES} byte single-mesh limit")
            total_mesh_bytes += size
    if total_mesh_bytes > lib.MAX_MESH_TOTAL_BYTES:
        fail(errors, f"{profile_dir.name}: total mesh bytes {total_mesh_bytes} exceeds {lib.MAX_MESH_TOTAL_BYTES} byte limit")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-index", action="store_true", help="also verify index.json is up to date")
    args = parser.parse_args()

    errors: list[str] = []
    schema = lib.load_schema()
    validator = jsonschema.Draft202012Validator(schema)

    seen_ids: dict[str, str] = {}

    if not lib.PROFILES_DIR.exists():
        print("ERROR: profiles/ directory not found", file=sys.stderr)
        return 1

    profile_dirs = list(lib.iter_profile_dirs())
    if not profile_dirs:
        print("ERROR: no profiles found under profiles/", file=sys.stderr)
        return 1

    for profile_dir in profile_dirs:
        profile_json = profile_dir / "profile.json"
        if not profile_json.exists():
            fail(errors, f"{profile_dir.name}: missing profile.json")
            continue
        try:
            doc = lib.load_profile(profile_dir)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{profile_dir.name}/profile.json: invalid JSON: {exc}")
            continue

        check_schema(profile_dir, doc, validator, errors)
        check_id_matches_dir(profile_dir, doc, errors)
        check_thumbnail(profile_dir, doc, errors)
        check_readme(profile_dir, doc, errors)
        check_semantic(profile_dir, doc, errors)
        check_file_allowlist(profile_dir, errors)

        pid = doc.get("id")
        if pid:
            if pid in seen_ids:
                fail(errors, f"duplicate id {pid!r}: {seen_ids[pid]} and {profile_dir.name}")
            else:
                seen_ids[pid] = profile_dir.name
        for alias in doc.get("aliases", []):
            if alias in seen_ids:
                fail(errors, f"duplicate id {alias!r} (alias of {pid}): {seen_ids[alias]} and {profile_dir.name}")
            else:
                seen_ids[alias] = f"{profile_dir.name} (alias)"

    if args.check_index:
        import build_index

        expected = build_index.build_index()
        if not lib.INDEX_PATH.exists():
            fail(errors, "index.json is missing; run scripts/build_index.py")
        else:
            import json

            actual = json.loads(lib.INDEX_PATH.read_text())
            # generated_at is intentionally excluded from the comparison.
            actual_cmp = {**actual, "generated_at": 0}
            expected_cmp = {**expected, "generated_at": 0}
            if actual_cmp != expected_cmp:
                fail(errors, "index.json is stale: does not match `python scripts/build_index.py` output (did you hand-edit it?)")

    if errors:
        print(f"FAILED with {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(profile_dirs)} profiles validated, {len(seen_ids)} ids/aliases registered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
