---
id: "000067"
title: specs update resolves the refs again and replaces the copies
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_kit.py:test_update_replaces_the_copy_and_keeps_include
  - tests/test_kit.py:test_update_stops_for_an_unknown_repository
  - tests/test_kit.py:test_update_of_the_kit_runs_the_check
  - tests/test_kit.py:test_update_without_arguments_updates_each_repository
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
  - src/specs_kit/devshell.py
scope:
  - src/specs_kit/
---

# specs update resolves the refs again and replaces the copies

`specs update [<repo> [<ref>]]` must update the copies below `specs/.upstream/` (000048):

| Form | Effect |
| --- | --- |
| `specs update` | Resolves the `ref` of each repository of `specs.toml` again. |
| `specs update <repo>` | Resolves the `ref` of `<repo>` again. |
| `specs update <repo> <ref>` | Sets `ref` of `<repo>` in `specs.toml` to `<ref>` as given, a tag, a branch or a commit, and resolves it. |

`<repo>` is the full name of the repository, or `kit` for `github.com/frederikbeimgraben/specs`.
For each repository, the command must replace the copy with the `specs/` folder at the commit
that `ref` names, and write the `ref`, the commit, `include` and the hash to `specs.lock`
(000082). When the table of `<repo>` has `include`, the command must copy only the folders of
`include` and must keep `include` unchanged. The kit comes first.

For the kit, the command must also replace the templates, the skills, the CI files of 000066
and the entry `specs` in `.mcp.json`. When `flake.nix` has the input `specs` of 000066, the
command must set its ref to the new commit of the kit and run `nix flake update specs`.
Without this input, it must not change `flake.nix` and `flake.lock`. When it changed
`flake.nix` in a devShell (`IN_NIX_SHELL`) without direnv, it must tell to leave the shell and
run `nix develop`, because a program cannot load its shell again.

The command must stop with an error when `<repo>` is not in `specs.toml`, when this program is
an older commit of the kit than the kit commit in `specs.lock`, when `<repo>` at `<ref>` has no
folder of `include`, when the kit at `<ref>` has no `specs/.templates/`, or when
`.gitlab-ci.yml` has an `include` that is not a list. It must then change no file of the
repository with the error.

The command must replace only the parts whose switch in `[features]` is on, and must not change
`flake.nix` when `flake` is off (000084). Before it copies, the command must run the migrations
of 000081. At its end, it must do the steps of `specs install` (000083).

Reason: `specs.toml` keeps the version that the project wants, and one command takes the newest
commit of each version (000048). New rules of an update can show errors in the project, and the
index must show the new rules.

Test: `tests/test_kit.py`.
