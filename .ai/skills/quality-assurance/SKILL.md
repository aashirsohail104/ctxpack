---
name: quality-assurance
description: Use when performing comprehensive quality assurance on ctxpack — coordinates multiple review skills and produces an overall quality report
---

# Quality Assurance

## Purpose
Coordinate comprehensive quality assurance across all review dimensions: specification, implementation, documentation, performance, architecture, and testing.

## Inputs
- Entire project (code, docs, tests, spec)

## Outputs
- Comprehensive QA report
- Quality score per dimension
- Critical issues list
- Overall quality assessment

## Workflow
1. Invoke specification review
2. Invoke architecture review
3. Invoke code review (Python CLI review + engineering best practices)
4. Invoke documentation review
5. Invoke test analysis (hidden test analysis + test coverage assessment)
6. Invoke performance review
7. Invoke repository audit
8. Aggregate all findings into a single report
9. Prioritize issues by severity

## Quality Dimensions
| Dimension | Weight | Sources |
|-----------|--------|---------|
| Correctness | 30% | Spec review, hidden tests |
| Reliability | 20% | Error handling, determinism |
| Maintainability | 15% | Architecture, code style, docs |
| Performance | 10% | Complexity analysis, benchmarking |
| Test Quality | 15% | Coverage, edge cases |
| Documentation | 10% | README, SPEC, inline docs |

## Limitations
- Quality assessment is heuristic, not absolute
- Some dimensions require subjective judgment

## Success Criteria
- [ ] All quality dimensions assessed
- [ ] Critical issues identified and prioritized
- [ ] Overall quality score calculated
- [ ] Actionable improvement plan produced
