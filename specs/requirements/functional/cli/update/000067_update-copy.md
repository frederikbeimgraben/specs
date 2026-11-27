---
id: "000067"
title: specs update replaces a copy and its ref
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_kit.py:test_update_replaces_the_copy_and_keeps_include
  - tests/test_kit.py:test_update_stops_for_an_unknown_repository
  - tests/test_kit.py:test_update_of_the_kit_runs_the_check
implementation:
  - src/specs_kit/kit.py
  - src/specs_kit/cli.py
  - src/specs_kit/devshell.py
scope:
  - src/specs_kit/
---

# specs update replaces a copy and its ref

`specs update <repo> <ref>` must replace the copy of `<repo>` below `.specs/upstream/` with the
`specs/` folder of `<repo>` at `<ref>`, and set `ref` in `specs.toml` to the commit of `<ref>`.
When the table of `<repo>` has `include`, the command must copy only the folders of `include`
(000048) and must keep `include` unchanged.
`specs update [<ref>]` must do the same for the kit, and must also replace the templates, the
skills, the CI files of 000066 and the entry `specs` in `.mcp.json`. When `flake.nix` has the
input `specs` of 000066, the command must set its ref to the new commit and run
`nix flake update specs`. Without this input, it must not change `flake.nix` and `flake.lock`.
When it changed `flake.nix` in a devShell (`IN_NIX_SHELL`) without direnv, it must tell to
leave the shell and run `nix develop`, because a program cannot load its shell again.
Without `<ref>`, it must take the default branch. The command must stop with an error when
`<repo>` is not in `specs.toml`, when `<repo>` at `<ref>` has no folder of `include`, when the
kit at `<ref>` has no `.specs/templates/`, or when `.gitlab-ci.yml` has an `include` that is
not a list. It must then change no file.

At its end, `specs update` must run `specs check --write` (000065) and print its report after
its own message. It must end with the exit code 1 when the check finds errors.

Reason: An update is one command and one diff (000048). New rules of an update can show errors
in the project, and the index must show the new rules.

Test: `tests/test_kit.py`.
