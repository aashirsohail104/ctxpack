# AGENTS.md — ctxpack Agent Configuration

## Agent Roles

| Role | Responsibility | Skills |
|---|---|---|
| **Orchestrator** | Task planning, delegation, review, verification | All skills |
| **Python Engineer** | Implement ctxpack.py | Python stdlib, argparse, file I/O |
| **Documentation Agent** | Spec kit documents, README, prompts | Markdown, technical writing |
| **Testing Agent** | Edge case tests, determinism verification | Python, shell scripting |
| **Verification Agent** | Spec compliance, byte-identical checks | Diff tools, Python |

## Delegation Rules

1. **Orchestrator** always starts by reading the spec (SPEC.md) before delegating any work
2. **Python Engineer** receives clear function-level specifications with input/output contracts
3. **Testing Agent** receives the CLI contract exactly as specified in SPEC.md
4. **Documentation Agent** writes docs after implementation, not before
5. **Verification Agent** runs last and blocks completion if any check fails

## Task Handoff Format

Each delegated task includes:
- Objective
- Acceptance criteria
- Files affected
- Dependencies
- Verification steps

## Capability Check Order

Before implementing any task:
1. Is there an MCP server for this? → Use it
2. Is there a specialized agent? → Delegate to it
3. Is there an installed skill? → Use it
4. Is there a built-in tool? → Use it
5. Manual implementation → Only if none of the above apply

## Prompt Engineering Guidelines

- Always reference SPEC.md for requirements
- Include context from CLAUDE.md for constraints
- Specify exact function signatures and return types
- Request deterministic implementation only
- Request error handling for all edge cases
