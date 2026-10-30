"""
release.py - write releases/latest.json for the build in releases/.
Lives in the server project, next to server.py. Needs nothing from the app project.

    python release.py 1.1.0                     # writes releases/latest.json
    python release.py 1.1.0 -n "Fixed a bug"    # same, with release notes

The version must match __version__ in the build you copied into releases/.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

# ---- settings: change these once for your project ----
APP_NAME = "main"                                  # build filename, without .exe
BASE_URL = "http://192.168.122.1:5000/download"        # must match server.py's route
RELEASES = Path(__file__).parent / "releases"      # releases/ next to this script
# -------------------------------------------------------


def find_build() -> Path:
    for candidate in (RELEASES / f"{APP_NAME}.exe", RELEASES / APP_NAME):
        if candidate.is_file():
            return candidate
    sys.exit(f"No build found - expected {RELEASES / APP_NAME} or {RELEASES / APP_NAME}.exe")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser(description="Write releases/latest.json.")
    p.add_argument("version", help="version of the build in releases/, e.g. 1.1.0")
    p.add_argument("-n", "--notes", default="", help="release notes")
    a = p.parse_args()

    build = find_build()
    manifest = {
        "version": a.version,
        "url": f"{BASE_URL}/{build.name}",
        "sha256": sha256_of(build),
        "notes": a.notes,
    }
    out = RELEASES / "latest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {out}:")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()