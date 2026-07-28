# Antigravity Platform Adapter

## Setup

Antigravity is a configuration-driven AI coding environment. Reference `.ai/` components in its configuration.

## Configuration

```yaml
agents:
  source: .ai/agents/
  format: markdown-frontmatter
skills:
  source: .ai/skills/
  format: opencode-compatible
commands:
  source: .ai/commands/
  format: markdown
```

## Agent Discovery

Antigravity reads agent definitions from configured source directories. Point it to `.ai/agents/`.

## Skill Discovery

Skills are loaded from `.ai/skills/` directories. Each `SKILL.md` provides the skill definition.

## Known Limitations

- Platform is evolving; adapter may need updates
- Command registration details depend on Antigravity version
