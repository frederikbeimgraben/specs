---
id: "000037"
title: A diagram has at most 25 elements
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - scripts/check_specs.py
  - specs/config.toml
scope:
  - specs/
---

# A diagram has at most 25 elements

A diagram must have at most 25 elements. A larger structure must become several structure
specs, for example one for each module. `max_elements` in `specs/config.toml` can set a
different limit for a project.

Reason: A person cannot read a diagram with more elements on one screen.

Test: `scripts/check_specs.py` counts the rows of `## Elements`.
