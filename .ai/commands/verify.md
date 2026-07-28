# /verify — Verify Bundle

## Purpose
Verify that a ctxpack bundle is correct: format, budget, token counting, manifest consistency.

## Orchestration
1. Invoke `agent-bundle-generation` for format check
2. Invoke `agent-manifest-validation` for manifest check
3. Invoke `agent-token-budget` for budget check

## Output
Verification report.

## Usage
```
/verify --out <bundle-file> [--manifest <manifest-file>]
```

## Verification
- [ ] Bundle format is correct
- [ ] Manifest matches bundle
- [ ] Budget was respected
- [ ] Token counting is correct
