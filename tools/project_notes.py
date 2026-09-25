"""Keeps a repository's own instructions in PROJECT.md, the one instruction file the kit never rewrites.

CLAUDE.md is the kit's and is replaced whole. Whatever a repository had written there is moved here once,
under a heading that says where it came from, so the replacement never loses a note; after that the two
files change independently.
"""
from __future__ import annotations

MOVED_HEADING = "## Moved from CLAUDE.md"


def composeProject(existing: str | None, template: str, movedNotes: str) -> str:
    project = existing if existing is not None else template
    if movedNotes.strip() == "":
        return project
    return f"{project.rstrip()}\n\n{MOVED_HEADING}\n\n{movedNotes.strip()}\n"
