# Hackathon Submission Workflow

## Goals
Prepare ctxpack for a hackathon submission: exhaustive verification, edge case testing, and polish.

## Execution Order
1. Run `/spec-check` for specification compliance
2. Run `/hidden-tests` for adversarial testing
3. Run `/test-all` for comprehensive testing
4. Run `/verify` on multiple sample bundles
5. Run `/docs` for documentation review
6. Run `/cleanup` for repository polish
7. Run `/release` for final readiness check
8. One final determinism verification

## Required Agents
- All agents

## Required Skills
- `.ai/skills/quality-assurance/SKILL.md`
- `.ai/skills/hidden-test-analysis/SKILL.md`
- `.ai/skills/deterministic-output-verification/SKILL.md`
- `.ai/skills/release-readiness/SKILL.md`

## Expected Outputs
- Exhaustive verification report
- All issues resolved
- Repository is clean and organized
- Package is release-ready

## Verification Checklist
- [ ] SPEC.md matches implementation exactly
- [ ] All tests pass
- [ ] Hidden tests pass
- [ ] Determinism verified (3+ runs)
- [ ] All edge cases handled
- [ ] Documentation is complete
- [ ] Repository is clean
- [ ] Version is set
