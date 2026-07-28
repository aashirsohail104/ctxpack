# /cleanup — Repository Cleanup

## Purpose
Identify and suggest cleanup: orphaned files, temp artifacts, unused code, .gitignore improvements.

## Orchestration
1. Invoke `agent-repository-quality`
2. Reference `repository-cleanup` skill

## Output
Cleanup suggestions with categorized actions.

## Usage
```
/cleanup [--dry-run]
```

## Verification
- [ ] Artifact files identified
- [ ] Unused files identified
- [ ] .gitignore suggestions made
- [ ] Safe to execute suggestions
