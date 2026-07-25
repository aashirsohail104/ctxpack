# JOURNAL.md — ctxpack Post-Mortem

## 1. Three decisions we made, and what we rejected in each case

**Decision 1: TF keyword overlap + extension scoring ranking**
Rejected: Pure filename matching (misses content relevance), import graph analysis (added complexity, can't handle non-Python files), file recency (not deterministic across machines).
Why: The combination ties directly to the task description (the primary signal), adds domain knowledge via extensions, and is fully deterministic using only stdlib.

**Decision 2: Head-only truncation for oversized files**
Rejected: Exclude entirely (wastes potential context), smart head+tail slice (disjointed reading experience, complex implementation).
Why: The head of a file (imports, docstrings, definitions) is the most contextually valuable portion for an AI reader. Head-only is simple, deterministic, and provides coherent content.

**Decision 3: Single-file implementation**
Rejected: Multi-module package with separate cli/scanner/ranker/packer modules.
Why: Single file is simpler for judging, fresh-clone testing, and demo. Fewer imports, simpler execution, and everything is visible in one place. The file is organized with clear section headers separating logical components.

## 2. The hardest bug we hit, and how we found the root cause

**The bug:** Budget overrun at tight boundaries — a bundle with budget 50 was producing 51-55 tokens.

**The hunt:** We initially suspected off-by-one errors in the truncation logic. Debug output showed the issue was in `max_content_chars = remaining * 4 - count_tokens(overhead_str)`. The `count_tokens` function uses `math.ceil(len/4)`, so for a 62-char overhead string it returns 16 tokens (= ceil(62/4) = 16). But 62 chars only uses ceil(62/4) = 16 * 4 = 64 chars worth of budget, not 16*4=64. The actual max content chars should be `remaining * 4 - len(overhead_str)` = 128 - 62 = 66, not 128 - (ceil(62/4)*4) = 128 - 64 = 64.

**The fix:** Use `len(overhead_str)` for char-level calculations, not `count_tokens()`. The invariant `ceil(chars/4) <= remaining` is equivalent to `chars <= remaining * 4`, so we should count actual characters, not token-rounded values, when computing maximum content length.

## 3. Something Claude Code got wrong or confidently misled us on, and how we caught it

**The issue:** Argparse error handling. The initial implementation caught `SystemExit` from argparse with a broken pattern: `except SystemExit: sys.exit(1 if any('required' in e for e in ['']) else 0)`. This was functionally dead code — the conditional `any('required' in e for e in [''])` always evaluates to `False` because the list `['']` is a single empty string, and `'required' in ''` is always `False`. This meant every `SystemExit` was re-exited with code 0 instead of the intended code 1.

**How we caught it:** During edge case testing, we ran missing-arg scenarios and observed exit code 0 instead of the required exit code 1. The broken catch block was silently swallowing the correct exit code.

**The fix:** Removed the broken `try/except` wrapper entirely and subclassed `argparse.ArgumentParser` to override `error()` with clean one-liner output and exit code 1.

## 4. What we would do differently with two more hours

1. **Add .gitignore support**: Parse `.gitignore` patterns and exclude matched files. This is the highest-value stretch goal and would make the tool significantly more useful on real projects.

2. **Performance optimization for 3000+ files**: Profile the scanner to handle large repos efficiently. Current implementation loads all file content into memory — for 3000+ files we should use lazy reading and streaming.

3. **Better path handling**: Normalize all paths to forward slashes in the bundle for cross-platform consistency. Currently backslashes appear on Windows, slashes on Unix.

## 5. Who wrote what

| Person | Contribution |
|---|---|
| **Lead Engineer (AI/OpenCode)** | Full implementation: SPEC.md, ARCHITECTURE.md, CLAUDE.md, AGENTS.md, ctxpack.py, all tests, debugging, documentation |
