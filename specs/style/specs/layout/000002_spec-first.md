---
id: "000002"
title: A change request starts as a spec
kind: style
status: approved
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - specs/
scope:
  - specs/
---

# A change request starts as a spec

A change request must follow these steps:

1. Write the change as a new spec or as a change to a spec, with the steps of 000003.
2. Give the spec to the owner for review.
3. Start the implementation only after the owner approves the spec.
4. If the owner asks for changes, change the spec and give it for review again.

Reason: The owner approves what the code must do before the work starts. The approved spec is
then the measure for the review of the code.

Test: Review. A pull request with code names the approved spec that it implements.
