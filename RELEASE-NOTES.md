# Release 0.7.1

Release the current JEP Core 0.7 CLI after repairing the acceptance regression gate.

- Default creation and verification use `/v0.7/events/*`; audience is optional unless a selected profile requires it.
- Explicit `--legacy` / `--legacy-format` options preserve the historical decoder contract. No fallback after current validation fails.
- Invalid and indeterminate verification return exit code 2; input or transport errors return 1.
- Large inline JSON is parsed before filesystem probing.
- Package, import, user-agent, tag, and built distribution versions are aligned and checked before publication.
