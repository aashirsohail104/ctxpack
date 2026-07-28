# /hidden-tests — Simulate Hidden Tests

## Purpose
Simulate hackathon judging by probing edge cases and boundary conditions that automated tests might check.

## Orchestration
1. Invoke `agent-hidden-test-simulation`
2. Reference `hidden-test-analysis` skill

## Output
Hidden test report with pass/fail for each potential test case.

## Usage
```
/hidden-tests [--path <path>]
```

## Verification
- [ ] All SPEC.md edge cases covered
- [ ] Boundary conditions tested
- [ ] Adversarial scenarios considered
