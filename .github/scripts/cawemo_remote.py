"""Narrow remote SSH payload. No archives, deletes, root-wide copies or fallback.

Only cawemo_publish.py sends this trusted tooling, with EXPECTED set to a locally
validated manifest. Remote Python 3 and standard rsync are activation prerequisites.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


SCOPE = "cawemo/1.9"
MANIFEST = "cawemo-publish-manifest.json"
OPTIONS = ["-rt", "--delay-updates", "--chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r"]
MAX_ENTRIES = 8192
MAX_TOTAL = 512 * 1024 * 1024


def roots(stage, live):
    for root in (stage, live):
        if (len(root) > 512 or not re.fullmatch(r"/[A-Za-z0-9_./-]+", root) or
                any(part in ("", ".", "..") for part in root[1:].split("/")) or
                len(Path(root).parts) < 3 or root.endswith(("/cawemo", "/cawemo/1.9"))):
            raise ValueError("Unsafe docs root")
    if stage == live or stage.startswith(live + "/") or live.startswith(stage + "/"):
        raise ValueError("Stage/Live roots overlap")


def real_parents(path):
    for parent in [*reversed(path.parents), path]:
        if parent.is_symlink():
            raise ValueError("Symlink in remote scope")
        if parent.exists() and not parent.is_dir():
            raise ValueError("Non-directory scope parent")


def tree(path):
    real_parents(path)
    count, total = 0, 0
    if path.exists():
        for root, dirs, files in os.walk(path, followlinks=False):
            for name in dirs + files:
                count += 1
                info = (Path(root) / name).lstat()
                if (not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)) or
                        (stat.S_ISREG(info.st_mode) and info.st_nlink != 1)):
                    raise ValueError("Remote scope has links/special files")
                total += info.st_size
                if count > MAX_ENTRIES or total > MAX_TOTAL:
                    raise ValueError("Excessive remote scope (including retained files)")


def verify(path, expected):
    raw = (json.dumps(expected, sort_keys=True, separators=(",", ":")) + "\n").encode()
    manifest_file = path / MANIFEST
    if manifest_file.stat().st_size != len(raw) or manifest_file.read_bytes() != raw:
        raise ValueError("Remote manifest differs from trusted Stage build")
    for name, entry in expected["files"].items():
        file = path / name
        if not file.is_file() or file.stat().st_size != entry["size"]:
            raise ValueError("Remote expected file missing or wrong size")
        digest = hashlib.sha256()
        with file.open("rb") as content:
            for block in iter(lambda: content.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != entry["sha256"]:
            raise ValueError("Remote expected bytes differ from trusted build")


def file_parents(path, expected):
    for name in [MANIFEST, *expected["files"]]:
        target = path / name
        real_parents(target.parent)
        if target.exists() and not target.is_file():
            raise ValueError("Remote expected file has incompatible type")


def execute(mode, stage, live, expected):
    roots(stage, live)
    stage_root, live_root = Path(stage), Path(live)
    for root in (stage_root, live_root):
        real_parents(root)
        if not root.is_dir():
            raise ValueError("Docs roots must already exist")
    stage_scope, live_scope = stage_root / SCOPE, live_root / SCOPE
    tree(stage_scope)
    file_parents(stage_scope, expected)
    if mode == "prepare-stage":
        stage_scope.mkdir(parents=True, exist_ok=True)
    elif mode == "verify-stage":
        verify(stage_scope, expected)
    elif mode == "promote":
        tree(live_scope)
        file_parents(live_scope, expected)
        verify(stage_scope, expected)
        live_scope.mkdir(parents=True, exist_ok=True)
        # Do not overwrite retained older Live downloads with unmanifested Stage
        # extras. Only the trusted build's exact files are promoted.
        files = "\0".join([MANIFEST, *sorted(expected["files"])]) + "\0"
        subprocess.run(["rsync", *OPTIONS, "--files-from=-", "--from0", "--",
                        f"{stage_scope}/", f"{live_scope}/"],
                       input=files, text=True, check=True, timeout=600)
        tree(live_scope)
        verify(live_scope, expected)
    else:
        raise ValueError("Invalid remote operation")


if __name__ == "__main__":
    try:
        os.umask(0o022)
        execute(*sys.argv[1:], EXPECTED)  # Set by trusted local tooling, never remote input.
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        sys.exit(f"Cawemo remote transfer failed: {error}")
