---
id: "000053"
title: Readability limits the single expression
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/
scope:
  - src/
---

# Readability limits the single expression

Code must split an expression that is deeper than three levels or longer than 8 lines. The
parts must become named locals or a named helper function.

Reason: The goal of 000052 is code that is easier to read, not one long expression.
