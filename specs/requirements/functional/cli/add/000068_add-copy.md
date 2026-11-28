---
id: "000068"
title: spezi add adds the copy of a different repository
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_add_copies_the_rules
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi add adds the copy of a different repository

`spezi add [<repo> [<ref>]] [-y] [-r]` must ask the questions (spec 000085). It must then copy
the `specs/` folder of `<repo>` at `<ref>` to `specs/.upstream/<repo>/`. It adds
`[upstream."<repo>"]` with `<ref>` as given as `ref` to `spezi.toml`, and writes the entry of
`<repo>` to `spezi.lock` (spec 000082).

Reason: A project takes the rules of a different repository with one command (spec 000048).

Test: `tests/test_kit.py`.
