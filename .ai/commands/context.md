# /context — Analyze Context

## Purpose
Analyze repository context: extract meaning, understand relationships, and produce a context map for AI assistants.

## Orchestration
1. Invoke `agent-context-analysis`
2. Reference `context-optimization` skill

## Output
Context map with module purposes, dependencies, and relevance ordering.

## Usage
```
/context [--path <path>]
```

## Verification
- [ ] Purpose of each module documented
- [ ] Dependency relationships mapped
- [ ] Context prioritized by relevance
