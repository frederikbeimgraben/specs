---
id: "000199"
title: A new key of the front matter changes the model in the same pull request
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/conventions/specs/format/000009_front-matter.md
scope:
  - specs/
  - src/spezi/project.py
---

# A new key of the front matter changes the model in the same pull request

A pull request with a new key of the front matter must also change the spec model
(spec 000040). It must also change the rule of the front matter (spec 000009).

Reason: The model, the rule and the code then agree after each merge.

Test: Review.
