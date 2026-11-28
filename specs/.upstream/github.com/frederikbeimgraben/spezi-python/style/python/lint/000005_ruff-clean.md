---
id: "000005"
title: ruff reports no warning
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# ruff reports no warning

`ruff check` must report 0 warnings with the rule selection in `pyproject.toml`. The selection
must be an explicit list of rules. Code must not turn off a rule with `# noqa`, except for a
rule that the code cannot obey, with the rule code in the comment.

Reason: An explicit list stays the same when a new ruff version changes its default rules.

Test: `ruff check`.
