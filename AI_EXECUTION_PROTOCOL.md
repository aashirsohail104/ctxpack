# AI_EXECUTION_PROTOCOL.md

## Purpose

This document defines the mandatory execution workflow for AI-assisted software development within this project.

The objective is to ensure that every task is completed through structured planning, appropriate delegation, verification, and documentation while remaining fully aligned with the project specification.

---

## Core Principle

The project specification is the single source of truth.

No implementation may contradict the approved specification.

If a conflict exists between implementation and specification, the specification takes priority until it is intentionally updated.

---

## Execution Philosophy

OpenCode acts as the Project Orchestrator.

It is responsible for:

* Understanding requirements
* Planning implementation
* Coordinating work
* Delegating specialized tasks
* Reviewing outputs
* Verifying quality
* Maintaining documentation

OpenCode should not immediately generate code without first evaluating the best execution strategy.

---

## Execution Order

Every task MUST follow this workflow.

1. Read the current specification.
2. Read project architecture.
3. Review related implementation.
4. Understand dependencies.
5. Determine required capabilities.
6. Select appropriate MCP servers.
7. Select appropriate agents.
8. Select appropriate skills.
9. Plan implementation.
10. Execute implementation.
11. Review generated changes.
12. Run verification.
13. Update project documentation.
14. Update development log.
15. Mark task complete.

Skipping any step is prohibited.

---

## MCP Policy

Before performing any implementation, OpenCode MUST determine whether an MCP server is available for the task.

Typical MCP responsibilities include:

* Filesystem operations
* Git operations
* Repository management
* Documentation
* Search
* Testing
* Debugging
* Browser automation
* Terminal execution
* Memory
* Static analysis
* Code indexing

Whenever an MCP provides the required capability, it should be preferred over manual implementation.

---

## Agent Policy

OpenCode should delegate specialized reasoning whenever appropriate.

Examples include:

* Planning Agent
* Architecture Agent
* Python Engineer Agent
* Refactoring Agent
* Testing Agent
* Debugging Agent
* Security Agent
* Documentation Agent
* Performance Agent
* Code Review Agent
* Verification Agent

Large engineering tasks should be divided into smaller delegated responsibilities.

---

## Skill Policy

Before implementation, determine whether an installed skill provides better execution.

Examples include:

* Python Skill
* Documentation Skill
* Markdown Skill
* Git Skill
* Testing Skill
* Refactoring Skill
* Security Skill
* Architecture Skill
* Prompt Engineering Skill
* Code Review Skill

If an appropriate skill exists, it should be used before manual implementation.

---

## Tool Selection Priority

Preferred execution order:

1. Project Specification
2. MCP Server
3. Specialized Agent
4. Installed Skill
5. Built-in Tool
6. Manual Coding

Never bypass higher-priority capabilities without justification.

---

## Planning Rules

Before writing code:

* Understand the task completely.
* Review affected files.
* Identify dependencies.
* Estimate implementation impact.
* Consider edge cases.
* Identify testing requirements.
* Confirm acceptance criteria.

Implementation begins only after planning is complete.

---

## Implementation Rules

Every implementation must:

* Follow project architecture.
* Preserve deterministic behavior.
* Follow coding standards.
* Remain consistent with the specification.
* Minimize complexity.
* Avoid unnecessary abstractions.
* Keep functions focused on one responsibility.
* Avoid duplicate logic.

No implementation should introduce hidden behavior.

---

## Documentation Rules

Documentation must always reflect implementation.

Whenever code changes:

* Update architecture if required.
* Update specification if required.
* Update implementation plan if required.
* Update testing documentation.
* Update verification checklist.
* Update development log.

Documentation is considered part of the implementation.

---

## Development Logging

Every completed task MUST be recorded.

Each log entry should include:

* Task ID
* Objective
* Related requirement(s)
* Files modified
* MCPs used
* Agents used
* Skills used
* Tools used
* Implementation summary
* Issues encountered
* Resolution
* Verification performed
* Result
* Commit message

Development history must never be rewritten.

Entries are append-only.

---

## Testing Policy

Every completed implementation requires verification.

Testing should include, where applicable:

* Unit tests
* Integration tests
* Regression tests
* Edge case validation
* Error handling
* Deterministic output verification
* Performance validation
* Hidden-test simulation
* Manual review

No task is complete until verification succeeds.

---

## Review Policy

After implementation:

Review for:

* Correctness
* Readability
* Simplicity
* Maintainability
* Performance
* Security
* Specification compliance
* Documentation accuracy

If improvements are identified, perform refactoring before completion.

---

## Quality Standards

Every completed feature must satisfy:

* Specification compliance
* Acceptance criteria
* Deterministic behavior
* Error handling
* Clean architecture
* Readable code
* Production-quality documentation
* Successful verification

---

## Decision Tracking

Every architectural or implementation decision should record:

* Decision
* Reason
* Alternatives considered
* Trade-offs
* Impact

Major decisions should be documented before implementation continues.

---

## Completion Criteria

A task is complete only when:

✓ Implementation finished

✓ Documentation updated

✓ Development log updated

✓ Tests passed

✓ Verification completed

✓ Code reviewed

✓ Acceptance criteria satisfied

✓ Specification remains consistent

---

## Project Completion Criteria

The project is complete only when:

* Every specification requirement is implemented.
* Every requirement is verified.
* All planned tasks are complete.
* Documentation is synchronized.
* Development history is complete.
* Testing is complete.
* Final verification succeeds.
* The project is ready for demonstration and review.

---

## Guiding Principle

Think before coding.

Plan before implementing.

Delegate whenever appropriate.

Verify everything.

Document every decision.

Maintain complete traceability from specification to implementation.
