---
id: "000128"
title: One reference can hold a list of rules
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - spezi.toml
scope:
  - specs/
---

# One reference can hold a list of rules

One pair of parentheses of (spec 000017) can hold a list of rules. A `, ` must separate two
items. An item is a local or a foreign short form, for example `(spec 000088, 000089)`.

Reason: A text that names several rules stays short.

Test: `spezi check` reads each item of the list.
