# Task: Rebuild ctxpack.py

## Objective
Rebuild the complete ctxpack CLI tool as a single Python file using standard library only.

## Specification Reference
SPEC.md at project root — CLI contract, ranking strategy, truncation policy, noise rules, manifest schema.

## Acceptance Criteria
1. CLI: `ctxpack --path <folder> --task "<desc>" --budget <int> [--out <file>] [--manifest <file>]`
2. Exit codes: 0 success, 1 bad args, 2 path not found
3. Token counting: `math.ceil(len(text) / 4)`
4. Budget never exceeded
5. Deterministic output (byte-identical on repeat runs)
6. Manifest with budget, used, included[], excluded[]
7. Noise filtered (.git, node_modules, lockfiles, binaries, etc.)
8. Head truncation for oversized files
9. Compact directory tree in bundle
10. No tracebacks — clean one-line errors to stderr

## Implementation Steps

### Step 1: Constants and Token Counter
- NOISE_DIRS, NOISE_FILES, NOISE_EXTENSIONS, EXTENSION_SCORES, EXT_TO_LANG, STOPWORDS
- `count_tokens(text)` — pure function, math.ceil(len/4)

### Step 2: CLI Scaffold
- CtxArgumentParser (custom argparse with clean errors)
- `parse_args(argv)` — validate --path, --task, --budget, --out, --manifest
- Exit codes: 1 for bad args, 2 for bad path

### Step 3: File Scanner
- `scan_files(root_path)` — recursive os.walk with noise filtering
- Returns (included_files, excluded_files)
- Noise: dirs, filenames, extensions, size > 1MB, minified detection, binary detection

### Step 4: Task Parser + File Ranker
- `parse_task(task_desc)` — lowercase tokenization, stopword filtering
- `get_extension_score(filepath)` — priority map
- `rank_files(included_files, task_keywords)` — TF overlap + extension scoring
- Sort descending by score, then ascending by path for determinism

### Step 5: Directory Tree Builder
- `build_tree(root_path)` — compact tree with unicode chars
- Exclude noise paths from tree

### Step 6: Budget-Aware Packer
- `bundle_files(ranked, budget, tree_str, task_desc, root_path)` 
- Header + task section + tree (if budget >= 500)
- File sections in rank order
- Head truncation with `[... TRUNCATED ...]` marker when file doesn't fit
- Budget never exceeded

### Step 7: Manifest Builder
- `build_manifest(budget, used, included, excluded, task_desc)` — JSON with indent=2, sort_keys
- `one_line_summary(...)` — stderr summary

### Step 8: Main Orchestrator
- `main()` — wire everything, handle stdout encoding fallback

## Risks
- Windows stdout encoding (cp1252) causing UnicodeEncodeError
- Budget boundary conditions with ceil rounding
- File path separator differences (Windows \\ vs Linux /)

## Dependencies
- Python 3.10+ standard library only
- No third-party packages
