#!/usr/bin/env python3
"""Stop hook: ask the agent to apply the scriptify skill when the turn that
just ended composed a non-trivial script.

Reads the hook payload from stdin and inspects the transcript since the last
user prompt. Fails open: any error lets the agent stop normally.
"""
import json
import os
import sys

SCRIPT_EXTENSIONS = {
    ".sh", ".bash", ".zsh", ".py", ".sql", ".js", ".mjs", ".ts",
    ".rb", ".pl", ".ps1", ".r", ".jl", ".lua", ".awk",
}
INLINE_INTERPRETERS = ("python -c", "python3 -c", "node -e", "perl -e", "ruby -e")

REASON = (
    "You composed one or more scripts during this turn. Apply the scriptify "
    "skill now: review them against its promotion rules and, only if any "
    "qualify, end your response with the save suggestion. If none qualify, "
    "stop without mentioning scriptify."
)


def is_user_prompt(entry):
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        return True
    return any(block.get("type") != "tool_result" for block in content or [])


def is_script(tool_use):
    name = tool_use.get("name")
    args = tool_use.get("input") or {}
    if name == "Bash":
        command = args.get("command", "")
        return (
            command.count("\n") >= 2
            or "<<" in command
            or any(i in command for i in INLINE_INTERPRETERS)
        )
    if name in ("Write", "Edit"):
        path = args.get("file_path", "")
        return os.path.splitext(path)[1].lower() in SCRIPT_EXTENSIONS
    return False


def main():
    payload = json.load(sys.stdin)
    # The agent is already continuing because of this hook: don't loop.
    if payload.get("stop_hook_active"):
        return

    with open(payload["transcript_path"], encoding="utf-8") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    start = max((i for i, e in enumerate(entries) if is_user_prompt(e)), default=-1)
    tool_uses = [
        block
        for e in entries[start + 1:]
        if e.get("type") == "assistant" and not e.get("isSidechain")
        for block in e.get("message", {}).get("content") or []
        if isinstance(block, dict) and block.get("type") == "tool_use"
    ]

    # The skill already ran this turn (proactively or via /scriptify).
    if any(
        t.get("name") == "Skill" and "scriptify" in (t.get("input") or {}).get("skill", "")
        for t in tool_uses
    ):
        return

    if any(is_script(t) for t in tool_uses):
        print(json.dumps({"decision": "block", "reason": REASON}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
