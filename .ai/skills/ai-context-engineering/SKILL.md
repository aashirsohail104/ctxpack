---
name: ai-context-engineering
description: Use when engineering AI context for coding assistants — designs prompts, optimizes context usage, and structures agent instructions
---

# AI Context Engineering

## Purpose
Design and optimize context for AI coding assistants. Covers prompt structure, progressive disclosure, context budgeting, and agent instruction design.

## Inputs
- Task description
- Available context (files, specs, documentation)
- AI platform constraints

## Outputs
- Optimized context structure
- Progressive disclosure plan
- Context budget allocation
- Agent instructions

## Workflow
1. Analyze the task and identify what context is needed
2. Prioritize context by relevance to the task
3. Design progressive disclosure: what's always loaded vs on-demand
4. Structure the context: critical instructions at edges, details in middle
5. Budget tokens: reserve for system prompt, task, file contents
6. Design fallback: what happens if context is insufficient

## Context Engineering Principles
- **Progressive disclosure**: Load only what's needed, when needed
- **Attention placement**: Critical info at start/end, details in middle
- **Token efficiency**: Every token should earn its place
- **Signal over noise**: Prefer high-signal content over comprehensive listing

## Limitations
- Optimal context structure depends on the AI model
- Context engineering is iterative, not one-shot

## Success Criteria
- [ ] Context is organized by relevance
- [ ] Critical instructions are prominent
- [ ] Token budget is respected
- [ ] Progressive disclosure is designed
