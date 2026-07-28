---
name: architecture-review
description: Use when reviewing the overall architecture of ctxpack — evaluates modularity, separation of concerns, scalability, and dependency management
---

# Architecture Review

## Purpose
Review the architecture of ctxpack for modularity, separation of concerns, scalability, and appropriate abstraction levels.

## Inputs
- ctxpack.py implementation
- SPEC.md
- .ai/docs/architecture-overview.md

## Outputs
- Architecture assessment
- Modularity analysis
- Scalability concerns
- Improvement recommendations

## Workflow
1. Map the function call graph (main → parse_args → scan_files → rank_files → bundle_files → output)
2. Evaluate each function's single responsibility
3. Check for tight coupling between modules
4. Assess scalability for large directories (1000+ files)
5. Evaluate error propagation across the pipeline
6. Check data flow: inputs → processing → outputs

## Architecture Principles
- **Single Responsibility**: Each function does exactly one thing
- **Open/Closed**: Pipeline is open for extension via ranking/bundling
- **Dependency Inversion**: High-level modules don't depend on low-level details
- **Determinism**: No global state, no randomness

## Limitations
- Cannot evaluate against future requirements
- Single-file constraint limits modularity

## Success Criteria
- [ ] Each function has a single responsibility
- [ ] Pipeline is linear and comprehensible
- [ ] No circular dependencies
- [ ] Architecture supports the required use cases
