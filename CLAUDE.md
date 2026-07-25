# CLAUDE.md — ctxpack

## Project Overview

ctxpack is a Python CLI tool that packs relevant project files into a token-budgeted markdown bundle for AI coding assistants. It solves the context window bottleneck.

## Key Constraints

- Python 3.10+, standard library only — no third-party packages, no network calls
- Deterministic output — same input always produces byte-identical output
- Token counting: `math.ceil(len(text) / 4)` — no tiktoken
- Single file implementation: `ctxpack.py`

## CLI Contract (EXACT — hidden tests check this)

```
ctxpack --path <folder> --task "<task description>" --budget <int> [--out <file>] [--manifest <file>]
```

Exit codes: 0 success, 1 bad args, 2 path not found.

## Error Handling Rules

- NEVER print raw tracebacks. Always one-line error to stderr.
- Bad input → exit 1. Missing path → exit 2.
- Use `sys.stderr.write()` for errors, never print exceptions directly.
- Wrap all file operations in try/except.

## Token Counting

```python
import math
tokens = math.ceil(len(text) / 4)
```

The budget applies to the COMPLETE bundle output string — headers, separators, code fences, tree diagram, everything.

## Ranking Strategy

1. Tokenize `--task` into lowercase tokens, filter stopwords and short tokens (< 3 chars)
2. For each file, count how many task tokens appear in content, normalize by file length
3. Score extension: .py/.js/.ts=10, .md=7, .json=3, others=2
4. Final = (keyword_ratio * 0.6) + (extension_score / 10 * 0.4)
5. Sort descending, select top files until budget is full

## Truncation Policy

When a file exceeds remaining budget: include head only up to remaining chars, append `[... TRUNCATED ...]` marker.

## Noise Detection

Skip these paths/patterns:
- `.git/`, `node_modules/`, `__pycache__/`, `.venv/`, `venv/`
- Lockfiles: `package-lock.json`, `yarn.lock`, etc.
- Build artifacts: `dist/`, `build/`, `target/`, `*.pyc`
- Binary/media: `.png`, `.jpg`, `.ico`, `.zip`, `.tar`, etc.
- IDE files: `.DS_Store`, `Thumbs.db`, `.idea/`
- Large files > 1 MB
- Minified files (single line, > 5000 chars, no newlines)
- Non-UTF-8 files
- Stretch: `.gitignore` support

## Manifest Schema

```json
{
  "budget": 8000,
  "used": 7912,
  "included": [{"path": "...", "tokens": 812, "reason": "..."}],
  "excluded": [{"path": "...", "reason": "..."}]
}
```

If no `--manifest`, print one-line to stderr: `"ctxpack: X files included (Y/Z tokens), W files excluded"`

## Bundle Format

```markdown
# ctxpack bundle — <project>

## Task
<description>

## Project Structure
<tree>

## Files

### path/to/file.py

```python
<content>
```
```

## Edge Cases That Must Work

- Empty directory → empty bundle, exit 0
- Single file > budget → head-truncated
- Budget = 0 → error, exit 1
- Binary file → skip, manifest reason
- Bad path → error, exit 2
- Massive file count → rank and select top fits
- Adversarial content → treat as normal text
- Repeat run → byte-identical output

## Implementation Order

1. CLI argument parsing with argparse
2. Token counter utility
3. File scanner with noise filtering
4. Task tokenizer and keyword extractor
5. File ranker (keyword overlap + extension scoring)
6. Packer: budget management, selection, truncation
7. Bundle formatter (markdown output with tree)
8. Manifest generator
9. Main orchestrator wiring everything together
10. Testing and edge case verification

## Code Style

- Single file: `ctxpack.py`
- Functions are ordered: top-level `main()`, then helper functions in call order
- Each function has a single responsibility
- Constants at top of file (NOISE_PATTERNS, EXTENSION_SCORES, STOPWORDS, etc.)
- Deterministic sorting: always use `sorted()` with explicit keys
- No global state
