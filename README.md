# JEP CLI — JEP Core 0.7

Command-line client for the current JEP Core 0.7 reference API.

Default commands use:

```text
POST /v0.7/events/create
POST /v0.7/events/verify
GET  /health
```

Historical pre-0.7 verification is explicit through `jep verify-legacy`.
The CLI never retries a failed 0.7 event as 0.6.

## Install

```bash
pip install -e ".[dev]"
```

## Configuration

```bash
export JEP_API_URL=http://127.0.0.1:8000
export JEP_API_KEY=
```

## Create a J event

```bash
jep create \
  --verb J \
  --who did:example:agent-789 \
  --what '{"claim":"approve","subject":"demo"}'
```

For D/T/V, provide the Core 0.7 minimum structures:
- D: `what.delegatee` + `what.scope`
- T: `--ref` + `what.termination_scope`
- V: `--ref` + `what.verification_scope` + `what.result`

## Verify

```bash
jep verify event.json --mode archival
```

Current validation output uses:
- `status = valid | invalid | indeterminate`
- independent `checks`
- `event_identity`
- `event_hash`
- optional `acceptance`

## Explicit legacy verification

```bash
jep verify-legacy historical-event.json --mode archival
```

Use this only when the artifact is already known to be pre-0.7.

## Boundaries

JEP Core validity does not establish substantive truth, legal effect,
authorization validity, causality, policy outcome, or complete-log status.

## Related repositories

- JEP Core: https://github.com/hjs-spec/jep-core
- JEP API: https://github.com/hjs-spec/jep-api
- Python SDK: https://github.com/hjs-spec/sdk-py
- JavaScript SDK: https://github.com/hjs-spec/sdk-js
- Go SDK: https://github.com/hjs-spec/sdk-go

## Public draft

https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/

## License

MIT
