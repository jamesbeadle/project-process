"""Reads and writes a value at a dotted path inside nested JSON, so a caller names "prose.maxLineLength" once.

UNSET distinguishes a path that is absent from one whose value happens to be null.
"""
from __future__ import annotations

UNSET = object()


def valueAt(holder: dict, dottedPath: str) -> object:
    found = holder
    for name in dottedPath.split("."):
        if not isinstance(found, dict) or name not in found:
            return UNSET
        found = found[name]
    return found


def placeValueAt(holder: dict, dottedPath: str, value: object) -> None:
    names = dottedPath.split(".")
    parent = holder
    for name in names[:-1]:
        parent = parent.setdefault(name, {})
    parent[names[-1]] = value
