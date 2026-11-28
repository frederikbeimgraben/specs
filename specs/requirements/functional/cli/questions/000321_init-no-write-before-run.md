---
id: "000321"
title: spezi init writes no file before Run?
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/ask.py
  - src/spezi/kit.py
  - src/spezi/review.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi init writes no file before Run?

`spezi init` must not change a file before the answer to `Run?` (spec 000319).

Reason: A person who cancels finds the project as before.

Test: `tests/test_questions.py`.
