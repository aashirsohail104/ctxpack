# Improve Codebase Architecture — Skill Reference

Saved for reference before proceeding with restructuring.

## Purpose

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Key Vocabulary (from /codebase-design skill)

- **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**
- The deletion test: "would deleting it concentrate complexity, or just move it?"
- "The interface is the test surface"
- "One adapter = hypothetical seam, two = real"

## Process

### 1. Explore

- Scope before scan — YAGNI. Weight recent changes.
- If user named a direction, take it. Otherwise walk git log for hot spots.
- Read CONTEXT.md and ADRs in the area first.
- Use `subagent_type=Explore` to walk codebase.
- Note friction: bouncing between modules, shallow modules, lack of locality, untested code.
- Apply deletion test.

### 2. Present candidates as HTML report

- Write to `<tmpdir>/architecture-review-<timestamp>.html`
- Open with `xdg-open`/`open`/`start`
- Tailwind via CDN, Mermaid via CDN for diagrams
- Each candidate card: Files, Problem, Solution, Benefits, Before/After diagram, Recommendation strength (Strong/Worth exploring/Speculative)
- End with Top recommendation section
- Use CONTEXT.md vocabulary for domain, /codebase-design vocabulary for architecture
- ADR conflicts: only surface when friction is real enough to warrant revisiting
- Do NOT propose interfaces yet
- Ask user: "Which of these would you like to explore?"

### 3. Grilling loop

- Run /grilling skill to walk decision tree
- Side effects:
  - Naming a deepened module after a concept not in CONTEXT.md? Add the term.
  - Sharpening a fuzzy term? Update CONTEXT.md right there.
  - User rejects candidate with load-bearing reason? Offer ADR.
  - Want to explore alternative interfaces? Run /codebase-design skill.

## When to Use

- Before major refactoring
- When code feels hard to navigate or test
- When AI tools struggle to understand the codebase
- After significant feature accumulation without architectural review

## Output

- HTML report in temp directory (not in repo)
- Optionally: CONTEXT.md updates, ADRs, deepened module designs
