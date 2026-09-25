---
name: scriptify
description: Use after composing a non-trivial script (shell, Python, SQL, etc.) while completing a task, to offer saving it as a reusable, parameterized script outside the session.
allowed-tools: Write, Edit, Bash(chmod +x:*), AskUserQuestion
---

Goal: offer to save the disposable scripts composed by the agent so they can be reused later, outside the agent.

AI agents create scripts to answer the user queries. These are usually cleaned up after the session is over. This skill proposes to the user saving these disposable scripts for future reuse.

# Manual invocation

When the user invokes this skill directly (e.g. `/scriptify`), review the scripts composed earlier in the session, apply the promotion rules below to each of them, and propose the ones that qualify. If none qualify, say so briefly.

# Suggestion format

Suggestions to promote ephemeral scripts should be proposed at the end of the agent response that generated or used the disposable script, never in the middle of a task.

- If several scripts qualify, propose them together in a single suggestion.
- If no user can answer (non-interactive or headless runs, subagents), propose on the coordinating agent after the activity.

The suggestion names the script and shows how it would be called:

- (Agent) I generated this script to answer your request: <script purpose><script excerpt with core functionality>. Save it as `<name> <parameters>`?

Case A:

- (User) <negative answer, e.g: No thank you> 
- (Agent) Understood. [The agent continues working as usual and does not propose the same script again in this session].

Case B:

- (User) <positive answer, e.g: Yes, please save it> 
- (Agent) Great! Where should I save it? [The agent asks for the destination, offering these defaults as alternatives:
  - The location the user chose last time (see Memory).
  - The project's `scripts/` directory, if the script is specific to the current project.]
- (User) <chosen default or custom path>
- (Agent) [The agent saves the script in the chosen destination, then shows the destination path and contents to the user].

If a file with the same name already exists at the destination, ask before replacing it.

# Rules to promote a disposable script to a persistent one 

Not all disposable scripts are proposed to be saved for later re-use, use the following rules to decide whether or not to propose them:

- The script is not trivial. One liners changing just one or two basic commands (ls, cd, echo, grep ...) are considered trivial.
- The script has a clear context that can be translated into input parameters.
- It has a clear purpose and is not just a collection of unrelated commands.
- No script saved before already does the same job (see Memory). If one does, propose extending or reusing it instead of saving a new one.
  
# Promoted scripts interface

When promoting a disposable script as a persistent one, add a minimalist interface based on parameters. The script must work outside the agent session.

- Keep the language the script was written in, and use its usual way of parsing arguments (e.g. `argparse` in Python).
- Include a help message explaining the parameters.
- Start with a shebang and make the file executable.
- On missing or invalid arguments, print the help message and exit with a non-zero code.
- Write results to stdout and errors to stderr.
- List the tools or libraries it depends on in a header comment.
- Do not hardcode secrets in the script, use input parameters, environment variables or both instead.
- Allow passing connection strings through the script input parameters. Offer a default value if the target is generic enough.
- Replace other values specific to the session (temporary paths, one-off IDs, the agent's working directory) with parameters.
- One example:
  ```bash
  #!/usr/bin/env bash
  # primes.sh - Print the prime numbers in a range.
  set -euo pipefail

  usage() {
    echo "Usage: $(basename "$0") <start> <end>"
    echo "  start  Lower bound of the range (inclusive)"
    echo "  end    Upper bound of the range (inclusive)"
  }

  [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && { usage; exit 0; }
  [[ $# -ne 2 ]] && { usage >&2; exit 1; }

  start=$1 end=$2
  for ((n = start < 2 ? 2 : start; n <= end; n++)); do
    for ((d = 2; d * d <= n; d++)); do
      ((n % d == 0)) && continue 2
    done
    echo "$n"
  done
  ```

# Memory

Unless the user explicitly requests not to, keep a memory of the promoted scripts, their purpose, name and location.

Also add an entry (name, purpose, usage line) to a `SCRIPTS.md` index in the destination directory, creating it if needed. This keeps saved scripts discoverable by the user and by agents without memory.
