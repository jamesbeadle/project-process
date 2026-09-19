# project-process

The one way every software project is run, whatever its stack: the code follows one set of rules, the rules travel with the repository, the code is measured and refactored on a rhythm nobody has to remember, every piece of work is done on a `fix/` or `feature/` branch and reaches the default branch only by a reviewed pull request, every piece of work is logged where the project is managed, and two people's Claudes talk to each other through that log instead of through pasted messages. This repository is the kit that installs it and the doctrine that runs it. Your Business Today (YBT) is the hub it plugs into.

Install it into any repository, new or old, with one command, run from inside that repository. Run the same command again whenever the kit changes; it touches only what differs.

```
bash ~/Documents/Claude/Projects/project-process/bootstrap.sh --kit ~/Documents/Claude/Projects/project-process
```

With a checkout of this kit anywhere, `--kit` points at it. The kit is public, so the one-liner needs no checkout:

```
curl -fsSL https://raw.githubusercontent.com/jamesbeadle/project-process/main/bootstrap.sh | bash
```

## The six parts

**1. One set of coding rules.** `kit/claude/code-rules.md` is *How I Write Code*, the whole standard, and the bootstrap places it — with the short working-process doctrine in front of it — inside a managed block at the top of the repository's `CLAUDE.md`. The block is refreshed on every run; everything below it belongs to the repository. See "Where the instruction files live" for why it is a block in the repository and not a file on a machine.

**2. A measured score, a measured plan, a ratcheted refactor — as Claude scripts, not CI.** `kit/refactor/` is installed as `tools/refactor/` and does three things. The **audit** measures a codebase against the rules: the standard baseline checks (files over the line limit, the worst file, functions over the limit, else blocks, duplication, explanatory comments, inline magic values, orphan components and functions, long member chains, deep indentation, overlong function names), the design pattern file count check (the files the repository's own patterns predict but which are missing; entities whose file count is outside what their complexity predicts), the prose check (conditions with calls tangled inside calls, comparisons to raw literals, accessor names that want to be a property), and the site definition (every routed view and every component of the site written in the widget notation from the views themselves, and the markup written by hand where a catalogue widget should be — "The site definition" below). The **score** turns every figure into one percentage, and the **gate** fails when a ratcheted figure is worse than the committed baseline. Two sentences from the person run it, through the skills the kit installs in `.claude/skills/`:

- *"Run the code quality check"* — `code-quality-check`: on a `quality/check-<date>` branch, a box at the bottom of the repository's `README.md` holding the score, with its breakdown, the count of every file in the repository by area (frontend, backend, API, database, infrastructure…) and the refactoring plan expandable beneath it; `tools/refactor/refactor-plan.md`, the steps a refactor of that repository follows, in order; and `tools/refactor/site-definition.md`, what a user sees at each route. No source changes.
- *"Refactor the repo"* — `refactor-round`: one measured round on `refactor/round-N` that takes the next steps from the top of that plan — widget adoption, then component breakout, then utility function identification, then design pattern identification and modification, then the sweep to zero — behaviour unchanged, baseline first and last, ending with the new score.

`end-of-day` runs the round if one is due, the connector check, and the plain-English summary on the day's tasks. All of them commit on a branch, push, and open a pull request for the person to merge (part 6); nothing runs on GitHub. `playbook.md` is the nine-stage method; the bootstrap takes Stage 0 (the baseline) for a repository that has none. (`--with-ci-gate` installs a GitHub workflow for anyone who does want the gate on their pushes.) "How the score is made" below has the arithmetic.

**3. The refactor round on a deploy rhythm.** A round is due every N commits on the default branch since the baseline was last committed — `tools/refactor/deploys_since_baseline.sh` says so, from git alone, ten unless told otherwise. Optionally, YBT counts pushes to the branch through the repository's GitHub webhook and raises `REFACTOR: round N` on the project as the reminder at N; the round is still run by a person's Claude, on its own branch. Nothing about the rhythm lives in the repository beyond the baseline commit, so adding an old repository is running the bootstrap once; the count starts from that commit.

**4. Every conversation is logged on a task.** YBT's `get_current_context` carries the working doctrine, so any Claude connected to YBT reads it before doing anything: read what is new, find the task the work belongs to (`FIX: …` for a bug, the story for a feature), raise one only when nothing matches, read the task's attachments before starting, attach any file the work depends on (`attach_file_to_task`, by public link up to 25 MB or inline under 3 MB), mark it in progress, and leave a work-log message when the work stops. The tasks and their conversations are the record of what was done and why, kept for analysis rather than deleted on completion.

**5. Members talk through their Claudes.** A question for another person on the project is posted on the task or goal naming them; their Claude reads it through `read_latest_messages` at the start of their next session, brings it to them, and posts the answer back. Support tasks carry a raiser and a resolution. No relay through chat apps.

**6. Nothing lands on the default branch but a reviewed pull request.** Every change a Claude makes starts on a branch named for its task — `fix/<slug>` for a `FIX:` task, `feature/<slug>` for a story, `refactor/round-N` for a round — is committed there step by step, pushed, and opened as a pull request titled with the task. A person merges. The doctrine block in `CLAUDE.md` says so, and the bootstrap also installs `tools/branch_guard/` as a Claude Code `PreToolUse` hook in `.claude/settings.json`: it refuses any `git commit`, `merge`, `rebase`, `cherry-pick` or `revert` on the default branch, any push that would move it (`git push origin HEAD:main` included) and `gh pr merge`, and tells Claude to branch instead. The hook merges into whatever `.claude/settings.json` the repository already has and travels with the clone, so it holds in Cowork, cloud sessions and every colleague's Claude Code alike. For the same rule against people as well as Claudes, turn on branch protection for the default branch in GitHub (Settings → Branches → require a pull request before merging).

## Where the instruction files live

Claude Code reads instruction files from several places and **concatenates them all** — nothing replaces anything. Managed policy first, then `~/.claude/CLAUDE.md` (the machine), then the repository's `CLAUDE.md` (or `.claude/CLAUDE.md`), then `CLAUDE.local.md`, then any `CLAUDE.md` in a subdirectory when a file in it is read. When two say different things, the more specific one is later in the context and is what Claude follows. `@path` imports pull other files in (four levels deep), and `.claude/rules/*.md` files load beside the root file, path-scoped when they carry `paths:` front matter.

What that means for a team: a rule that lives in `~/.claude/CLAUDE.md` on one machine reaches exactly that machine. It does **not** reach a cloud session, a routine, the Builder, or a colleague — they see the clone and nothing else. Cowork reads the connected folder's `CLAUDE.md` and skips imports that point outside it. So the rules that every session must follow go in the repository, in the one file every tool reads, which is why the kit writes a managed block into `CLAUDE.md` rather than asking for an import or a machine-level file. The machine-level file is for personal preferences only; it is still loaded, on top.

Skills (`.claude/skills/<name>/SKILL.md`) are procedures invoked on demand and travel with the clone the same way; the kit installs `code-quality-check`, `refactor-round` and `end-of-day` there. Skills in `~/.claude/skills/` are personal and stay on the machine.

## How the score is made

Seventeen elements in four groups. Each element scores 100% with no offenders and falls in a straight line to 0% when its offenders, measured against the size of the codebase, reach its zero point; the score is the average of the elements by weight. An element that cannot be measured in a repository (no entities declared in `rules.json`, no jscpd for duplication) lends its weight to the rest, and the box says *not measured*. A score below 100% never displays as 100.0%.

| Group | Element | Measured against | 0% at | Weight |
| --- | --- | --- | --- | --- |
| Standard baseline checks (60) | Files over the line limit | all source files | 50% of files | 10 |
| | Worst file | the limit | 9 limits over (1,000 lines at a limit of 100) | 5 |
| | Functions over the line limit | all functions | 25% of functions | 8 |
| | Else blocks | all `if` branches | 50% of branches | 5 |
| | Duplication % | — | 20% | 8 |
| | Explanatory comment lines | thousand source lines | 50 per thousand | 4 |
| | Inline magic values (hex colours, inline styles, repeated literals) | thousand source lines | 20 per thousand | 4 |
| | Orphan components and functions | all components and functions | 10% | 4 |
| | Long member chain lines (one chain more than two property hops deep; calls are not hops) | thousand source lines | 30 per thousand | 4 |
| | Deeply indented lines | thousand source lines | 30 per thousand | 4 |
| | Overlong function names | all functions | 10% of functions | 4 |
| Design pattern file count (20) | Files the patterns predict but are missing | all predicted files | 50% | 10 |
| | Entities outside their expected file count | all entities | 50% | 10 |
| Prose (20) | Conditions with calls tangled inside calls | all `if` branches | 25% of branches | 8 |
| | Conditions compared to a raw literal | all `if` branches | 25% of branches | 6 |
| | Accessor names that want to be a property | all functions | 10% of functions | 6 |
| Widget adoption (8) | Markup written by hand where a widget should be | all widget slots (every widget used, plus every place one should be) | 50% of slots | 8 |

The weights and zero points live in `kit/refactor/audit/score/elements.py`; a repository overrides any of them in its `rules.json` under `score.elements.<key>` (`{"weight": …, "zeroAt": …}`), and the box prints them beside every reading so the number can be worked out by hand. The score is measured, never judged — no opinion of Claude's enters it, so the same code always scores the same. The standard checks are deliberately not independent: the worst file cannot keep falling while files remain over the limit, so in the end they reach zero together, and the overflow between them on the way is the round's to put in order.

The **design pattern file count check** reads patterns off the file names. A file name is a subject and a role — `CreateProjectHandler` is the `Handler` of `CreateProject`; a SvelteKit route folder is the subject of its `+page.svelte` and `+page.server.ts`. A role that four or more subjects share is a family, and when three quarters or more of the subjects with one role also have another, that is a pattern and it predicts the file for the rest. A subject that truly has no such job is listed in `rules.json` under `designPatterns.acceptedGaps`. Separately, the entities declared under `designPatterns.entityGlobs` are counted for properties and for files named for them; the repository's own median ratio of files to properties says how many files each entity's complexity predicts, and an entity outside half-to-double that is out of range.

## The site definition

The audit also defines the site in widgets, from the code, so the definition can never go stale: every routed view (`@page` in Razor, the `+page` file's path in SvelteKit) and every component of the site is read as a tree of the shared widgets it composes and written in one notation — `a, b` stacked top to bottom · `[ a b ]` side by side · `(3) a` three of them, `(n) a` one per item · `?when: a` shown on a condition · `( a | b )` one or the other · `Widget{ … }` a catalogue widget with its content · `Part=( … )` one of the site's own components opened out · `⚠table→RecordsTable` markup written by hand where the named widget should be. The quality check writes it to `tools/refactor/site-definition.md`: the table of what is written by hand, widget by widget; each route opened out to what a user sees there; each component with its definition and how many views use it. A home page reads, for instance, `PageHeader{ DropdownMenu }, [ (3) StatTile ], MyTodosPanel=( ⚠h2→SectionHeader, LoadGate{ … } ), NextValuationsPanel=( ⚠h2→SectionHeader, ⚠table→RecordsTable )`, and *"find every view that hand-rolls a table"* is a search of that file.

The vocabulary is the repository's, in `rules.json` under `siteDefinition`: `catalogue` names the shared widgets every view is meant to compose (the presets leave it empty, which means *not measured*, so a repository is measured only once it names its widgets), and `handRolled` says which element each widget owns (`{"element": "table", "ownedBy": "RecordsTable"}`), with `unlessClassPrefixes` and `unlessAttributes` for the classes of markup a rule leaves alone; an owner not yet in the catalogue is a widget to build. A widget's own file is never measured against the rules, and an owner counts as present anywhere inside it. The figure scores the *Widget adoption* group, ratchets in the gate, and is Pass 1 of the refactoring plan — file-sized steps, the fullest first, each adopting one widget in a few files, ahead of component breakout because a widget that exists is the cheapest shrink — which is how the round holds the site to *the same kind of data uses the same widget everywhere* without anyone re-surveying the views.

## The brand and the widgets' designs

Optional, for a site big enough to have a widget catalogue. Two layers in one structure under `docs/design/`: the **brand sheet** (`brand.md` — every colour, type, spacing, radius, elevation and motion token in the theme with its *role*, what it is for and never for) and a **design sheet per widget** that has one (`widgets/<Widget>.md` — anatomy, tokens, states, variants, behaviour, in the theme's token names, extracted from images or any reference the person supplies; a widget with no sheet is brand only). The index is `widgets.json`. A Claude building or changing a widget reads the sheet if there is one, else the brand sheet — that is the doctrine line in `CLAUDE.md`. The `widget-design` skill does the work on request: *"Set up the widget designs"*, *"Extract the brand from <references>"*, *"Extract the design for <Widget> from <images>"*, *"Check the site against the brand"*, *"Check the widgets against their designs"*. None of it is scored or gated, because a design is a judgement: the audit only reports the standing — sheets held, each check's last run or *never* — in the site definition and the README box, and every refactor round repeats it in its first lines so a stale check is seen every ten commits without the round running it.

## Onboarding a repository

Run the bootstrap in the repository (it detects the stack — `dotnet-blazor`, `sveltekit` or `generic` — and the default branch, or take `--stack` and `--branch`). Read the block it put at the top of `CLAUDE.md`, and `tools/refactor/rules.json`, which is the repository's own copy of the preset: nothing in it is ever overwritten, and a newer kit only adds the blocks it lacks. Commit what it wrote on a branch (`git switch -c feature/project-process-<version>`), push it and merge the pull request — that merge is where the deploy count starts. From then on *Run the code quality check* publishes the score and the plan, *Refactor the repo* works the plan, `end-of-day` closes each working day, and a round runs when it is due.

Optionally, in YBT: record the repository URL and default branch on the project (the project's Edit form, or `update_project_details`), send **push** events from the repository's GitHub webhook to `<ybt>/api/github-webhook` with the shared secret, and set *Refactor every N deploys*; YBT then raises `REFACTOR: round N` on the project as the reminder. For a repository the Builder will work on, the Builder's own rails apply as well (`--with-migration-gate` installs the optional migration gate) — `docs/builder-architecture.md` in the YBT repository has them.

`bootstrap.sh --check` reports drift from the kit without writing anything and exits 1 when something differs.

## Onboarding a person

Invite them to the project in YBT (`invite_to_project` by email, or the project's People panel); they join at once. They press **Connect** in YBT to add the YBT connector to their own Claude and sign in as themselves — there is no token to copy. From then on their Claude reads the working doctrine from `get_current_context` on every session and follows it: nothing to install, nothing to paste. Only the repository's clone needs the kit, and it is already in it.

## What is in this repository

| Path | What it is |
| --- | --- |
| `bootstrap.sh` | The idempotent installer |
| `tools/managed_block.py` | Keeps the block at the top of a `CLAUDE.md` |
| `tools/managed_rules.py` | Adds the rule blocks a newer kit expects to an existing `rules.json`, touching nothing already in it |
| `tools/managed_settings.py` | Registers the branch guard in `.claude/settings.json`, keeping everything else in it |
| `kit/hooks/branch_guard/` | The branch guard hook, installed as `tools/branch_guard/` |
| `kit/claude/code-rules.md` | *How I Write Code* — the standard |
| `kit/claude/working-process.md` | The always-on doctrine placed before the rules |
| `kit/refactor/` | The audit, the score, the plan, the gate, the playbook and the stack presets |
| `kit/refactor/deploys_since_baseline.sh` | Says when a round is due, from git alone |
| `kit/skills/code-quality-check/SKILL.md` | *Run the code quality check*: the score box in the README, the file count by area, the refactoring plan |
| `kit/skills/refactor-round/SKILL.md` | *Refactor the repo*: one measured round that works the plan — widget adoption, breakout, utilities, patterns, sweep |
| `kit/skills/end-of-day/SKILL.md` | The day's close: the round if due, the connector check, the plain-English summary |
| `kit/skills/widget-design/SKILL.md` | The brand sheet and the widgets' design sheets: set up, extract from images, check the site against them |
| `kit/workflows/code-audit.yml` | Optional (`--with-ci-gate`): the gate as a GitHub check |
| `kit/workflows/migration-gate.yml` | Optional (`--with-migration-gate`): the Builder's schema gate |
| `VERSION` | Stamped into every installed block and `tools/refactor/kit-version` |

## Maintaining the kit

Change the rules or the doctrine here — on a branch, like everything else — bump `VERSION`, and once it is merged re-run the bootstrap in each repository, on a branch there too; it rewrites the block, the kit files and the guard's hook entry, adds to `rules.json` only the blocks it lacks, and leaves `baseline.json`, the rest of `.claude/settings.json` and the repository's own notes alone. From 1.5.1 widget adoption is Pass 1 of the plan, in file-sized steps, so a round reaches it instead of asking whether to skip 200 breakout steps to get there; the round never asks which steps to take. From 1.5.0 the kit carries the brand and widget designs: the `widget-design` skill, the doctrine line, and the standing of the design checks in the site definition, the README box and every round's first lines — nothing scored, nothing gated, and nothing until a repository sets up `docs/design/widgets.json`. From 1.4.1 the site definition's line numbers are right after a multi-line razor comment (1.4.0 dropped the comment's line breaks, so every finding after one read early; counts were unaffected). From 1.4.0 the audit carries the site definition: the `siteDefinition` block is added to an existing `rules.json` from the stack's preset with an empty catalogue, the score gains the *Widget adoption* element (not measured until the catalogue is named, so an existing score does not move by itself), the gate ratchets the hand-rolled figure once a baseline holds it, and the refactoring plan's passes after component breakout move down one. From 1.3.2 the refactoring plan treats two functions as one only when their bodies match word for word, and a file as using a view's function only when it imports it from that view; a name that recurs across components (`onSubmit`, `reload`) no longer produces a step. From 1.3.1 the member chain check measures the depth of one chain of properties (`prose.maxMemberChainDepth`, two unless set) instead of the dots on a line; the old `prose.maxMemberAccessesPerLine` is no longer read and can be deleted, and `longMemberChainLines` means something new, so it is comparable again from a repository's next baseline. A repository installed before 1.3.0 keeps its `rules.json` exactly as it is; the bootstrap only adds the top-level blocks a newer kit expects and the file lacks (`areas`, `designPatterns`, `score`), from the stack's preset, and never touches a block that is already there. The presets and the audit checks are heuristic and language-tolerant (C-family and TypeScript function shapes and names, C# and TypeScript booleans, `//`, `#`, `@*` and `<!--` comments); a new stack is a new preset, not a new check.
