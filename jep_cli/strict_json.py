"""Strict JSON input boundary; signature/profile validation stays with the API."""
from __future__ import annotations

import json
import math
from typing import Any

import rfc8785


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member: {key!r}")
        result[key] = value
    return result


def _constant(token):
    raise ValueError(f"non-JSON numeric constant: {token}")


def validate(value: Any) -> None:
    """Reject lossy/invalid input without rewriting values or signed members.

    Large integer policy matches Core 0.7.4: exact binary64 integers and their
    JCS shortest-decimal spellings are supported. This is not signature checking.
    """
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, str):
        value.encode("utf-8", errors="strict")
    elif isinstance(value, int):
        if abs(value) > 2**53 - 1:
            try:
                number = float(value)
                if not math.isfinite(number):
                    raise ValueError("integer exceeds binary64 range")
                if int(number) != value and rfc8785.dumps(number) != str(value).encode("ascii"):
                    raise ValueError("integer is neither exact binary64 nor its JCS spelling")
            except OverflowError as exc:
                raise ValueError("integer exceeds binary64 range") from exc
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite number")
    elif isinstance(value, list):
        for item in value:
            validate(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("JSON member names must be strings")
            validate(key)
            validate(item)
    else:
        raise ValueError("unsupported JSON value")


def loads(text: str | bytes) -> Any:
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="strict")
    # Reject raw surrogate code points even before JSON parsing.
    text.encode("utf-8", errors="strict")
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
        validate(value)
        return value
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds parser capacity") from exc


def dumps(value: Any) -> str:
    try:
        validate(value)
        return json.dumps(value, ensure_ascii=False, allow_nan=False)
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds parser capacity") from exc
