# Specification Compliance Prompt

## Purpose
Prompt an AI to verify spec compliance.

## Template
```
Verify that [implementation] complies with [specification].

For each section in the spec:
1. Extract behavioral claims
2. Find corresponding implementation code
3. Verify behavior matches
4. Report any gaps

Focus on:
- CLI flags and arguments
- Exit codes
- Error messages
- Token counting
- Ranking algorithm
- Output format
- Edge cases
```
