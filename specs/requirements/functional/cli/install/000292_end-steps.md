---
id: "000292"
title: Five commands end with the steps of spezi install
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_kit.py:test_update_of_the_kit_runs_the_check
implementation:
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# Five commands end with the steps of spezi install

`spezi init`, `spezi update`, `spezi add`, `spezi configure` and `spezi remove` must end with the
steps of `spezi install` (spec 000083). For `spezi configure`, this is after it writes
`spezi.toml`.

Reason: Each command leaves the project in the state of its settings. New rules can show errors,
and the index shows the new rules.

Test: `tests/test_kit.py`.
