# Architecture — ctxpack

## Design Philosophy

Single-file CLI tool using Python standard library only. No external dependencies, no network calls. Designed for deterministic, auditable output.

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    CLI      │────▶│   Scanner   │────▶│   Ranker    │────▶│   Packer    │
│  (argparse) │     │ (walk+filter)│     │ (TF+ext)    │     │ (budget mgmt)│
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                   │
                                                          ┌────────▼────────┐
                                                          │  Formatter      │
                                                          │  (bundle + man) │
                                                          └─────────────────┘
```

## Component Breakdown

### 1. CLI Module (`parse_args()`)

Parses command-line arguments via `argparse`. Validates inputs and returns a namespace. All error handling (missing args, bad types, nonexistent paths) happens here with appropriate exit codes.

### 2. Token Counter (`count_tokens(text)`)

Pure function. `math.ceil(len(text) / 4)`. Used everywhere token counts are needed.

### 3. Scanner (`scan_files(path)`)

Recursively walks `--path`, yielding `FileInfo` tuples:
- `path`: relative path string
- `full_path`: absolute path string
- `size`: file size in bytes

Filters out noise at the path level before attempting to read. Yields lazily — doesn't load all files into memory at once.

### 4. File Reader (`read_file(full_path)`)

Attempts UTF-8 decode. Returns content string or `None` if unreadable/binary. Wraps all I/O in try/except.

### 5. Task Parser (`parse_task(task_desc)`)

Tokenizes the task description: lowercase, split, filter stopwords and short tokens. Returns a `set` of keywords.

### 6. Ranker (`rank_files(files, task_keywords)`)

For each readable file:
- Count task keyword occurrences in content
- Normalize by file length → keyword ratio
- Look up extension score from EXTENSION_SCORES dict
- Compute: `(keyword_ratio * 0.6) + (extension_score / 10 * 0.4)`
- Sort descending by score

Returns list of `(path, content, score, token_count)` tuples.

### 7. Directory Tree (`build_tree(path)`)

Recursively builds a compact text-based tree. Excludes noise paths. Returns a string.

### 8. Packer (`pack_files(ranked_files, budget, tree_str, task_desc)`)

The core algorithm:
1. Reserve tokens for bundle overhead (header, task, tree, separators)
2. Iterate ranked files in score order
3. For each file: if `content_token_count <= remaining`, include full content
4. If `content_token_count > remaining`, head-truncate to fit
5. Stop when budget is exhausted or all files are processed
6. Return bundle string, included list, excluded list

### 9. Manifest Builder (`build_manifest(...)`)

Constructs the manifest dict with budget, used, included[], excluded[]. Serializes to JSON with `indent=2` for deterministic output.

### 10. Main Orchestrator (`main()`)

Wires everything together:
1. Parse args
2. Validate path exists and is a directory (exit 2 if not)
3. Scan files
4. Parse task
5. Build tree
6. Rank files
7. Pack files
8. Write bundle (--out or stdout)
9. Write manifest (--manifest or stderr one-liner)
10. Exit 0

## Data Flow

```
CLI args → Scanner → [(path, full_path, size), ...]
                    → Reader → [(path, content, token_count), ...]
Task desc → Parser → {keywords}
Scanner output + keywords → Ranker → [(path, content, score), ...]
Ranker output + budget + tree → Packer → bundle_string, included[], excluded[]
Packer output → Formatter → bundle.md + manifest.json
```

## Determinism Guarantees

1. `sorted()` with explicit keys everywhere — never rely on dict/hash ordering
2. `json.dumps(indent=2, sort_keys=True)` for manifest
3. Same file list order every time (os.walk order can vary → sort before processing)
4. Same ranking scores (pure function of input)
5. Same truncation decisions (pure function of budget and content)

## File Structure

```
ctxpack/
├── ctxpack.py                  # CLI implementation
├── SPEC.md                     # Specification
├── README.md                   # Quick start
├── CLAUDE.md                   # Claude Code context
├── AI_EXECUTION_PROTOCOL.md    # Workflow protocol
├── .gitignore
├── docs/
│   ├── AGENTS.md               # Agent configuration
│   ├── ARCHITECTURE.md         # This file
│   ├── IMPLEMENTATION_PLAN.md  # Task breakdown
│   ├── DEVELOPMENT_LOG.md      # Build history
│   ├── PROMPTS.md              # Key prompts
│   └── JOURNAL.md              # Reflection
└── sample_project/             # Test fixture
```

## Noise Patterns (Built-in)

```python
NOISE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv',
              'env', '.eggs', 'dist', 'build', 'target', '.next',
              '.nuxt', '.idea', '.vscode', '.svn', '.hg'}
NOISE_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
               'Gemfile.lock', 'poetry.lock', 'Cargo.lock',
               '.DS_Store', 'Thumbs.db'}
NOISE_EXTENSIONS = {'.pyc', '.pyo', '.png', '.jpg', '.jpeg', '.gif',
                    '.svg', '.ico', '.zip', '.tar', '.gz', '.bz2',
                    '.rar', '.7z', '.mp4', '.mp3', '.wav', '.o',
                    '.class', '.jar', '.war', '.exe', '.dll', '.so',
                    '.dylib', '.bin'}
```
