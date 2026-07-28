---
name: bundle-validation
description: Use when validating ctxpack bundle output format — checks markdown structure, code fences, headers, and overall correctness
---

# Bundle Validation

## Purpose
Validate that ctxpack bundle output matches the specified format: markdown structure, headers, code fences, language tags, and overall presentation.

## Inputs
- Bundle markdown output
- SPEC.md format specification

## Outputs
- Format compliance report
- Structural issues found
- Corrections needed

## Workflow
1. Check bundle starts with `# ctxpack bundle — <project>`
2. Verify `## Task` section contains the task description
3. Verify `## Project Structure` section has tree diagram
4. Verify each file has `### path/to/file` header and fenced code block
5. Check language tag on code fences matches file extension
6. Verify truncation markers present when expected
7. Check for any format violations

## Best Practices
- Parse the bundle programmatically for reliable validation
- Check both presence and correctness of each format element
- Verify the bundle is valid markdown (no unclosed fences)

## Limitations
- Cannot verify semantic correctness of content, only format
- Minor whitespace variations may not matter

## Success Criteria
- [ ] Bundle follows SPEC.md format exactly
- [ ] All code fences are properly opened and closed
- [ ] Language tags match file extensions
- [ ] Truncation markers present when files are truncated
