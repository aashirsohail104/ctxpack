# Security Prompt

## Purpose
Prompt an AI to review code for security issues.

## Template
```
Review [code/file] for security vulnerabilities:

1. Input validation — are all inputs validated?
2. Path traversal — are file paths sanitized?
3. Injection — is there any command injection risk?
4. Information disclosure — does it leak sensitive info?
5. Error handling — do error messages reveal internals?

Provide findings with severity ratings.
```

## Usage
Use when reviewing code for security. Note: ctxpack is stdlib-only with no network calls, so attack surface is minimal.
