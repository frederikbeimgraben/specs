---
id: "000284"
title: spezi init gives the project a devShell
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_init_keeps_an_existing_flake
implementation:
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/cli.py
  - src/spezi/install.py
  - src/spezi/data/
scope:
  - src/spezi/
---

# spezi init gives the project a devShell

`spezi init` must give the project a devShell with the program `spezi`:

| Case | Action |
| --- | --- |
| No `flake.nix` | Write `flake.nix` with the input `nixpkgs` at `nixos-unstable`, the input `spezi` (spec 000285), and a devShell `default` with the program for `x86_64-linux`, `aarch64-linux`, `x86_64-darwin` and `aarch64-darwin`. Then run `nix flake lock`, and `git add` for `flake.nix`, `flake.lock` and `.envrc` in a git repository. |
| `flake.nix` without the input `spezi` | Change no file. Show the lines of the input to add. |
| `flake.nix` without `spezi.packages` | Change no file. Show the package to add to the devShell. |
| No `.envrc` | Write `.envrc` with `use flake`, and tell to run `direnv allow`. |
| `.envrc` without `use flake` | Show the line to add. Add it only when the user answers yes (spec 000085). |

Reason: The kit never changes a `flake.nix` that exists, because it cannot read every form of
Nix code. It changes an `.envrc` only when the user agrees.

Test: `tests/test_kit.py`.
