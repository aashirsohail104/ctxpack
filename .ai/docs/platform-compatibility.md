# Platform Compatibility

## Supported Platforms

| Platform | Agent Support | Skill Support | Command Support | Notes |
|----------|--------------|---------------|-----------------|-------|
| OpenCode | Full | Full | Full | Native skill loading via `.opencode/skills/` |
| Claude Code | Full | Full | Partial | Uses CLAUDE.md, hooks, and `/` commands |
| Cursor | Full | Full | Partial | `.cursorrules` for rules, terminal for commands |
| Codex CLI | Full | Full | Partial | `.codex/skills/` for skills |
| Antigravity | Full | Full | Partial | Configuration-driven |
| Gemini CLI | Full | Full | Partial | Compatible with standard markdown |

## Platform Adapter Convention

Each platform adapter in `.ai/platforms/<name>/` contains:

- `README.md` — Platform-specific setup and configuration
- `config.json` or config template — Platform-specific configuration example
- `setup.sh` (optional) — Setup script if needed

The adapters contain only compatibility guidance and configuration examples. They never duplicate core engineering logic from `.ai/skills/` or `.ai/agents/`.

## Vendor-Neutral Core

All core AI engineering logic lives in these directories, independent of any platform:

- `.ai/agents/` — Agent definitions
- `.ai/skills/` — Skill definitions
- `.ai/commands/` — Command definitions
- `.ai/workflows/` — Workflow definitions
- `.ai/standards/` — Engineering standards
- `.ai/prompts/` — Universal prompts

Platform-specific directories only contain the thin adapter layer.
