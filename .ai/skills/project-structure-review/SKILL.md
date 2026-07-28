---
name: project-structure-review
description: Use when reviewing the project directory structure — evaluates organization, naming conventions, separation of concerns, and navigability
---

# Project Structure Review

## Purpose
Review the project directory structure for logical organization, clear naming, proper separation of concerns, and ease of navigation.

## Inputs
- Repository root directory

## Outputs
- Structure assessment
- Organization issues
- Structuring recommendations

## Workflow
1. Map the complete directory tree
2. Assess top-level organization (is it intuitive?)
3. Check naming convention consistency
4. Verify separation: runtime code vs docs vs AI toolkit
5. Check depth (are directories too nested?)
6. Evaluate whether file locations match their purpose
7. Compare against standard Python project layouts

## Structure Principles
- **Flat enough**: Maximum 3-4 levels deep
- **Logical grouping**: Related files together
- **Clear naming**: Directory names explain contents
- **Separation**: Runtime vs documentation vs AI toolkit clearly separated

## Limitations
- Structure preferences are subjective
- Some organization is dictated by platform conventions

## Success Criteria
- [ ] Top-level structure is intuitive
- [ ] Naming is consistent
- [ ] Runtime code is clearly separated from docs and AI toolkit
- [ ] Any developer can find files by guessing names
