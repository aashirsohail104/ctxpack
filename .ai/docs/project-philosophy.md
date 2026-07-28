# Project Philosophy

## Why ctxpack Exists

AI coding assistants have a fundamental bottleneck: context windows. Even the largest models can only process so many tokens at once. When working on a codebase, you cannot simply dump every file into context — you need a curated selection of the most relevant code.

ctxpack solves this by packing relevant project files into a token-budgeted markdown bundle. It selects files based on task relevance, filters noise (dependencies, binaries, build artifacts), and produces one clean, deterministic output.

## Why the AI Toolkit Exists

The `.ai/` directory is a vendor-neutral AI engineering toolkit. It transforms ctxpack into a project that multiple AI coding assistants (OpenCode, Claude Code, Cursor, Codex CLI, Antigravity, Gemini CLI, and future platforms) can understand, extend, test, maintain, and review.

## Design Principles

1. **Specification-driven development** — Every behavior is documented in SPEC.md before implementation.
2. **Deterministic workflows** — Same input always produces same output.
3. **Modular responsibilities** — Each agent, skill, and command has one job.
4. **Single responsibility per agent** — No monolithic agents.
5. **Reusable skills** — Skills are shared across agents, not duplicated.
6. **Vendor-neutral specifications** — No platform lock-in.
7. **Human-readable documentation** — Written for humans and AI alike.
8. **No runtime AI dependency** — ctxpack runs with only Python stdlib.
9. **Production-quality standards** — Engineering rigor throughout.
