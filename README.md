# Scriptify

Crystallize and reuse agent actions by preserving agent produced disposable scripts.

## Why?

Agents constantly write throwaway scripts to answer our requests. Ask one
_"which pods restarted the most in the last 24h?"_ and it will likely write a
small program, run it, show you the result, and throw the program away.

Across day-to-day engineering work, that adds up to a large body of scripts
that are lost when they could be:

- **Reused outside the agent:** dropped into cron jobs, CI, or other
  deterministic automation.
- **Trusted:** a saved script has been reviewed and behaves the same way every
  time, unlike a fresh regeneration that may differ in small ways.
- **Recalled instead of regenerated:** writing the same script again costs
  tokens, time, energy, and money.

Scriptify fixes this in two ways. It **saves** useful scripts as
parameterized, reusable tools that live outside the session. And it makes the
agent **recall** them from that library before writing new code, so it stops
reinventing the wheel.

<img width="871" height="483" alt="Mr. Meeseeks — created for a single task, then gone" src="https://github.com/user-attachments/assets/4a7fab34-40d8-473c-b134-91f3cfe9fdca" />

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
