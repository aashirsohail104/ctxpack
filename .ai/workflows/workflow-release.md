# Release Workflow

## Goals
Prepare and execute a production release of ctxpack.

## Execution Order
1. Run `/release` for readiness check
2. Fix any blocking issues
3. Update version in ctxpack.py
4. Update CHANGELOG.md
5. Run `/test-all` for final verification
6. Run `/verify` on a sample bundle
7. Create git tag
8. Write release notes

## Required Agents
- `agent-release`
- `agent-test-engineering`
- `agent-documentation`

## Required Skills
- `.ai/skills/release-readiness/SKILL.md`
- `.ai/skills/quality-assurance/SKILL.md`

## Expected Outputs
- Tagged release
- Release notes
- Verified release artifacts

## Verification Checklist
- [ ] Version consistent everywhere
- [ ] All tests pass
- [ ] Determinism verified
- [ ] CHANGELOG complete
- [ ] Git tag created
- [ ] Release notes written
