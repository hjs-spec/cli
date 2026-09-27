# Release 0.7.2

- Reject duplicate members, invalid UTF-8/Unicode, non-finite numbers and unsupported precision-losing integers before parsing or forwarding event input. The same boundary applies to inline JSON, files and standard input, including explicit legacy commands.
- Preserve supported large JCS numbers and every signed member without normalization. Signature, profile and authorization checks remain with the API.
- Reject repeated extension arguments and malformed JSON-looking input instead of silently replacing a value or treating a damaged object as plain text. Plain-text creation arguments remain supported.
- Validate outgoing request values and successful JSON responses with the same boundary. No automatic legacy fallback is introduced.

Protocol remains Core 0.7 / wire 1. Published protocol drafts and historical signed artifacts are unchanged.
