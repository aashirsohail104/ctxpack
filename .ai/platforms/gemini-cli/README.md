# Gemini CLI Platform Adapter

## Setup

Gemini CLI works with standard markdown inputs. Reference `.ai/` components in your prompts.

## Usage

When working with ctxpack on Gemini CLI, reference these paths:

- Specification: `SPEC.md`
- Quick reference: `CLAUDE.md`
- Agents: `.ai/agents/*.md`
- Skills: `.ai/skills/*/SKILL.md`
- Standards: `.ai/standards/*.md`

## Agent Discovery

Gemini CLI does not have a native agent system. Load agent definitions from `.ai/agents/` as system prompts.

## Skill Discovery

Load skills from `.ai/skills/` as needed. Each `SKILL.md` contains a complete skill definition.

## Known Limitations

- No automatic discovery — all references are manual
- No command system — workflows must be executed step by step
- Best used as a reference library invoked through prompts
