---
id: "000009"
title: A spec starts with a YAML front matter
kind: convention
status: draft
owner: frederikbeimgraben
updated: 2026-11-26
implementation:
  - scripts/check_specs.py
scope:
  - specs/
---

# A spec starts with a YAML front matter

The file must start with a YAML front matter block between two `---` lines. The block must have
these keys, in this order:

| Key | Type | Value |
| --- | --- | --- |
| `id` | string | The six-digit number of the rule in double quotes, for example `"000024"`. |
| `title` | string | The title of the rule. It is the same text as the `#` title. |
| `kind` | enum | `functional`, `non-functional`, `protocol`, `structure`, `style`, `convention`, `workflow`, `agent` or `decision` (000004). |
| `status` | enum | `draft`, `approved`, `replaced` or `removed` (000010). |
| `owner` | string | The GitHub login of the person who approves the rule. |
| `updated` | date | The date of the last change, as `YYYY-MM-DD`. |
| `replaced_by` | string | Only with `status: replaced`: the full rule ID of the new rule. |
| `version` | string | Only with `kind: protocol`: the version of the format, a whole number from 1 (000030). |
| `media_type` | string | Only with `kind: protocol`: the media type, for example `application/json`. |
| `diagram` | enum | Only with `kind: structure`: the diagram type (000034). |
| `tests` | list of strings | Optional: the tests that check the rule, as `"<path>:<function>"`. |
| `protocols` | list of strings | Optional, only for `functional` and `non-functional`: the protocol specs that the rule uses (000032). |
| `structures` | list of strings | Optional, only for `functional` and `non-functional`: the structure specs that the rule uses (000039). |
| `implementation` | list of strings or `null` | Only with `status: draft` or `approved`: the paths of the code that implements the rule. `null` while nobody implemented it. |
| `scope` | list of strings | The paths that the rule applies to. |

The block must not have other keys. `scope` must be the last key. Each path must exist, as a
path from the repository root. The Markdown body must not hold metadata.

Reason: Every Markdown tool reads standard front matter. One fixed set of keys lets one tool
read every spec. The quotes keep the leading zeros, because YAML reads `000024` as a number.

Test: `scripts/check_specs.py` checks the keys, their order and their values.
