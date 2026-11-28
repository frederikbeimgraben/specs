---
id: "000165"
title: gitattributes keeps the line ends of the copies
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_install.py:test_check_finds_a_missing_line_in_gitattributes
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# gitattributes keeps the line ends of the copies

When `specs/.upstream/` holds a copy, `.gitattributes` in the root of the project must hold the line
`specs/.upstream/** -text`.

Reason: `.gitattributes`it on Windows can change the line ends of a file at checkout. The line stops this, so
the copy keeps the bytes of its hash.

Test: When `specs/.upstream/` holds a copy, `spezi check` checks that `.gitattributes` holds the line.
