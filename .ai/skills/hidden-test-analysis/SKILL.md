---
name: hidden-test-analysis
description: Use when simulating hackathon judging or discovering hidden test failures — probes edge cases that automated tests might check
---

# Hidden Test Analysis

## Purpose
Simulate adversarial testing to discover hidden failures that automated test suites might check. Probes edge cases, boundary conditions, and spec violations.

## Inputs
- ctxpack.py implementation
- SPEC.md specification
- Current test suite (if any)

## Outputs
- List of potential hidden test cases
- Expected behavior for each
- Current implementation behavior for each
- Gap analysis

## Workflow
1. Review SPEC.md for every explicit and implicit behavioral claim
2. For each claim, design a test case that would verify it
3. Consider: CLI flags, exit codes, error messages, token counting, ranking, noise filtering, manifest, bundle format, edge cases
4. Run each test case mentally (or with actual tool if available)
5. Record pass/fail for each
6. Prioritize failures by severity

## Edge Cases to Always Check
- Budget = 1 (minimum)
- Budget = exact size of header
- Empty directory
- Directory with only noise files
- Single file larger than budget
- Task description with no stopwords
- Task description that matches nothing
- Very long task description
- Non-ASCII characters in files
- Files with BOM markers
- Symlinks, permission-denied files

## Best Practices
- Think like a contest judge: test the boundary, not the happy path
- Check that error messages are exactly as specified
- Verify exit codes are correct (0, 1, 2)

## Limitations
- Cannot run actual tests without the testing framework
- Some edge cases may be implementation-specific

## Success Criteria
- [ ] All edge cases from SPEC.md have test coverage
- [ ] Adversarial scenarios are considered
- [ ] Boundary conditions are tested
