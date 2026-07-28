# /manifest — Generate Manifest

## Purpose
Generate a JSON manifest documenting all files considered, included, and excluded.

## Orchestration
1. Invoke `agent-manifest-validation`
2. Reference `manifest-review` skill

## Output
JSON manifest file.

## Usage
```
/manifest --path <path> --task "<desc>" --budget <int> --manifest <file>
```

## Verification
- [ ] Manifest schema matches SPEC.md
- [ ] All files accounted for
- [ ] Statistics self-consistent
