# AGENTS.md

This repository is a starter kit for specs. `README.md` tells what it does.

- `specs/conventions/specs/` and `specs/workflow/specs/` hold the base rules. They are specs, and they win over this file (spec 000001).
- `specs/agents/` holds the rules for agents. Read them before each task.
- `specs/style/` holds the code style. The Python code in `src/` follows it.
- A change of a rule starts as a spec change with `status: draft` (spec 000002). The owner approves it.
- All text follows ASD-STE100 (spec 000025).
- Skills: `spezi-write`, `spezi-structure`, `spezi-approve`, `spezi-check`, `spezi-adopt`.
- Command: `nix run . -- <command>`. Check: `nix run . -- install`. It must show 0 errors.
- Code check: `nix develop -c ruff check src tests`, `nix develop -c basedpyright`. Both must show 0 errors.
- Tests: `nix develop -c pytest`. All tests must pass.
- `spezi init` and `spezi update` copy `specs/.templates/`, the skills `.claude/skills/spezi-*` and `src/spezi/data/` into a project. A new file of the kit that a project needs must be in one of these places.

<!-- spezi:begin (written by spezi install, do not edit) -->
## Rules for agents

The rules for agents (A) and the workflow rules (W) that apply to this project. Before a
task, read each rule in this table that applies to the task. A rule wins over other text
in this file. The ID links to the rule.

| ID | Title | Status |
| --- | --- | --- |
| [A/work/approval/000045](/specs/agents/work/approval/000045_one-spec-per-question.md) | An agent asks for the approval of one spec in one question | approved |
| [A/work/approval/000046](/specs/agents/work/approval/000046_show-the-whole-spec.md) | An agent shows the whole spec for its approval | approved |
| [A/work/questions/000043](/specs/agents/work/questions/000043_ask-each-detail.md) | An agent asks the user about each open detail | approved |
| [A/work/questions/000044](/specs/agents/work/questions/000044_follow-the-spec.md) | To follow a spec is not an assumption | approved |
| [A/work/questions/000095](/specs/agents/work/questions/000095_one-detail-per-question.md) | An agent asks about one detail in one question | approved |
| [W/kit/migrations/000090](/specs/workflow/kit/migrations/000090_migration-ci.md) | The CI migrates demo projects from each migration | approved |
| [W/kit/migrations/000203](/specs/workflow/kit/migrations/000203_start-commits.md) | The start commits come from the migrations | approved |
| [W/kit/migrations/000204](/specs/workflow/kit/migrations/000204_install-twice.md) | A migrated demo installs two times | approved |
| [W/kit/release/000091](/specs/workflow/kit/release/000091_release-workflow.md) | A tag publishes the package and the binaries | approved |
| [W/kit/release/000205](/specs/workflow/kit/release/000205_pr-builds-only.md) | A pull request builds and tests the release | approved |
| [W/kit/release/000206](/specs/workflow/kit/release/000206_publish-after-binaries.md) | The release publishes only after each binary passes | approved |
| [W/kit/release/000207](/specs/workflow/kit/release/000207_version-from-git.md) | The version comes from the git tag | approved |
| [W/kit/release/000208](/specs/workflow/kit/release/000208_flake-version.md) | The flake sets the version from the commit | approved |
| [W/specs/process/000001](/specs/workflow/specs/process/000001_precedence.md) | A spec wins over other guidance | approved |
| [W/specs/process/000002](/specs/workflow/specs/process/000002_spec-first.md) | A change request starts as a spec | approved |
| [W/specs/process/000003](/specs/workflow/specs/process/000003_change-process.md) | A change goes through a pull request | approved |
| [W/specs/process/000202](/specs/workflow/specs/process/000202_tell-the-owner.md) | An agent tells the owner when code and a spec do not agree | approved |
<!-- spezi:end -->
