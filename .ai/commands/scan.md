# /scan — Scan Repository

## Purpose
Scan the repository structure and produce a file inventory.

## Orchestration
1. Invoke `agent-repository-scanner`
2. Reference `project-structure-review` skill

## Output
File inventory with categories (source, test, config, docs)

## Usage
```
/scan [--path <path>]
```

## Verification
- [ ] All files accounted for
- [ ] Dependencies mapped
- [ ] Entry points identified
