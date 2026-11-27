---
id: "000066"
title: specs init adds the kit to a project
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_kit.py:test_init_writes_the_kit_files
  - tests/test_kit.py:test_init_ci_runs_on_the_base_branch
  - tests/test_kit.py:test_init_keeps_an_existing_flake
  - tests/test_kit.py:test_init_takes_the_forge_from_the_remote
  - tests/test_kit.py:test_init_stops_when_the_kit_is_there
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/devshell.py
  - src/specs_kit/cli.py
  - src/specs_kit/data/
scope:
  - src/specs_kit/
---

# specs init adds the kit to a project

`specs init [<dir>] [--forge github|gitlab|codeberg]` must add the kit to the project in
`<dir>`, or in the current folder. It must write these files:

| File | Content |
| --- | --- |
| `specs.toml` | The settings, with `forge` and the `ref` of the kit. |
| `specs/` | An empty folder for the rules of the project. |
| `specs/.upstream/github.com/frederikbeimgraben/specs/` | The rules of the kit at the commit of the program (000048). |
| `specs/.templates/` | The templates of the kit. |
| `.claude/skills/spec-*` | The skills of the kit. |
| `.github/workflows/specs.yml`, `.gitlab/ci/specs.yml` or `.forgejo/workflows/specs.yml` | The CI job for the forge, which runs `specs check` at the `ref` of the kit. On GitHub and Codeberg, it runs for each pull request and for each push to the branch of `base_ref`, for example `develop` for `origin/develop`. For Codeberg, the job runs on the hosted Forgejo Actions runner `codeberg-small`. |
| `.gitlab-ci.yml` | Only for GitLab: the entry `- local: .gitlab/ci/specs.yml` below `include:`, if it is not there. The other content stays. |
| `.mcp.json` | The MCP server `specs` at the `ref` of the kit. Other servers stay. |

The command must also give the project a devShell with the program `specs`:

| Case | Action |
| --- | --- |
| No `flake.nix` | Write `flake.nix` with the input `nixpkgs` at `nixos-unstable`, the input `specs` at the `ref` of the kit, and a devShell `default` with the program for `x86_64-linux`, `aarch64-linux`, `x86_64-darwin` and `aarch64-darwin`. Then run `nix flake lock`, and `git add` for `flake.nix`, `flake.lock` and `.envrc` in a git repository. |
| `flake.nix` without the input `specs` | Change no file. Show the lines of the input to add. |
| `flake.nix` without `specs.packages` | Change no file. Show the package to add to the devShell. |
| No `.envrc` | Write `.envrc` with `use flake`, and tell to run `direnv allow`. |
| `.envrc` without `use flake` | Change no file. Show the line to add. |

The line of the input must be `inputs.specs.url = "github:frederikbeimgraben/specs/<ref>";`,
below the comment `# The specs command of the kit. The ref must be the ref in specs.toml.`.
The input `specs` must not follow the input `nixpkgs` of the project.

At its end, the command must run `specs check --write` (000065) and print its report after its
own message. It must end with the exit code 1 when the check finds errors.

Without `--forge`, the command must take the forge from `git remote origin`. It must stop with
an error and change no file when `specs.toml` exists, when the forge is unknown, when
`.gitlab-ci.yml` has an `include` that is not a list, when `<dir>` is the kit, or when the
program does not come from a clean commit of the kit.

Reason: One command gives a project the same start as every other project. The kit never
changes a `flake.nix` or an `.envrc` that exists, because it cannot read every form of Nix code.

Test: `tests/test_kit.py`.
