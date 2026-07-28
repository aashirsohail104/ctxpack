# /rank — Rank Files by Relevance

## Purpose
Rank files by relevance to a given task description. Verifies the ranking algorithm and produces a ranked list.

## Orchestration
1. Invoke `agent-context-ranking`
2. Reference `context-packing` skill

## Output
Ranked file list with scores and relevance explanations.

## Usage
```
/rank --task "<description>" [--path <path>]
```

## Verification
- [ ] Top-ranked files are genuinely relevant
- [ ] Scoring weights are appropriate
- [ ] No ranking anomalies
