---
id: "000066"
title: spezi init adds the kit to a project
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_writes_the_kit_files
  - tests/test_kit.py:test_init_ci_runs_on_the_base_branch
  - tests/test_kit.py:test_init_keeps_an_existing_flake
  - tests/test_kit.py:test_init_takes_the_forge_from_the_remote
  - tests/test_kit.py:test_init_reads_the_forge_from_the_host_only
  - tests/test_kit.py:test_init_stops_when_the_kit_is_there
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# spezi init adds the kit to a project

`spezi init [<dir>] [--forge github|gitlab|codeberg] [-y]` must add the kit to the project in
`<dir>`, or in the current folder. First it must ask the questions of 000085, and it must write
the answers to `spezi.toml`. It must write these files:

| File | Content |
| --- | --- |
| `spezi.toml` | The settings, with the answers of 000085 and the `ref` of the kit: the tag of the kit with the highest version, else its default branch, as in 000068. |
| `spezi.lock` | The commit that this `ref` names, and the hash of the copy of the kit (000082). |
| `specs/` | An empty folder for the rules of the project. |
| `specs/.upstream/github.com/frederikbeimgraben/spezi/` | The rules of the kit at this commit (000048). |
| `specs/.templates/` | The templates of the kit at this commit. |
| `.claude/skills/spezi-*` | The skills of the kit. |
| `.github/workflows/spezi.yml`, `.gitlab/ci/spezi.yml` or `.forgejo/workflows/spezi.yml` | The CI job for the forge, which runs `spezi check` at the commit of the kit. On GitHub and Codeberg, it runs for each pull request and for each push to the branch of `base_ref`, for example `develop` for `origin/develop`. For Codeberg, the job runs on the hosted Forgejo Actions runner `codeberg-small`. |
| `.gitlab-ci.yml` | Only for GitLab: the entry `- local: .gitlab/ci/spezi.yml` below `include:`, if it is not there. The other content stays. |
| `.mcp.json` | The MCP server `spezi` at the commit of the kit. Other servers stay. |

The command must also give the project a devShell with the program `spezi`:

| Case | Action |
| --- | --- |
| No `flake.nix` | Write `flake.nix` with the input `nixpkgs` at `nixos-unstable`, the input `spezi` at the commit of the kit, and a devShell `default` with the program for `x86_64-linux`, `aarch64-linux`, `x86_64-darwin` and `aarch64-darwin`. Then run `nix flake lock`, and `git add` for `flake.nix`, `flake.lock` and `.envrc` in a git repository. |
| `flake.nix` without the input `spezi` | Change no file. Show the lines of the input to add. |
| `flake.nix` without `spezi.packages` | Change no file. Show the package to add to the devShell. |
| No `.envrc` | Write `.envrc` with `use flake`, and tell to run `direnv allow`. |
| `.envrc` without `use flake` | Show the line to add. Add it only when the user answers yes (000085). |

The line of the input must be `inputs.spezi.url = "github:frederikbeimgraben/spezi/<commit>";`,
with the commit of `spezi.lock`, below the comment
`# The spezi command of the kit. The ref must be the commit in spezi.lock.`.
The input `spezi` must not follow the input `nixpkgs` of the project.

The command must write only the parts whose switch in `[features]` is on (000084). At its end,
it must do the steps of `spezi install` (000083).

Without `--forge`, the command must propose the forge of `git remote origin` (000085). It must
stop with an error and change no file when `spezi.toml` exists, when the forge is unknown, when
the switch `ci` is on and `.gitlab-ci.yml` has an `include` that is not a list, when `<dir>` is
the kit, or when this program is an older commit of the kit than the commit of the `ref`.

Reason: One command gives a project the same start as every other project. The kit never
changes a `flake.nix` that exists, because it cannot read every form of Nix code, and changes an
`.envrc` only when the user agrees.

Test: `tests/test_kit.py`.
