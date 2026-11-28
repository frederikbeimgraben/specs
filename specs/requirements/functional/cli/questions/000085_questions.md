---
id: "000085"
title: init, add and update ask questions on a terminal
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

# init, add and update ask questions on a terminal

When stdin and stdout are a terminal, `spezi init`, `spezi add` and `spezi update` must ask their
questions (spec 000316, 000317, 000318).

Reason: A person sees and chooses each setting and each version before a command changes the
project.

Test: `tests/test_questions.py`.
