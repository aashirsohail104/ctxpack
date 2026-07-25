# PROMPTS.md — 5 Most Important Prompts

## Prompt 1: Architecture and Ranking Strategy Decision

**What we asked:**
"Ranking strategy: How should ctxpack score file relevance against the --task description? Options: TF keyword overlap + extension scoring, Simple extension + depth scoring, Filename substring matching. Truncation policy: Include head only vs Exclude entirely vs Smart head+tail slice. Directory tree in bundle: worth the token cost? File structure: Single file vs package?"

**What we got back:**
TF keyword overlap + extension scoring, head-only truncation, include compact tree (~200-300 tokens), single file implementation.

**What we changed and why:**
We went with all recommended options. The TF keyword overlap approach is deterministic, uses only stdlib, and ties directly to the task description. Head-only truncation preserves imports/docstrings (most contextually valuable). Single file simplifies judging and testing.

---

## Prompt 2: Specification Document Creation

**What we asked:**
Read the full hackathon brief and produce a complete SPEC.md covering CLI contract, ranking strategy justification, truncation policy, noise detection, edge case handling, and definition of done.

**What we got back:**
A comprehensive 285-line SPEC.md with all required sections, including alternatives-considered tables for every major decision.

**What we changed and why:**
Added explicit edge case handling tables (empty dir, single huge file, adversarial content, repeat runs). Clarified that the budget applies to the complete bundle output string. Defined exact stopword filtering rules for task tokenization.

---

## Prompt 3: Budget-Aware Packer Implementation

**What we asked:**
Implement bundle_files() that takes ranked files, budget, tree string, and task description, and produces a markdown bundle never exceeding the budget. Include head truncation when files don't fit.

**What we got back:**
Initial implementation had a bug where `remaining * 4 - count_tokens(overhead)` overestimated available chars due to `ceil()` rounding in `count_tokens()`. This caused budget overruns at tight boundaries.

**What we changed and why:**
Fixed by using `len(overhead_str)` instead of `count_tokens(overhead_str)` in the char-level calculation. The `remaining * 4 - len(overhead_str)` calculation is the correct max content chars because `ceil(chars/4) <= remaining` requires `chars <= remaining * 4`. Also changed `used` calculation from `budget - remaining` (sum of per-section ceil values) to `count_tokens(bundle)` on the final assembled string for accuracy.

---

## Prompt 4: Error Handling and Exit Codes

**What we asked:**
Implement proper CLI error handling with exit codes 0/1/2, clean one-line error messages, no tracebacks.

**What we got back:**
Initial implementation used argparse with `required=True` and caught `SystemExit` — but argparse's default error handler printed ugly usage messages and exited with code 2.

**What we changed and why:**
Subclassed `argparse.ArgumentParser` to override `error()` with a clean one-liner to stderr and exit code 1. Removed the broken `try/except SystemExit` wrapper in `main()`. This gives clean "Error: --path is required" messages instead of argparse's multi-line usage output.

---

## Prompt 5: Windows Compatibility and Encoding

**What we asked:**
Make ctxpack work on Windows — handle stdout encoding, file path separators, and UTF-8 file I/O.

**What we got back:**
The em dash character (\u2014) in the bundle header caused `UnicodeEncodeError: 'charmap' codec can't encode character` when writing to stdout on Windows (cp1252 encoding).

**What we changed and why:**
Replaced all em dashes with ASCII-safe `--` (double hyphen). Added `sys.stdout.reconfigure(encoding='utf-8')` fallback when stdout write fails with `UnicodeEncodeError`. All file I/O uses explicit `encoding='utf-8'`. Path separators use `os.path.join` and display as-is (backslashes on Windows, forward slashes on Linux) — the tool is encoding-aware but separator-agnostic.
