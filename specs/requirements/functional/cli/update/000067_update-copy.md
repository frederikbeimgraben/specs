---
id: "000067"
title: specs update replaces a copy and its ref
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/kit.py
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
leave the shell and run `nix develop`, because a program cannot load its shell again. Without
`<ref>`, it must take the default branch. The command must stop with an error when `<repo>` is not in
`specs.toml`, when `<repo>` at `<ref>` has no folder of `include`, when the kit at `<ref>` has
no `.specs/templates/`, or when `.gitlab-ci.yml` has an `include` that is not a list. It must
then change no file.

Reason: An update is one command and one diff (000048).
