---
id: "000051"
title: specs/ holds only the rules of the project
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/specs_kit/project.py
scope:
  - specs/
  - .specs/
---

# specs/ holds only the rules of the project

`specs/` must hold only the rules of the project and the copy of the index in `README.md`
(000007). All other files of the kit must be below `.specs/`:

| Path | Content |
| --- | --- |
| `.specs/upstream/` | The copies of the rules of different repositories (000048). |
| `.specs/templates/` | The templates for a new spec (000008). |
| `.specs/index.md` | The index (000007). |

The settings must be in `specs.toml` in the root of the repository.

Reason: A reader of `specs/` sees only the rules that the project wrote. The files of the
kit change with `specs update` and stay out of the way.

Test: `specs check` fails for a file in `specs/` that is not below a kind folder and is not
`README.md`.
