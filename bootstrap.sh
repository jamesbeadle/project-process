#!/usr/bin/env bash
# project-process bootstrap — installs or refreshes the kit in a repository. Idempotent:
# run it again and it reports "unchanged" for everything it already did.
#
#   curl -fsSL https://raw.githubusercontent.com/jamesbeadle/project-process/main/bootstrap.sh | bash -s -- [options]
#   ./bootstrap.sh --kit /path/to/project-process --repo /path/to/repository [options]
#
# Options:
#   --repo <path>      the repository to install into (default: the git root of the current directory)
#   --kit <path>       a local checkout of the kit (default: a shallow clone of the kit repository)
#   --stack <name>     dotnet-blazor | sveltekit | generic (default: detected from the repository)
#   --branch <name>    the default branch the audit and the cadence watch (default: detected, else main)
#   --check            change nothing; exit 1 if anything would change (drift from the kit)
#   --with-migration-gate  also install the Builder's migration-gate workflow
set -euo pipefail

KIT_REPOSITORY="https://github.com/jamesbeadle/project-process"
REPOSITORY=""
KIT=""
STACK=""
DEFAULT_BRANCH=""
IS_CHECK_ONLY="no"
WITH_MIGRATION_GATE="no"
CHANGED_COUNT=0

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPOSITORY="$2"; shift 2 ;;
    --kit) KIT="$2"; shift 2 ;;
    --stack) STACK="$2"; shift 2 ;;
    --branch) DEFAULT_BRANCH="$2"; shift 2 ;;
    --check) IS_CHECK_ONLY="yes"; shift ;;
    --with-migration-gate) WITH_MIGRATION_GATE="yes"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

say() { printf '%s\n' "$*"; }
report() { say "  $1  $2"; }
noteChange() { CHANGED_COUNT=$((CHANGED_COUNT + 1)); }

resolveRepository() {
  if [ -z "$REPOSITORY" ]; then REPOSITORY="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; fi
  REPOSITORY="$(cd "$REPOSITORY" && pwd)"
}

obtainKit() {
  if [ -n "$KIT" ]; then KIT="$(cd "$KIT" && pwd)"; return; fi
  KIT="$(mktemp -d)/project-process"
  git clone --quiet --depth 1 "$KIT_REPOSITORY" "$KIT"
}

detectStack() {
  if [ -n "$STACK" ]; then return; fi
  if ls "$REPOSITORY"/*.sln >/dev/null 2>&1 || find "$REPOSITORY" -maxdepth 3 -name '*.csproj' -not -path '*/node_modules/*' | grep -q .; then STACK="dotnet-blazor"
  elif [ -f "$REPOSITORY/svelte.config.js" ]; then STACK="sveltekit"
  else STACK="generic"; fi
}

detectDefaultBranch() {
  if [ -n "$DEFAULT_BRANCH" ]; then return; fi
  DEFAULT_BRANCH="$(git -C "$REPOSITORY" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)"
  if [ -z "$DEFAULT_BRANCH" ]; then DEFAULT_BRANCH="main"; fi
}

writeIfDifferent() {
  local source="$1" destination="$2"
  if [ -f "$destination" ] && cmp -s "$source" "$destination"; then report unchanged "$destination"; return; fi
  local outcome="updated"; [ -f "$destination" ] || outcome="created"
  noteChange
  if [ "$IS_CHECK_ONLY" = "yes" ]; then report "would-$outcome" "$destination"; return; fi
  mkdir -p "$(dirname "$destination")"
  cp "$source" "$destination"
  report "$outcome" "$destination"
}

writeOnce() {
  local source="$1" destination="$2"
  if [ -f "$destination" ]; then report kept "$destination"; return; fi
  noteChange
  if [ "$IS_CHECK_ONLY" = "yes" ]; then report would-create "$destination"; return; fi
  mkdir -p "$(dirname "$destination")"
  cp "$source" "$destination"
  report created "$destination"
}

installClaudeBlock() {
  local body; body="$(mktemp)"
  cat "$KIT/kit/claude/working-process.md" > "$body"
  printf '\n' >> "$body"
  cat "$KIT/kit/claude/code-rules.md" >> "$body"
  local mode=""; [ "$IS_CHECK_ONLY" = "yes" ] && mode="check"
  local outcome; outcome="$(python3 "$KIT/tools/managed_block.py" "$REPOSITORY/CLAUDE.md" "$body" "$(cat "$KIT/VERSION")" $mode)"
  if [ "$outcome" != "unchanged" ]; then noteChange; fi
  if [ "$IS_CHECK_ONLY" = "yes" ] && [ "$outcome" != "unchanged" ]; then outcome="would-$outcome"; fi
  report "$outcome" "$REPOSITORY/CLAUDE.md"
  rm -f "$body"
}

installRefactorKit() {
  local target="$REPOSITORY/tools/refactor" file
  for file in $(cd "$KIT/kit/refactor" && find audit -name '*.py' | sort); do
    writeIfDifferent "$KIT/kit/refactor/$file" "$target/$file"
  done
  writeIfDifferent "$KIT/kit/refactor/README.md" "$target/README.md"
  writeIfDifferent "$KIT/kit/refactor/playbook.md" "$target/playbook.md"
  writeIfDifferent "$KIT/VERSION" "$target/kit-version"
  writeOnce "$KIT/kit/refactor/presets/$STACK.json" "$target/rules.json"
}

installWorkflow() {
  local rendered; rendered="$(mktemp)"
  sed "s/__DEFAULT_BRANCH__/$DEFAULT_BRANCH/g" "$KIT/kit/workflows/code-audit.yml" > "$rendered"
  writeIfDifferent "$rendered" "$REPOSITORY/.github/workflows/code-audit.yml"
  rm -f "$rendered"
  if [ "$WITH_MIGRATION_GATE" = "yes" ]; then
    writeIfDifferent "$KIT/kit/workflows/migration-gate.yml" "$REPOSITORY/.github/workflows/migration-gate.yml"
  fi
}

installSkills() {
  writeIfDifferent "$KIT/kit/skills/refactor-round/SKILL.md" "$REPOSITORY/.claude/skills/refactor-round/SKILL.md"
}

establishBaseline() {
  local target="$REPOSITORY/tools/refactor"
  if [ -f "$target/baseline.json" ]; then report kept "$target/baseline.json"; return; fi
  noteChange
  if [ "$IS_CHECK_ONLY" = "yes" ]; then report would-create "$target/baseline.json"; return; fi
  command -v jscpd >/dev/null 2>&1 || say "  note      jscpd is not installed; the duplication figure is skipped in this baseline (npm install -g jscpd)"
  (cd "$REPOSITORY" && python3 -m tools.refactor.audit.run_audit . --output tools/refactor/audit-output >/dev/null)
  cp "$target/audit-output/audit.json" "$target/baseline.json"
  cp "$target/audit-output/audit-report.md" "$target/baseline-report.md"
  report created "$target/baseline.json"
  report created "$target/baseline-report.md"
}

printNextSteps() {
  say ""
  say "Next, in Your Business Today (once per repository):"
  say "  1. Record the repository URL on the project (set_project_client or the project's Edit form)."
  say "  2. Point the repository's GitHub webhook at <ybt>/api/github-webhook with the shared secret,"
  say "     sending pull request AND push events — pushes to '$DEFAULT_BRANCH' are the deploys the cadence counts."
  say "  3. Set 'Refactor every N deploys' on the project (default 10; 0 turns the cadence off)."
}

main() {
  resolveRepository
  obtainKit
  detectStack
  detectDefaultBranch
  say "project-process kit v$(cat "$KIT/VERSION") → $REPOSITORY (stack: $STACK, default branch: $DEFAULT_BRANCH)"
  installClaudeBlock
  installRefactorKit
  installWorkflow
  installSkills
  establishBaseline
  if [ "$IS_CHECK_ONLY" = "yes" ]; then
    if [ "$CHANGED_COUNT" -gt 0 ]; then say "Drift: $CHANGED_COUNT item(s) differ from the kit."; exit 1; fi
    say "In step with the kit."; exit 0
  fi
  if [ "$CHANGED_COUNT" -eq 0 ]; then say "Nothing to do — already in step with the kit."; else say "$CHANGED_COUNT item(s) written. Review with git status, then commit."; printNextSteps; fi
}

main
