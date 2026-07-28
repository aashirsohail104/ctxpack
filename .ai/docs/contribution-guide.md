# Contribution Guide

## How to Contribute

### Adding a Skill

1. Create `.ai/skills/<skill-name>/SKILL.md`
2. Include YAML frontmatter with `name` and `description`
3. Follow the skill template in `.ai/templates/skill-template.md`
4. Cross-reference any agents that should use it
5. Verify: no duplicates, no broken references

### Adding an Agent

1. Create `.ai/agents/agent-<name>.md`
2. Include YAML frontmatter with triggering conditions
3. Define responsibilities, process, output format
4. Reference relevant skills from `.ai/skills/`
5. Verify: single responsibility, no duplication

### Adding a Command

1. Create `.ai/commands/<name>.md`
2. Define the command structure per your platform
3. Reference agents and skills it orchestrates
4. Include usage examples

### Adding a Workflow

1. Create `.ai/workflows/<name>.md`
2. Define goals, execution order, agents, skills, outputs
3. Include verification checklist

## Quality Checks

Before submitting any change:

- [ ] All references to other `.ai/` components are valid
- [ ] No duplicate functionality
- [ ] English is clear and proofread
- [ ] Frontmatter is valid YAML
- [ ] Files follow naming conventions
- [ ] ctxpack.py is unchanged (unless explicitly modifying runtime)

## AI Contributors

If you are an AI coding assistant reading this:

1. Read the specification (SPEC.md) before making changes
2. Understand CLAUDE.md for project conventions
3. Load the relevant skill from `.ai/skills/` before acting
4. Verify assumptions with tools before making changes
5. Never modify `ctxpack.py` unless explicitly asked
6. Record reasoning for architectural decisions
