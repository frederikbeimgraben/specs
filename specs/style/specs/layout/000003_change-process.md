---
id: "000003"
title: A change goes through a pull request
kind: style
status: draft
owner: frederikbeimgraben
updated: 2026-11-23
implementation:
  - specs/
scope:
  - specs/
---

# A change goes through a pull request

A change to a spec must follow these steps:

1. Find the topic folder. If there is none, make it.
2. Copy the template and give the rule its number (000013).
3. Set `status: draft` and set `updated` to the current date.
4. Update the index with `python3 scripts/check_specs.py --write`.
5. Open a pull request. The owner sets `approved` (000010).
6. Before the merge, bring the branch up to the base branch and run the check again.

Reason: Step 6 shows a number that the base branch took in the meantime.
