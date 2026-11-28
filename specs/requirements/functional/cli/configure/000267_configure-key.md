---
id: "000267"
title: spezi configure sets one key without questions
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_configure.py:test_configure_sets_a_switch
implementation:
  - src/spezi/configure.py
  - src/spezi/settings.py
  - src/spezi/cli.py
  - src/spezi/mcp_server.py
scope:
  - src/spezi/
---

# spezi configure sets one key without questions

`spezi configure <key> <value>` must set one key without questions. `<key>` is `forge`,
`base_ref`, `code_dirs`, `code_suffixes`, `max_elements` or `features.<switch>`. `<value>` has
the plain form of its key: `true` or `false`, a whole number, a text, or a list with a comma
between the entries, for example `src,lib`.

Reason: A script or an agent sets one value with one command.

Test: `tests/test_configure.py`.
