# Documentation Workflow

## Goals
Review and update all project documentation to ensure accuracy and completeness.

## Execution Order
1. Invoke `agent-documentation` for current state assessment
2. Update README.md if needed
3. Update SPEC.md if implementation has changed
4. Update CHANGELOG.md with recent changes
5. Verify all markdown files are valid
6. Check cross-references between documents

## Required Agents
- `agent-documentation`

## Required Skills
- `.ai/skills/documentation-review/SKILL.md`
- `.ai/skills/markdown-validation/SKILL.md`

## Expected Outputs
- Updated documentation files
- Documentation validation report

## Verification Checklist
- [ ] README is current and accurate
- [ ] SPEC.md matches implementation
- [ ] All markdown is valid
- [ ] Cross-references are correct
