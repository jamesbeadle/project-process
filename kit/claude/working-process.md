# How We Work

This block is installed by the project-process kit and refreshed by re-running its bootstrap; edit the kit, not this copy. Everything below the block is this repository's own working notes.

## The work is logged in Your Business Today

Every piece of work on this repository is done on a task in Your Business Today (YBT), reached through the YBT connector. YBT's `get_current_context` carries the working doctrine and is read first in every session; `describe_action` carries the doctrine of each action. In short:

1. **Start by reading what is new.** Call `read_latest_messages`. Anything addressed to the person you are working with, bring to them; post their answer on the same goal or task.
2. **Find the task before touching anything.** Call `find_tasks` on the project for the matter at hand and work on the task you find. Raise one only when nothing matches: a bug as `FIX: <what is wrong>`, a feature by its user story. Mark it in progress when the work starts.
3. **Leave a work log when the work stops.** One message on the task's conversation: what changed, which files or records, decisions taken and why, what is left. Then mark it done if it is done, or leave it in progress and say what is next.
4. **A question for another member goes on the task or goal,** naming them. Their Claude brings it to them through `read_latest_messages` and posts the answer back. Never relay through chat apps.

## The code stays at the standard through Claude scripts, not CI

The repository carries `tools/refactor/` — an audit that measures the code against the rules below and a gate that fails when a ratcheted figure is worse than the committed baseline. Nothing runs on GitHub: the gate is run by the Claude scripts in `.claude/skills/` — `refactor-round` (one measured round: baseline first, worst files first, behaviour unchanged, baseline last) and `end-of-day` (the day's close: the round if one is due, the connector check, the plain-English summary on the day's tasks). A round is due when `tools/refactor/deploys_since_baseline.sh` says so: the commits on the default branch since the baseline was last committed, ten or more unless the project says otherwise. Your Business Today can also raise `REFACTOR: round N` on the project as the reminder when its own deploy count reaches N. Either way a person's Claude runs the round in the working tree and the person commits — the scripts never commit, push or open pull requests, and refactor rounds never add behaviour or change the schema.

## The rules travel with the repository

The coding rules that follow are the whole standard. They live here, in the repository, because a machine-level `~/.claude/CLAUDE.md` does not reach cloud sessions or anyone else's machine. Repository-specific conventions belong below the block, in this file's own notes; decisions worth keeping belong in `docs/`.
