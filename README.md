# project-process

The one way every software project is run, whatever its stack: the code follows one set of rules, the rules travel with the repository, the code is measured and refactored on a rhythm nobody has to remember, every piece of work is logged where the project is managed, and two people's Claudes talk to each other through that log instead of through pasted messages. This repository is the kit that installs it and the doctrine that runs it. Your Business Today (YBT) is the hub it plugs into.

Install it into any repository, new or old, with one command. Run the same command again whenever the kit changes; it touches only what differs.

```
curl -fsSL https://raw.githubusercontent.com/jamesbeadle/project-process/main/bootstrap.sh | bash
```

## The five parts

**1. One set of coding rules.** `kit/claude/code-rules.md` is *How I Write Code*, the whole standard, and the bootstrap places it — with the short working-process doctrine in front of it — inside a managed block at the top of the repository's `CLAUDE.md`. The block is refreshed on every run; everything below it belongs to the repository. See "Where the instruction files live" for why it is a block in the repository and not a file on a machine.

**2. Measured, ratcheted refactoring.** `kit/refactor/` is the audit and gate that measure a codebase against the rules (file length, function length, else blocks, duplication, comments, magic values, prose, orphan components) and fail any change that makes a ratcheted figure worse than the committed baseline. Installed as `tools/refactor/` with `.github/workflows/code-audit.yml` running it on every pull request and push. `playbook.md` is the nine-stage method; the bootstrap takes Stage 0 (the baseline) for a repository that has none.

**3. The refactor round on a deploy rhythm.** YBT counts pushes to the repository's default branch through the GitHub webhook it already receives, and every N of them (10 by default, set per project) raises `REFACTOR: round N` on the project and sends it to the Builder. The round is `kit/skills/refactor-round/SKILL.md`, installed as a project skill: baseline first, worst files first, behaviour unchanged, baseline last, pull request with the before and after. Nothing about the rhythm lives in the repository, so adding an old repository is registering it in YBT and running the bootstrap once; the count starts from then.

**4. Every conversation is logged on a task.** YBT's `get_current_context` carries the working doctrine, so any Claude connected to YBT reads it before doing anything: read what is new, find the task the work belongs to (`FIX: …` for a bug, the story for a feature), raise one only when nothing matches, mark it in progress, and leave a work-log message when the work stops. The tasks and their conversations are the record of what was done and why, kept for analysis rather than deleted on completion.

**5. Members talk through their Claudes.** A question for another person on the project is posted on the task or goal naming them; their Claude reads it through `read_latest_messages` at the start of their next session, brings it to them, and posts the answer back. Support tasks carry a raiser and a resolution. No relay through chat apps.

## Where the instruction files live

Claude Code reads instruction files from several places and **concatenates them all** — nothing replaces anything. Managed policy first, then `~/.claude/CLAUDE.md` (the machine), then the repository's `CLAUDE.md` (or `.claude/CLAUDE.md`), then `CLAUDE.local.md`, then any `CLAUDE.md` in a subdirectory when a file in it is read. When two say different things, the more specific one is later in the context and is what Claude follows. `@path` imports pull other files in (four levels deep), and `.claude/rules/*.md` files load beside the root file, path-scoped when they carry `paths:` front matter.

What that means for a team: a rule that lives in `~/.claude/CLAUDE.md` on one machine reaches exactly that machine. It does **not** reach a cloud session, a routine, the Builder, or a colleague — they see the clone and nothing else. Cowork reads the connected folder's `CLAUDE.md` and skips imports that point outside it. So the rules that every session must follow go in the repository, in the one file every tool reads, which is why the kit writes a managed block into `CLAUDE.md` rather than asking for an import or a machine-level file. The machine-level file is for personal preferences only; it is still loaded, on top.

Skills (`.claude/skills/<name>/SKILL.md`) are procedures invoked on demand and travel with the clone the same way; the kit installs `refactor-round` there. Skills in `~/.claude/skills/` are personal and stay on the machine.

## Onboarding a repository

Run the bootstrap in the repository (it detects the stack — `dotnet-blazor`, `sveltekit` or `generic` — and the default branch, or take `--stack` and `--branch`). Read the block it put at the top of `CLAUDE.md`, and `tools/refactor/rules.json`, which is the repository's own copy of the preset and is never overwritten. Commit what it wrote. Then, in YBT: record the repository URL on the project (`set_project_client`, or the project's Edit form), point the repository's GitHub webhook at `<ybt>/api/github-webhook` with the shared secret and **push as well as pull request events**, and set *Refactor every N deploys* on the project. Pushes to the default branch count from that moment; the first round is raised at N.

For a repository the Builder will work on, the Builder's own rails apply as well (branch protection, the `ci` check, auto-merge; `--with-migration-gate` installs the optional migration gate) — `docs/builder-architecture.md` in the YBT repository has them.

`bootstrap.sh --check` reports drift from the kit without writing anything and exits 1 when something differs; a repository can run it in CI to find out it is behind.

## Onboarding a person

Invite them to the project in YBT (`invite_to_project` by email, or the project's People panel); they join at once. They press **Connect** in YBT to add the YBT connector to their own Claude and sign in as themselves — there is no token to copy. From then on their Claude reads the working doctrine from `get_current_context` on every session and follows it: nothing to install, nothing to paste. Only the repository's clone needs the kit, and it is already in it.

## What is in this repository

| Path | What it is |
| --- | --- |
| `bootstrap.sh` | The idempotent installer |
| `tools/managed_block.py` | Keeps the block at the top of a `CLAUDE.md` |
| `kit/claude/code-rules.md` | *How I Write Code* — the standard |
| `kit/claude/working-process.md` | The always-on doctrine placed before the rules |
| `kit/refactor/` | The audit, the gate, the playbook and the stack presets |
| `kit/skills/refactor-round/SKILL.md` | The round the cadence runs |
| `kit/workflows/code-audit.yml` | The gate in CI |
| `kit/workflows/migration-gate.yml` | Optional: the Builder's schema gate |
| `VERSION` | Stamped into every installed block and `tools/refactor/kit-version` |

## Maintaining the kit

Change the rules or the doctrine here, bump `VERSION`, and re-run the bootstrap in each repository; it rewrites the block and the kit files and leaves `rules.json`, `baseline.json` and the repository's own notes alone. The presets and the audit checks are heuristic and language-tolerant (C-family and TypeScript function shapes and names, C# and TypeScript booleans, `//`, `#`, `@*` and `<!--` comments); a new stack is a new preset, not a new check.
