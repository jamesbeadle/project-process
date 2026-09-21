"""Keeps the kit's process server registered in a repository's MCP configuration.

Usage: python3 managed_mcp.py <.mcp.json path> <server name> <command> <argument> [check]
Prints created | updated | unchanged; with "check" it only prints what it would do.
The file travels with the clone, so whatever servers the repository already registers are kept exactly as
they were; only the kit's own entry is added, or refreshed when what it should run has changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SERVERS = "mcpServers"


def parse(existing: str | None) -> dict | None:
    if existing is None or existing.strip() == "":
        return {}
    try:
        return json.loads(existing)
    except json.JSONDecodeError:
        return None


def registerServer(configuration: dict, name: str, command: str, argument: str) -> None:
    servers = configuration.setdefault(SERVERS, {})
    servers[name] = {"command": command, "args": [argument]}


def outcomeOf(existing: str | None, composed: str) -> str:
    if existing is None:
        return "created"
    if composed == existing:
        return "unchanged"
    return "updated"


def main() -> int:
    configurationPath, name, command, argument = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
    isCheckOnly = sys.argv[5:] == ["check"]
    existing = configurationPath.read_text(encoding="utf-8") if configurationPath.exists() else None
    configuration = parse(existing)
    if configuration is None:
        print(f"error: {configurationPath} is not valid JSON; fix it or move it aside and re-run")
        return 1
    registerServer(configuration, name, command, argument)
    composed = json.dumps(configuration, indent=2) + "\n"
    outcome = outcomeOf(existing, composed)
    if outcome != "unchanged" and not isCheckOnly:
        configurationPath.write_text(composed, encoding="utf-8")
    print(outcome)
    return 0


if __name__ == "__main__":
    sys.exit(main())
