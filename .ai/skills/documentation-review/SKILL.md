---
name: documentation-review
description: Use when reviewing project documentation for completeness, accuracy, and clarity — checks README, SPEC, docs, and AI toolkit docs
---

# Documentation Review

## Purpose
Review all project documentation for completeness, accuracy, clarity, and consistency with the implementation.

## Inputs
- All documentation files (README.md, SPEC.md, docs/*.md, .ai/docs/*.md, .ai/standards/*.md)

## Outputs
- Documentation completeness report
- Accuracy issues (doc says X, code does Y)
- Clarity issues (confusing or ambiguous passages)
- Missing documentation

## Workflow
1. Read all documentation files
2. Verify README explains what ctxpack is and how to use it
3. Verify SPEC.md is complete and accurate
4. Check docs/*.md for consistency with implementation
5. Verify CLAUDE.md is up to date
6. Check all cross-references between documents
7. Verify .ai/docs/ explains the toolkit philosophy

## Best Practices
- Start with the highest-level document (README) and work down
- Check for outdated information
- Verify that every documented CLI flag actually exists

## Limitations
- Cannot verify documentation against user understanding
- Some docs may describe future plans, not current state

## Success Criteria
- [ ] README explains the project adequately
- [ ] SPEC.md matches implementation
- [ ] No outdated or contradictory information
- [ ] All cross-references are valid
