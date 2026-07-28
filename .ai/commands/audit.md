# /audit — Repository Audit

## Purpose
Perform a comprehensive repository audit: structure, naming, cleanliness, unused files.

## Orchestration
1. Invoke `agent-repository-quality`
2. Reference `repository-audit` skill
3. Reference `repository-cleanup` skill

## Output
Repository audit report.

## Usage
```
/audit [--path <path>]
```

## Verification
- [ ] Structure assessed
- [ ] Naming conventions checked
- [ ] Unused files identified
- [ ] Cleanliness evaluated
