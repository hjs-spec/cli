# JEP CLI v0.6

Command-line tool for creating and verifying JEP v0.6 events through the JEP API.

This CLI targets:

```text
POST /events/create
POST /events/verify
GET  /health
```

It is aligned with:

- `draft-wang-jep-judgment-event-protocol-06`
- `draft-wang-jep-profiles-00`
- `draft-wang-jep-conformance-00`
- `hjs-spec/jep-api`

## Status

Experimental implementation seed.

This CLI does not define new JEP-Core semantics and does not determine legal liability, factual truth, regulatory compliance, or complete-log availability.

## Installation

```bash
pip install -e ".[dev]"
```

## Configuration

Use flags:

```bash
jep --base-url http://127.0.0.1:8000 health
```

Or environment variables:

```bash
export JEP_API_URL=http://127.0.0.1:8000
export JEP_API_KEY=
```

## Commands

### Health

```bash
jep health
```

### Create a Judgment event

```bash
jep create \
  --verb J \
  --who did:example:agent-789 \
  --what '{"claim":"approve","subject":"demo"}' \
  --aud https://api.example.org
```

### Create with extensions

```bash
jep create \
  --verb J \
  --who did:example:agent-789 \
  --what '{"claim":"approve"}' \
  --ext 'https://example.org/profile={"name":"demo"}' \
  --ext-crit https://example.org/profile
```

### Verify an event from a file

```bash
jep verify event.json --mode archival
```

### Pipe create response into verify

```bash
jep create --verb J --who did:example:agent --what '{"claim":"approve"}' > response.json
jep extract-event response.json > event.json
jep verify event.json
```

## Input Rules

`--what` and event arguments may be:

- inline JSON;
- a plain string;
- a file path;
- `-` for stdin.

## Related Repositories

- JEP v0.6: https://github.com/hjs-spec/jep-v06
- JEP API v0.6: https://github.com/hjs-spec/jep-api
- JEP Python SDK v0.6: https://github.com/hjs-spec/jep-sdk-py
- JEP Go SDK v0.6: https://github.com/hjs-spec/jep-sdk-go
- HJS v0.5: https://github.com/hjs-spec/hjs-05
- JAC v0.5: https://github.com/hjs-spec/jac-agent-02

## Public Drafts

- JEP-Core: https://datatracker.ietf.org/doc/draft-wang-jep-judgment-event-protocol/
- JEP-Profiles: https://datatracker.ietf.org/doc/draft-wang-jep-profiles/
- JEP-Conformance: https://datatracker.ietf.org/doc/draft-wang-jep-conformance/

## License

MIT
