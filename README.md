# HJS CLI

Command-line interface for [HJS: A Judgment Event Protocol](https://github.com/hjs-protocol/spec).

<p align="center">
    <a href="https://github.com/hjs-protocol/cli">
        <img src="https://img.shields.io/badge/Status-CLI%20Tool%20%7C%20v1.0.0-blue" alt="Status">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
    </a>
    <a href="https://github.com/hjs-protocol/cli/issues">
        <img src="https://img.shields.io/badge/Issues-Welcome-brightgreen" alt="Issues">
    </a>
    <a href="https://www.npmjs.com/package/@hjs/cli">
        <img src="https://img.shields.io/npm/v/@hjs/cli" alt="npm version">
    </a>
</p>

---

## Overview

HJS CLI is a command-line tool for interacting with the HJS protocol. It allows you to:

- Create and manage judgment records
- Delegate authority to other entities
- Terminate responsibility chains
- Verify records and receipts
- Configure API access

## Installation

### Via npm (recommended)

```bash
npm install -g @hjs/cli
```

### From source

```bash
git clone https://github.com/hjs-protocol/cli.git
cd cli
npm install
npm link
```

## Quick Start

### 1. Configure your API key

```bash
hjs config set api-key YOUR_API_KEY
```

If you're using a self-hosted HJS API instance, you can also set the API URL:

```bash
hjs config set api-url https://your-hjs-instance.com
```

### 2. Create a judgment record

```bash
hjs judgment create \
  --entity user@example.com \
  --action approve \
  --scope '{"amount": 1000, "currency": "USD"}'
```

### 3. Query a record

```bash
hjs judgment get jgd_1234567890abcd
```

### 4. Verify a record

```bash
hjs verify jgd_1234567890abcd
```

## Commands

### `hjs judgment`

Manage judgment records.

| Command | Description |
|---------|-------------|
| `create` | Create a new judgment record |
| `get <id>` | Retrieve a judgment by ID |
| `list` | List judgment records (with filters) |
| `export` | Export judgment records |

**Options:**

- `--entity, -e` - Entity identifier (required for create)
- `--action, -a` - Action name (required for create)
- `--scope, -s` - JSON scope/context
- `--timestamp, -t` - Custom timestamp (ISO 8601)
- `--immutability, -i` - Anchor type (ots, none)
- `--format, -f` - Output format (json, text)

### `hjs delegation`

Manage delegations.

| Command | Description |
|---------|-------------|
| `create` | Create a new delegation |
| `get <id>` | Retrieve a delegation by ID |
| `list` | List delegations |
| `revoke <id>` | Revoke a delegation |

### `hjs termination`

Manage terminations.

| Command | Description |
|---------|-------------|
| `create` | Create a termination record |
| `get <id>` | Retrieve a termination by ID |
| `list` | List terminations |

### `hjs verify`

Verify records and receipts.

| Command | Description |
|---------|-------------|
| `<id>` | Verify a record by ID |
| `receipt <file>` | Verify a receipt file |

### `hjs config`

Manage CLI configuration.

| Command | Description |
|---------|-------------|
| `set <key> <value>` | Set a configuration value |
| `get <key>` | Get a configuration value |
| `list` | List all configuration |
| `clear` | Clear configuration |

Configuration is stored in `~/.hjs/config.json`.

## Examples

### Create a judgment with scope

```bash
hjs judgment create \
  --entity loan-officer-123 \
  --action approve_loan \
  --scope '{"amount": 50000, "risk_score": 0.12, "customer_id": "cust_789"}'
```

### Delegate authority

```bash
# Create a judgment first
JUDGMENT_ID=$(hjs judgment create --entity manager@company.com --action "delegate_access" --quiet)

# Delegate to an employee
hjs delegation create \
  --delegator manager@company.com \
  --delegatee employee@company.com \
  --judgment-id $JUDGMENT_ID \
  --scope '{"permissions": ["read", "write"]}' \
  --expiry "2026-12-31T23:59:59Z"
```

### Verify a record with receipt

```bash
# Download receipt
hjs judgment get jgd_1234567890abcd --format receipt > record.ots

# Verify offline
hjs verify receipt record.ots
```

## Configuration

The CLI can be configured via:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Config file** (`~/.hjs/config.json`)

### Environment variables

| Variable | Description |
|----------|-------------|
| `HJS_API_URL` | API endpoint (default: https://api.hjs.sh) |
| `HJS_API_KEY` | API key for authentication |
| `HJS_OUTPUT` | Default output format (json, text) |

### Config file example

```json
{
  "apiUrl": "https://api.hjs.sh",
  "apiKey": "your-api-key-here",
  "output": "text",
  "defaults": {
    "immutability": "none"
  }
}
```

## Development

### Setup

```bash
git clone https://github.com/hjs-protocol/cli.git
cd cli
npm install
```

### Testing

```bash
npm test
```

### Building

```bash
npm run build
```

### Contributing

Please see our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## Related Repositories

- [Protocol Specification](https://github.com/hjs-protocol/spec)
- [Core Implementation (Rust)](https://github.com/hjs-protocol/core)
- [API Service](https://github.com/hjs-protocol/api)
- [Python SDK](https://github.com/hjs-protocol/sdk-py)
- [JavaScript SDK](https://github.com/hjs-protocol/sdk-js)

## License

MIT © [Human Judgment Systems Foundation Ltd.](https://humanjudgment.org)

---

**© 2026 Human Judgment Systems Foundation Ltd.**  
This document is licensed under the [MIT License](https://opensource.org/licenses/MIT).
```
