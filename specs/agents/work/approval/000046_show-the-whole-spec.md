---
id: "000046"
title: An agent shows the whole spec for its approval
kind: agent
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - .claude/skills/spezi-approve/SKILL.md
scope:
  - specs/
---

# An agent shows the whole spec for its approval

An agent that asks for the approval of a spec must show the complete text of the spec file to
the user. It must not show only a summary or a part.

Reason: The owner approves the text that is in the file. A summary can leave out the part that
the owner does not agree with.

Test: Review.
