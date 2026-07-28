# /bundle — Generate Bundle

## Purpose
Generate a complete ctxpack bundle with ranked files, tree diagram, and proper formatting.

## Orchestration
1. Invoke `agent-repository-scanner` for file inventory
2. Invoke `agent-context-ranking` for relevance scoring
3. Invoke `agent-token-budget` for budget management
4. Invoke `agent-bundle-generation` for markdown output

## Output
Complete ctxpack markdown bundle.

## Usage
```
/bundle --path <path> --task "<desc>" --budget <int> [--out <file>]
```

## Verification
- [ ] Bundle format matches SPEC.md
- [ ] Budget never exceeded
- [ ] All files included with proper formatting
