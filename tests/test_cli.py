"""Tests for JEP CLI against JEP Core 0.7."""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from jep_cli.main import main, parse_json_value, parse_ext_items


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True, "profile": "jep-core-0.7"})
        else:
            self._json(404, {"message": "not found"})

    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/v0.7/events/create":
            event = {
                "jep": "1",
                "id": payload.get("id", "urn:uuid:00000000-0000-7000-8000-000000000001"),
                "verb": payload["verb"],
                "who": payload.get("who", "did:example:agent"),
                "when": 1234567890,
                "what": payload["what"],
                "sig": "header..sig",
            }
            for key in ("aud", "ref", "ext", "ext_crit"):
                if payload.get(key) is not None:
                    event[key] = payload[key]
            self._json(200, {
                "event": event,
                "event_hash": "sha256:abc",
                "validation": {
                    "status": "valid",
                    "mode": "archival",
                    "profile": "jep-core-0.7",
                    "event_identity": {"who": event["who"], "id": event["id"]},
                    "checks": {"syntax": "pass", "cryptographic": "pass", "event_identity": "pass"},
                    "event_hash": "sha256:abc",
                    "warnings": [],
                    "errors": [],
                }
            })
            return
        if self.path == "/v0.7/events/verify":
            self._json(200, {
                "status": "valid",
                "mode": payload.get("mode", "archival"),
                "profile": "jep-core-0.7",
                "event_identity": {"who": payload["event"]["who"], "id": payload["event"]["id"]},
                "checks": {"syntax": "pass", "cryptographic": "pass", "event_identity": "pass"},
                "event_hash": "sha256:def",
                "warnings": [],
                "errors": [],
            })
            return
        if self.path == "/events/verify-legacy":
            self._json(200, {"valid": True, "level": 1, "profile": "jep-core-0.6"})
            return
        self._json(404, {"message": "not found"})

    def log_message(self, *args):
        pass


@pytest.fixture()
def api_server():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()


def test_parse_json_value_string_and_json(tmp_path):
    assert parse_json_value('{"a":1}') == {"a": 1}
    assert parse_json_value("plain") == "plain"
    f = tmp_path / "data.json"
    f.write_text('{"b":2}')
    assert parse_json_value(str(f)) == {"b": 2}


def test_parse_ext_items():
    ext = parse_ext_items(['https://example.org/x={"a":1}', 'https://example.org/y=plain'])
    assert ext["https://example.org/x"] == {"a": 1}
    assert ext["https://example.org/y"] == "plain"


def test_health(api_server, capsys):
    code = main(["--base-url", api_server, "health"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["profile"] == "jep-core-0.7"


def test_create_v07(api_server, capsys):
    code = main([
        "--base-url", api_server, "create",
        "--verb", "J",
        "--who", "did:example:agent",
        "--what", '{"claim":"approve"}',
    ])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["event"]["id"]
    assert out["validation"]["status"] == "valid"


def test_verify_v07(api_server, capsys, tmp_path):
    event = {
        "jep": "1",
        "id": "urn:uuid:00000000-0000-7000-8000-000000000001",
        "verb": "J",
        "who": "did:example:agent",
        "when": 123,
        "what": {"claim": "approve"},
        "sig": "header..sig",
    }
    p = tmp_path / "event.json"
    p.write_text(json.dumps(event))
    code = main(["--base-url", api_server, "verify", str(p)])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["status"] == "valid"
    assert out["checks"]["event_identity"] == "pass"


def test_explicit_legacy_verify(api_server, capsys, tmp_path):
    p = tmp_path / "legacy.json"
    p.write_text(json.dumps({"jep": "1", "nonce": "legacy"}))
    code = main(["--base-url", api_server, "verify-legacy", str(p)])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["profile"] == "jep-core-0.6"


def test_extract_event(capsys, tmp_path):
    p = tmp_path / "response.json"
    p.write_text(json.dumps({"event": {"jep": "1", "id": "urn:uuid:x", "verb": "J"}}))
    code = main(["extract-event", str(p)])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["verb"] == "J"


def test_invalid_verb(capsys):
    code = main(["create", "--verb", "X", "--what", "x"])
    assert code != 0
