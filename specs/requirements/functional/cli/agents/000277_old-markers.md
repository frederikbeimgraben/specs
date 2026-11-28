---
id: "000277"
title: A migration gives an old block the new markers
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/migrations/m0003_agents_marker.py
scope:
  - src/spezi/
  - AGENTS.md
  - CLAUDE.md
---

# A migration gives an old block the new markers

A migration (spec 000081) must give the new marker lines (spec 000271) to a block with
the line `<!-- specs:begin (written by specs check --write, do not edit) -->`. It must do the same
for a block with the markers of the old name `specs`.

Reason: A project of an older kit gets one block and not two.

Test: `tests/test_migrations.py`.
