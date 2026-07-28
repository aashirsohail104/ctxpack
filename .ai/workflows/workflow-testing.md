# Testing Workflow

## Goals
Ensure comprehensive test coverage for ctxpack.

## Execution Order
1. Run `/test-all` for current test status
2. Analyze gaps in coverage
3. Run `/hidden-tests` for adversarial scenarios
4. Add missing tests
5. Verify determinism
6. Verify all edge cases from SPEC.md are covered

## Required Agents
- `agent-test-engineering`
- `agent-hidden-test-simulation`

## Required Skills
- `.ai/skills/hidden-test-analysis/SKILL.md`
- `.ai/skills/deterministic-output-verification/SKILL.md`

## Expected Outputs
- Updated test suite
- Test coverage report
- Hidden test analysis

## Verification Checklist
- [ ] All unit tests pass
- [ ] All edge cases covered
- [ ] Determinism verified
- [ ] Hidden tests pass
