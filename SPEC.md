# ctxpack — Specification

## Overview

`ctxpack` is a Python command-line tool that packs relevant project files into a single markdown bundle constrained by a token budget. It solves the context window bottleneck for AI coding assistants by selecting the most task-relevant files from a codebase and producing one optimized context bundle.

---

## CLI Contract

### Interface

```
ctxpack --path <folder> --task "<task description>" --budget <int> [--out <file>] [--manifest <file>]
```

### Flags

| Flag | Required | Description |
|---|---|---|
| `--path` | Yes | Folder to pack. Must be a readable directory. |
| `--task` | Yes | Free-text description of the developer's task. Used for relevance ranking. |
| `--budget` | Yes | Maximum tokens for the entire bundle output (inclusive of headers, separators, tree). |
| `--out` | No | File path to write the bundle. If omitted, write to stdout. |
| `--manifest` | No | File path to write the manifest JSON. If omitted, print a one-line summary to stderr. |

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success — bundle produced within budget |
| `1` | Invalid arguments — missing required flag, bad flag value, etc. |
| `2` | Path not found or unreadable |

### Error Handling

All errors produce a single-line error message to stderr and the appropriate exit code. No raw Python tracebacks are ever printed.

---

## Token Counting

### Rule

```python
import math
tokens = math.ceil(len(text) / 4)
```

- Every character counts: whitespace, newlines, punctuation.
- The budget applies to the **complete bundle output string**, including all headers, file paths, separators, code fences, and the directory tree.
- No external tokenizers (tiktoken, etc.) are used.
- This rule is deterministic and identical across all implementations.

---

## Ranking Strategy

### Approach: Weighted TF Keyword Overlap + Extension Scoring

**Why this approach:**
- TF-IDF-style keyword overlap directly ties relevance scoring to the developer's task description, which is the primary signal of what matters.
- Extension scoring adds domain knowledge: `.py` files are more likely relevant than `.json` for most coding tasks.
- The combination is deterministic, uses only Python stdlib, and produces explainable scores that can be reported in the manifest.

### Algorithm

1. **Tokenize `--task`**: Split the task description into lowercase tokens, filtering out common English stopwords and short tokens (< 3 chars).
2. **Tokenize each file**: Read file content, lowercase, extract word tokens.
3. **Score keyword overlap**: Count how many task tokens appear in the file content. Normalize by file length to avoid biasing toward huge files.
4. **Score extension**: Assign a base priority score by extension:
   - `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.go`, `.rs`, `.java`, `.c`, `.cpp`, `.h`, `.hpp` = 10
   - `.md`, `.rst`, `.txt` = 7
   - `.yaml`, `.yml`, `.toml`, `.cfg`, `.ini`, `.conf` = 5
   - `.json`, `.xml`, `.csv` = 3
   - `.css`, `.scss`, `.less`, `.html` = 4
   - `.sh`, `.bat`, `.ps1`, `Makefile`, `Dockerfile` = 6
   - All other text extensions = 2
5. **Combine score**: `final_score = (keyword_overlap_ratio * 0.6) + (extension_score / 10 * 0.4)`
6. **Sort descending** by final score.

### Alternatives Considered and Rejected

| Alternative | Reason Rejected |
|---|---|
| Pure filename substring matching | Misses content relevance entirely; files named `utils.py` would never rank regardless of content. |
| Directory depth scoring only | Ignores the task description; would rank all shallow files equally. |
| Import graph analysis | Requires parsing Python imports; adds complexity, fragility, and cannot work for non-Python files. Not worth the marginal gain. |
| File recency (mtime) | Not deterministic across different machines/filesystems; irrelevant to task relevance. |
| Pure keyword overlap (no extension) | Would rank README.md and large data files above source code; extension signal is necessary. |

---

## Truncation Policy

### Rule: Include Head-Only

When a file's content exceeds the remaining token budget:

1. Calculate how many characters fit within the remaining budget: `max_chars = remaining_budget * 4`
2. Include the first `max_chars` characters of the file (head-only truncation).
3. Append a truncation marker: `[... TRUNCATED: file exceeds remaining budget ...]`
4. Record in the manifest: `"truncated": true`, `"reason": "Head-only truncation: file too large for remaining budget"`.

**Why head-only:**
- The head of a file typically contains imports, docstrings, type definitions, and class/function signatures — the most contextually valuable portion for an AI reader.
- Tail-only or middle slicing would lose this structural information.
- Head-only is deterministic, simple to implement, and easy to explain.
- A smart head+tail slice would require the AI to read disjointed content; head-only provides a coherent reading experience.

### Alternatives Considered and Rejected

| Alternative | Reason Rejected |
|---|---|
| Exclude entirely | Wastes the opportunity to include partial but valuable context. |
| Smart slice (head + tail) | Produces disjointed content; harder to implement deterministically; marginal benefit over head-only. |
| Include tail only | Loses imports, definitions, and entry points — the most important context. |

### Edge Case: File Larger Than Entire Budget

If a single file is larger than the entire budget, include only the portion that fits (head-only). The directory tree and headers must fit within the budget as well, so the file portion will be strictly `(budget - overhead) * 4` characters. If even the overhead doesn't fit, produce an error.

---

## Noise Detection

### Categories of Noise

| Category | Detection Method | Manifest Reason |
|---|---|---|
| Version control | Directory named `.git`, `.svn`, `.hg` | "Version control directory" |
| Package dependencies | `node_modules/`, `vendor/`, `.venv/`, `venv/`, `env/`, `__pycache__/`, `.eggs/`, `*.egg-info/`, `*.pyc`, `*.pyo` | "Build/dependency artifact" |
| Lockfiles | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Gemfile.lock`, `poetry.lock`, `Cargo.lock` | "Lockfile — auto-generated" |
| Build artifacts | `dist/`, `build/`, `target/`, `.next/`, `.nuxt/`, `*.o`, `*.class`, `*.jar`, `*.war` | "Build artifact" |
| Binary files | File read error due to non-UTF-8 encoding + extension check | "Binary or unreadable file" |
| IDE/OS files | `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` | "IDE/OS metadata file" |
| Archive files | `.zip`, `.tar`, `.gz`, `.bz2`, `.rar`, `.7z` | "Archive file" |
| Image/Media files | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`, `.mp4`, `.mp3`, `.wav` | "Media file" |
| Large generated files | File size > 1 MB | "Large file — may be generated" |
| Minified files | Single-line files > 5000 chars with no newlines | "Minified file — likely generated" |

### Detection Algorithm

1. **Path-based filtering**: Check directory/file name against noise patterns before attempting to read.
2. **Extension-based filtering**: Skip known binary/media/archive extensions.
3. **Read attempt**: Try to read as UTF-8. If decoding fails, treat as binary.
4. **Post-read heuristics**: Check file size, line count, and minification patterns.

### .gitignore Support (Stretch)

If `.gitignore` is present at the root of `--path`, parse its patterns and exclude matched files. This augments the built-in noise list rather than replacing it.

---

## Manifest Schema

### Exact JSON Structure

```json
{
  "budget": 8000,
  "used": 7912,
  "included": [
    {
      "path": "src/agent.py",
      "tokens": 812,
      "reason": "Relevance score: 0.87 — keyword match (agent, run, task) + .py extension"
    }
  ],
  "excluded": [
    {
      "path": "package-lock.json",
      "reason": "Lockfile — auto-generated"
    }
  ]
}
```

### Keys

| Key | Type | Description |
|---|---|---|
| `budget` | int | The budget passed via `--budget` |
| `used` | int | Total tokens used in the bundle |
| `included` | array | Files selected for the bundle. Each entry has `path`, `tokens`, `reason`. |
| `excluded` | array | Files considered but excluded. Each entry has `path`, `reason`. |

### One-Line Summary (stderr, no --manifest flag)

```
ctxpack: 8 files included (7912/8000 tokens), 142 files excluded
```

---

## Bundle Output Format

### Structure

```
# ctxpack bundle — <project name>

## Task
<task description>

## Project Structure
<compact tree diagram>

## Files

### path/to/file.py

```<language>
<content or first N chars + truncation marker>
```
```

### Directory Tree

A compact text-based tree diagram. Format:

```
project/
├── src/
│   ├── agent.py
│   └── utils.py
├── tests/
│   └── test_agent.py
└── README.md
```

The tree is included only if budget permits (target: ~200-300 tokens). If the budget is extremely small (< 500 tokens total), the tree is excluded and noted in the manifest.

---

## Definition of Done

`ctxpack` is complete when:

1. **CLI contract met**: All flags work as specified; exit codes (0, 1, 2) are correct.
2. **Token counting correct**: `math.ceil(len(text) / 4)` is used for every token calculation.
3. **Budget never exceeded**: The complete bundle output never exceeds `--budget` by a single token.
4. **Manifest complete**: Every file considered is accounted for — included or excluded with reason.
5. **Noise filtered**: `.git`, `node_modules`, lockfiles, build artifacts, binaries are excluded.
6. **Deterministic**: The same command twice produces byte-identical output.
7. **Graceful error handling**: Bad input → one-line error + correct exit code, never a traceback.
8. **Ranking relevant**: Files are sorted by task relevance before selection.
9. **Truncation handled**: Files too large for remaining budget are head-truncated with a clear marker.
10. **Directory tree included**: Compact tree in bundle if budget permits.
11. **All edge cases handled**: Empty directory, single huge file, tiny budget, binary files, adversarial content, massive file counts.
12. **Tested and verified**: All tests pass, deterministic output confirmed, edge cases verified.

---

## Edge Case Handling

| Case | Behavior |
|---|---|
| Empty directory | Produces empty bundle (just tree or header), exit 0 |
| Single file > budget | Head-truncated, included with truncation marker |
| Budget = 0 | Error: "Budget must be a positive integer", exit 1 |
| Budget = 1 | Include what fits (likely just header) |
| Binary/non-UTF-8 file | Skip, manifest reason: "Binary or unreadable file" |
| Bad path (not found) | Error: "Path not found: <path>", exit 2 |
| Bad path (file, not dir) | Error: "Path is not a directory: <path>", exit 2 |
| Missing --path | Error: "--path is required", exit 1 |
| Missing --task | Error: "--task is required", exit 1 |
| Missing --budget | Error: "--budget is required", exit 1 |
| Non-integer --budget | Error: "--budget must be an integer", exit 1 |
| Negative --budget | Error: "--budget must be a positive integer", exit 1 |
| Very large file count | Process all files, rank by relevance, select top fits |
| Adversarial content (injection prompts) | Treated as normal text content — no special handling needed as we don't execute the content |
| Repeat run | Byte-identical output (deterministic ranking, sorting) |
| Permission denied on file | Skip, manifest reason: "Permission denied" |
| Symlink loops | Skip broken symlinks, manifest reason: "Unreadable file (symlink loop)" |

---

## Future Considerations (Out of Scope for V1)

- MCP server interface exposing the same selection logic
- Plugin system for custom rankers
- Caching for repeated runs on the same project
- Integration with AI coding assistant APIs
- Support for multiple task descriptions
