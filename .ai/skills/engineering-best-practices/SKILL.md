---
name: engineering-best-practices
description: Use when reviewing code for engineering best practices — checks readability, maintainability, error handling, testing patterns, and Python conventions
---

# Engineering Best Practices

## Purpose
Review code for engineering best practices: readability, maintainability, defensive programming, error handling, testing patterns, and Pythonic conventions.

## Inputs
- Source code files

## Outputs
- Best practice compliance report
- Issues found
- Improvement suggestions

## Workflow
1. Check code readability: clear naming, appropriate abstraction, consistent style
2. Check error handling: every failure mode considered, graceful degradation
3. Check defensive programming: input validation, boundary checks
4. Check testing: test coverage, edge cases, meaningful assertions
5. Check determinism: no random/time-dependent behavior
6. Check Pythonic patterns: list comprehensions, context managers, idiomatic stdlib usage

## Python Best Practices Checklist
- [ ] Type hints on all function signatures
- [ ] Docstrings on public functions
- [ ] Context managers for file I/O
- [ ] Consistent naming (snake_case for functions/variables)
- [ ] No wildcard imports
- [ ] Constants are UPPERCASE
- [ ] Functions are small and focused
- [ ] No mutable default arguments

## Limitations
- Some practices are style preferences, not hard rules
- Single-file constraint limits some best practices

## Success Criteria
- [ ] Code is readable and well-structured
- [ ] Error handling is comprehensive
- [ ] Tests cover edge cases
- [ ] Pythonic idioms are used appropriately
