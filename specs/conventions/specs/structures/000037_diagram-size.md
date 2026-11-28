---
id: "000037"
title: A diagram has at most 25 elements
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
  - spezi.toml
scope:
  - specs/
---

# A diagram has at most 25 elements

A diagram must have at most 25 elements. A larger structure must become several structure
specs, for example one for each module. `max_elements` in `spezi.toml` can set a
different limit for a project.

Reason: A person cannot read a diagram with more elements on one screen.

Test: `spezi check` counts the rows of `## Elements`.
