# Context Engineering Kit — Skill Reference

**Source**: https://github.com/NeoLabHQ/context-engineering-kit
**Installed to**: `C:\Users\Haroon Traders\.opencode\skills\context-engineering-kit`

## Plugins Available

| Plugin | Focus |
|---|---|
| `customaize-agent` | Context engineering, prompt engineering, agent creation |
| `sdd` | Spec-driven development: plan, implement, brainstorm |
| `sadd` | Sub-agent driven development: parallel/competitive execution |
| `tdd` | Test-driven development, test writing, coverage |
| `kaizen` | Root cause analysis, problem analysis, PDCA |
| `reflexion` | Reflection, critique, memorize patterns |
| `review` | PR review, local changes review |
| `git` | Commits, PR creation, issue analysis |
| `mcp` | MCP server setup (serena, codemap, context7, arxiv) |
| `docs` | Concise writing, documentation updates |
| `fpf` | First principles thinking, hypotheses, status |

## Key Skills for ctxpack

### Sub-Agent Driven Development (sadd)
Use when executing plans with independent tasks. Fresh sub-agent per task + review between tasks. Supports sequential, parallel, and competitive execution patterns.

### Spec-Driven Development (sdd)
Refine, parallelize, and verify draft task specifications into implementation-ready tasks. Multi-agent workflow with quality gates at each phase.

### Context Engineering
Fundamentals of context composition: system prompts, tool definitions, retrieved documents, message history. The discipline of curating the smallest high-signal token set.

### TDD / Test-Driven Development
Write tests first, then implement. Test coverage analysis and fix-tests workflow.

### Kaizen / Root Cause Tracing
Analyze problems, trace root causes, execute PDCA cycles for continuous improvement.

## Notable Sub-skills

| Skill | Plugin | Description |
|---|---|---|
| `context-engineering` | customaize-agent | Context composition fundamentals |
| `prompt-engineering` | customaize-agent | Prompt design patterns |
| `create-agent` | customaize-agent | Agent creation workflow |
| `create-skill` | customaize-agent | Skill creation workflow |
| `create-command` | customaize-agent | Command creation workflow |
| `plan-task` | sdd | Draft → refined implementation plan |
| `implement-task` | sdd | Execute planned implementation |
| `test-driven-development` | tdd | TDD workflow |
| `subagent-driven-development` | sadd | Multi-agent task execution |
| `launch-sub-agent` | sadd | Launch a single sub-agent |
| `do-in-parallel` | sadd | Parallel execution pattern |
| `do-in-steps` | sadd | Sequential execution pattern |
| `do-competitively` | sadd | Competitive execution pattern |
| `reflect` | reflexion | Architectural reflection |
| `critique` | reflexion | Design critique |
| `root-cause-tracing` | kaizen | Root cause analysis |
| `commit` | git | Git commit with formatting |
| `build-mcp` | mcp | MCP server building guide |
| `review-local-changes` | review | Local diff review |

## Directory Structure

```
context-engineering-kit/
├── CLAUDE.md                     # Root context file
├── plugins/
│   ├── customaize-agent/         # Agent/skill/command creation
│   │   ├── skills/
│   │   │   ├── context-engineering/SKILL.md
│   │   │   ├── prompt-engineering/SKILL.md
│   │   │   └── ...
│   │   └── commands/
│   ├── sdd/                      # Spec-driven development
│   │   ├── skills/
│   │   │   ├── plan-task/SKILL.md
│   │   │   ├── implement-task/SKILL.md
│   │   │   └── ...
│   │   └── commands/
│   ├── sadd/                     # Sub-agent driven development
│   │   ├── skills/
│   │   │   ├── subagent-driven-development/SKILL.md
│   │   │   ├── launch-sub-agent/SKILL.md
│   │   │   └── ...
│   │   └── commands/
│   ├── tdd/                      # Test-driven development
│   ├── kaizen/                   # Continuous improvement
│   ├── reflexion/                # Reflection & critique
│   ├── review/                   # Code review
│   ├── git/                      # Git operations
│   ├── mcp/                      # MCP setup
│   └── docs/                     # Documentation
└── .specs/                       # Feature specifications
```
