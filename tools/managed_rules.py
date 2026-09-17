"""Adds the rule blocks a newer kit expects to a repository's rules.json, leaving everything already there as it was.

Usage: managed_rules.py <rules.json> <preset.json> [check]
Prints "unchanged", or "updated" followed by the keys it added. With "check" it changes nothing.
"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

INDENT = "  "


def renderBlock(key: str, value: object) -> str:
    rendered = json.dumps(value, indent=2)
    return textwrap.indent(f"{json.dumps(key)}: {rendered}", INDENT)


def withBlocksAdded(rulesText: str, missing: dict) -> str:
    body = rulesText.rstrip()
    closingBrace = body.rindex("}")
    existing = body[:closingBrace].rstrip()
    blocks = ",\n".join(renderBlock(key, value) for key, value in missing.items())
    return f"{existing},\n{blocks}\n}}\n"


def main() -> int:
    rulesPath, presetPath = Path(sys.argv[1]), Path(sys.argv[2])
    isCheckOnly = sys.argv[3:] == ["check"]
    rules, preset = json.loads(rulesPath.read_text()), json.loads(presetPath.read_text())
    missing = {key: value for key, value in preset.items() if key not in rules}
    if not missing:
        print("unchanged")
        return 0
    if not isCheckOnly:
        updated = withBlocksAdded(rulesPath.read_text(), missing)
        json.loads(updated)
        rulesPath.write_text(updated)
    print("updated (added " + ", ".join(missing) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
