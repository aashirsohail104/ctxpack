# ctxpack Usage Examples

## Basic Usage

### Pack a project for debugging
```
ctxpack --path /my/project --task "Debug authentication flow" --budget 4000
```

### Pack with output file
```
ctxpack --path /my/project --task "Add user profile feature" --budget 8000 --out bundle.md
```

### Pack with manifest
```
ctxpack --path /my/project --task "Review API endpoints" --budget 6000 --out bundle.md --manifest manifest.json
```

## Edge Cases

### Empty directory
```
ctxpack --path /empty/dir --task "Any task" --budget 1000
# Outputs bundle with header + tree, exit 0
```

### Single large file
```
ctxpack --path /dir --task "Review code" --budget 500
# Head-truncates the file, includes truncation marker
```

### Minimum budget
```
ctxpack --path /dir --task "Test" --budget 1
# Includes only what fits (likely just header)
```

## AI Toolkit Examples

### Run a spec check
```
# Load .ai/commands/spec-check.md and follow its orchestration
```

### Run a full audit
```
# Follow .ai/workflows/workflow-repository-audit.md
```

### Prepare a release
```
# Follow .ai/workflows/workflow-release.md
```
