# Changelog

All notable changes to **ctxpack** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-07-28

### Added
- Initial release of the token-budgeted context bundler.
- CLI with the contract: `ctxpack --path <folder> --task "<task>" --budget <int> [--out <file>] [--manifest <file>]`.
- Spec-compliant ranking (keyword overlap × extension priority), head-only truncation, and manifest emission.
- `.ai/` engineering toolkit (agents, skills, commands, workflows, prompts, platforms, templates, docs, examples, standards).
- Test fixture repos covering empty, single-file, deeply-nested, binary, unicode, and `.gitignore` cases.

### Notes
- The optional `--report` flag emits an HTML engineering dashboard. The HTML embeds a runtime timestamp, so it is **not** covered by the spec's byte-identical determinism guarantee — the bundle and manifest outputs are.
- `ctxpack.py` at the repository root is a thin shim that re-exports the `ctxpack` package; the real implementation lives under `src/ctxpack/`.
