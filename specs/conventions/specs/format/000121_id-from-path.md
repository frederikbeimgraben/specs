---
id: "000121"
title: The file does not hold the rule ID
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# The file does not hold the rule ID

The file must not hold the full rule ID. The ID follows from the file path (spec 000012).

Reason: A moved file then has the correct ID without a change of its text.

Test: Review.
