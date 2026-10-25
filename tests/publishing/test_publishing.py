"""Focused offline publisher tests. All fixtures stay inside this worktree."""

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import textwrap
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".github/scripts"))
import cawemo_artifact as artifact
import cawemo_publish as publish
import cawemo_remote as remote
import cawemo_result as result


class Fixture(unittest.TestCase):
    def setUp(self):
        self.work = ROOT / ".local-validation/tests" / self.id().rsplit(".", 1)[-1]
        self.work.mkdir(parents=True, exist_ok=False)
        self.source, self.tree = self.work / "source", self.work / "public"
        self.tree.mkdir()
        self.provenance = artifact.provenance("a" * 40, "b" * 40, "123456")
        self.downloads = ["download/cawemo-1.9.43.tar.gz", "download/cawemo-1.9.43.zip"]
        self.assets = []
        files = {"index.html": b"<!doctype html><html>Cawemo 1.9</html>"}
        for suffix, content in (("css", b"body {color: black}"), ("js", b"console.log('docs');")):
            self.assets.append(f"{suffix}/docs.{hashlib.sha256(content).hexdigest()}.{suffix}")
            files[self.assets[-1]] = content
        files.update({name: b"source-owned " + name.encode() for name in self.downloads})
        links = "".join(f'<a href="{artifact.PREFIX}{name}">1.9.43</a>' for name in self.downloads)
        files[artifact.INSTALL] = (
            f'<!doctype html><html><link href="{artifact.PREFIX}{self.assets[0]}">'
            f'{links}<script src="{artifact.PREFIX}{self.assets[1]}"></script></html>').encode()
        for name, content in files.items():
            path = self.tree / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            if name in self.downloads:
                path = self.source / "static" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        install = self.source / "content/technical-guide/installation/_index.md"
        install.parent.mkdir(parents=True)
        install.write_text("\n".join('{{< refstatic "' + name + '" >}}' for name in self.downloads))
        self.manifest_digest = artifact.create_manifest(self.tree, self.source, self.provenance)
        self.raw = (self.tree / artifact.MANIFEST).read_bytes()
        self.manifest = artifact.decode_manifest(self.raw, self.manifest_digest, self.provenance)
        self.env = {
            "VERSION": "1.9", "DRY_RUN": "false", "DESTINATION": "aws",
            "NATIVE_ENABLED": "true",
            "CONFIRM_LIVE_PROMOTE": publish.CONFIRM, "SOURCE_SHA": "a" * 40,
            "TOOLING_SHA": "b" * 40, "STAGE_RUN_ID": "123456", "MANIFEST_SHA256": self.manifest_digest,
            "DOCS_SSH_USER": "docs", "DOCS_AWS_SSH_HOST": "webserver-docs.camunda-it.rocks",
            "DOCS_AWS_SMOKE_RESOLVE": "192.0.2.42", "DOCS_SSH_HOST": "legacy.example.invalid",
            "DOCS_SSH_PRIVATE_KEY": "offline-test-key", "DOCS_SSH_KNOWN_HOSTS": "offline-test-host-key",
            "DOCS_STAGE_ROOT": str(self.work / "stage"), "DOCS_LIVE_ROOT": str(self.work / "live"),
        }
        self.archive = self.work / "build.tar"
        self.archive_digest = artifact.pack(self.tree, self.archive)

    def tearDown(self):
        shutil.rmtree(self.work)

    def malformed(self, change):
        manifest = copy.deepcopy(self.manifest)
        change(manifest)
        raw = json.dumps(manifest).encode()
        return artifact.decode_manifest(raw, hashlib.sha256(raw).hexdigest(), self.provenance)


class ArtifactTests(Fixture):
    def test_pack_restore_exact_files_and_bytes(self):
        destination = self.work / "restored"
        artifact.restore(self.archive, destination, self.archive_digest)
        artifact.verify_tree(destination, self.manifest, self.raw)
        self.assertEqual(artifact.sha256(destination / self.downloads[0]), artifact.sha256(self.source / "static" / self.downloads[0]))

    def test_missing_and_wrong_trusted_archive_digest_rejected_before_writes(self):
        for digest in ("", "0" * 64):
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                artifact.restore(self.archive, self.work / "restored", digest)
            self.assertFalse((self.work / "restored").exists())

    def test_existing_or_symlink_restore_destination_rejected(self):
        for destination in (self.tree, self.work / "link"):
            if destination.name == "link":
                destination.symlink_to(self.tree, target_is_directory=True)
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                artifact.restore(self.archive, destination, self.archive_digest)

    def test_archive_input_special_files_and_links_rejected_without_reading(self):
        archive = self.work / "unsafe-input"
        for kind in ("fifo", "symlink", "hardlink"):
            with self.subTest(kind=kind):
                if kind == "fifo":
                    os.mkfifo(archive)
                elif kind == "symlink":
                    archive.symlink_to(self.archive)
                else:
                    os.link(self.archive, archive)
                with self.assertRaises(ValueError):
                    artifact.restore(archive, self.work / "bad-restore", self.archive_digest)
                archive.unlink()
        self.assertFalse((self.work / "bad-restore").exists())

    def test_pack_does_not_overwrite_existing_or_linked_archive_paths(self):
        with self.assertRaises(ValueError):
            artifact.pack(self.tree, self.archive)
        link = self.work / "archive-link"
        link.symlink_to(self.archive)
        with self.assertRaises(ValueError):
            artifact.pack(self.tree, link)
        self.assertEqual(artifact.sha256(self.archive), self.archive_digest)

    def test_symlink_restore_parent_rejected(self):
        parent = self.work / "parent-link"
        parent.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):
            artifact.restore(self.archive, parent / "new", self.archive_digest)
        self.assertFalse((self.source / "new").exists())

    def make_bad_archive(self, entries):
        archive = self.work / "bad.tar"
        with tarfile.open(archive, "w", format=tarfile.PAX_FORMAT) as output:
            for name in ("index.html", artifact.INSTALL, artifact.MANIFEST):
                info = tarfile.TarInfo(name)
                info.size = 1
                output.addfile(info, io.BytesIO(b"x"))
            for name, type_, size, link in entries:
                info = tarfile.TarInfo(name)
                info.type, info.size, info.linkname = type_, size, link
                output.addfile(info, io.BytesIO(b"x" * size) if type_ == tarfile.REGTYPE else None)
        return archive

    def test_real_malicious_tar_members_rejected_without_extraction(self):
        cases = [
            ("../escape", tarfile.REGTYPE, 1, ""),
            ("/absolute", tarfile.REGTYPE, 1, ""),
            ("a/../../escape", tarfile.REGTYPE, 1, ""),
            ("a//b", tarfile.REGTYPE, 1, ""),
            ("./dot", tarfile.REGTYPE, 1, ""),
            ("a\\b", tarfile.REGTYPE, 1, ""),
            ("a?query", tarfile.REGTYPE, 1, ""),
            ("link", tarfile.SYMTYPE, 0, "../escape"),
            ("hardlink", tarfile.LNKTYPE, 0, "index.html"),
            ("device", tarfile.CHRTYPE, 0, ""),
            ("block", tarfile.BLKTYPE, 0, ""),
            ("fifo", tarfile.FIFOTYPE, 0, ""),
            ("contiguous", tarfile.CONTTYPE, 0, ""),
            ("index.html", tarfile.REGTYPE, 1, ""),
        ]
        for entry in cases:
            with self.subTest(entry=entry):
                archive = self.make_bad_archive([entry])
                with self.assertRaises(ValueError):
                    artifact.restore(archive, self.work / "bad-restore", artifact.sha256(archive))
                self.assertFalse((self.work / "bad-restore").exists())

    def test_archive_file_parent_rejected(self):
        archive = self.make_bad_archive([("parent", tarfile.REGTYPE, 1, ""), ("parent/child", tarfile.REGTYPE, 1, "")])
        with self.assertRaises(ValueError):
            artifact.restore(archive, self.work / "bad-restore", artifact.sha256(archive))
        self.assertFalse((self.work / "bad-restore").exists())

    def test_real_sparse_and_pax_archives_rejected(self):
        archive = self.work / "metadata.tar"
        for kind in ("sparse", "pax"):
            with self.subTest(kind=kind):
                with tarfile.open(archive, "w", format=tarfile.PAX_FORMAT) as output:
                    member = tarfile.TarInfo("index.html")
                    if kind == "sparse":
                        member.type = tarfile.GNUTYPE_SPARSE
                    else:
                        member.pax_headers = {"comment": "unexpected extension metadata"}
                    output.addfile(member)
                with self.assertRaises((ValueError, tarfile.TarError)):
                    artifact.restore(archive, self.work / "bad-restore", artifact.sha256(archive))
                self.assertFalse((self.work / "bad-restore").exists())

    def test_archive_bounds_and_missing_required_file_rejected(self):
        with patch.object(artifact, "MAX_FILE", 1), self.assertRaises(ValueError):
            artifact.restore(self.archive, self.work / "bad-restore", self.archive_digest)
        with patch.object(artifact, "MAX_FILES", 1), self.assertRaises(ValueError):
            artifact.restore(self.archive, self.work / "bad-restore", self.archive_digest)
        with patch.object(artifact, "MAX_TOTAL", 1), self.assertRaises(ValueError):
            artifact.restore(self.archive, self.work / "bad-restore", self.archive_digest)
        missing = self.work / "missing.tar"
        with tarfile.open(missing, "w"):
            pass
        with self.assertRaises(ValueError):
            artifact.restore(missing, self.work / "bad-restore", artifact.sha256(missing))
        self.assertFalse((self.work / "bad-restore").exists())

    def test_build_links_hardlinks_and_special_files_rejected(self):
        bad = self.tree / "bad"
        for kind in ("symlink", "hardlink", "fifo"):
            with self.subTest(kind=kind):
                if kind == "symlink":
                    bad.symlink_to(self.tree / "index.html")
                elif kind == "hardlink":
                    os.link(self.tree / "index.html", bad)
                else:
                    os.mkfifo(bad)
                with self.assertRaises(ValueError):
                    artifact.pack(self.tree, self.work / "bad-pack.tar")
                bad.unlink()

    def test_source_bundle_or_generated_links_changes_fail(self):
        (self.tree / artifact.MANIFEST).unlink()
        (self.source / "static" / self.downloads[0]).write_bytes(b"other release")
        with self.assertRaisesRegex(ValueError, "download bytes"):
            artifact.create_manifest(self.tree, self.source, self.provenance)
        (self.source / "content/technical-guide/installation/_index.md").write_text("no download links")
        with self.assertRaisesRegex(ValueError, "links"):
            artifact.create_manifest(self.tree, self.source, self.provenance)

    def test_manifest_missing_provenance_wrong_digest_and_duplicates_rejected(self):
        for digest in ("", "f" * 64):
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                artifact.decode_manifest(self.raw, digest, self.provenance)
        with self.assertRaises(ValueError):
            self.malformed(lambda m: m.pop("provenance"))
        with self.assertRaises(ValueError):
            self.malformed(lambda m: m["provenance"].update(source_sha="c" * 40))
        duplicate = self.raw[:-2] + b',"schema":1}'
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            artifact.decode_manifest(duplicate, hashlib.sha256(duplicate).hexdigest(), self.provenance)

    def test_malformed_manifests_fail_closed(self):
        changes = [
            lambda m: m.update(schema=True),
            lambda m: m.update(extra="unrecognized"),
            lambda m: m.update(files=[]),
            lambda m: m["files"]["index.html"].update(size=True),
            lambda m: m["files"]["index.html"].update(size=-1),
            lambda m: m["files"]["index.html"].update(size=artifact.MAX_FILE + 1),
            lambda m: m["files"]["index.html"].update(sha256="not a hash"),
            lambda m: m["files"].update({"../escape": m["files"]["index.html"]}),
            lambda m: m["files"].update({"parent": m["files"]["index.html"], "parent/child": m["files"]["index.html"]}),
            lambda m: m["files"].pop(artifact.INSTALL),
            lambda m: m.update(downloads=[]),
            lambda m: m.update(downloads=[self.downloads[0], self.downloads[0]]),
            lambda m: m.update(downloads=["download/cawemo-1.9.42.tar.gz", self.downloads[1]]),
            lambda m: m.update(assets=[]),
            lambda m: m["files"][self.assets[0]].update(sha256="0" * 64),
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.malformed(change)

    def test_manifest_and_tree_resource_bounds(self):
        for name, maximum in (("MAX_MANIFEST", 1), ("MAX_FILES", 1), ("MAX_TOTAL", 1)):
            with self.subTest(name=name), patch.object(artifact, name, maximum), self.assertRaises(ValueError):
                artifact.decode_manifest(self.raw, self.manifest_digest, self.provenance)
        (self.tree / "extra").write_bytes(b"not in build")
        with self.assertRaises(ValueError):
            artifact.verify_tree(self.tree, self.manifest, self.raw)

    def test_build_cannot_prepopulate_its_own_manifest(self):
        with self.assertRaisesRegex(ValueError, "own provenance"):
            artifact.create_manifest(self.tree, self.source, self.provenance)


class FakeHTTPS:
    def __init__(self, fixture, phase="stage"):
        self.host, self.destination = publish.HOSTS[phase], "aws"
        self.responses = {}
        self.requests = []
        self.responses[artifact.PREFIX + artifact.MANIFEST] = (200, {"content-type": "application/json"}, fixture.raw)
        for name in fixture.manifest["files"]:
            path = artifact.PREFIX + (name[:-10] if name.endswith("index.html") else name)
            mime = "text/html"
            if name.endswith(".css"):
                mime = "text/css"
            elif name.endswith(".js"):
                mime = "text/javascript"
            elif name.endswith((".zip", ".gz")):
                mime = "application/octet-stream"
            self.responses[path] = (200, {"content-type": mime}, (fixture.tree / name).read_bytes())
        install_path = artifact.PREFIX + "technical-guide/installation/"
        for path, status, target in (
                ("/cawemo/", 301, artifact.PREFIX),
                ("/cawemo/technical-guide/installation/", 307, install_path),
                ("/cawemo/99.0/technical-guide/installation/", 307, install_path)):
            self.responses[path] = (status, {"location": target}, b"")

    def get(self, path, limit=artifact.MAX_FILE):
        self.requests.append(path)
        response = self.responses[path]
        if len(response[2]) > limit:
            raise ValueError("Response bound exceeded")
        return response


class HTTPTests(Fixture):
    def test_full_product_gate_checks_every_expected_file_and_redirects(self):
        client = FakeHTTPS(self)
        self.assertEqual(publish.check(client, self.env, self.tree), self.manifest)
        self.assertTrue(all(artifact.PREFIX + name in client.requests for name in self.downloads + self.assets))
        self.assertIn("/cawemo/99.0/technical-guide/installation/", client.requests)

    def test_download_redirect_or_html_fallback_is_not_a_pass(self):
        path = artifact.PREFIX + self.downloads[0]
        for response in (
                (307, {"location": artifact.PREFIX}, b""),
                (200, {"content-type": "text/html"}, b"<html>version root</html>"),
                (404, {"content-type": "application/octet-stream"}, b"missing"),
                (200, {"content-type": "application/octet-stream", "location": artifact.PREFIX}, b"other")):
            client = FakeHTTPS(self)
            client.responses[path] = response
            with self.subTest(response=response), self.assertRaises(ValueError):
                publish.check(client, self.env)

    def test_direct_digest_and_length_mismatch_fail(self):
        entry = self.manifest["files"][self.downloads[0]]
        for data in (b"x", b"x" * entry["size"]):
            with self.subTest(size=len(data)), self.assertRaises(ValueError):
                publish.direct((200, {"content-type": "application/zip"}, data), self.downloads[0], entry)

    def test_wrong_content_types_for_html_css_js_json_fail_even_with_exact_bytes(self):
        for name, data in [(artifact.MANIFEST, self.raw), *[(name, (self.tree / name).read_bytes()) for name in [artifact.INSTALL, *self.assets]]]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                publish.direct((200, {"content-type": "text/plain"}, data), name)

    def test_exact_installation_and_fingerprinted_assets_are_required(self):
        for name in [artifact.INSTALL, *self.assets]:
            client = FakeHTTPS(self)
            path = artifact.PREFIX + (name[:-10] if name == artifact.INSTALL else name)
            status, headers, data = client.responses[path]
            client.responses[path] = (status, headers, data[:-1] + b"x")
            with self.subTest(name=name), self.assertRaises(ValueError):
                publish.check(client, self.env)

    def test_remote_installation_link_contract_not_just_self_consistent_hashes(self):
        client = FakeHTTPS(self)
        path = artifact.PREFIX + "technical-guide/installation/"
        status, headers, _ = client.responses[path]
        bad_html = b'<!doctype html><html><a href="/cawemo/1.9/">wrong installation</a></html>'
        manifest = copy.deepcopy(self.manifest)
        manifest["files"][artifact.INSTALL] = {"sha256": hashlib.sha256(bad_html).hexdigest(), "size": len(bad_html)}
        raw = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
        client.responses[artifact.PREFIX + artifact.MANIFEST] = (200, {"content-type": "application/json"}, raw)
        client.responses[path] = (status, headers, bad_html)
        env = dict(self.env, MANIFEST_SHA256=hashlib.sha256(raw).hexdigest())
        with self.assertRaisesRegex(ValueError, "installation links"):
            publish.check(client, env)

    def test_redirect_status_host_scheme_suffix_query_fragment_are_strict(self):
        path = "/cawemo/technical-guide/installation/"
        target = artifact.PREFIX + "technical-guide/installation/"
        for status, location in [
                (302, target), (307, artifact.PREFIX), (307, "/cawemo/1.8/technical-guide/installation/"),
                (307, "https://evil.invalid" + target), (307, "http://stage.docs.camunda.org" + target),
                (307, target + "?x=1"), (307, target + "#other"),
                (307, "https://user@stage.docs.camunda.org" + target), (307, "")]:
            client = FakeHTTPS(self)
            client.responses[path] = (status, {"location": location}, b"")
            with self.subTest(status=status, location=location), self.assertRaises(ValueError):
                publish.check(client, self.env)

    def test_manifest_cannot_supply_its_own_trust(self):
        client = FakeHTTPS(self)
        client.responses[artifact.PREFIX + artifact.MANIFEST] = (
            200, {"content-type": "application/json"}, self.raw.replace(b"a" * 40, b"c" * 40))
        with self.assertRaises(ValueError):
            publish.check(client, self.env)

    def test_canonical_tls_aws_only_resolve_and_no_unsafe_curl_options(self):
        for destination, ip in (("aws", "192.0.2.42"), ("aws", "2001:db8::42"), ("legacy", "")):
            with self.subTest(destination=destination, ip=ip):
                client = publish.HTTPS(destination, "stage", ip, self.work / ("http-" + destination + str(len(ip))))
                command = client.command(artifact.PREFIX, 123)
                self.assertEqual(command[:2], ["curl", "--disable"])
                self.assertEqual(command[-1], "https://stage.docs.camunda.org/cawemo/1.9/")
                self.assertNotIn("--location", command)
                self.assertNotIn("-L", command)
                self.assertNotIn("-k", command)
                self.assertNotIn("--insecure", command)
                self.assertIn("--noproxy", command)
                self.assertIn("--proxy", command)
                self.assertEqual(command[command.index("--proxy") + 1], "")
                self.assertIn("=https", command)
                if destination == "aws":
                    address = f"[{ip}]" if ":" in ip else ip
                    self.assertEqual(command[command.index("--resolve") + 1], f"stage.docs.camunda.org:443:{address}")
                else:
                    self.assertNotIn("--resolve", command)

    def test_missing_or_malformed_aws_route_never_falls_back_to_dns(self):
        for route in ("", "not-an-ip", "192.0.2.1:443", "fe80::1%eth0", "192.0.2.1\n--insecure"):
            with self.subTest(route=route), self.assertRaises(ValueError):
                publish.HTTPS("aws", "stage", route, self.work / "invalid-http")
        self.assertFalse((self.work / "invalid-http").exists())

    def test_curl_errors_and_ambiguous_headers_fail_closed(self):
        client = publish.HTTPS("aws", "stage", "192.0.2.42", self.work / "http")
        client.version_checked = True
        bad_headers = (
            "HTTP/2 200\nlocation: /one\nLocation: /two\n\n",
            "HTTP/2 200\ncontent-type: text/html\nContent-Type: text/html\n\n",
            "HTTP/2 200\ncontent-length: 100\n\n",
            "HTTP/2 200\ncontent-length: x\n\n",
            "HTTP/2 200\n folded header: bad\n\n",
            "HTTP/2 100\n\nHTTP/2 200\n\n",
            "garbage\n\n",
        )
        for headers in bad_headers:
            (client.workdir / "headers").write_text(headers)
            (client.workdir / "body").write_bytes(b"html")
            with self.subTest(headers=headers), patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout="200")), self.assertRaises(ValueError):
                client.get(artifact.PREFIX)
        with patch.object(publish.subprocess, "run", return_value=Mock(returncode=60, stdout="000")), self.assertRaises(ValueError):
            client.get(artifact.PREFIX)
        with patch.object(publish.subprocess, "run", side_effect=subprocess.TimeoutExpired("curl", 40)), self.assertRaises(subprocess.TimeoutExpired):
            client.get(artifact.PREFIX)

    def test_http_body_and_header_resource_bounds(self):
        client = publish.HTTPS("aws", "stage", "192.0.2.42", self.work / "http")
        client.version_checked = True
        (client.workdir / "headers").write_text("HTTP/2 200\n\n")
        (client.workdir / "body").write_bytes(b"too long")
        with patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout="200")), self.assertRaises(ValueError):
            client.get(artifact.PREFIX, 1)
        (client.workdir / "headers").write_bytes(b"x" * 65537)
        with patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout="200")), self.assertRaises(ValueError):
            client.get(artifact.PREFIX)

    def test_valid_curl_response_parser_and_invalid_paths(self):
        client = publish.HTTPS("aws", "stage", "192.0.2.42", self.work / "http")
        client.version_checked = True
        (client.workdir / "headers").write_text("HTTP/2 200\ncontent-type: text/html\ncontent-length: 4\n\n")
        (client.workdir / "body").write_bytes(b"html")
        with patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout="200")):
            self.assertEqual(client.get(artifact.PREFIX), (200, {"content-type": "text/html", "content-length": "4"}, b"html"))
        for path in ("//evil.invalid", "https://evil.invalid", "/a?query", "/a#fragment", "/a\\b", "/a\nb"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                client.command(path, 100)

    def test_old_or_malformed_curl_fails_before_any_network_request(self):
        client = publish.HTTPS("aws", "stage", "192.0.2.42", self.work / "http")
        for version in ("curl 8.3.0 old", "curl 7.88.1 old", "", "unrecognized tool"):
            with self.subTest(version=version), patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout=version)) as run, self.assertRaisesRegex(ValueError, "streaming"):
                client.get(artifact.PREFIX)
            self.assertEqual(run.call_args.args[0], ["curl", "--disable", "--version"])
            self.assertEqual(run.call_count, 1)
            self.assertFalse(client.version_checked)

    def test_supported_curl_version_is_checked_once(self):
        client = publish.HTTPS("aws", "stage", "192.0.2.42", self.work / "http")
        with patch.object(publish.subprocess, "run", return_value=Mock(returncode=0, stdout="curl 8.4.0 (offline)")) as run:
            client.check_curl_version()
            client.check_curl_version()
        self.assertEqual(run.call_count, 1)
        self.assertTrue(client.version_checked)


class TransferTests(Fixture):
    def test_real_stage_and_live_require_exact_activation_before_any_remote_work(self):
        for phase in ("stage", "live"):
            for enabled in (None, "", "false", "True", "true ", "1"):
                env = dict(self.env)
                if enabled is None:
                    env.pop("NATIVE_ENABLED")
                else:
                    env["NATIVE_ENABLED"] = enabled
                with self.subTest(phase=phase, enabled=enabled), \
                        patch.object(publish, "config") as config, \
                        patch.object(publish, "ssh_files") as ssh_files, \
                        patch.object(publish, "check") as check, \
                        patch.object(publish, "remote_call") as remote_call, \
                        patch.object(publish.subprocess, "run") as run:
                    with self.assertRaisesRegex(ValueError, "disabled until authorized"):
                        publish.transfer(env, phase, self.tree, self.work / "ssh", Mock())
                    for operation in (config, ssh_files, check, remote_call, run):
                        operation.assert_not_called()

    def test_dry_run_remains_available_without_activation(self):
        env = dict(self.env, DRY_RUN="true")
        env.pop("NATIVE_ENABLED")
        for phase in ("stage", "live"):
            with self.subTest(phase=phase):
                publish.request_inputs(env, phase)

    def test_explicit_activation_preserves_provenance_and_confirmation_requirements(self):
        for phase in ("stage", "live"):
            with self.subTest(phase=phase):
                publish.request_inputs(self.env, phase)
                with self.assertRaises(ValueError):
                    publish.request_inputs(dict(self.env, MANIFEST_SHA256=""), phase)
        with self.assertRaises(ValueError):
            publish.request_inputs(dict(self.env, CONFIRM_LIVE_PROMOTE=""), "live")

    def test_version_dry_run_confirmation_and_provenance_fail_closed(self):
        changes = [{"VERSION": "1.8"}, {"DRY_RUN": ""}, {"DRY_RUN": "False"},
                   {"CONFIRM_LIVE_PROMOTE": publish.CONFIRM + " "}, {"SOURCE_SHA": ""},
                   {"TOOLING_SHA": ""}, {"STAGE_RUN_ID": "0"}, {"MANIFEST_SHA256": ""}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                publish.request_inputs(dict(self.env, **change), "live")

    def test_missing_job_local_vault_values_fail_explicitly(self):
        for key in ("DOCS_SSH_USER", "DOCS_SSH_PRIVATE_KEY", "DOCS_SSH_KNOWN_HOSTS",
                    "DOCS_STAGE_ROOT", "DOCS_LIVE_ROOT", "DOCS_AWS_SSH_HOST", "DOCS_AWS_SMOKE_RESOLVE"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                publish.config(dict(self.env, **{key: ""}))

    def test_ssh_user_host_and_root_injections_rejected(self):
        for changes in (
                {"DOCS_SSH_USER": "root"}, {"DOCS_SSH_USER": "-oProxyCommand=x"},
                {"DOCS_SSH_USER": "docs;id"}, {"DOCS_AWS_SSH_HOST": "other.invalid"},
                {"DESTINATION": "legacy", "DOCS_SSH_HOST": "host --option"},
                {"DESTINATION": "legacy", "DOCS_SSH_HOST": "host:22"},
                {"DESTINATION": "legacy", "DOCS_SSH_HOST": "$(id)"},
                {"DESTINATION": "legacy", "DOCS_SSH_HOST": "-host"},
                {"DESTINATION": "other"}, {"DOCS_STAGE_ROOT": "/"},
                {"DOCS_STAGE_ROOT": "/var//docs"}, {"DOCS_STAGE_ROOT": "/var/../docs"},
                {"DOCS_STAGE_ROOT": "/var/docs/."}, {"DOCS_STAGE_ROOT": "/var/docs;id"},
                {"DOCS_STAGE_ROOT": "/var/docs with spaces"}, {"DOCS_STAGE_ROOT": "/var/docs'quote"},
                {"DOCS_STAGE_ROOT": self.env["DOCS_LIVE_ROOT"]},
                {"DOCS_STAGE_ROOT": self.env["DOCS_LIVE_ROOT"] + "/nested"},
                {"DOCS_LIVE_ROOT": self.env["DOCS_STAGE_ROOT"] + "/nested"},
                {"DOCS_STAGE_ROOT": "/var/docs/cawemo/1.9"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                publish.config(dict(self.env, **changes))

    def test_dry_runs_never_create_ssh_files_connect_or_make_remote_directories(self):
        for phase in ("stage", "live"):
            with self.subTest(phase=phase), patch.object(publish.subprocess, "run", side_effect=AssertionError("remote command")), patch.object(publish, "ssh_files", side_effect=AssertionError("SSH files")):
                publish.transfer(dict(self.env, DRY_RUN="true"), phase, self.tree, self.work / "ssh", Mock())
            self.assertFalse((self.work / "ssh").exists())
            self.assertFalse(Path(self.env["DOCS_STAGE_ROOT"]).exists())
            self.assertFalse(Path(self.env["DOCS_LIVE_ROOT"]).exists())

    def test_ssh_uses_only_strict_pinned_known_hosts_without_tofu_or_config(self):
        directory = self.work / "ssh"
        options = publish.ssh_files(directory, self.env)
        self.assertIn("StrictHostKeyChecking=yes", options)
        self.assertIn("GlobalKnownHostsFile=/dev/null", options)
        self.assertIn("BatchMode=yes", options)
        self.assertIn("ProxyCommand=none", options)
        self.assertIn("ProxyJump=none", options)
        self.assertEqual(options[options.index("-F") + 1], "/dev/null")
        self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((directory / "key").stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE((directory / "known_hosts").stat().st_mode), 0o600)

    def test_stage_transfer_commands_are_non_deleting_and_scoped(self):
        with patch.object(publish, "remote_call") as remote_call, patch.object(publish.subprocess, "run") as run:
            publish.transfer(self.env, "stage", self.tree, self.work / "ssh")
        self.assertEqual([call.args[2] for call in remote_call.call_args_list], ["prepare-stage", "verify-stage"])
        command = run.call_args.args[0]
        self.assertEqual(command[0], "rsync")
        self.assertEqual(command[-1], "docs@webserver-docs.camunda-it.rocks:" + self.env["DOCS_STAGE_ROOT"] + "/cawemo/1.9/")
        self.assertFalse(any("delete" in option for option in command))
        self.assertNotIn("-a", command)
        self.assertFalse((self.work / "ssh").exists())

    def test_real_promotion_revalidates_stage_and_stays_on_one_host(self):
        client = FakeHTTPS(self)
        with patch.object(publish, "remote_call") as remote_call, patch.object(publish.subprocess, "run") as run:
            publish.transfer(self.env, "live", self.tree, self.work / "ssh", client)
        self.assertEqual(remote_call.call_args.args[1:3], ("docs@webserver-docs.camunda-it.rocks", "promote"))
        self.assertTrue(client.requests)
        run.assert_not_called()

    def test_promotion_wrong_destination_or_stage_hash_blocks_all_ssh(self):
        for corrupt in (False, True):
            client = FakeHTTPS(self)
            if corrupt:
                client.responses[artifact.PREFIX + self.downloads[0]] = (200, {"content-type": "application/octet-stream"}, b"wrong")
            else:
                client.destination = "legacy"
            with self.subTest(corrupt=corrupt), patch.object(publish, "ssh_files") as ssh, self.assertRaises(ValueError):
                publish.transfer(self.env, "live", self.tree, self.work / "ssh", client)
            ssh.assert_not_called()

    def test_missing_rsync_and_real_rsync_failure_have_no_fallback(self):
        with patch.object(publish.shutil, "which", side_effect=lambda name: None if name == "rsync" else "/usr/bin/ssh"), self.assertRaisesRegex(ValueError, "rsync"):
            publish.transfer(self.env, "stage", self.tree, self.work / "ssh")
        with patch.object(publish, "remote_call"), patch.object(publish.subprocess, "run", side_effect=subprocess.CalledProcessError(23, "rsync")), self.assertRaises(subprocess.CalledProcessError):
            publish.transfer(self.env, "stage", self.tree, self.work / "ssh")
        self.assertFalse((self.work / "ssh").exists())

    def test_remote_payload_is_trusted_code_with_quoted_fixed_scope_arguments(self):
        with patch.object(publish.subprocess, "run") as run:
            publish.remote_call(["ssh", "-F", "/dev/null"], "docs@approved.invalid", "promote", self.env, self.manifest)
        self.assertEqual(run.call_args.args[0][-2], "docs@approved.invalid")
        payload = run.call_args.kwargs["input"]
        self.assertTrue(payload.startswith("EXPECTED = "))
        self.assertIn('SCOPE = "cawemo/1.9"', payload)
        self.assertNotIn("extractall", payload)

    def rsync_stub(self):
        directory = self.work / "bin"
        directory.mkdir()
        executable = directory / "rsync"
        executable.write_text(
            f"#!{sys.executable}\n"
            "import pathlib, shutil, sys\n"
            "args = sys.argv[1:]\n"
            "assert not any('delete' in arg for arg in args)\n"
            "assert args[-3] == '--'\n"
            "source = pathlib.Path(args[-2])\n"
            "target_name = args[-1]\n"
            "if ':' in target_name:\n"
            "    host, target_name = target_name.split(':', 1)\n"
            "    assert host == 'docs@webserver-docs.camunda-it.rocks'\n"
            "target = pathlib.Path(target_name)\n"
            "assert str(target).endswith('/cawemo/1.9')\n"
            "if '--files-from=-' in args:\n"
            "    assert str(source).endswith('/cawemo/1.9') and '--from0' in args\n"
            "    for name in sys.stdin.read().split('\\0'):\n"
            "        if name:\n"
            "            dest = target / name\n"
            "            dest.parent.mkdir(parents=True, exist_ok=True)\n"
            "            shutil.copyfile(source / name, dest)\n"
            "else:\n"
            "    assert source.name == 'public'\n"
            "    shutil.copytree(source, target, dirs_exist_ok=True)\n")
        executable.chmod(0o755)
        return str(directory) + os.pathsep + os.environ.get("PATH", "")

    def remote_roots(self):
        stage, live = Path(self.env["DOCS_STAGE_ROOT"]), Path(self.env["DOCS_LIVE_ROOT"])
        stage.mkdir()
        live.mkdir()
        return stage, live

    def test_non_deleting_stage_and_same_host_promotion_retain_old_downloads_and_other_versions(self):
        stage, live = self.remote_roots()
        remote.execute("prepare-stage", str(stage), str(live), self.manifest)
        stage_scope, live_scope = stage / artifact.SCOPE, live / artifact.SCOPE
        for root in (stage, live):
            old = root / artifact.SCOPE / "download/cawemo-1.9.42.zip"
            old.parent.mkdir(parents=True, exist_ok=True)
            old.write_bytes(b"older Stage release" if root == stage else b"older Live release must remain")
            other = root / "cawemo/1.8/index.html"
            other.parent.mkdir(parents=True)
            other.write_bytes(b"other maintenance version")
        live_extra = live_scope / "download/cawemo-1.9.41.tar.gz"
        live_extra.write_bytes(b"live-only older release")
        def local_remote_call(ssh, target, operation, env, manifest):
            self.assertEqual(target, "docs@webserver-docs.camunda-it.rocks")
            remote.execute(operation, env["DOCS_STAGE_ROOT"], env["DOCS_LIVE_ROOT"], manifest)
        with patch.dict(os.environ, {"PATH": self.rsync_stub()}), patch.object(publish, "remote_call", side_effect=local_remote_call):
            publish.transfer(self.env, "stage", self.tree, self.work / "ssh")
        self.assertEqual((stage_scope / "download/cawemo-1.9.42.zip").read_bytes(), b"older Stage release")
        remote.execute("verify-stage", str(stage), str(live), self.manifest)
        with patch.dict(os.environ, {"PATH": str(self.work / "bin") + os.pathsep + os.environ.get("PATH", "")}):
            remote.execute("promote", str(stage), str(live), self.manifest)
        for root in (stage, live):
            self.assertEqual((root / artifact.SCOPE / "download/cawemo-1.9.42.zip").read_bytes(),
                             b"older Stage release" if root == stage else b"older Live release must remain")
            self.assertEqual((root / "cawemo/1.8/index.html").read_bytes(), b"other maintenance version")
        self.assertEqual(live_extra.read_bytes(), b"live-only older release")
        remote.verify(live_scope, self.manifest)

    def test_remote_corruption_blocks_promotion_before_live_scope_creation(self):
        stage, live = self.remote_roots()
        scope = stage / artifact.SCOPE
        shutil.copytree(self.tree, scope)
        (scope / self.downloads[0]).write_bytes(b"bad source")
        with patch.object(remote.subprocess, "run") as run, self.assertRaises(ValueError):
            remote.execute("promote", str(stage), str(live), self.manifest)
        run.assert_not_called()
        self.assertFalse((live / artifact.SCOPE).exists())

    def test_remote_expected_file_parents_fail_before_writes(self):
        stage, live = self.remote_roots()
        scope = stage / artifact.SCOPE
        scope.mkdir(parents=True)
        (scope / "technical-guide").write_bytes(b"file instead of directory")
        with self.assertRaises(ValueError):
            remote.execute("prepare-stage", str(stage), str(live), self.manifest)
        self.assertEqual((scope / "technical-guide").read_bytes(), b"file instead of directory")
        self.assertFalse((scope / artifact.MANIFEST).exists())

    def test_remote_symlink_parent_and_scope_links_are_rejected(self):
        stage, live = self.remote_roots()
        (stage / "cawemo").symlink_to(live, target_is_directory=True)
        with self.assertRaises(ValueError):
            remote.execute("prepare-stage", str(stage), str(live), self.manifest)
        (stage / "cawemo").unlink()
        shutil.copytree(self.tree, stage / artifact.SCOPE)
        (stage / artifact.SCOPE / "extra-link").symlink_to(live, target_is_directory=True)
        with self.assertRaises(ValueError):
            remote.execute("promote", str(stage), str(live), self.manifest)
        self.assertFalse((live / artifact.SCOPE).exists())

    def test_remote_extras_are_bounded_and_not_an_expected_manifest_failure(self):
        stage, live = self.remote_roots()
        shutil.copytree(self.tree, stage / artifact.SCOPE)
        (stage / artifact.SCOPE / "old-file").write_bytes(b"retained")
        remote.execute("verify-stage", str(stage), str(live), self.manifest)
        with patch.object(remote, "MAX_ENTRIES", 1), self.assertRaises(ValueError):
            remote.execute("verify-stage", str(stage), str(live), self.manifest)
        with patch.object(remote, "MAX_TOTAL", 1), self.assertRaises(ValueError):
            remote.execute("verify-stage", str(stage), str(live), self.manifest)


class ResultTests(unittest.TestCase):
    def expected(self, phase, dry):
        results = {"validate": "success", "publish": "success",
                   "pre-product": "skipped", "pre-global": "skipped",
                   "post-product": "skipped", "post-global": "skipped"}
        if not dry:
            results.update({"post-product": "success", "post-global": "success"})
            if phase == "live":
                results.update({"pre-product": "success", "pre-global": "success"})
        return results

    def test_real_product_and_global_gates_fail_independently(self):
        for phase in ("stage", "live"):
            expected = self.expected(phase, False)
            self.assertTrue(result.destination_result(phase, "false", expected))
            for key, value in expected.items():
                for bad in ("failure", "cancelled", "skipped", "success"):
                    if bad != value:
                        changed = dict(expected, **{key: bad})
                        with self.subTest(phase=phase, key=key, bad=bad):
                            self.assertFalse(result.destination_result(phase, "false", changed))

    def test_dry_run_requires_explicit_skipped_real_gates_not_smoke_pass(self):
        for phase in ("stage", "live"):
            expected = self.expected(phase, True)
            self.assertTrue(result.destination_result(phase, "true", expected))
            self.assertFalse(result.destination_result(phase, "true", dict(expected, **{"post-product": "success"})))

    def test_aggregate_never_hides_failed_skipped_cancelled_or_missing_destinations(self):
        self.assertTrue(result.aggregate({"legacy": "success", "aws": "success"}))
        self.assertFalse(result.aggregate({}))
        for failed in ("failure", "skipped", "cancelled", ""):
            self.assertFalse(result.aggregate({"legacy": "success", "aws": failed}))


class WiringTests(unittest.TestCase):
    def test_activation_is_repository_controlled_at_every_entrypoint_and_destination(self):
        for name in ("stage", "promote", "publish"):
            text = (ROOT / f".github/workflows/docs-cawemo-{name}.yml").read_text()
            self.assertIn("NATIVE_ENABLED: ${{ vars.DOCS_CAWEMO_NATIVE_ENABLED }}", text)
            self.assertNotIn("inputs.NATIVE_ENABLED", text)
            self.assertNotIn("inputs['NATIVE_ENABLED']", text)

    def test_stage_activation_guard_runs_before_destination_resolution(self):
        text = (ROOT / ".github/workflows/docs-cawemo-stage.yml").read_text()
        validation = text.split("      - name: Validate manual-only request\n", 1)[1].split("\n      - name:", 1)[0]
        script = textwrap.dedent(validation.split("        run: |\n", 1)[1])
        for dry, enabled, event, version, success in (
                ("false", "", "workflow_dispatch", "1.9", False),
                ("false", "false", "workflow_dispatch", "1.9", False),
                ("false", "True", "workflow_dispatch", "1.9", False),
                ("false", "true", "workflow_dispatch", "1.9", True),
                ("true", "", "workflow_dispatch", "1.9", True),
                ("false", "true", "push", "1.9", False),
                ("false", "true", "workflow_dispatch", "1.8", False)):
            with self.subTest(dry=dry, enabled=enabled, event=event, version=version):
                completed = subprocess.run(
                    ["bash", "-c", script], capture_output=True, text=True, timeout=5,
                    env={"PATH": os.environ["PATH"], "EVENT": event, "VERSION": version,
                         "DRY_RUN": dry, "NATIVE_ENABLED": enabled})
                self.assertEqual(completed.returncode == 0, success, completed.stderr)
        self.assertLess(text.index('"$NATIVE_ENABLED" != true'),
                        text.index("      - name: Resolve destinations"))

    def test_only_dispatch_entrypoints_share_whole_run_queue_and_numeric_independent_matrix(self):
        for name in ("stage", "promote"):
            text = (ROOT / f".github/workflows/docs-cawemo-{name}.yml").read_text()
            self.assertIn("workflow_dispatch:", text)
            self.assertNotIn("  push:", text)
            self.assertNotIn("  schedule:", text)
            self.assertIn("group: docs-cawemo\n  queue: max\n  cancel-in-progress: false", text)
            self.assertIn("fail-fast: false", text)
            self.assertIn("fromJSON", text)
            self.assertIn('fromJSON(\'["legacy","aws"]\')[matrix.target]', text)
            self.assertIn("default: true", text)
            self.assertIn("options: ['1.9']", text)
            self.assertIn("resolve-static-destinations@7a717518ad8f395ab4cc81dfdc65da4b7f2e2f03", text)
            self.assertIn("if: always()", text)

    def test_product_and_global_jobs_are_independent_and_required(self):
        text = (ROOT / ".github/workflows/docs-cawemo-publish.yml").read_text()
        self.assertIn("needs: [validate, pre-product, pre-global]", text)
        self.assertIn("needs: [validate, pre-product, pre-global, publish, post-product, post-global]", text)
        self.assertEqual(text.count("needs: publish"), 2)
        self.assertEqual(text.count("needs: validate"), 2)
        self.assertEqual(text.count("camunda-docs-smoke-test.yml@7a717518ad8f395ab4cc81dfdc65da4b7f2e2f03"), 2)
        self.assertNotIn("continue-on-error", text)
        self.assertNotIn("docs-rsync@", text)
        self.assertIn("--phase stage", text)
        self.assertIn("needs.pre-product.result == 'success' && needs.pre-global.result == 'success'", text)

    def test_source_and_workflow_tooling_remain_separate_and_archive_trust_is_build_output(self):
        text = (ROOT / ".github/workflows/docs-cawemo-stage.yml").read_text()
        self.assertIn("ref: ${{ github.sha }}\n          path: .workflow", text)
        self.assertIn("ref: ${{ needs.resolve.outputs.source-sha }}\n          path: cawemo-source", text)
        self.assertIn("archive-sha256: ${{ needs.build.outputs.archive-sha256 }}", text)
        self.assertIn("docs-hugo-build@689027f45f5e565999c9b2e0c4294a18669c4a66", text)
        self.assertIn("docs-link-checker@cccb09bbc59bed8fdf5ef7122be148fb57a70c8e", text)
        self.assertIn("ignore-regex: ^/(optimize|manual|cawemo|security|get-started|enterprise)", text)
        promote = (ROOT / ".github/workflows/docs-cawemo-promote.yml").read_text()
        self.assertNotIn("docs-hugo-build", promote)
        self.assertIn("manifest-sha256", promote)

    def test_pr_checks_cover_1_9_without_privileged_trigger_or_vault(self):
        text = (ROOT / ".github/workflows/docs-cawemo-checks.yml").read_text()
        self.assertIn("pull_request:\n    branches: ['1.9']", text)
        for forbidden in ("pull_request_target", "id-token:", "contents: write", "secrets.", "vault-action", "workflow_dispatch"):
            self.assertNotIn(forbidden, text)
        self.assertIn("docs-hugo-build@689027f45f5e565999c9b2e0c4294a18669c4a66", text)


if __name__ == "__main__":
    unittest.main()
