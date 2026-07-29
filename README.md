# ctxpack

Context packing tool for AI coding assistants. Selects and packs the most task-relevant files from a project folder into a single markdown bundle that fits a token budget.

---

## Quick Start

### Prerequisites

- Python 3.10+
- No third-party packages required

### Clone and Run

```bash
git clone <repo-url> ctxpack
cd ctxpack
python ctxpack.py --path ./my-project --task "implement a sorting algorithm" --budget 4000 --out bundle.md
```

---

## Usage

### Basic

```bash
python ctxpack.py --path /path/to/project --task "fix bug in login handler" --budget 8000
```

Writes bundle to stdout, prints one-line summary to stderr.

### Write to File

```bash
python ctxpack.py --path . --task "add tests" --budget 6000 --out context.md
```

### Write Manifest

```bash
python ctxpack.py --path . --task "refactor module" --budget 10000 --manifest manifest.json
```

### Everything

```bash
python ctxpack.py --path src/ --task "add error handling" --budget 5000 --out bundle.md --manifest manifest.json
```

---

## CLI Reference

| Flag | Required | Description |
|---|---|---|
| `--path` | Yes | Folder to pack |
| `--task` | Yes | Task description for relevance ranking |
| `--budget` | Yes | Maximum token budget for the bundle |
| `--out` | No | Output file (default: stdout) |
| `--manifest` | No | Manifest JSON file (default: one-line to stderr) |

### Exit Codes

- `0` — Success
- `1` — Invalid arguments
- `2` — Path not found or unreadable

---

## Output

The bundle is a markdown file containing:

- Task description
- Project structure tree
- Selected file contents with syntax-highlighted code blocks
- Truncation markers where files are cut to fit budget

The manifest is a JSON file accounting for every file considered.

---

## How It Works

1. **Scan**: Recursively walk the project folder, filtering out noise (`.git`, `node_modules`, binaries, etc.)
2. **Rank**: Score each file by keyword overlap with the task description + file extension priority
3. **Pack**: Select the highest-ranked files until budget is exhausted, head-truncating oversized files
4. **Output**: Produce the markdown bundle and manifest

---

## Project Structure

```
ctxpack/
├── ctxpack.py                  # CLI implementation
├── SPEC.md                     # Specification
├── README.md                   # This file
├── CLAUDE.md                   # Claude Code context
├── CHANGELOG.md                # Version history
├── .gitignore
├── .ai/                        # AI engineering toolkit
│   ├── agents/                 # 14 specialized agents
│   ├── skills/                 # 20 reusable skills
│   ├── commands/               # 18 invokable commands
│   ├── workflows/              # 10 multi-step workflows
│   ├── prompts/                # 11 prompt templates
│   ├── platforms/              # 7 platform adapters
│   ├── templates/              # 3 reusable templates
│   ├── docs/                   # Toolkit documentation
│   ├── examples/               # Usage examples
│   └── standards/              # Engineering standards
└── docs/
    └── ARCHITECTURE.md          # Architecture documentation
```

---

## Development

```bash
# Run tests
python -m unittest discover -s tests -t .

# Test determinism
python ctxpack.py --path . --task "test" --budget 1000 --out a.md
python ctxpack.py --path . --task "test" --budget 1000 --out b.md
fc /b a.md b.md  # Windows: should report no differences
```

---

## License

Hackathon project — Module 1
