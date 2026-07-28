# Performance Optimization Workflow

## Goals
Analyze and optimize ctxpack performance.

## Execution Order
1. Run `/performance` for baseline analysis
2. Identify bottlenecks from the analysis
3. Implement optimizations (one at a time)
4. Verify determinism is preserved
5. Run tests to check for regressions
6. Re-run performance analysis to measure improvement

## Required Agents
- `agent-performance`
- `agent-test-engineering`

## Required Skills
- `.ai/skills/performance-review/SKILL.md`
- `.ai/skills/deterministic-output-verification/SKILL.md`

## Expected Outputs
- Performance analysis report
- Optimized implementation
- Verified performance improvement

## Verification Checklist
- [ ] Performance improvement measured
- [ ] Determinism preserved
- [ ] All tests pass
- [ ] No regressions
