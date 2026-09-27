# Scriptify

Crystallize and reuse agent actions by preserving agent produced disposable scripts.

## Installation

```bash
npx skills add https://github.com/pfcoperez/scriptify
```

Or just ask your agent to install it.

### As a Claude Code plugin

```
/plugin marketplace add pfcoperez/scriptify
/plugin install scriptify@scriptify
```

The plugin bundles the skill and a Stop hook that makes it trigger reliably (see below). The hook requires `python3`.

## Prerequisites

- An AI coding agent with [npx skills](https://www.npmjs.com/package/skills) support

## Making it trigger reliably

Agents load skills by matching them to the task at hand. Saving scripts is a side effect of other work: you ask for the primes in a range, not for a script to be saved, so the agent may never load this skill on its own.

To make it apply consistently, add a line like this to your `CLAUDE.md` or `AGENTS.md`:

```markdown
After writing a non-trivial script, apply the scriptify skill.
```

In Claude Code, installing it as a plugin does this for you: its [Stop hook](https://docs.claude.com/en/docs/claude-code/hooks) checks each finished turn for composed scripts (multi-line or heredoc shell commands, inline interpreters, written script files) and, if it finds any, asks the agent to apply the skill before stopping. Turns without scripts are not affected.

## Usage

The skill is designed to alter agent behavior without active user request but it can be invoked manually with:

```
/scriptify
```
