---
name: context-optimization
description: Use when optimizing token usage in ctxpack bundles — analyzes budget allocation, truncation, and content selection efficiency
---

# Context Optimization

## Purpose
Optimize how ctxpack uses its token budget: analyze budget allocation, truncation decisions, and content selection for maximum relevance.

## Inputs
- Bundle output
- Manifest JSON
- Budget value
- File ranking scores

## Outputs
- Budget utilization analysis (% used, wasted)
- Truncation impact assessment
- Recommendation for better selection

## Workflow
1. Calculate budget utilization (used/budget)
2. Check for budget waste (files with low scores that consumed tokens)
3. Assess truncation: are truncated files still useful?
4. Evaluate whether tree inclusion was worth the tokens
5. Compare ranking scores against actual utility

## Best Practices
- Focus on the tradeoff between file count and truncation depth
- Small files with high relevance beat large files with marginal relevance
- Tree diagram is valuable context for AI readers

## Limitations
- Cannot determine "ideal" budget — depends on AI assistant model
- Optimization recommendations are heuristic, not provable

## Success Criteria
- [ ] Budget utilization above 80%
- [ ] No low-scoring files consume significant budget
- [ ] Truncated files still provide useful context
