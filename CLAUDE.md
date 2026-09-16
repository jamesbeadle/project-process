# project-process — working on the kit itself

This repository is the kit, so it does not carry the installed block; `kit/claude/working-process.md` and `kit/claude/code-rules.md` are the doctrine and apply here as they do everywhere.

Above all: nothing is committed to `main` by a Claude. Branch first — `fix/<slug>` or `feature/<slug>` — commit there, push, and open a pull request for a person to merge. `.claude/settings.json` runs `kit/hooks/branch_guard` as a `PreToolUse` hook and refuses a commit or push that would move `main`.

A change to the kit bumps `VERSION`. Before opening the pull request, run `bash bootstrap.sh --kit . --repo <a scratch git repository>` twice (the second run must report nothing to do) to prove the bootstrap still installs cleanly.
