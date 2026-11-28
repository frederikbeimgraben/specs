---
id: "000164"
title: Only these commands change a copy
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/changes.py
  - src/spezi/check.py
  - src/spezi/kit.py
  - src/spezi/install.py
scope:
  - specs/
---

# Only these commands change a copy

Only these commands must change a copy (spec 000048), its `ref` and its entry in `spezi.lock`:

| Command | Effect |
| --- | --- |
| `spezi init` | Adds the copy of the kit (spec 000066). |
| `spezi add <repo> [<ref>] [--include <folder>]...` | Adds the copy of a new repository (spec 000068). |
| `spezi update [<repo> [<ref>]]` | Resolves the `ref` of one repository, or of each, again and replaces its copy (spec 000067). |
| `spezi configure` | Changes the `ref` or `include` of a repository, then does the steps of `spezi install` (spec 000086). |
| `spezi remove <repo>` | Removes the copy of a repository (spec 000087). |
| `spezi install` | Loads each copy again that does not agree with `spezi.lock`, and changes no `ref` (spec 000083). |

Reason: One `ref` makes an update of the rules one diff in one pull request.

Test: Review.
