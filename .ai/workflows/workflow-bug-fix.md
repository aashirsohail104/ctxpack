# Bug Fix Workflow

## Goals
Fix a bug in ctxpack with proper testing and verification.

## Execution Order
1. Reproduce the bug and understand root cause
2. Write a failing test that demonstrates the bug
3. Fix the bug in ctxpack.py
4. Verify the test passes
5. Verify no regressions in other tests
6. Update changelog

## Required Agents
- `agent-code-review` — Bug analysis
- `agent-test-engineering` — Test writing

## Required Skills
- `.ai/skills/engineering-best-practices/SKILL.md`
- `.ai/skills/python-cli-review/SKILL.md`

## Expected Outputs
- Bug fix in ctxpack.py
- Test covering the bug scenario
- Changelog entry

## Verification Checklist
- [ ] Bug is fixed
- [ ] Test covers the bug scenario
- [ ] All existing tests still pass
- [ ] Determinism verified
