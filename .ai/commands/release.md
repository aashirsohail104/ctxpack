# /release — Release Preparation

## Purpose
Prepare and verify a release: version consistency, tests, documentation, changelog.

## Orchestration
1. Invoke `agent-release`
2. Reference `release-readiness` skill
3. Run all tests

## Output
Release readiness report and release checklist.

## Usage
```
/release [--version <semver>]
```

## Verification
- [ ] Version consistent everywhere
- [ ] All tests pass
- [ ] CHANGELOG updated
- [ ] Git tag matches version
