"""Small HTTP client for JEP CLI v0.6."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib import request, error


class JEPCLIError(Exception):
    pass


class JEPAPIError(JEPCLIError):
    def __init__(self, status: int, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(f"JEP API error ({status}): {message}")
        self.status = status
        self.message = message
        self.payload = payload or {}


class JEPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", api_key: str = "", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def create_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._json("POST", "/events/create", payload)

    def verify_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._json("POST", "/events/verify", payload)

    def health(self) -> Dict[str, Any]:
        return self._json("GET", "/health", None)

    def _json(self, method: str, path: str, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        data = None
        headers = {
            "content-type": "application/json",
            "user-agent": "JEP-CLI/0.6.0",
        }
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
            headers["x-api-key"] = self.api_key
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        req = request.Request(self.base_url + path, data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8")
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = {"message": body}
            msg = parsed.get("message") or parsed.get("error") or body
            raise JEPAPIError(exc.code, msg, parsed) from exc
