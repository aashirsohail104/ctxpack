---
name: token-budget-optimization
description: Use when analyzing token budget allocation in ctxpack — checks waste, truncation efficiency, and recommends optimal budget values
---

# Token Budget Optimization

## Purpose
Analyze and optimize token budget allocation in ctxpack bundles. Identify waste, improve truncation decisions, and recommend budget values.

## Inputs
- Bundle output
- Manifest JSON
- Budget value
- Directory contents

## Outputs
- Budget efficiency report
- Waste identification
- Truncation analysis
- Budget recommendation

## Workflow
1. Calculate total tokens used vs budget
2. Identify fixed overhead (headers, tree) as percentage of budget
3. Find files with low relevance scores that consume significant tokens
4. Check if truncation markers waste tokens on nearly-empty files
5. Analyze tree cost vs value for the given budget
6. Recommend optimal budget for this project/task

## Efficiency Metrics
- **Token density**: useful content / total tokens
- **Overhead ratio**: header+tree tokens / content tokens
- **Truncation loss**: tokens of truncated content / total content tokens
- **Budget utilization**: used tokens / budget

## Best Practices
- Aim for >80% budget utilization
- Keep overhead under 20% for large budgets, under 40% for small budgets
- Consider excluding tree for budgets under 500 tokens

## Limitations
- Cannot determine optimal budget without knowing AI model context limits
- "Waste" is relative to task relevance, which is subjective

## Success Criteria
- [ ] Budget utilization is calculated correctly
- [ ] Waste is identified with specific examples
- [ ] Recommendations are actionable
