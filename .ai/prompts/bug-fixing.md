# Bug Fixing Prompt

## Purpose
Prompt an AI to diagnose and fix a bug.

## Template
```
Diagnose the following bug in [project]:

Bug description: [description]
Steps to reproduce: [steps]
Expected behavior: [expected]
Actual behavior: [actual]

1. Find the root cause
2. Write a failing test that demonstrates the bug
3. Fix the bug
4. Verify the test passes
5. Check for regressions
```

## Usage
Use when fixing bugs. Always write a failing test first.
