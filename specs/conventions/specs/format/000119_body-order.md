---
id: "000119"
title: The body has the title, the rule text and the labels
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

# The body has the title, the rule text and the labels

After the front matter, a spec must have one `#` title, then the rule text, then the labels
(spec 000015).

Reason: A reader and a tool find each part at a fixed place.

Test: `spezi check`: the body starts with the title.
