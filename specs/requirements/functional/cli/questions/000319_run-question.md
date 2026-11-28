---
id: "000319"
title: A command asks Run? before each copy
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_questions.py:test_init_cancel_changes_no_file
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# A command asks Run? before each copy

Before the copy of each repository, `spezi init`, `spezi add` and `spezi update` must show a
summary (spec 000320) and ask `Run?`, with the proposal yes. When the user answers no, or
cancels, the command stops with an error before it changes the copy of this repository. A
repository that `spezi update` updated before stays updated.

Reason: The person sees the change before it happens.

Test: `tests/test_questions.py`.
