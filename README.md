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

### As a Claude Code plugin

```
/plugin marketplace add pfcoperez/scriptify
/plugin install scriptify@scriptify
```

The plugin bundles the skill and a Stop hook that makes it trigger reliably (see below). The hook requires `python3`.

### For other agents

```bash
npx skills add https://github.com/pfcoperez/scriptify
```

Or just ask your agent to install it.

## Prerequisites

- An AI coding agent with [npx skills](https://www.npmjs.com/package/skills) support
- Python3, if installed as Claude Code plugin. 

## Usage

The skill is designed to alter agent behavior without active user request but it can be invoked manually with:

```
/scriptify
```

📝If not used as a Claude Code plugin, the invocation of the skill is not deterministic. In these cases, `AGENTS.md` can be used to increase the chances of it being invoked by adding instructions such as:

```
Invoke /scriptify after you have finished working on a prompt
```
