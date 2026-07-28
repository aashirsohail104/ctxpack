# Codex CLI Platform Adapter

## Setup

Codex CLI supports `.codex/skills/` for skill loading. Symlink or copy `.ai/skills/` entries.

## Skill Discovery

```bash
mkdir -p .codex/skills/ctxpack
cp -r .ai/skills/* .codex/skills/ctxpack/
```

## Agent Discovery

Codex CLI does not have a native agent system. Use agents from `.ai/agents/` as reference prompts.

## Command Execution

Codex CLI supports custom commands. Reference `.ai/commands/` for implementation guidance.

## Configuration

Place an `.codex/config.json` referencing:
```json
{
  "skills": [".ai/skills/*"]
}
```

## Known Limitations

- No native agent system
- Commands must be manually adapted
- Skill format may need minor adjustments
