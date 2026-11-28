---
id: "000166"
title: spezi install adds the line to gitattributes
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_install.py:test_install_adds_the_line_to_gitattributes
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# spezi install adds the line to gitattributes

`spezi install` must add the line of (spec 000165) when it is missing. It must
not change the other lines of `.gitattributes`.

Reason: A project gets the line without work by hand, and its own lines stay.

Test: `tests/test_install.py`.
