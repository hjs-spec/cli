# Acceptance context and exit status

Current Core 0.7 verification forwards `--mode archival` or `--mode acceptance` to the API. `--expected-audience` and `--max-age-seconds` are optional profile checks; acceptance alone does not require them or a Core nonce. The API owns idempotent acceptance by Event Identity `(who,id)`.

Verification exits with status 0 only when the API reports `status: valid`; invalid or indeterminate results exit with status 2. Input/transport errors handled by the CLI exit with status 1. `--ref` accepts either a digest or a JSON reference descriptor. All verification assurance comes from the configured API; the CLI does not perform local cryptographic verification.

`--legacy` selects the historical verifier explicitly and uses its `valid` result. It is an archival compatibility path, not a fallback after current validation fails. See [current commands](README.md#verify).
