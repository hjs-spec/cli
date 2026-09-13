# Acceptance context and exit status

`jep verify --mode acceptance` requires `--expected-audience`. The value is forwarded to the API and negative verification exits with status 2. Malformed input/transport errors exit with status 1. `--ref` accepts either a digest or a JSON reference descriptor. All verification assurance comes from the configured API; the CLI does not perform local cryptographic verification.
