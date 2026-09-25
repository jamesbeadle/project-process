"""Writes the kit's CLAUDE.md whole, and keeps the repository's own instructions in PROJECT.md.

Usage: python3 managed_block.py <CLAUDE.md path> <block body path> <kit version> <PROJECT.md path> <PROJECT.md template> [check]
Prints two outcomes, CLAUDE.md's then PROJECT.md's, each created | updated | unchanged; with "check" it only
prints what it would do. CLAUDE.md is the block and nothing else. Whatever the repository wrote outside the
block is moved into PROJECT.md once, except a file whose only content was a copy of the code rules, which the
block supersedes. PROJECT.md is created from the template when missing and never rewritten after that.
"""
from __future__ import annotations

import sys
from pathlib import Path

from project_notes import composeProject

BEGIN_MARKER = "<!-- project-process:begin -->"
END_MARKER = "<!-- project-process:end -->"
RULES_TITLE = "# How I Write Code"


def buildBlock(body: str, kitVersion: str) -> str:
    header = (f"{BEGIN_MARKER}\n<!-- project-process kit v{kitVersion} — replaced whole by bootstrap.sh; edit the kit, "
              "and write this repository's own instructions in PROJECT.md -->")
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


def notesOutsideBlock(existing: str) -> str:
    parts = splitExisting(existing)
    if parts is None:
        return "" if isOnlyTheRules(existing) else existing
    before, _, after = parts
    return f"{before.strip()}\n\n{after.strip()}".strip()


def outcomeOf(existing: str | None, composed: str) -> str:
    if existing is None:
        return "created"
    if composed == existing:
        return "unchanged"
    return "updated"


def readIfPresent(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def main() -> int:
    claudePath, bodyPath, kitVersion = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    projectPath, templatePath = Path(sys.argv[4]), Path(sys.argv[5])
    isCheckOnly = len(sys.argv) > 6 and sys.argv[6] == "check"
    block = buildBlock(bodyPath.read_text(encoding="utf-8"), kitVersion)
    existingClaude, existingProject = readIfPresent(claudePath), readIfPresent(projectPath)
    project = composeProject(existingProject, templatePath.read_text(encoding="utf-8"), notesOutsideBlock(existingClaude or ""))
    claudeOutcome, projectOutcome = outcomeOf(existingClaude, block), outcomeOf(existingProject, project)
    if not isCheckOnly:
        writeIfChanged(projectPath, project, projectOutcome)
        writeIfChanged(claudePath, block, claudeOutcome)
    print(claudeOutcome, projectOutcome)
    return 0


def writeIfChanged(path: Path, text: str, outcome: str) -> None:
    if outcome != "unchanged":
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
