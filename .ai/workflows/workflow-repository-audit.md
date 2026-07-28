# Repository Audit Workflow

## Goals
Perform a comprehensive audit of the ctxpack repository.

## Execution Order
1. Run `/scan` for file inventory
2. Run `/audit` for structure and cleanliness
3. Run `/repo-health` for overall health
4. Run `/cleanup` for cleanup suggestions
5. Aggregate findings into a single report

## Required Agents
- `agent-repository-scanner`
- `agent-repository-quality`
- `agent-documentation`

## Required Skills
- `.ai/skills/repository-audit/SKILL.md`
- `.ai/skills/repository-cleanup/SKILL.md`
- `.ai/skills/project-structure-review/SKILL.md`

## Expected Outputs
- Comprehensive repository audit report
- Cleanup action items
- Health score

## Verification Checklist
- [ ] Structure assessed
- [ ] Cleanliness evaluated
- [ ] Naming conventions checked
- [ ] .gitignore reviewed
- [ ] Action items prioritized
