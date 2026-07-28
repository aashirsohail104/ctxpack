---
name: repository-audit
description: Use when auditing the overall health and organization of the ctxpack repository — checks structure, cleanliness, unused files, naming consistency
---

# Repository Audit

## Purpose
Audit the ctxpack repository for organization, cleanliness, naming consistency, and structural health.

## Inputs
- Repository root directory

## Outputs
- Repository structure report
- Naming convention compliance
- Unused or orphaned files
- Suggested improvements

## Workflow
1. Map the complete directory tree
2. Check every file against naming conventions
3. Identify unused files (not referenced by anything)
4. Check for consistency between actual structure and documented structure
5. Verify .gitignore is appropriate
6. Check for temporary/artifact files that should be removed

## Best Practices
- Be thorough: list every file and its status
- Distinguish between "should remove" and "nice to organize"
- Check for files in wrong locations

## Limitations
- Cannot know author intent for unusual files
- "Unused" is heuristic (no imports/references)

## Success Criteria
- [ ] All files follow naming conventions
- [ ] No orphaned or unused files
- [ ] Structure matches documentation
- [ ] .gitignore covers all generated/artifact files
