# Implementation Plan — ctxpack

## Phase 0: Spec Kit Documentation (First Commit)

| Task | Files | Acceptance Criteria |
|---|---|---|
| 0.1 SPEC.md | `SPEC.md` | CLI contract, ranking strategy, truncation policy, noise rules, definition of done |
| 0.2 README.md | `README.md` | Clone-to-run in under 5 minutes |
| 0.3 CLAUDE.md | `CLAUDE.md` | Complete context for Claude Code |
| 0.4 AGENTS.md | `AGENTS.md` | Agent configuration and delegation rules |
| 0.5 ARCHITECTURE.md | `ARCHITECTURE.md` | Component breakdown and data flow |
| 0.6 IMPLEMENTATION_PLAN.md | `IMPLEMENTATION_PLAN.md` | This file — task breakdown |
| 0.7 DEVELOPMENT_LOG.md | `DEVELOPMENT_LOG.md` | Append-only log initialized |

**First commit**: SPEC.md only. Second commit: remaining spec kit documents.

---

## Phase 1: Core Implementation

### Task 1.1 — CLI Scaffold

**Objective**: Implement argument parsing with argparse, error handling, exit codes.

**Acceptance Criteria**:
- All 5 flags work (--path, --task, --budget, --out, --manifest)
- Missing required flags → exit 1 with one-line error
- Non-integer --budget → exit 1
- Bad --path → exit 2
- --path is file not dir → exit 2
- No raw tracebacks

**Files**: `ctxpack.py`

**Dependencies**: None

**Verification**:
```bash
python ctxpack.py  # error: --path required, exit 1
python ctxpack.py --path nonexistent --task "x" --budget 100  # exit 2
python ctxpack.py --path . --task "x" --budget abc  # exit 1
python ctxpack.py --path . --task "x" --budget 100  # exit 0 (empty bundle)
```

---

### Task 1.2 — Token Counter

**Objective**: Implement `count_tokens(text)`.

**Acceptance Criteria**:
- `count_tokens("hello")` = 2
- `count_tokens("")` = 0
- `count_tokens("a" * 100)` = 25
- Uses `math.ceil(len(text) / 4)`

**Files**: `ctxpack.py`

**Dependencies**: None

**Verification**: Unit test with known values.

---

### Task 1.3 — File Scanner

**Objective**: Recursively walk --path, filter noise, detect binaries.

**Acceptance Criteria**:
- Yields all readable text files
- Skips .git, node_modules, __pycache__, .venv
- Skips lockfiles, build artifacts, media files
- Skips non-UTF-8 files (detected by read attempt)
- Skips files > 1 MB
- Handles permission errors gracefully
- Sorted output for determinism

**Files**: `ctxpack.py`

**Dependencies**: Task 1.1

**Verification**: Point at a sample project with noise; verify noise is excluded.

---

### Task 1.4 — Task Parser + Ranker

**Objective**: Tokenize task description, rank files by relevance.

**Acceptance Criteria**:
- Tokenizes task into keywords (lowercase, no stopwords, min 3 chars)
- Scores files by keyword overlap + extension priority
- Higher keyword overlap = higher score
- .py/.js files score higher than .json for same keyword overlap
- Deterministic sort

**Files**: `ctxpack.py`

**Dependencies**: Task 1.2, Task 1.3

**Verification**: Create files with varying relevance; verify ranking order.

---

### Task 1.5 — Directory Tree Builder

**Objective**: Build compact text tree of project structure.

**Acceptance Criteria**:
- Text format with `├──`, `└──`, `│` characters
- Excludes noise directories from tree
- Handles empty directories
- Returns string, token-counted

**Files**: `ctxpack.py`

**Dependencies**: None

**Verification**: Visual inspection of tree output.

---

### Task 1.6 — Packer (Budget Management)

**Objective**: Select files within budget, handle truncation.

**Acceptance Criteria**:
- Never exceeds budget
- Includes full files in rank order
- Head-truncates oversized files with `[... TRUNCATED ...]` marker
- Includes directory tree if budget permits (> 500 tokens)
- Produces complete bundle string

**Files**: `ctxpack.py`

**Dependencies**: Task 1.4, Task 1.5

**Verification**:
```bash
python ctxpack.py --path . --task "test" --budget 1000 --out bundle.md
# Verify bundle.md tokens <= 1000
```

---

### Task 1.7 — Manifest Builder

**Objective**: Generate manifest JSON or one-line summary.

**Acceptance Criteria**:
- JSON manifest with exact schema (budget, used, included[], excluded[])
- Included entries have path, tokens, reason
- Excluded entries have path, reason
- One-line stderr when --manifest is absent
- Deterministic JSON output (sort_keys=True, indent=2)

**Files**: `ctxpack.py`

**Dependencies**: Task 1.6

**Verification**: Inspect JSON output; verify all files accounted for.

---

### Task 1.8 — Main Orchestrator

**Objective**: Wire all components together in `main()`.

**Acceptance Criteria**:
- Complete end-to-end flow: args → scan → rank → pack → output
- Correct exit codes in all scenarios
- No tracebacks

**Files**: `ctxpack.py`

**Dependencies**: Tasks 1.1–1.7

**Verification**: Full integration test with sample project.

---

## Phase 2: Testing & Polish

### Task 2.1 — Determinism Test

**Objective**: Verify byte-identical output on repeat runs.

**Acceptance Criteria**: Two runs with same args produce identical output files.

**Verification**: `fc /b` on Windows or `diff` on Unix.

---

### Task 2.2 — Edge Case Tests

**Objective**: Test all edge cases from SPEC.md.

**Acceptance Criteria**: Each edge case produces correct behavior.

| Case | Expected |
|---|---|
| Empty directory | Bundle with tree only, exit 0 |
| Single file > budget | Head-truncated |
| Budget = 0 | Exit 1 |
| Binary file | Skipped in manifest |
| Bad path | Exit 2 |
| Adversarial content | Treated as text |
| Massive file count | Processes and ranks |

---

### Task 2.3 — .gitignore Support (Stretch)

**Objective**: Parse and respect .gitignore patterns.

**Acceptance Criteria**: Files matching .gitignore patterns are excluded.

---

### Task 2.4 — Performance Check (Stretch)

**Objective**: 3000 files in under 30 seconds.

**Acceptance Criteria**: Generates 3000 small files and runs ctxpack in < 30s.

---

## Phase 3: Final Documentation

### Task 3.1 — PROMPTS.md

Document 5 most important prompts used during development.

### Task 3.2 — JOURNAL.md

Answer 5 reflection questions (post-implementation).

### Task 3.3 — Final DEVELOPMENT_LOG.md Entry

Record final task completions.

---

## Commit Strategy

| Commit | Contents |
|---|---|
| 1 | `SPEC.md` |
| 2 | All remaining spec kit documents |
| 3 | `ctxpack.py` — complete implementation |
| 4+ | Bug fixes, edge case patches, documentation updates |
