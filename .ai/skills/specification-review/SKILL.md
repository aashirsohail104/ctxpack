---
name: specification-review
description: Use when reviewing specification documents for completeness, consistency, and correctness — validates SPEC.md against implementation
---

# Specification Review

## Purpose
Review specification documents (SPEC.md) for completeness, consistency, and correctness against the implementation.

## Inputs
- Specification file (SPEC.md)
- Implementation file (ctxpack.py)

## Outputs
- Gap analysis: specified but not implemented
- Consistency issues: conflicts between spec sections or between spec and code
- Correctness: spec behaviors that don't match actual behavior

## Workflow
1. Read the specification fully
2. Extract every behavioral claim (CLI flags, exit codes, error messages, token counting, ranking, manifest format, bundle format)
3. For each claim, verify it against the implementation
4. Report gaps, inconsistencies, and errors
5. Check for undefined behaviors (spec omissions)

## Best Practices
- Treat SPEC.md as authoritative — code should match spec, not vice versa
- Be specific: cite exact line numbers from both spec and implementation
- Distinguish between "spec missing" and "implementation wrong"

## Limitations
- Cannot verify subjective claims (e.g., "easy to use")
- Spec may describe future features not yet implemented

## Success Criteria
- [ ] Every behavioral claim in spec is matched to implementation code
- [ ] No contradictions between spec sections
- [ ] All edge cases in spec are handled in implementation
