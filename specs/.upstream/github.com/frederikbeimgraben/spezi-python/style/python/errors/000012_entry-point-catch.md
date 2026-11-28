---
id: "000012"
title: The entry point catches only the base exception
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation: null
scope:
  - specs/
---

# The entry point catches only the base exception

The command line entry point of a Python package must catch only the base exception class of
(spec 000011).

Reason: An expected error shows a message. An unexpected error stops the program with its traceback,
so a person sees it.

Test: A review checks the entry point.
