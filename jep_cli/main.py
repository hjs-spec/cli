"""JEP CLI v0.6 command line interface."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from .client import JEPClient, JEPCLIError


VALID_VERBS = {"J", "D", "T", "V"}


def parse_json_value(value: str) -> Any:
    if value == "-":
        return json.load(sys.stdin)

    path = Path(value)
    if path.exists() and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def parse_ext_items(items: list[str]) -> Dict[str, Any]:
    ext: Dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"extension must be key=json_or_string, got: {item}")
        key, raw = item.split("=", 1)
        ext[key] = parse_json_value(raw)
    return ext


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def build_client(args: argparse.Namespace) -> JEPClient:
    base_url = args.base_url or os.environ.get("JEP_API_URL", "http://127.0.0.1:8000")
    api_key = args.api_key or os.environ.get("JEP_API_KEY", "")
    return JEPClient(base_url=base_url, api_key=api_key, timeout=args.timeout)


def cmd_create(args: argparse.Namespace) -> int:
    if args.verb not in VALID_VERBS:
        raise ValueError("verb must be J, D, T, or V")

    payload: Dict[str, Any] = {
        "verb": args.verb,
        "what": parse_json_value(args.what),
    }
    if args.who:
        payload["who"] = args.who
    if args.aud:
        payload["aud"] = args.aud
    if args.ref:
        payload["ref"] = args.ref
    if args.ttl_minutes is not None:
        payload["ttl_minutes"] = args.ttl_minutes
    if args.digest_only_who:
        payload["digest_only_who"] = True
    if args.ext:
        payload["ext"] = parse_ext_items(args.ext)
    if args.ext_crit:
        payload["ext_crit"] = args.ext_crit

    result = build_client(args).create_event(payload)
    print_json(result)
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    event = parse_json_value(args.event)
    if not isinstance(event, dict):
        raise ValueError("event must be JSON object or path to JSON event file")
    payload = {
        "event": event,
        "mode": args.mode,
        "consume_nonce": args.consume_nonce,
    }
    result = build_client(args).verify_event(payload)
    print_json(result)
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    result = build_client(args).health()
    print_json(result)
    return 0


def cmd_extract_event(args: argparse.Namespace) -> int:
    data = parse_json_value(args.response)
    if not isinstance(data, dict) or "event" not in data:
        raise ValueError("response must contain an event field")
    print_json(data["event"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jep",
        description="JEP CLI v0.6 for creating and verifying JEP-Core events through the JEP API.",
    )
    parser.add_argument("--base-url", default="", help="JEP API base URL. Default: JEP_API_URL or http://127.0.0.1:8000")
    parser.add_argument("--api-key", default="", help="API key. Default: JEP_API_KEY")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")

    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a JEP event")
    create.add_argument("--verb", required=True, choices=sorted(VALID_VERBS), help="JEP verb: J, D, T, or V")
    create.add_argument("--who", default="", help="Actor identifier")
    create.add_argument("--what", required=True, help="JSON value, string, file path, or '-' for stdin")
    create.add_argument("--aud", default="", help="Audience / validation context")
    create.add_argument("--ref", default="", help="Reference event hash")
    create.add_argument("--ttl-minutes", type=int, default=None, help="Optional TTL extension in minutes")
    create.add_argument("--digest-only-who", action="store_true", help="Request digest-only privacy extension")
    create.add_argument("--ext", action="append", default=[], help="Extension key=json_or_string. May be repeated")
    create.add_argument("--ext-crit", action="append", default=[], help="Critical extension URI. May be repeated")
    create.set_defaults(func=cmd_create)

    verify = sub.add_parser("verify", help="Verify a JEP event")
    verify.add_argument("event", help="Event JSON object, event JSON file path, or '-' for stdin")
    verify.add_argument("--mode", default="archival", help="Validation mode")
    verify.add_argument("--consume-nonce", action="store_true", help="Ask verifier to consume nonce")
    verify.set_defaults(func=cmd_verify)

    health = sub.add_parser("health", help="Check JEP API health")
    health.set_defaults(func=cmd_health)

    extract = sub.add_parser("extract-event", help="Extract event object from /events/create response")
    extract.add_argument("response", help="Response JSON object, response JSON file path, or '-' for stdin")
    extract.set_defaults(func=cmd_extract_event)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        return int(args.func(args) or 0)
    except SystemExit as exc:
        # Allows tests and embedded callers to receive an exit code instead of
        # terminating the Python process. The console entry point still exits
        # via the __main__ block below.
        return int(exc.code or 0)
    except (JEPCLIError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"jep: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
