---
id: "000009"
title: A spec starts with a YAML front matter
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/check.py
  - src/spezi/project.py
scope:
  - specs/
---

# A spec starts with a YAML front matter

The front matter must have these keys, in this order:

| Key | Type | Value |
| --- | --- | --- |
| `id` | string | The six-digit number of the rule in double quotes, for example `"000024"`. |
| `title` | string | The title of the rule. It is the same text as the `#` title. |
| `kind` | enum | `functional`, `non-functional`, `protocol`, `structure`, `style`, `convention`, `workflow`, `agent` or `decision` (spec 000004). |
| `status` | enum | `draft`, `approved`, `replaced` or `removed` (spec 000010). |
| `owner` | string | The login on the forge of `spezi.toml` (GitHub, GitLab or Codeberg) of the person who approves the rule. |
| `updated` | date | The date of the last change, as `YYYY-MM-DD`. |
| `replaced_by` | list of strings | Only with `status: replaced`: the numbers of the rules of the same repository that replace this rule (spec 000010). |
| `replaces` | list of strings | Optional, only with `status: draft` or `approved`: the rules that this rule replaces, in the short form (spec 000047). |
| `version` | string | Only with `kind: protocol`: the version of the format, a whole number from 1 (spec 000030). |
| `media_type` | string | Only with `kind: protocol`: the media type, for example `application/json`. |
| `diagram` | enum | Only with `kind: structure`: the diagram type (spec 000034). |
| `tests` | list of strings | Optional: the tests that check the rule, as `"<path>:<function>"`. |
| `protocols` | list of strings | Optional, only for `functional` and `non-functional`: the numbers of the protocol specs that the rule uses (spec 000032). |
| `structures` | list of strings | Optional, only for `functional` and `non-functional`: the numbers of the structure specs that the rule uses (spec 000039). |
| `implementation` | list of strings or `null` | Only with `status: draft` or `approved`: the paths of the code that implements the rule. `null` while nobody implemented it. |
| `scope` | list of strings | The paths that the rule applies to. |

Reason: One fixed set of keys lets one tool read every spec. The quotes keep the leading zeros,
because YAML reads `000024` as a number. The short form stays the same when a rule moves to a
different folder (spec 000014).

Test: `spezi check` checks the keys, their order and their values.
