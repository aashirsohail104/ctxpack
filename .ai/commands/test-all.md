# /test-all — Run All Tests with Coverage

## Purpose
Run the complete test suite including unit tests, integration tests, and edge case tests.

## Orchestration
1. Invoke `agent-test-engineering` for comprehensive testing
2. Invoke `agent-hidden-test-simulation` for adversarial testing
3. Run all test suites

## Output
Comprehensive test report with coverage analysis.

## Usage
```
/test-all
```

## Verification
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All edge case tests pass
- [ ] Determinism verified
