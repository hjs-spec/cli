#!/usr/bin/env bash
set -euo pipefail

export JEP_API_URL="${JEP_API_URL:-http://127.0.0.1:8000}"

jep health

jep create \
  --verb J \
  --who did:example:agent-789 \
  --what '{"claim":"approve","subject":"demo"}' \
  --aud https://api.example.org > response.json

jep extract-event response.json > event.json
jep verify event.json
