#!/usr/bin/env python3
"""Generate the public LIMIZI asset manifest consumed by the MVU frontend."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPOSITORY_ROOT / "assets"
MANIFEST_PATH = ASSET_ROOT / "manifest.json"
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4"}


def collect_paths() -> list[str]:
    return sorted(
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for path in ASSET_ROOT.rglob("*")
        if path.is_file()
        and path != MANIFEST_PATH
        and path.suffix.lower() in MEDIA_EXTENSIONS
    )


def main() -> None:
    manifest = {
        "version": os.environ.get("GITHUB_SHA", "local"),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "paths": collect_paths(),
        "aliases": {
            "沐子": ["沐子", "李沐子"],
            "李沐子": ["李沐子", "沐子"],
            "祁谣": ["祁谣", "祁瑶"],
            "祁瑶": ["祁瑶", "祁谣"],
            "敖烈": ["敖烈", "熬烈"],
            "熬烈": ["熬烈", "敖烈"],
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {MANIFEST_PATH} with {len(manifest['paths'])} assets")


if __name__ == "__main__":
    main()
