---
id: "000256"
title: The index, the copies and the templates have no switch
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/project.py
  - src/spezi/install.py
  - src/spezi/kit.py
  - src/spezi/devshell.py
  - src/spezi/check.py
  - src/spezi/data/spezi.toml
scope:
  - src/spezi/
  - spezi.toml
---

# The index, the copies and the templates have no switch

The index `specs/README.md`, the copies below `specs/.upstream/` and the templates in
`specs/.templates/` must have no switch in `[features]` (spec 000084).

Reason: The check needs these parts in each project.

Test: Review.
