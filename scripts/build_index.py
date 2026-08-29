#!/usr/bin/env python3
"""Generate index.json from profiles/*/profile.json (see
docs/design/robot-abstraction.md §5.1 in Oloo-AI/oloo-studio).

index.json is CI-generated and must never be hand-edited; scripts/validate.py
--check-index enforces that by re-running this and diffing.

Usage: python scripts/build_index.py [--write]
  --write   write the result to index.json (default: print to stdout)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time

import registry_lib as lib

RAW_BASE = "https://raw.githubusercontent.com/Oloo-AI/robot-profiles/main/"
JSDELIVR_BASE = "https://cdn.jsdelivr.net/gh/Oloo-AI/robot-profiles@main/"

# Minimum Oloo Studio app version required to consume this registry's schema.
# Bump alongside schema/robot-profile-v2.schema.json breaking changes. Registry sync
# shipped in the 0.1.x daemon (oloo-studio C1.5b), so 0.1.0 is the floor.
MIN_APP_VERSION = "0.1.0"

REGISTRY_VERSION = 1
SCHEMA_VERSION = 2


def urls_for(rel_path: str) -> dict[str, str]:
    return {"raw": RAW_BASE + rel_path, "jsdelivr": JSDELIVR_BASE + rel_path}


def build_entry(profile_dir) -> dict:
    doc = lib.load_profile(profile_dir)
    pid = doc["id"]
    profile_bytes = (profile_dir / "profile.json").read_bytes()
    sha256 = hashlib.sha256(profile_bytes).hexdigest()

    bus = doc.get("bus")
    if bus is None:
        bus = sorted({b["protocol"] for b in doc.get("buses", [])})

    vendor = doc.get("vendor", {}).get("name", "")

    entry = {
        "id": pid,
        "name_zh": doc["name"],
        "name_en": doc.get("name_en", doc["name"]),
        "kind": doc["kind"],
        "vendor": vendor,
        "dof": doc["dof"],
        "bus": bus,
        "support_status": doc["support_status"],
        "schema_version": doc.get("schema_version", SCHEMA_VERSION),
        "min_app_version": MIN_APP_VERSION,
        "sha256": sha256,
        "profile_url": urls_for(f"profiles/{pid}/profile.json"),
    }

    thumb = profile_dir / "thumbnail.webp"
    if thumb.exists():
        entry["thumbnail_url"] = urls_for(f"profiles/{pid}/thumbnail.webp")

    urdf_path = profile_dir / "urdf" / "robot.urdf"
    if urdf_path.exists():
        entry["urdf_url"] = urls_for(f"profiles/{pid}/urdf/robot.urdf")

    return entry


def build_index(generated_at: int | None = None) -> dict:
    entries = [build_entry(d) for d in lib.iter_profile_dirs()]
    entries.sort(key=lambda e: e["id"])
    return {
        "generated_at": generated_at if generated_at is not None else int(time.time()),
        "registry_version": REGISTRY_VERSION,
        "profiles": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write to index.json instead of stdout")
    parser.add_argument(
        "--frozen-time",
        type=int,
        default=None,
        help="use this unix timestamp for generated_at instead of the current time (mainly for tests)",
    )
    args = parser.parse_args()

    index = build_index(generated_at=args.frozen_time)
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if args.write:
        lib.INDEX_PATH.write_text(text)
        print(f"wrote {lib.INDEX_PATH} ({len(index['profiles'])} profiles)", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
