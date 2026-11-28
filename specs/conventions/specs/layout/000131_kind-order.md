---
id: "000131"
title: A rule goes to the first kind that applies
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A rule goes to the first kind that applies

A rule must go to the first kind of this list that applies to it:

1. It records why the product uses one solution and not a different one: `decision`.
2. It controls the behavior of the product: `functional` or `non-functional`.
3. It controls a format that the product exchanges: `protocol`.
4. It controls the structure of the code: `structure`.
5. It controls how code or tests look: `style`.
6. It controls how specs look: `convention`.
7. It controls how people and agents work: `workflow`.
8. It applies only to agents: `agent`.

Reason: The list gives one kind to each rule (spec 000004), so that two agents put the same rule
in the same folder.

Test: Review.
