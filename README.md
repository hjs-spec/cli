# JEP CLI — JEP Core 0.7

Command-line client for creating and verifying current JEP Core 0.7 events
through the JEP API.

Default endpoints:

```text
POST /v0.7/events/create
POST /v0.7/events/verify
GET  /health
```

Historical pre-0.7 handling is explicit through `--legacy`; the CLI never
retries a failed 0.7 event with a legacy decoder.

## Status

Experimental reference client. It does not define Core semantics or determine
truth, authorization validity, legal effect, causality, or policy outcome.

## Installation

```bash
pip install jep-cli
```

## Configuration

```bash
export JEP_API_URL=http://127.0.0.1:8000
export JEP_API_KEY=
```

## Create

Judgment:

```bash
jep create \
  --verb J \
  --who did:example:agent-789 \
  --what '{"claim":"approve","subject":"demo"}'
```

Delegation:

```bash
jep create \
  --verb D \
  --who did:example:principal \
  --what '{"delegatee":"did:example:agent","scope":{"actions":["read"]}}'
```

Termination and Verification require `--ref`. Pass a typed reference as
JSON when the target is another JEP event.

## Verify

```bash
jep verify event.json --mode archival
```

0.7 validation returns `status` plus independent `checks`, not a cumulative
Validation Level.

## Explicit legacy verification

```bash
jep verify old-event.json \
  --legacy \
  --legacy-format json-sorted-v1
```

Legacy selection must come from known artifact context. Do not use a failed 0.7
validation as evidence that an event should be treated as 0.6.

## JEP Core 0.7 model

- Event Identity is `(who,id)`.
- Event Hash identifies an exact signed artifact.
- Core does not require a top-level nonce.
- D requires `delegatee + scope`.
- T requires target `ref + termination_scope`.
- V requires target `ref + verification_scope + result`.
- chain and policy semantics remain outside Core.

## Related repositories

- JEP Core: https://github.com/hjs-spec/jep-core
- JEP API: https://github.com/hjs-spec/jep-api
- Python SDK: https://github.com/hjs-spec/sdk-py
- JavaScript SDK: https://github.com/hjs-spec/sdk-js
- Go SDK: https://github.com/hjs-spec/sdk-go

## Public draft

- https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/

## License

MIT
