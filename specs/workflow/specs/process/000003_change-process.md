---
id: "000003"
title: A change goes through a pull request
kind: workflow
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - specs/
scope:
  - specs/
---

# A change goes through a pull request

A change to a spec must follow these steps:

1. Find the topic folder. If there is none, make it.
2. For a new spec, make the file with `spezi new` (spec 000008). It gives the rule its number
   (spec 000013). For a change to a spec, change its file.
3. Set `status: draft` and set `updated` to the current date.
4. Update the index with `spezi install` (spec 000007).
5. Open a pull request. The owner sets `approved` (spec 000010).
6. Before the merge, bring the branch up to the base branch and run the check again.

Reason: A change to a spec keeps its number. Step 6 shows a number that the base branch took in
the meantime.
