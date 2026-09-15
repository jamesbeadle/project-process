# How We Work

This block is installed by the project-process kit and refreshed by re-running its bootstrap; edit the kit, not this copy. Everything below the block is this repository's own working notes.

## The work is logged in Your Business Today

Every piece of work on this repository is done on a task in Your Business Today (YBT), reached through the YBT connector. YBT's `get_current_context` carries the working doctrine and is read first in every session; `describe_action` carries the doctrine of each action. In short:

1. **Start by reading what is new.** Call `read_latest_messages`. Anything addressed to the person you are working with, bring to them; post their answer on the same goal or task.
2. **Find the task before touching anything.** Call `find_tasks` on the project for the matter at hand and work on the task you find. Raise one only when nothing matches: a bug as `FIX: <what is wrong>`, a feature by its user story. Mark it in progress when the work starts.
3. **Leave a work log when the work stops.** One message on the task's conversation: what changed, which files or records, decisions taken and why, what is left. Then mark it done if it is done, or leave it in progress and say what is next.
4. **A question for another member goes on the task or goal,** naming them. Their Claude brings it to them through `read_latest_messages` and posts the answer back. Never relay through chat apps.

## The code stays at the standard by itself

The repository carries `tools/refactor/` — an audit that measures the code against the rules below and a gate that fails any change that makes a ratcheted figure worse. Every pull request and every push to the default branch runs it (`.github/workflows/code-audit.yml`). YBT counts pushes to the default branch and, every N deploys (10 by default, set on the project), raises `REFACTOR: round N` on the project and sends it to the Builder; the round runs `.claude/skills/refactor-round/SKILL.md`. Never raise a refactor round by hand — change the rhythm on the project instead. Refactor rounds never add behaviour and never change the schema.

## The rules travel with the repository

The coding rules that follow are the whole standard. They live here, in the repository, because a machine-level `~/.claude/CLAUDE.md` does not reach cloud sessions, the Builder, or anyone else's machine. Repository-specific conventions belong below the block, in this file's own notes; decisions worth keeping belong in `docs/`.
