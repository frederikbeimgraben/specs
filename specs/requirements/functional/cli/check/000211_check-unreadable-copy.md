---
id: "000211"
title: spezi check reports a rule of a copy that it cannot read
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_finds_a_rule_of_a_copy_that_it_cannot_read
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check reports a rule of a copy that it cannot read

`spezi check` must read each rule of the copies. It must report each rule that it cannot read,
for example a rule without front matter. It must not count that rule.

Reason: The project must not change a copy (spec 000048), so the check reports only what it
needs to read the rules.

Test: `tests/test_check.py`.
