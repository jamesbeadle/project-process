"""Keeps the kit's managed block at the top of a repository's CLAUDE.md.

Usage: python3 managed_block.py <CLAUDE.md path> <block body path> <kit version> [check]
Prints created | updated | unchanged; with "check" it only prints what it would do.
The block is everything between the two markers;
whatever the repository wrote outside them is kept exactly as it was, except a file whose
only content was a copy of the code rules, which the block now supersedes.
"""
from __future__ import annotations

import sys
from pathlib import Path

BEGIN_MARKER = "<!-- project-process:begin -->"
END_MARKER = "<!-- project-process:end -->"
RULES_TITLE = "# How I Write Code"


def buildBlock(body: str, kitVersion: str) -> str:
    header = f"{BEGIN_MARKER}\n<!-- project-process kit v{kitVersion} — refreshed by bootstrap.sh; edit the kit, not this block -->"
    return f"{header}\n\n{body.strip()}\n\n{END_MARKER}\n"


def splitExisting(text: str) -> tuple[str, str, str] | None:
    beginAt = text.find(BEGIN_MARKER)
    endAt = text.find(END_MARKER)
    if beginAt < 0 or endAt < 0 or endAt < beginAt:
        return None
    afterEnd = endAt + len(END_MARKER)
    return text[:beginAt], text[beginAt:afterEnd], text[afterEnd:]


def isOnlyTheRules(remainder: str) -> bool:
    stripped = remainder.strip()
    if not stripped.startswith(RULES_TITLE):
        return False
    otherTitles = [line for line in stripped.splitlines()[1:] if line.startswith("# ")]
    return len(otherTitles) == 0


def compose(existing: str, block: str) -> str:
    parts = splitExisting(existing)
    if parts is None:
        remainder = "" if isOnlyTheRules(existing) else existing
        return joinBlockAndRemainder(block, remainder)
    before, _, after = parts
    remainder = before.rstrip() + ("\n\n" if before.strip() and after.strip() else "") + after.lstrip("\n")
    return joinBlockAndRemainder(block, remainder)


def joinBlockAndRemainder(block: str, remainder: str) -> str:
    if remainder.strip() == "":
        return block
    return block + "\n" + remainder.lstrip("\n").rstrip() + "\n"


def outcomeOf(existing: str | None, composed: str) -> str:
    if existing is None:
        return "created"
    if composed == existing:
        return "unchanged"
    return "updated"


def main() -> int:
    claudePath, bodyPath, kitVersion = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    isCheckOnly = len(sys.argv) > 4 and sys.argv[4] == "check"
    block = buildBlock(bodyPath.read_text(encoding="utf-8"), kitVersion)
    existing = claudePath.read_text(encoding="utf-8") if claudePath.exists() else None
    composed = compose(existing or "", block)
    outcome = outcomeOf(existing, composed)
    if outcome != "unchanged" and not isCheckOnly:
        claudePath.write_text(composed, encoding="utf-8")
    print(outcome)
    return 0


if __name__ == "__main__":
    sys.exit(main())
