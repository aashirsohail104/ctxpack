# Code Review Workflow

## Goals
Perform a comprehensive code review of ctxpack.

## Execution Order
1. Run `/scan` to understand the codebase
2. Run `/context` to understand module relationships
3. Invoke `agent-code-review` for line-by-line review
4. Invoke `agent-architecture` for architectural review
5. Aggregate findings into a single report

## Required Agents
- `agent-repository-scanner`
- `agent-context-analysis`
- `agent-code-review`
- `agent-architecture`

## Required Skills
- `.ai/skills/engineering-best-practices/SKILL.md`
- `.ai/skills/python-cli-review/SKILL.md`
- `.ai/skills/architecture-review/SKILL.md`

## Expected Outputs
- Code review report with prioritized issues
- Architecture assessment
- Improvement recommendations

## Verification Checklist
- [ ] Readability assessed
- [ ] Correctness verified
- [ ] Architecture evaluated
- [ ] Performance considered
- [ ] Issues prioritized
