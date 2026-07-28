# /spec-check — Specification Compliance Check

## Purpose
Verify that the implementation matches the specification (SPEC.md) exactly.

## Orchestration
1. Invoke `agent-architecture` for spec review
2. Reference `specification-review` skill

## Output
Spec compliance report with gaps and inconsistencies.

## Usage
```
/spec-check
```

## Verification
- [ ] Every behavioral claim in spec is implemented
- [ ] No implementation behavior contradicts spec
- [ ] All error messages match spec exactly
