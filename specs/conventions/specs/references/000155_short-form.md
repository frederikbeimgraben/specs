---
id: "000155"
title: Code, front matter and spec text use the short form
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
scope:
  - specs/
---

# Code, front matter and spec text use the short form

Code (spec 000017), the front matter (spec 000009) and the text of a spec must use the short
form of (spec 000047).

Reason: The short form stays the same when a rule moves to a different folder.

Test: `spezi check` checks that each reference to a different repository uses the short form.
