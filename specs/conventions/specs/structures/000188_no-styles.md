---
id: "000188"
title: The diagram holds no styles
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/sections.py
scope:
  - specs/
---

# The diagram holds no styles

The Mermaid block (spec 000034) must not hold styles, colors or click actions: no `style`,
`classDef`, `linkStyle`, `click`, `cssClass` or `:::`.

Reason: Styles make the diagram unclear in dark and high contrast modes.

Test: `spezi check` checks the styles.
