---
name: repository-cleanup
description: Use when cleaning up the ctxpack repository — identifies orphaned files, temp artifacts, unused code, and organization issues
---

# Repository Cleanup

## Purpose
Identify and suggest cleanup for the ctxpack repository: orphaned files, temporary artifacts, unused code, build outputs, and structural improvements.

## Inputs
- Repository root directory
- .gitignore contents

## Outputs
- Files to remove
- Files to relocate
- .gitignore updates
- General cleanup suggestions

## Workflow
1. Scan all files in the repository
2. Check .gitignore covers common artifacts: __pycache__, *.pyc, .env, etc.
3. Identify orphaned files (not referenced by any other file)
4. Check for IDE files (.vscode/, .idea/, *.swp, etc.)
5. Check for OS metadata files (.DS_Store, Thumbs.db)
6. Identify large files that should not be committed
7. Check for empty directories
8. Suggest .gitignore additions

## Cleanup Categories
- **Remove**: Temp files, backups, build artifacts, IDE metadata
- **Keep but ignore**: Add to .gitignore
- **Move**: Files in wrong directories
- **Remove if unused**: Orphaned code or docs

## Best Practices
- Be conservative: if unsure, keep the file
- Check git history before suggesting removal
- Prefer updating .gitignore over deleting user files

## Limitations
- Cannot know if apparently-orphaned files have value
- Some files may be referenced dynamically or externally

## Success Criteria
- [ ] All temp/artifact files identified
- [ ] .gitignore is comprehensive
- [ ] No empty directories remain
- [ ] Cleanup suggestions are safe and justified
