# Cursor Platform Adapter

## Setup

Cursor uses `.cursorrules` for project-level AI configuration. Reference the `.ai/` toolkit there.

## Configuration

Add to `.cursorrules`:
```
This project includes an AI engineering toolkit in .ai/. Key resources:
- Agents: .ai/agents/
- Skills: .ai/skills/
- Standards: .ai/standards/
- Documentation: .ai/docs/
```

## Agent Discovery

Cursor does not have a native agent system. Agents in `.ai/agents/` serve as reference prompts for specific tasks.

## Skill Discovery

There is no native skill loading. Reference skills directly by their `.ai/skills/<name>/SKILL.md` path when needed.

## Command Execution

Commands are standard markdown documentation. Execute the described steps manually.

## Known Limitations

- No agent, skill, or command auto-discovery
- All components must be referenced manually
- Best suited as documentation-only
