# Engineering Standards

## Coding Conventions

- Python 3.10+, standard library only — no third-party packages
- Single-file implementation: `ctxpack.py`
- Functions ordered: top-level `main()`, then helpers in call order
- Each function has a single responsibility
- Constants at top of file
- Deterministic sorting: always `sorted()` with explicit keys
- No global state
- Type hints on function signatures
- Docstrings for public functions only
- Use `sys.stderr.write()` for errors, never `print()`

## Documentation Conventions

- `*.md` files use GitHub-flavored markdown
- Code blocks specify language identifier
- Headers use ATX-style (`##` not underlined)
- Links use relative paths within the project
- Files under `.ai/` use consistent YAML frontmatter where applicable

## Repository Organization

- Runtime code: root directory (`ctxpack.py`)
- AI toolkit: `.ai/` directory
- Documentation: `docs/` and `.ai/docs/`
- Specifications: `SPEC.md` at root

## Testing Standards

- Tests use `unittest.TestCase` (stdlib only)
- Test files named `test_ctxpack.py`
- Tests cover: unit, integration, edge cases, determinism
- Each edge case in SPEC.md has a corresponding test
- No network calls in tests
- Tests must be deterministic

## Markdown Standards

- No HTML in markdown files
- Use fenced code blocks with language tags
- Tables use GFM pipe syntax
- Lists use `-` for unordered, `1.` for ordered

## Specification Standards

- SPEC.md is the authoritative specification
- Every behavioral claim must be tracked to an implementation line
- SPEC.md defines: CLI contract, token counting, ranking, noise, manifest, bundle format
- Edge cases explicitly enumerated

## File Naming Conventions

- Lowercase with hyphens: `engineering-standards.md`
- Python files: `snake_case.py`
- Test files: `test_<module>.py`
- Agent files: `agent-<name>.md`
- Skill files: lowercase with hyphens

## Release Standards

- Version in `ctxpack.py` as `__version__`
- Changelog in `docs/CHANGELOG.md`
- Tagged git releases
- Release verification checklist: all tests pass, determinism confirmed, edge cases verified

## AI Collaboration Standards

- Every AI agent reads the specification before acting
- Verify assumptions before making changes
- Preserve deterministic behavior
- No unnecessary code modifications
- Reproducible results always
- Record reasoning for significant architectural decisions
- Respect separation between runtime code and AI assets
