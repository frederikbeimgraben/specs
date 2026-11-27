---
id: "000065"
title: specs check checks the specs and writes the index
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/check.py
  - src/specs_kit/index.py
  - src/specs_kit/cli.py
scope:
  - src/specs_kit/
---

# specs check checks the specs and writes the index

`specs check` must run every check of the conventions on the specs of the project. It must also
check that `specs.toml` and the copies of 000048 agree, and check each `§` reference in
`code_dirs` (000017). It must print one line for each
error, then the count of specs and errors. It must exit with 1 when it finds an error, else
with 0. `specs check --write` must first write `.specs/index.md` and `specs/README.md` (000007).
Without `--write`, the command must not change a file.

Reason: CI and an agent run the same check with one command.
