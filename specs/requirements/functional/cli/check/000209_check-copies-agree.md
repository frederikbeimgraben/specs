---
id: "000209"
title: spezi check checks the settings, the lock and the copies
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check checks the settings, the lock and the copies

`spezi check` must check that `spezi.toml`, `spezi.lock` and the copies agree
(spec 000048, 000082).

Reason: A copy that does not agree with the lock is not the copy that the project wants.

Test: `tests/test_check.py`.
