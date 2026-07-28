# Generic Platform Adapter

## Purpose

Baseline adapter for AI coding platforms not explicitly listed. Follows universal conventions.

## Agent Discovery

Read `.ai/agents/*.md` — each file defines one agent with YAML frontmatter and system prompt body.

## Skill Discovery

Read `.ai/skills/*/SKILL.md` — each directory is one skill. Frontmatter describes when to use it.

## Command Execution

Commands are documented in `.ai/commands/*.md`. Execute the steps described manually or adapt to your platform's command system.

## Known Limitations

- No automatic command registration
- No automatic agent loading
- Requires manual reference to `.ai/` structure
