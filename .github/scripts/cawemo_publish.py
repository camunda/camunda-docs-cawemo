#!/usr/bin/env python3
"""Cawemo destination-local HTTPS checks and explicitly non-deleting transfer."""

import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from urllib.parse import urljoin, urlsplit

import cawemo_artifact as artifact
import cawemo_remote as remote


HOSTS = {"stage": "stage.docs.camunda.org", "live": "docs.camunda.org"}
CONFIRM = "promote cawemo docs 1.9 to live"


def request_inputs(env, phase):
    if phase not in HOSTS or env.get("VERSION") != "1.9" or env.get("DRY_RUN") not in ("true", "false"):
        raise ValueError("Only version 1.9 and explicit boolean dry-run are accepted")
    if env["DRY_RUN"] == "false" and env.get("NATIVE_ENABLED") != "true":
        raise ValueError("Real publishing is disabled until authorized DOCS_CAWEMO_NATIVE_ENABLED=true activation")
    if phase == "live" and env["DRY_RUN"] == "false" and env.get("CONFIRM_LIVE_PROMOTE") != CONFIRM:
        raise ValueError(f"Real Live promotion requires exact confirmation: {CONFIRM}")
    if phase == "stage" or env["DRY_RUN"] == "false":
        artifact.provenance(env.get("SOURCE_SHA", ""), env.get("TOOLING_SHA", ""), env.get("STAGE_RUN_ID", ""))
        if not re.fullmatch(artifact.DIGEST, env.get("MANIFEST_SHA256", "")):
            raise ValueError("Trusted Stage build manifest SHA-256 required")


def route(destination, value):
    if destination not in ("legacy", "aws"):
        raise ValueError("Invalid destination")
    if destination == "aws":
        try:
            ipaddress.ip_address(value)
            if "%" in value:
                raise ValueError("Scoped IP")
        except ValueError as error:
            raise ValueError("AWS requires approved Vault IP; DNS fallback forbidden") from error


def config(env):
    destination = env.get("DESTINATION", "")
    route(destination, env.get("DOCS_AWS_SMOKE_RESOLVE", ""))
    host = env.get("DOCS_AWS_SSH_HOST" if destination == "aws" else "DOCS_SSH_HOST", "")
    if destination == "aws" and host != "webserver-docs.camunda-it.rocks":
        raise ValueError("AWS SSH host is not approved")
    if len(host) > 253 or not host or any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label) for label in host.split(".")):
        raise ValueError("Missing or unsafe SSH host")
    user = env.get("DOCS_SSH_USER", "")
    if not re.fullmatch(r"[a-z_][a-z0-9_-]{0,31}", user) or user == "root":
        raise ValueError("Missing or unsafe SSH user")
    for name in ("DOCS_SSH_PRIVATE_KEY", "DOCS_SSH_KNOWN_HOSTS", "DOCS_STAGE_ROOT", "DOCS_LIVE_ROOT"):
        if not env.get(name, "").strip() or len(env[name]) > 1024 * 1024:
            raise ValueError(f"Missing required job-local Vault output: {name}")
    remote.roots(env["DOCS_STAGE_ROOT"], env["DOCS_LIVE_ROOT"])
    return user, host


class HTTPS:
    def __init__(self, destination, phase, ip, workdir):
        route(destination, ip)
        if phase not in HOSTS:
            raise ValueError("Invalid phase")
        self.destination, self.host, self.ip = destination, HOSTS[phase], ip
        self.version_checked = False
        self.workdir = workdir
        self.workdir.mkdir(parents=True, exist_ok=False)

    def check_curl_version(self):
        if not self.version_checked:
            completed = subprocess.run(["curl", "--disable", "--version"],
                                       capture_output=True, text=True, timeout=5)
            match = re.match(r"curl (\d+)\.(\d+)\.(\d+)\b", completed.stdout)
            if completed.returncode or not match or tuple(map(int, match.groups())) < (8, 4, 0):
                raise ValueError("curl >= 8.4.0 is required for streaming max-filesize bounds; no fallback")
            self.version_checked = True

    def command(self, path, limit):
        if not path.startswith("/") or path.startswith("//") or re.search(r"[\s?#\\]", path):
            raise ValueError("Unsafe canonical request path")
        command = [
            "curl", "--disable", "--silent", "--show-error", "--noproxy", "*",
            "--proxy", "", "--proto", "=https", "--tlsv1.2",
            "--connect-timeout", "10", "--max-time", "30", "--max-filesize", str(limit),
            "--dump-header", str(self.workdir / "headers"), "--output", str(self.workdir / "body"),
            "--write-out", "%{http_code}",
        ]
        if self.destination == "aws":
            address = f"[{self.ip}]" if ":" in self.ip else self.ip
            command += ["--resolve", f"{self.host}:443:{address}"]
        return command + ["--url", f"https://{self.host}{path}"]

    def get(self, path, limit=artifact.MAX_FILE):
        self.check_curl_version()
        completed = subprocess.run(self.command(path, limit), capture_output=True, text=True, timeout=40)
        if completed.returncode:
            raise ValueError(f"Canonical HTTPS request failed: {path} (curl {completed.returncode})")
        if not re.fullmatch(r"[1-5][0-9]{2}", completed.stdout):
            raise ValueError("Invalid curl status")
        header_file, body_file = self.workdir / "headers", self.workdir / "body"
        if header_file.stat().st_size > 65536 or body_file.stat().st_size > limit:
            raise ValueError("Excessive HTTP response")
        headers = {}
        lines = header_file.read_text().splitlines()
        if not lines or not re.fullmatch(r"HTTP/(?:1\.[01]|2|3) [1-5][0-9]{2}(?: .*)?", lines[0]):
            raise ValueError("Malformed HTTP headers")
        if int(lines[0].split()[1]) != int(completed.stdout):
            raise ValueError("HTTP header/status mismatch")
        for line in lines[1:]:
            if not line:
                continue
            if ":" not in line or line[0].isspace():
                raise ValueError("Ambiguous HTTP headers")
            name, value = line.split(":", 1)
            name = name.lower()
            if name in ("location", "content-type", "content-length") and name in headers:
                raise ValueError("Duplicate critical HTTP header")
            headers[name] = value.strip()
        body = body_file.read_bytes()
        if "content-length" in headers and (not headers["content-length"].isdigit() or int(headers["content-length"]) != len(body)):
            raise ValueError("HTTP Content-Length mismatch")
        return int(completed.stdout), headers, body


def direct(response, name, entry=None):
    status, headers, body = response
    if status != 200 or "location" in headers:
        raise ValueError(f"Expected direct HTTP 200 (no version-root fallback): {name}")
    mime = headers.get("content-type", "").split(";", 1)[0].lower()
    accepted = None
    if name.endswith(".html"):
        accepted = {"text/html"}
    elif name.endswith(".css"):
        accepted = {"text/css"}
    elif name.endswith(".js"):
        accepted = {"application/javascript", "text/javascript", "application/x-javascript"}
    elif name.endswith(".zip"):
        accepted = {"application/zip", "application/octet-stream", "application/x-zip-compressed"}
    elif name.endswith(".tar.gz"):
        accepted = {"application/gzip", "application/x-gzip", "application/octet-stream"}
    elif name == artifact.MANIFEST:
        accepted = {"application/json"}
    if accepted is not None and mime not in accepted:
        raise ValueError(f"Unexpected Content-Type for {name}")
    if entry is not None and (len(body) != entry["size"] or hashlib.sha256(body).hexdigest() != entry["sha256"]):
        raise ValueError(f"Served bytes differ from trusted build: {name}")
    return body


def expected_manifest(client, env, local=None):
    expected = artifact.provenance(env.get("SOURCE_SHA", ""), env.get("TOOLING_SHA", ""), env.get("STAGE_RUN_ID", ""))
    raw = direct(client.get(artifact.PREFIX + artifact.MANIFEST, artifact.MAX_MANIFEST), artifact.MANIFEST)
    manifest = artifact.decode_manifest(raw, env.get("MANIFEST_SHA256", ""), expected)
    if local is not None and raw != (local / artifact.MANIFEST).read_bytes():
        raise ValueError("Destination manifest differs from restored trusted artifact")
    return manifest


def check(client, env, local=None):
    manifest = expected_manifest(client, env, local)
    installation = None
    for name, entry in manifest["files"].items():
        path = artifact.PREFIX + (name[:-10] if name == "index.html" or name.endswith("/index.html") else name)
        body = direct(client.get(path, max(1, entry["size"])), name, entry)
        if name == artifact.INSTALL:
            installation = body
    if artifact.installation_links(installation) != (manifest["downloads"], manifest["assets"]):
        raise ValueError("Served installation links differ from selected source build")
    install_path = artifact.PREFIX + "technical-guide/installation/"
    for path, status, target in (
            ("/cawemo/", 301, artifact.PREFIX),
            ("/cawemo/technical-guide/installation/", 307, install_path),
            ("/cawemo/99.0/technical-guide/installation/", 307, install_path)):
        actual_status, headers, _ = client.get(path)
        location = headers.get("location", "")
        expected_url = f"https://{client.host}{target}"
        parsed = urlsplit(urljoin(f"https://{client.host}{path}", location))
        if actual_status != status or not location or parsed.geturl() != expected_url:
            raise ValueError(f"Cawemo redirect contract failed: {path}")
        name = "index.html" if target == artifact.PREFIX else artifact.INSTALL
        direct(client.get(target), name, manifest["files"][name])
    print(f"Cawemo product gate passed: {client.destination}/{client.host}; {len(manifest['files'])} exact files plus redirect contracts")
    return manifest


def ssh_files(directory, env):
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    for name, key in (("key", "DOCS_SSH_PRIVATE_KEY"), ("known_hosts", "DOCS_SSH_KNOWN_HOSTS")):
        path = directory / name
        with path.open("x", encoding="utf-8") as output:
            os.chmod(path, 0o600)
            output.write(env[key].rstrip() + "\n")
    return [
        "ssh", "-F", "/dev/null", "-i", str((directory / "key").absolute()),
        "-o", f"UserKnownHostsFile={(directory / 'known_hosts').absolute()}",
        "-o", "GlobalKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=yes",
        "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-o", "IdentityAgent=none",
        "-o", "PasswordAuthentication=no", "-o", "KbdInteractiveAuthentication=no",
        "-o", "ProxyCommand=none", "-o", "ProxyJump=none", "-o", "ConnectTimeout=10",
        "-o", "ClearAllForwardings=yes", "-o", "ForwardAgent=no", "-o", "PermitLocalCommand=no",
        "-o", "RequestTTY=no", "-o", "ControlMaster=no", "-o", "ControlPath=none",
        "-o", "ServerAliveInterval=15", "-o", "ServerAliveCountMax=2", "-o", "LogLevel=ERROR",
    ]


def remote_call(ssh, target, operation, env, manifest):
    payload = f"EXPECTED = {manifest!r}\n" + Path(remote.__file__).read_text()
    command = shlex.join(["python3", "-", operation, env["DOCS_STAGE_ROOT"], env["DOCS_LIVE_ROOT"]])
    subprocess.run([*ssh, target, command], input=payload, text=True, check=True, timeout=900)


def transfer(env, phase, local, directory, client=None):
    request_inputs(env, phase)
    user, host = config(env)
    if env["DRY_RUN"] == "true":
        if phase == "stage":
            raw = (local / artifact.MANIFEST).read_bytes()
            manifest = artifact.decode_manifest(raw, env["MANIFEST_SHA256"],
                                                artifact.provenance(env["SOURCE_SHA"], env["TOOLING_SHA"], env["STAGE_RUN_ID"]))
            artifact.verify_tree(local, manifest, raw)
        print(f"DRY RUN ONLY: {phase} {artifact.SCOPE}; no SSH, remote mkdir, transfer or real product/global smoke. Real gates intentionally skipped.")
        return
    for tool in ("rsync", "ssh"):
        if not shutil.which(tool):
            raise ValueError(f"Required standard tool missing: {tool}")
    if phase == "stage":
        raw = (local / artifact.MANIFEST).read_bytes()
        manifest = artifact.decode_manifest(raw, env["MANIFEST_SHA256"],
                                            artifact.provenance(env["SOURCE_SHA"], env["TOOLING_SHA"], env["STAGE_RUN_ID"]))
        artifact.verify_tree(local, manifest, raw)
    else:
        if client is None or client.host != HOSTS["stage"] or client.destination != env["DESTINATION"]:
            raise ValueError("Real promotion requires this destination's Stage HTTPS validation")
        manifest = check(client, env)
    ssh = ssh_files(directory, env)
    target = f"{user}@{host}"
    try:
        if phase == "stage":
            remote_call(ssh, target, "prepare-stage", env, manifest)
            subprocess.run(["rsync", *remote.OPTIONS, "-e", shlex.join(ssh), "--",
                            f"{local.absolute()}/", f"{target}:{env['DOCS_STAGE_ROOT']}/{artifact.SCOPE}/"],
                           check=True, timeout=900)
            remote_call(ssh, target, "verify-stage", env, manifest)
        else:
            remote_call(ssh, target, "promote", env, manifest)
    finally:
        shutil.rmtree(directory)
    print(f"Transferred {artifact.SCOPE} without deletion; old downloads and other versions retained")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "transfer"))
    parser.add_argument("--phase", required=True, choices=("stage", "live"))
    parser.add_argument("--tree", type=Path, default=Path("public"))
    parser.add_argument("--workdir", type=Path, default=Path(".cawemo-http"))
    args = parser.parse_args()
    try:
        request_inputs(os.environ, args.phase)
        config(os.environ)
        if args.mode == "check":
            if os.environ["DRY_RUN"] != "false":
                raise ValueError("Real product gates must be skipped, never reported passed in dry-run")
            if os.environ.get("ARCHIVE_SHA256") and not args.tree.is_dir():
                raise ValueError("Stage post-publication requires the restored trusted build tree")
            client = HTTPS(os.environ["DESTINATION"], args.phase, os.environ.get("DOCS_AWS_SMOKE_RESOLVE", ""), args.workdir)
            check(client, os.environ, args.tree if args.tree.exists() else None)
        else:
            client = None
            if args.phase == "live" and os.environ["DRY_RUN"] == "false":
                client = HTTPS(os.environ["DESTINATION"], "stage", os.environ.get("DOCS_AWS_SMOKE_RESOLVE", ""), args.workdir)
            transfer(os.environ, args.phase, args.tree, Path(".cawemo-ssh"), client)
    except (ValueError, OSError, subprocess.SubprocessError, KeyError, TypeError) as error:
        parser.exit(1, f"Cawemo {args.mode} failed: {error}\n")


if __name__ == "__main__":
    main()
