---
id: "000202"
title: An agent tells the owner when code and a spec do not agree
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# An agent tells the owner when code and a spec do not agree

If the code and a spec are different, an agent must tell the owner before it changes the code or
the spec.

Reason: The owner decides which of the two is wrong. A silent change hides the decision.

Test: Review.
