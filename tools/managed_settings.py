"""Keeps the kit's branch guard registered in a repository's .claude/settings.json.

Usage: python3 managed_settings.py <settings.json path> <hook command> [check]
Prints created | updated | unchanged; with "check" it only prints what it would do.
The file is shared Claude Code settings and travels with the clone. Whatever the repository
already has in it — other hooks, permissions, anything — is kept exactly as it was; the guard
is added as one PreToolUse hook on the Bash tool, or its command refreshed if the kit's differs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GUARD_SCRIPT = "branch_guard"
TOOL_MATCHER = "Bash"


def main() -> int:
    settingsPath, hookCommand = Path(sys.argv[1]), sys.argv[2]
    isCheckOnly = len(sys.argv) > 3 and sys.argv[3] == "check"
    existing = settingsPath.read_text(encoding="utf-8") if settingsPath.exists() else None
    settings = parse(existing)
    if settings is None:
        print(f"error: {settingsPath} is not valid JSON; fix it or move it aside and re-run")
        return 1
    registerGuard(settings, hookCommand)
    composed = json.dumps(settings, indent=2) + "\n"
    outcome = outcomeOf(existing, composed)
    if outcome != "unchanged" and not isCheckOnly:
        settingsPath.parent.mkdir(parents=True, exist_ok=True)
        settingsPath.write_text(composed, encoding="utf-8")
    print(outcome)
    return 0


def parse(existing: str | None) -> dict | None:
    if existing is None or existing.strip() == "":
        return {}
    try:
        parsed = json.loads(existing)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def registerGuard(settings: dict, hookCommand: str) -> None:
    preToolUse = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    entry = bashEntryIn(preToolUse)
    if entry is None:
        preToolUse.append({"matcher": TOOL_MATCHER, "hooks": [guardHook(hookCommand)]})
        return
    hooks = entry.setdefault("hooks", [])
    guard = guardIn(hooks)
    if guard is None:
        hooks.append(guardHook(hookCommand))
        return
    guard["command"] = hookCommand


def bashEntryIn(preToolUse: list) -> dict | None:
    for entry in preToolUse:
        if isinstance(entry, dict) and entry.get("matcher") == TOOL_MATCHER:
            return entry
    return None


def guardIn(hooks: list) -> dict | None:
    for hook in hooks:
        if isinstance(hook, dict) and GUARD_SCRIPT in str(hook.get("command", "")):
            return hook
    return None


def guardHook(hookCommand: str) -> dict:
    return {"type": "command", "command": hookCommand}


def outcomeOf(existing: str | None, composed: str) -> str:
    if existing is None:
        return "created"
    if json.dumps(json.loads(existing) if existing.strip() else {}, indent=2) + "\n" == composed:
        return "unchanged"
    return "updated"


if __name__ == "__main__":
    sys.exit(main())
