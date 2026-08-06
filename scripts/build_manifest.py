#!/usr/bin/env python3
"""Build the self-excluded SHA-256 release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build() -> dict:
    files = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            raise ValueError(f"public package symlink forbidden: {relative}")
        if relative == "metrics-private" or relative.startswith("metrics-private/"):
            raise ValueError(f"private metrics forbidden in public package: {relative}")
        if not path.is_file() or ".git" in path.parts:
            continue
        if (
            ".pytest_cache" in path.parts
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
            or path.name == ".DS_Store"
            or relative == "review-queue.jsonl"
            or relative == "manifest.json"
        ):
            continue
        files[relative] = sha256(path)
    return {
        "schema_version": "agent-hiring-map-public-manifest/1.0",
        "hash_algorithm": "sha256",
        "self_excluded": True,
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("manifest drifted; run scripts/build_manifest.py")
        print(json.dumps({"status": "pass", "files": len(build()["files"])}))
        return
    OUTPUT.write_text(content, encoding="utf-8")
    print(json.dumps({"status": "written", "files": len(build()["files"])}))


if __name__ == "__main__":
    main()
