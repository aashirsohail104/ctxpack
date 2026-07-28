# ctxpack AI Engineering Toolkit

This directory contains a vendor-neutral AI engineering toolkit for **ctxpack** — a Python CLI that packs relevant project files into token-budgeted markdown bundles for AI coding assistants.

## Quick Start

```
.ai/
  agents/       Specialized AI assistants
  skills/       Reusable engineering capabilities
  commands/     User-invokable operations
  workflows/    Multi-step process orchestrations
  prompts/      Universal prompt library
  templates/    Reusable document templates
  docs/         Documentation and guides
  examples/     Usage examples
  standards/    Engineering conventions
  platforms/    Platform-specific adapters
```

## Core Principle

ctxpack is **always standalone** — it runs with only Python stdlib. The `.ai/` toolkit is an optional enhancement for AI contributors and maintainers.

## Platform Support

Works with: OpenCode, Claude Code, Cursor, Codex CLI, Antigravity, Gemini CLI

## Key Documents

- `SPEC.md` — Project specification (at project root)
- `CLAUDE.md` — Quick reference for AI assistants (at project root)
- `.ai/standards/engineering-standards.md` — Engineering conventions
- `.ai/docs/architecture-overview.md` — Architecture documentation
- `.ai/docs/contribution-guide.md` — How to contribute
