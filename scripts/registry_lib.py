"""Shared helpers for scripts/validate.py and scripts/build_index.py.

Kept dependency-light: only `jsonschema` is required beyond the stdlib
(see scripts/requirements.txt).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = REPO_ROOT / "profiles"
SCHEMA_PATH = REPO_ROOT / "schema" / "robot-profile-v2.schema.json"
INDEX_SCHEMA_PATH = REPO_ROOT / "schema" / "index.schema.json"
INDEX_PATH = REPO_ROOT / "index.json"

ID_PATTERN = re.compile(r"^[a-z0-9_]+$")
MAX_THUMBNAIL_BYTES = 100 * 1024
MAX_HERO_BYTES = 400 * 1024
MAX_URDF_BYTES = 2 * 1024 * 1024
MAX_MESH_BYTES = 10 * 1024 * 1024
MAX_MESH_TOTAL_BYTES = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = {".json", ".webp", ".png", ".urdf", ".stl", ".dae", ".glb", ".md"}


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def load_index_schema() -> dict:
    return json.loads(INDEX_SCHEMA_PATH.read_text())


def iter_profile_dirs():
    for path in sorted(PROFILES_DIR.iterdir()):
        if path.is_dir():
            yield path


def load_profile(profile_dir: Path) -> dict:
    return json.loads((profile_dir / "profile.json").read_text())
