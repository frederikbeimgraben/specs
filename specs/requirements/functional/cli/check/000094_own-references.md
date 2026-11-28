---
id: "000094"
title: spezi check finds a reference to a rule of own in a file for projects
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_finds_a_reference_to_an_own_rule_in_a_skill
implementation:
  - src/spezi/check.py
scope:
  - src/spezi/
---

# spezi check finds a reference to a rule of own in a file for projects

`spezi check` must report an error for each reference to a rule of the project in a folder of
`own` (spec 000048, 000078). It must do this check in these files: the skills
`.claude/skills/spezi-*/`, the templates `specs/.templates/` and the files below
`src/spezi/data/`. `spezi init` and `spezi update` copy these files into a project. The error
line must name the file, the line of the reference and the rule, for example
`.claude/skills/spezi-check/SKILL.md:21: (spec 000078) names a rule of own`.

Reason: A project does not get the rules of `own`. A reference to such a rule in a file of the
kit is a broken reference in each project.

Test: `tests/test_check.py`.
