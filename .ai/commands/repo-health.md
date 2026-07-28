# /repo-health — Repository Health Check

## Purpose
Perform a comprehensive health check on the repository: structure, conventions, cleanliness, test health, doc health.

## Orchestration
1. Invoke `agent-repository-quality`
2. Invoke `agent-test-engineering` (test health check)
3. Invoke `agent-documentation` (doc health check)
4. Reference `repository-audit` skill
5. Reference `quality-assurance` skill

## Output
Repository health report across all dimensions.

## Usage
```
/repo-health
```

## Verification
- [ ] Structure is healthy
- [ ] Tests are healthy
- [ ] Docs are healthy
- [ ] No critical issues
