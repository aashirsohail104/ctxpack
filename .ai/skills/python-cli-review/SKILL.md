---
name: python-cli-review
description: Use when reviewing Python CLI tool implementation — checks argparse usage, error handling, exit codes, and CLI contract compliance
---

# Python CLI Review

## Purpose
Review Python CLI implementation for correctness, error handling, and compliance with the CLI contract defined in SPEC.md.

## Inputs
- ctxpack.py implementation
- SPEC.md CLI section

## Outputs
- CLI contract compliance report
- Argparse usage issues
- Error handling gaps
- Exit code correctness

## Workflow
1. Verify all required flags exist: `--path`, `--task`, `--budget`
2. Verify all optional flags exist: `--out`, `--manifest`
3. Check argparse configuration: types, required, help text
4. Verify error handling: bad input → exit 1, path not found → exit 2
5. Check that errors go to stderr, not stdout
6. Verify no raw tracebacks are ever printed
7. Check exit code 0 on success
8. Verify --out writing and --manifest writing work correctly

## Error Handling Checklist
- [ ] Missing required arg → exit 1 with message
- [ ] Invalid budget value → exit 1 with message
- [ ] Budget ≤ 0 → exit 1 with message
- [ ] Path not found → exit 2 with message
- [ ] Path is file not dir → exit 2
- [ ] Cannot write --out → exit 1 with message
- [ ] Cannot write --manifest → exit 1 with message

## Best Practices
- Use custom ArgumentParser subclass for error handling
- Never let argparse print to stdout on error
- Wrap all file I/O in try/except

## Limitations
- Can only verify static code analysis, not runtime behavior
- Some errors depend on OS permissions (cannot test without running)

## Success Criteria
- [ ] CLI contract matches SPEC.md exactly
- [ ] All error cases handled with appropriate exit codes
- [ ] No tracebacks possible
