---
name: context-packing
description: Use when analyzing how ctxpack selects and packs files into a markdown bundle — validates the packing pipeline
---

# Context Packing

## Purpose
Analyze and validate the ctxpack file selection and packing pipeline: scanning, ranking, budget management, and bundle generation.

## Inputs
- Project directory
- Task description
- Budget value
- ctxpack.py implementation

## Outputs
- Packing pipeline analysis
- Selection correctness verification
- Budget compliance check

## Workflow
1. Understand the packing pipeline: scan → rank → budget → bundle
2. Verify scanner correctly filters noise
3. Verify ranker correctly scores and sorts files
4. Verify budget allocator respects limits
5. Verify bundle formatter produces correct markdown
6. Check edge cases: empty dir, single file, budget=1, etc.

## Best Practices
- Start from SPEC.md to understand expected behavior
- Test with small directories where results are manually verifiable
- Verify the "deterministic output" property explicitly

## Limitations
- Cannot test against real-world large codebases without running the tool
- Ranking "correctness" is subjective; verify algorithm not preference

## Success Criteria
- [ ] Scanner produces correct included/excluded lists
- [ ] Ranker sorts files by task relevance
- [ ] Budget never exceeded
- [ ] Bundle format matches SPEC.md
