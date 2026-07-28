# OpenCode Platform Adapter

## Setup

Reference the `.ai/` directory in your OpenCode config to make skills and commands available.

## Agent Discovery

OpenCode reads agents from `.opencode/agents/`. Symlink or copy agents from `.ai/agents/`:
```
.opencode/agents/
  architecture-agent.md -> ../../.ai/agents/agent-architecture.md
```

Alternatively, configure agent paths in `opencode.json`:
```json
{
  "agents": [".ai/agents/*.md"]
}
```

## Skill Discovery

OpenCode loads skills from `.opencode/skills/`. Reference `.ai/skills/`:
```json
{
  "skills": [".ai/skills/*"]
}
```

## Command Execution

OpenCode uses custom commands from `.opencode/commands/`. Create command files there that reference the workflow in `.ai/commands/`.

## Configuration

```json
{
  "tools": ["Read", "Write", "Grep", "Glob", "Bash"],
  "agents": [".ai/agents/*.md"],
  "skills": [".ai/skills/*"]
}
```

## Known Limitations

- Commands must be manually registered in `.opencode/commands/`
- Agent formats differ slightly; frontmatter is compatible
