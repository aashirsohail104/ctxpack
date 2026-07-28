---
name: manifest-review
description: Use when reviewing ctxpack manifest output — validates JSON structure, statistics, inclusion/exclusion completeness
---

# Manifest Review

## Purpose
Review ctxpack manifest JSON output for correctness, completeness, and consistency.

## Inputs
- Manifest JSON file
- Bundle output
- Input directory

## Outputs
- Manifest integrity check
- Inclusion/exclusion completeness
- Statistics validation (budget vs used vs actual)
- Consistency check between manifest and bundle

## Workflow
1. Validate manifest JSON structure (budget, used, included, excluded)
2. Check budget >= used (never exceed)
3. Verify every file in bundle has a manifest entry
4. Verify every excluded file has a reason
5. Cross-check excluded count against actual directory contents
6. Validate all paths are relative and unique

## Best Practices
- Verify manifest statistics independently by tokenizing the bundle
- Check that truncated files have `"truncated": true`
- Ensure no duplicate paths in included or excluded

## Limitations
- Cannot verify the quality of exclusion reasons
- Large manifests are tedious to manually review

## Success Criteria
- [ ] Manifest JSON is valid and well-formed
- [ ] Every file in bundle has a manifest entry
- [ ] Excluded files have meaningful reasons
- [ ] Statistics are self-consistent
