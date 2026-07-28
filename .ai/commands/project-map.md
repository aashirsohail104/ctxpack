# /project-map — Map Project Structure

## Purpose
Create a detailed project map showing relationships between modules, entry points, and dependencies.

## Orchestration
1. Invoke `agent-repository-scanner` for inventory
2. Invoke `agent-context-analysis` for relationship mapping

## Output
Project map with dependency graph and module relationships.

## Usage
```
/project-map [--path <path>]
```

## Verification
- [ ] Entry points identified
- [ ] Module dependencies mapped
- [ ] Import relationships documented
