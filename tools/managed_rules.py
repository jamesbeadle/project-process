"""Brings a repository's rules.json up to the kit's: adds the blocks it lacks, and resets the values the kit owns.

Usage: managed_rules.py <rules.json> <preset.json> <kit-owned.json> [check]
Prints "unchanged", "updated (...)" when only missing blocks were added, or "retuned (...)" when a value the
kit owns moved, followed by one line per audit figure that value decides. Those figures are the only ones the
caller refreshes in the baseline; every other ratchet stands. With "check" it changes nothing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from nested_values import UNSET, placeValueAt, valueAt


def readJson(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blocksMissingFrom(rules: dict, preset: dict) -> dict:
    return {key: value for key, value in preset.items() if key not in rules}


def valuesToRetune(rules: dict, preset: dict, doctrinePaths: list[str]) -> list[tuple]:
    retuned = []
    for dottedPath in doctrinePaths:
        kitValue = valueAt(preset, dottedPath)
        repositoryValue = valueAt(rules, dottedPath)
        if kitValue is not UNSET and repositoryValue != kitValue:
            retuned.append((dottedPath, repositoryValue, kitValue))
    return retuned


def render(value: object) -> str:
    if value is UNSET:
        return "unset"
    return json.dumps(value)


def describe(added: dict, retuned: list[tuple]) -> str:
    notes = []
    if added:
        notes.append("added " + ", ".join(added))
    for dottedPath, was, now in retuned:
        notes.append(f"set {dottedPath} {render(was)} -> {render(now)}")
    outcome = "retuned" if retuned else "updated"
    return f"{outcome} ({'; '.join(notes)})"


def reconcile(rules: dict, preset: dict, doctrinePaths: list[str]) -> tuple[dict, list[tuple]]:
    added = blocksMissingFrom(rules, preset)
    rules.update(added)
    retuned = valuesToRetune(rules, preset, doctrinePaths)
    for dottedPath, _, kitValue in retuned:
        placeValueAt(rules, dottedPath, kitValue)
    return added, retuned


def figuresDecidedBy(doctrine: dict, retuned: list[tuple]) -> list[str]:
    figures = set()
    for dottedPath, _, _ in retuned:
        figures.update(doctrine[dottedPath])
    return sorted(figures)


def main() -> int:
    rulesPath, presetPath, kitOwnedPath = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    isCheckOnly = sys.argv[4:] == ["check"]
    rules, preset, kitOwned = readJson(rulesPath), readJson(presetPath), readJson(kitOwnedPath)
    doctrine = kitOwned["doctrine"]
    added, retuned = reconcile(rules, preset, doctrine)
    if not added and not retuned:
        print("unchanged")
        return 0
    if not isCheckOnly:
        rulesPath.write_text(json.dumps(rules, indent=2) + "\n", encoding="utf-8")
    print(describe(added, retuned))
    for figurePath in figuresDecidedBy(doctrine, retuned):
        print(figurePath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
