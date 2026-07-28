# Claude Code Platform Adapter

## Setup

Claude Code uses CLAUDE.md (at project root) for project-level instructions. Add references to `.ai/` there as needed.

## Agent Discovery

Claude Code does not have a built-in agent system. Agents in `.ai/agents/` serve as reference for human users to invoke via Task tool prompts.

## Skill Discovery

Claude Code skills live in `~/.claude/skills/`. Symlink or copy `.ai/skills/` entries:
```bash
mkdir -p ~/.claude/skills/ctxpack
cp -r .ai/skills/* ~/.claude/skills/ctxpack/
```

## Command Execution

Claude Code supports `/` commands via `~/.claude/commands/`. Create command scripts there that reference workflows from `.ai/commands/`.

## Configuration

In `CLAUDE.md`, add:
```
## AI Toolkit

Skills are available in `.ai/skills/`. Agents are defined in `.ai/agents/`.
Commands are documented in `.ai/commands/`.
```

## Known Limitations

- No native agent loading — agents must be invoked manually via Task tool
- Skills must be linked into `~/.claude/skills/`
- Commands must be registered in `~/.claude/commands/`
