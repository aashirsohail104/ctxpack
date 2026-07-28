# Architecture Overview

## Runtime Architecture

ctxpack is a single-file Python CLI (`ctxpack.py`). Its architecture follows a linear pipeline:

1. **Argument parsing** (`parse_args`) — Validate and parse CLI flags
2. **File scanning** (`scan_files`) — Walk directory, filter noise
3. **Task parsing** (`parse_task`) — Extract keywords from task description
4. **File ranking** (`rank_files`) — Score files by relevance
5. **Project tree** (`build_tree`) — Generate directory tree
6. **Budget management** (`bundle_files`) — Select files until budget filled
7. **Bundle output** — Write markdown bundle
8. **Manifest** — Write JSON manifest or one-line summary

## AI Toolkit Architecture

The `.ai/` directory contains an independent AI engineering toolkit with these components:

### Agents (`.ai/agents/`)
Specialized AI assistants that perform specific engineering tasks. Each agent has a system prompt defining its role, responsibilities, and workflow.

### Skills (`.ai/skills/`)
Reusable capabilities that agents and commands invoke. Skills are the building blocks of the toolkit.

### Commands (`.ai/commands/`)
User-invokable operations that orchestrate agents and skills.

### Workflows (`.ai/workflows/`)
Multi-step processes that combine commands, agents, and skills in defined sequences.

### Platform Adapters (`.ai/platforms/`)
Lightweight compatibility layers for different AI coding environments.

## Separation of Concerns

| Layer | Responsibility | AI Dependency |
|-------|---------------|---------------|
| `ctxpack.py` | Runtime execution | None (stdlib only) |
| `.ai/agents/` | AI task specialization | Reading by AI |
| `.ai/skills/` | Reusable capabilities | Reading by AI |
| `.ai/commands/` | User-accessible operations | Platform-specific |
| `.ai/workflows/` | Process orchestration | Reading by AI |
