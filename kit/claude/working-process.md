# How We Work

This block is installed by the project-process kit and refreshed by re-running its bootstrap; edit the kit, not this copy. Everything below the block is this repository's own working notes.

## The work is logged in Your Business Today

Every piece of work on this repository is done on a task in Your Business Today (YBT), reached through the YBT connector. YBT's `get_current_context` carries the working doctrine and is read first in every session; `describe_action` carries the doctrine of each action. In short:

1. **Start by reading what is new.** Call `read_latest_messages`. Anything addressed to the person you are working with, bring to them; post their answer on the same goal or task.
2. **Find the task before touching anything.** Call `find_tasks` on the project for the matter at hand and work on the task you find. Raise one only when nothing matches: a bug as `FIX: <what is wrong>`, a feature by its user story. Mark it in progress when the work starts — and start it on a branch named for it (next section), never on the default branch.
3. **Leave a work log when the work stops.** One message on the task's conversation: what changed, which files or records, decisions taken and why, what is left, and the branch and pull request the work is on. Then mark it done if it is done, or leave it in progress and say what is next.
4. **A question for another member goes on the task or goal,** naming them. Their Claude brings it to them through `read_latest_messages` and posts the answer back. Never relay through chat apps.

## The work happens on a branch, never on the default branch

Nothing is committed to the default branch (`main`, or whatever `origin/HEAD` points at) by a Claude — not a fix, not a feature, not a refactor round, not a one-line change. The default branch only ever moves by a pull request that a person has reviewed and merged. Every session that is about to change a file does this, in order:

1. **Start from a fresh default branch.** `git fetch origin` and `git switch <default>` followed by `git pull --ff-only`; if the working tree already holds uncommitted changes, stop and ask the person what they belong to before going further.
2. **Branch before the first change.** `git switch -c fix/<slug>` for a `FIX:` task, `git switch -c feature/<slug>` for a story. The slug is the task's title in lower-case words joined by hyphens, with noise words dropped: `FIX: invoice total is rounded up` becomes `fix/invoice-total-rounding`; the story *A quantity surveyor sees the weekly cashflow grid* becomes `feature/weekly-cashflow-grid`. If a branch for that task already exists (`git branch --list 'fix/*' 'feature/*'`, and `origin`), switch to it and continue there rather than starting another.
3. **Commit on the branch as the work goes**, one commit per verified step, the message a sentence about the domain (`Round the invoice total once, at the line total`), never a list of files. Run the repository's checks before each commit.
4. **Push the branch and open the pull request when the work stops** — done or not. `git push -u origin <branch>`, then a pull request into the default branch whose title is the task's title (`FIX: invoice total is rounded up`) and whose body is the work log in short: what changed, why, what is left. With the GitHub CLI: `gh pr create --base <default> --title "<task title>" --body "<the log>"`; without it, push and give the person the compare link GitHub prints. A pull request that already exists for the branch is updated by the push — do not open a second one.
5. **The person merges.** Never merge, rebase onto or force-push the default branch, and never `git switch <default>` to commit there. When the task's work needs something already on another open branch, say so on the task rather than merging branches yourself.

The repository carries a guard as well as this rule: `tools/branch_guard/`, installed as a Claude Code `PreToolUse` hook in `.claude/settings.json`, refuses any `git commit`, `git merge` or `git push` that would land on the default branch and says why. When it refuses, do what it says — branch — rather than looking for a way round it.

A refactor round follows the same shape on a `refactor/round-N` branch (its skill says so); it is the one branch that is neither a fix nor a feature.

## The code stays at the standard through Claude scripts, not CI

The repository carries `tools/refactor/` — an audit that measures the code against the rules below and a gate that fails when a ratcheted figure is worse than the committed baseline. Nothing runs on GitHub: the gate is run by the Claude scripts in `.claude/skills/` — `refactor-round` (one measured round: baseline first, worst files first, behaviour unchanged, baseline last) and `end-of-day` (the day's close: the round if one is due, the connector check, the plain-English summary on the day's tasks). A round is due when `tools/refactor/deploys_since_baseline.sh` says so: the commits on the default branch since the baseline was last committed, ten or more unless the project says otherwise. Your Business Today can also raise `REFACTOR: round N` on the project as the reminder when its own deploy count reaches N. Either way a person's Claude runs the round on a `refactor/round-N` branch, commits each verified step there, pushes it and opens the pull request for the person to review and merge — never on the default branch — and refactor rounds never add behaviour or change the schema.

## The rules travel with the repository

The coding rules that follow are the whole standard. They live here, in the repository, because a machine-level `~/.claude/CLAUDE.md` does not reach cloud sessions or anyone else's machine. Repository-specific conventions belong below the block, in this file's own notes; decisions worth keeping belong in `docs/`.
