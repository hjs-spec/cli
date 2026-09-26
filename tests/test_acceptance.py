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


def test_failure_and_indeterminate_return_nonzero(monkeypatch):
    for status in ("invalid", "indeterminate"):
        class Client:
            def verify_event(self, payload):
                assert payload["expected_audience"] == "receiver"
                return {"status": status}
        monkeypatch.setattr(module, "build_client", lambda args: Client())
        assert module.main(["verify", '{}', "--mode", "acceptance", "--expected-audience", "receiver"]) == 2


def test_large_inline_event_is_not_treated_as_a_filename():
    import json
    event = {"what": {"claim": "x" * 4096}}
    assert module.parse_json_value(json.dumps(event)) == event
