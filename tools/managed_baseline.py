"""Refreshes the figures a changed rule made incomparable, leaving every other ratchet where it stood.

Usage: managed_baseline.py <baseline.json> <audit.json> <check.figure> [<check.figure> ...]
Prints "unchanged", or "refreshed" followed by each figure that moved. A figure absent from either file is
skipped: the gate already ignores what it cannot compare on both sides.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def readJson(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def figureIn(summaries: dict, checkName: str, figureName: str) -> object:
    checkSummary = summaries.get(checkName)
    if not isinstance(checkSummary, dict):
        return None
    return checkSummary.get(figureName)


def refresh(baselineSummaries: dict, currentSummaries: dict, figurePaths: list[str]) -> list[str]:
    moved = []
    for figurePath in figurePaths:
        checkName, figureName = figurePath.split(".", 1)
        wasValue = figureIn(baselineSummaries, checkName, figureName)
        nowValue = figureIn(currentSummaries, checkName, figureName)
        if wasValue is None or nowValue is None or wasValue == nowValue:
            continue
        baselineSummaries[checkName][figureName] = nowValue
        moved.append(f"{figurePath} {json.dumps(wasValue)} -> {json.dumps(nowValue)}")
    return moved


def main() -> int:
    baselinePath, currentPath = Path(sys.argv[1]), Path(sys.argv[2])
    figurePaths = sys.argv[3:]
    baseline, current = readJson(baselinePath), readJson(currentPath)
    moved = refresh(baseline["summaries"], current["summaries"], figurePaths)
    if not moved:
        print("unchanged")
        return 0
    baselinePath.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print("refreshed (" + "; ".join(moved) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
