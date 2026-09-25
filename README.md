# Scriptify

Crystallize and reuse agent actions by preserving agent produced disposable scripts.

## Installation

```bash
npx skills add https://github.com/pfcoperez/scriptify
```

Or just ask your agent to install it.

## Prerequisites

- An AI coding agent with [npx skills](https://www.npmjs.com/package/skills) support

## Making it trigger reliably

Agents load skills by matching them to the task at hand. Saving scripts is a side effect of other work: you ask for the primes in a range, not for a script to be saved, so the agent may never load this skill on its own.

To make it apply consistently, add a line like this to your `CLAUDE.md` or `AGENTS.md`:

```markdown
After writing a non-trivial script, apply the scriptify skill.
```

In Claude Code you can also use a [Stop hook](https://docs.claude.com/en/docs/claude-code/hooks) to remind the agent at the end of each turn.

## Usage

The skill is designed to alter agent behavior without active user request but it can be invoked manually with:

```
/scriptify
```
