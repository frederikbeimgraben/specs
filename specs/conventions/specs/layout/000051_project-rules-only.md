---
id: "000051"
title: specs/ holds the rules of the project and the files of the kit
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
implementation:
  - src/spezi/project.py
scope:
  - specs/
---

# specs/ holds the rules of the project and the files of the kit

`specs/` must hold the rules of the project in its kind folders (spec 000004). All other files of
the kit must be in these places of `specs/`:

| Path | Content |
| --- | --- |
| `specs/README.md` | The index (spec 000007). |
| `specs/.upstream/` | The copies of the rules of different repositories (spec 000048). |
| `specs/.templates/` | The templates for a new spec (spec 000008). |

The settings must be in `spezi.toml` in the root of the repository.

Reason: All files of the specs are in one folder. The hidden folders keep the files of the kit,
which change with `spezi update`, out of the way of a reader of the rules.

Test: `spezi check` fails for a file in `specs/` that is not below a kind folder, not below a
hidden folder and is not `README.md`.
