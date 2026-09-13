import json
from jep_cli import main as module


def test_acceptance_requires_expected_audience(capsys):
    assert module.main(["verify", '{"jep":"1"}', "--mode", "acceptance"]) == 1
    assert "expected-audience" in capsys.readouterr().err


def test_verification_failure_returns_nonzero(monkeypatch):
    class Client:
        def verify_event(self, payload):
            assert payload["expected_audience"] == "receiver"
            return {"valid": False}
    monkeypatch.setattr(module, "build_client", lambda args: Client())
    assert module.main(["verify", '{}', "--mode", "acceptance", "--expected-audience", "receiver"]) == 2
