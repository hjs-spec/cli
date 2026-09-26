from jep_cli import main as module


def test_acceptance_does_not_require_core_audience(monkeypatch, capsys):
    class FakeClient:
        def verify_event(self, payload):
            assert payload["mode"] == "acceptance"
            assert "expected_audience" not in payload
            return {
                "status": "valid",
                "mode": "acceptance",
                "profile": "jep-core-0.7",
                "checks": {"syntax": "pass", "cryptographic": "pass", "event_identity": "pass"},
                "acceptance": {"outcome": "accepted", "effect_applied": True},
            }

    monkeypatch.setattr(module, "build_client", lambda args: FakeClient())
    code = module.main([
        "verify",
        '{"jep":"1","id":"urn:uuid:x","verb":"J","who":"a","when":1,"what":{"claim":"x"},"sig":"s"}',
        "--mode", "acceptance",
    ])
    assert code == 0
    assert '"status": "valid"' in capsys.readouterr().out
