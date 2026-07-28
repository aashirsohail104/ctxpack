# Frequently Asked Questions

## General

**Q: What is ctxpack?**
A: A Python CLI tool that packs relevant project files into a token-budgeted markdown bundle for AI coding assistants.

**Q: What is the `.ai/` directory?**
A: A vendor-neutral AI engineering toolkit that helps AI coding assistants understand, extend, test, maintain, and review the project.

**Q: Does ctxpack depend on the `.ai/` directory to run?**
A: No. ctxpack runs with only Python stdlib. The `.ai/` directory is for AI contributors and maintainers.

## Skills and Agents

**Q: What's the difference between an agent and a skill?**
A: An agent is a specialized AI assistant with a defined role and responsibilities. A skill is a reusable capability that agents invoke. Agents orchestrate skills.

**Q: How do skills relate to commands?**
A: Commands are user-invokable operations that orchestrate agents and skills. A command might call multiple skills in sequence.

## Platform Support

**Q: Which platforms are supported?**
A: OpenCode, Claude Code, Cursor, Codex CLI, Antigravity, and Gemini CLI.

**Q: Can I use this with a platform not listed?**
A: Yes. The core toolkit is vendor-neutral. Create a platform adapter in `.ai/platforms/<name>/` following the existing pattern.

**Q: Are commands the same across all platforms?**
A: No. Each platform has its own command system. Commands in `.ai/commands/` are defined in a platform-neutral format and adapted per platform.
