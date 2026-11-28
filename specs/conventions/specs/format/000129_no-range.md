---
id: "000129"
title: A reference holds no range of numbers
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A reference holds no range of numbers

A reference (spec 000017) must not hold a range of numbers, for example `000001 to 000007`.

Reason: A search for a number does not find it in a range.

Test: Review.
