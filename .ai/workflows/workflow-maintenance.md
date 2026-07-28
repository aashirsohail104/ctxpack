# Maintenance Workflow

## Goals
Routine maintenance of ctxpack: dependency updates, tech debt reduction, code cleanup.

## Execution Order
1. Run `/scan` for current state
2. Run `/audit` for issues
3. Run `/performance` for optimization opportunities
4. Address identified issues (one at a time)
5. Run tests after each change
6. Update documentation if needed

## Required Agents
- `agent-repository-scanner`
- `agent-repository-quality`
- `agent-performance`
- `agent-code-review`

## Required Skills
- `.ai/skills/repository-audit/SKILL.md`
- `.ai/skills/performance-review/SKILL.md`
- `.ai/skills/engineering-best-practices/SKILL.md`

## Expected Outputs
- Clean repository
- Resolved tech debt
- Optimized performance
- Updated documentation

## Verification Checklist
- [ ] All tests pass after each change
- [ ] Determinism preserved
- [ ] Tech debt items tracked
- [ ] No regressions introduced
