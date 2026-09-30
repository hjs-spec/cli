# JEP CLI — JEP Core 0.7

Command-line client for creating and verifying current JEP Core 0.7 events
through the JEP API.

## Status

Experimental HTTP client. Event creation and verification run on the configured
API. Start the [local reference API](https://github.com/hjs-spec/jep-quickstart#start-a-local-api)
before running the examples below.

## Installation

```bash
pip install jep-cli==0.7.2
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
  --what '{"claim":"approve","subject":"demo"}' > response.json
jep extract-event response.json > event.json
```

`event.json` contains the signed event used by the verification command below.

Delegation:

```bash
jep create \
  --verb D \
  --who did:example:principal \
  --what '{"delegatee":"did:example:agent","scope":{"actions":["read"]}}'
```

For Termination and Verification, supply `--ref` and the verb-specific `what`
described in the [implementer guide](https://github.com/hjs-spec/jep-core/blob/main/docs/IMPLEMENTER-GUIDE.md).
Pass a typed reference as JSON when the target is another JEP event.

## Verify

```bash
jep verify event.json --mode archival
```

Validation returns `status` and independent `checks`. Look for `status: "valid"`
and `checks.cryptographic: "pass"` for the sample event.

## Explicit legacy verification

```bash
jep verify old-event.json \
  --legacy \
  --legacy-format json-sorted-v1
```

Legacy selection must come from known artifact context. Do not use a failed 0.7
validation as evidence that an event should be treated as 0.6.

## Related repositories

- Core contract and implementation path: https://github.com/hjs-spec/jep-core#current-contract
- JEP API: https://github.com/hjs-spec/jep-api
- Python SDK: https://github.com/hjs-spec/sdk-py
- JavaScript SDK: https://github.com/hjs-spec/sdk-js
- Go SDK: https://github.com/hjs-spec/sdk-go

## Public draft

- https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/

## License

MIT
