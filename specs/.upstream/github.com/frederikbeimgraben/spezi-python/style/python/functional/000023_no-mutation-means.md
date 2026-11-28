---
id: "000023"
title: Python code changes no value in place
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Python code changes no value in place

Python code must not use `.append`, `.add`, `.update`, `.extend`, `x[k] = v` or `del`
(spec github.com/frederikbeimgraben/spezi-functional:000004).

Reason: These are the means of Python that change a value in place.

Test: A review.
