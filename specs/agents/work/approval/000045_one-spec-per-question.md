---
id: "000045"
title: An agent asks for the approval of one spec in one question
kind: agent
status: approved
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - .claude/skills/spezi-approve/SKILL.md
scope:
  - specs/
---

# An agent asks for the approval of one spec in one question

An agent must ask for the approval of each spec in its own question. It must not ask for the
approval of two or more specs in one question.

Reason: The owner decides about each rule. A question about several specs hides the rule that
the owner does not agree with.

Test: Review.
