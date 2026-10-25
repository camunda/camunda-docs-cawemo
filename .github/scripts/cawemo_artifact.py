#!/usr/bin/env python3
"""Cawemo-only build provenance and bounded, link-free artifact restoration.

The archive handling is adapted from the native Manual publisher.
"""

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tarfile


SCOPE = "cawemo/1.9"
PREFIX = f"/{SCOPE}/"
INSTALL = "technical-guide/installation/index.html"
MANIFEST = "cawemo-publish-manifest.json"
REPOSITORY = "camunda/camunda-docs-cawemo"
MAX_FILES = 4096
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_MANIFEST = 2 * 1024 * 1024
SHA = r"[0-9a-f]{40}"
DIGEST = r"[0-9a-f]{64}"
DOWNLOAD = r"download/cawemo-1\.9\.\d+\.(?:zip|tar\.gz)"
FINGERPRINT = r"(?:css|js)/docs\.([0-9a-f]{64})\.(css|js)"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(name):
    if (not isinstance(name, str) or len(name) > 512 or
            not re.fullmatch(r"[A-Za-z0-9_./-]+", name) or
            any(part in ("", ".", "..") for part in name.split("/"))):
        raise ValueError("Unsafe relative path")
    if PurePosixPath(name).is_absolute():
        raise ValueError("Absolute artifact path")
    return name


def provenance(source_sha, tooling_sha, run_id):
    if (not re.fullmatch(SHA, source_sha) or not re.fullmatch(SHA, tooling_sha) or
            not re.fullmatch(r"[1-9][0-9]{0,19}", run_id)):
        raise ValueError("Missing or malformed source/tooling SHA or Stage run ID")
    return {
        "repository": REPOSITORY, "version": "1.9",
        "source_sha": source_sha, "tooling_sha": tooling_sha, "stage_run_id": run_id,
    }


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate manifest key")
        result[key] = value
    return result


def decode_manifest(raw, expected_digest, expected_provenance):
    if (len(raw) > MAX_MANIFEST or not re.fullmatch(DIGEST, expected_digest) or
            hashlib.sha256(raw).hexdigest() != expected_digest):
        raise ValueError("Missing trusted manifest digest, oversized manifest or digest mismatch")
    manifest = json.loads(raw, object_pairs_hook=no_duplicates)
    keys = {"schema", "provenance", "files", "downloads", "assets"}
    if not isinstance(manifest, dict) or set(manifest) != keys or type(manifest["schema"]) is not int or manifest["schema"] != 1:
        raise ValueError("Malformed manifest schema")
    if manifest["provenance"] != expected_provenance:
        raise ValueError("Stage provenance does not match trusted build outputs")
    files = manifest["files"]
    if not isinstance(files, dict) or not 1 <= len(files) <= MAX_FILES:
        raise ValueError("Missing or excessive manifest files")
    total = 0
    for name, entry in files.items():
        relative(name)
        if name == MANIFEST or not isinstance(entry, dict) or set(entry) != {"sha256", "size"}:
            raise ValueError("Malformed manifest file entry")
        if (type(entry["size"]) is not int or not 0 <= entry["size"] <= MAX_FILE or
                not isinstance(entry["sha256"], str) or not re.fullmatch(DIGEST, entry["sha256"])):
            raise ValueError("Invalid file size/digest")
        total += entry["size"]
        if any(str(parent) in files for parent in PurePosixPath(name).parents):
            raise ValueError("Manifest file used as parent")
    if total > MAX_TOTAL or "index.html" not in files or INSTALL not in files:
        raise ValueError("Missing required HTML or excessive content")
    downloads, assets = manifest["downloads"], manifest["assets"]
    if (not isinstance(downloads, list) or len(downloads) != 2 or
            any(not isinstance(name, str) or not re.fullmatch(DOWNLOAD, name) or name not in files for name in downloads) or
            len(set(downloads)) != 2 or
            {name.rsplit(".", 1)[-1] for name in downloads} != {"zip", "gz"} or
            downloads[0].split(".zip")[0].split(".tar.gz")[0] != downloads[1].split(".zip")[0].split(".tar.gz")[0]):
        raise ValueError("Missing exact ZIP/TAR download pair")
    if (not isinstance(assets, list) or len(assets) != 2 or
            any(not isinstance(name, str) or not re.fullmatch(FINGERPRINT, name) or name not in files for name in assets) or
            {name.rsplit(".", 1)[-1] for name in assets} != {"css", "js"}):
        raise ValueError("Missing fingerprinted CSS/JS")
    for name in assets:
        if re.fullmatch(FINGERPRINT, name).group(1) != files[name]["sha256"]:
            raise ValueError("Asset fingerprint/content digest mismatch")
    return manifest


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if (tag == "a" and key == "href") or (tag == "link" and key == "href") or (tag == "script" and key == "src"):
                if value:
                    self.links.append(value)


def installation_links(content):
    parser = Links()
    parser.feed(content.decode("utf-8"))
    downloads = sorted({link[len(PREFIX):] for link in parser.links
                        if link.startswith(PREFIX) and re.fullmatch(DOWNLOAD, link[len(PREFIX):])})
    assets = sorted({link[len(PREFIX):] for link in parser.links
                     if link.startswith(PREFIX) and re.fullmatch(FINGERPRINT, link[len(PREFIX):])})
    return downloads, assets


def scan(source):
    if source.is_symlink() or not source.is_dir() or any(p.is_symlink() for p in source.absolute().parents):
        raise ValueError("Build root must be a real directory without symlink parents")
    paths, total, count = [], 0, 0
    for root, dirs, files in os.walk(source, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(root) / name
            relative(path.relative_to(source).as_posix())
            info = path.lstat()
            if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)) or (path.is_file() and info.st_nlink != 1):
                raise ValueError("Build contains links or special files")
            paths.append(path)
            if len(paths) > MAX_FILES * 2:
                raise ValueError("Excessive build entries")
            if path.is_file():
                count += 1
                total += info.st_size
                if info.st_size > MAX_FILE or total > MAX_TOTAL or count > MAX_FILES:
                    raise ValueError("Excessive build size")
    return sorted(paths)


def verify_tree(source, manifest, raw):
    paths = scan(source)
    actual = {p.relative_to(source).as_posix() for p in paths if p.is_file()}
    if actual != set(manifest["files"]) | {MANIFEST}:
        raise ValueError("Build file set differs from manifest")
    if (source / MANIFEST).read_bytes() != raw:
        raise ValueError("Build manifest changed")
    for name, entry in manifest["files"].items():
        path = source / name
        if path.stat().st_size != entry["size"] or sha256(path) != entry["sha256"]:
            raise ValueError(f"Build bytes differ: {name}")
    if installation_links((source / INSTALL).read_bytes()) != (manifest["downloads"], manifest["assets"]):
        raise ValueError("Exact installation download/asset links differ")


def create_manifest(source, content_source, expected_provenance):
    paths = scan(source)
    if (source / MANIFEST).exists():
        raise ValueError("Build must not supply its own provenance manifest")
    downloads, assets = installation_links((source / INSTALL).read_bytes())
    text = (content_source / "content/technical-guide/installation/_index.md").read_text()
    expected_downloads = sorted(set(re.findall(r'refstatic "(' + DOWNLOAD + r')"', text)))
    if downloads != expected_downloads:
        raise ValueError("Generated installation links differ from selected source")
    for name in downloads:
        original = content_source / "static" / name
        if (original.is_symlink() or any(p.is_symlink() for p in original.absolute().parents) or
                not original.is_file() or original.stat().st_nlink != 1 or sha256(original) != sha256(source / name)):
            raise ValueError("Generated download bytes differ from source bundle")
    files = {p.relative_to(source).as_posix(): {"sha256": sha256(p), "size": p.stat().st_size}
             for p in paths if p.is_file()}
    manifest = {"schema": 1, "provenance": expected_provenance, "files": files,
                "downloads": downloads, "assets": assets}
    raw = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(raw).hexdigest()
    decode_manifest(raw, digest, expected_provenance)
    (source / MANIFEST).write_bytes(raw)
    verify_tree(source, manifest, raw)
    return digest


def pack(source, archive):
    paths = scan(source)
    if archive.exists() or archive.is_symlink() or any(p.is_symlink() for p in archive.absolute().parents):
        raise ValueError("Archive destination exists or has a symlink parent")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w", format=tarfile.USTAR_FORMAT) as output:
        for path in paths:
            output.add(path, arcname=path.relative_to(source).as_posix(), recursive=False)
    if archive.stat().st_size > MAX_TOTAL + MAX_FILES * 4096:
        raise ValueError("Excessive archive size")
    return sha256(archive)


def restore(archive, destination, expected):
    if (not re.fullmatch(DIGEST, expected) or archive.is_symlink() or not archive.is_file() or
            archive.stat().st_nlink != 1 or
            archive.stat().st_size > MAX_TOTAL + MAX_FILES * 4096 or sha256(archive) != expected):
        raise ValueError("Missing trusted archive SHA-256, excessive archive or digest mismatch")
    if destination.exists() or destination.is_symlink() or any(p.is_symlink() for p in destination.absolute().parents):
        raise ValueError("Restore destination exists or has a symlink parent")
    with tarfile.open(archive, "r:") as source:
        members, total, count = {}, 0, 0
        for member in source:
            name = relative(member.name)
            if (member.pax_headers or member.type not in (tarfile.REGTYPE, tarfile.AREGTYPE, tarfile.DIRTYPE) or
                    (member.isdir() and member.size != 0) or name in members):
                raise ValueError("Unsafe/duplicate archive member")
            if member.isfile():
                count += 1
            total += member.size
            if member.size < 0 or member.size > MAX_FILE or total > MAX_TOTAL or len(members) >= MAX_FILES * 2 or count > MAX_FILES:
                raise ValueError("Excessive archive content")
            members[name] = member
        if any(name not in members or not members[name].isfile() for name in ("index.html", INSTALL, MANIFEST)):
            raise ValueError("Missing required archive files")
        for name in members:
            if any(str(p) in members and not members[str(p)].isdir() for p in PurePosixPath(name).parents):
                raise ValueError("Archive file used as a directory")
        destination.mkdir(parents=True)
        for name, member in members.items():
            target = destination / name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with source.extractfile(member) as content, target.open("xb") as output:
                    shutil.copyfileobj(content, output)
                target.chmod(0o644)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "restore"))
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--archive-sha256", default="")
    args = parser.parse_args()
    try:
        expected = provenance(os.environ.get("SOURCE_SHA", ""), os.environ.get("TOOLING_SHA", ""),
                              os.environ.get("STAGE_RUN_ID", ""))
        if args.mode == "build":
            if args.source is None:
                raise ValueError("Selected content source required")
            manifest_digest = create_manifest(args.tree, args.source, expected)
            archive_digest = pack(args.tree, args.archive)
            message = f"source={expected['source_sha']}; tooling={expected['tooling_sha']}; Stage run={expected['stage_run_id']}; manifest-sha256={manifest_digest}; archive-sha256={archive_digest}"
            print(message)
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                output.write(f"archive-sha256={archive_digest}\nmanifest-sha256={manifest_digest}\n")
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
                summary.write(f"## Trusted Cawemo build outputs\n\n`{message}`\n")
        else:
            restore(args.archive, args.tree, args.archive_sha256)
            raw = (args.tree / MANIFEST).read_bytes()
            manifest = decode_manifest(raw, os.environ.get("MANIFEST_SHA256", ""), expected)
            verify_tree(args.tree, manifest, raw)
    except (ValueError, OSError, tarfile.TarError, KeyError, TypeError) as error:
        parser.exit(1, f"Cawemo artifact failed: {error}\n")


if __name__ == "__main__":
    main()
