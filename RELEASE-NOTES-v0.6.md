# JEP CLI v0.6.0 Release Notes

## Summary

This release upgrades the CLI into a JEP v0.6 API command-line seed.

## Added

- `jep create` for `POST /events/create`.
- `jep verify` for `POST /events/verify`.
- `jep health` for `GET /health`.
- `jep extract-event` helper.
- Support for J/D/T/V verbs.
- Support for `ext` and `ext_crit`.
- Support for file, inline JSON, string, and stdin inputs.
- Local HTTP-server-based tests.
- GitHub Actions workflow.

## Changed

- Replaced legacy command assumptions with JEP v0.6 API shape.
- Updated README and examples to current JEP v0.6.

## Boundary

This CLI is an implementation seed. It does not define new protocol semantics or claim production conformance.
