---
name: deterministic-output-verification
description: Use when verifying that ctxpack produces byte-identical output for identical inputs — critical for reproducibility
---

# Deterministic Output Verification

## Purpose
Verify that ctxpack produces byte-identical output when run multiple times with identical inputs. Determinism is a core constraint.

## Inputs
- ctxpack.py implementation
- Test directory and arguments

## Outputs
- Determinism verification report
- Sources of non-determinism (if any)

## Workflow
1. Run ctxpack with specific arguments, capture output hash
2. Run ctxpack again with identical arguments, capture output hash
3. Compare hashes — they must match exactly
4. Repeat with different arguments and directories
5. Check for sources of non-determinism: unordered dicts, unsorted lists, time-dependent values, random values, file system order

## Code Patterns to Check
- `sorted()` with explicit keys ✓ (good)
- `set()` iteration ✗ (non-deterministic order)
- `dict.items()` in Python ≥3.7 ✓ (insertion-ordered)
- File system iteration (os.listdir, os.walk) ✗ (order varies by OS/filesystem)
- `os.listdir()` without `sorted()` ✗
- Current time or random values ✗

## Best Practices
- Run verification at least 3 times
- Test with different directories (not just one)
- Verify both stdout and manifest output

## Limitations
- Cannot prove determinism for all possible inputs
- Python version differences can affect behavior

## Success Criteria
- [ ] Multiple identical runs produce identical output
- [ ] No unsorted iterations over unordered collections
- [ ] No time-based or random values in output
