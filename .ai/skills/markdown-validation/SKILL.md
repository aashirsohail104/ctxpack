---
name: markdown-validation
description: Use when validating markdown files for structural correctness — checks headers, code fences, lists, tables, and links
---

# Markdown Validation

## Purpose
Validate markdown files for structural correctness: proper header hierarchy, closed code fences, valid table syntax, working links.

## Inputs
- One or more markdown files

## Outputs
- Structural issues found
- Broken links (if paths are local)
- Format violations

## Workflow
1. Check all ATX headers are properly formatted (`## Header`)
2. Verify all fenced code blocks have closing ```
3. Check language tags on code fences are valid
4. Verify table syntax (pipe alignment, column count consistency)
5. Check list indentation is consistent
6. Validate relative links point to existing files
7. Check for mixed list types (should be consistent)

## Best Practices
- Use a markdown linter for automated checking
- Pay special attention to code fence matching (most common error)
- Verify YAML frontmatter is valid

## Limitations
- Cannot verify external URLs are valid
- Some markdown renderers handle errors differently

## Success Criteria
- [ ] All code fences are properly closed
- [ ] Header hierarchy is logical (no H1 → H3 jumps)
- [ ] Links to local files are valid
- [ ] Table syntax is correct
