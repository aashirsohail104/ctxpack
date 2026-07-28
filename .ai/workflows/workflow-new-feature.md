# New Feature Workflow

## Goals
Implement a new feature in ctxpack following specification-driven development.

## Execution Order
1. Review specification (SPEC.md) for feature requirements
2. Design the feature architecture
3. Implement the feature in ctxpack.py
4. Write tests for the feature
5. Verify determinism
6. Update documentation

## Required Agents
- `agent-architecture` — Design review
- `agent-test-engineering` — Test writing

## Required Skills
- `.ai/skills/specification-review/SKILL.md`
- `.ai/skills/engineering-best-practices/SKILL.md`
- `.ai/skills/python-cli-review/SKILL.md`

## Expected Outputs
- Updated ctxpack.py with new feature
- Tests for the new feature
- Updated documentation

## Verification Checklist
- [ ] Feature matches SPEC.md
- [ ] All tests pass
- [ ] Determinism verified
- [ ] Documentation updated
- [ ] No regressions
