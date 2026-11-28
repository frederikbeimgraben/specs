---
id: "000294"
title: spezi update keeps include
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_update_writes_include_once
implementation:
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/devshell.py
scope:
  - src/spezi/
---

# spezi update keeps include

When the table of `<repo>` has `include`, `spezi update` must copy only the folders of `include`
and keep `include`. Only a folder that the user adds (spec 000085) changes it.

Reason: The project keeps the part of the rules that it chose.

Test: `tests/test_kit.py`.
