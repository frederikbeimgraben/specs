---
id: "000034"
title: Each exception class of a package is a subclass of its base exception
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# Each exception class of a package is a subclass of its base exception

Each exception class of a Python package must be a subclass of the base exception class of
(spec 000011).

Reason: A caller catches each expected error of the package with one class.

Test: A review checks the exception classes.
