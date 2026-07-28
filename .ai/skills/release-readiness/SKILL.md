---
name: release-readiness
description: Use when checking if ctxpack is ready for release — validates version consistency, tests, documentation, and release checklist
---

# Release Readiness

## Purpose
Check if ctxpack is ready for a release. Validates version consistency, test coverage, documentation completeness, and release checklist items.

## Inputs
- ctxpack.py (check __version__)
- All test files
- All documentation
- git log / changelog

## Outputs
- Release readiness assessment
- Blocking issues
- Recommended actions

## Workflow
1. Check version string exists and is consistent
2. Verify all tests pass
3. Check documentation is up to date
4. Verify changelog reflects changes since last release
5. Check git tag matches version
6. Verify determinism (run twice, compare)
7. Check edge cases from SPEC.md
8. Verify CLI help text is correct
9. Check all file headers and footers

## Release Checklist
- [ ] Version string updated in ctxpack.py
- [ ] CHANGELOG.md updated
- [ ] All tests pass
- [ ] Determinism verified (3 runs, identical output)
- [ ] CLI help text matches spec
- [ ] SPEC.md is current
- [ ] README.md is current
- [ ] .ai/ toolkit is consistent
- [ ] Git tag created
- [ ] Release notes written

## Limitations
- Cannot verify external dependencies or packaging
- Subjective quality assessments (e.g., "documentation is clear")

## Success Criteria
- [ ] All blocking issues resolved
- [ ] Release checklist complete
- [ ] Version consistent across all files
