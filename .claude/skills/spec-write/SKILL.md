---
name: spec-write
description: Write a new spec or change a spec in specs/ (functional, non-functional, protocol, style, convention, workflow, agent or decision). Use for every change request before code, and when a rule must change.
---

# Write a spec

The rules are in `specs/conventions/specs/` and `specs/workflow/specs/`. A spec wins over this skill (000001).

## Steps

1. Find the kind with the list in 000004, then the kind folder and the topic folder `<area>/<topic>/`. If there is no topic
   folder, make it. Use lower case and `-` (000005).
2. Search `specs/` for a rule that already covers the change. Change that rule instead of a new
   one (000006).
3. Get the number. Take the highest number in `specs/` on the base branch and in every open pull
   request, plus one (000013):

   ```sh
   git fetch origin
   git ls-tree -r --name-only origin/main -- specs | grep -o '/[0-9]\{6\}_' | sort | tail -1
   ```

4. Copy the template of the kind (000008). For a UML diagram, use the skill `spec-structure`.
5. Name the file `<number>_<short-name>.md` (000016). Set `id` to the quoted number.
6. Set `status: draft`, `owner` to the login of the approver, and `updated` to today.
7. Write the rule text:
   - One rule, one thing (000019). Use `must` and `must not` (000021).
   - Use numbers, names, states and paths, so that a test can decide (000020).
   - Add `Reason:` with the cause (000022) and `Test:` with the check (000023).
   - Write ASD-STE100: active voice, at most 20 words for each instruction (000025).
   - No history, no ticket numbers, no introduction (000018, 000024).
8. Set `implementation: null` until code exists. Set `scope` to the paths that the rule
   controls. Each path must exist (000009).
9. Run `python3 scripts/check_specs.py --write`. Fix each error.
10. Open a pull request. Ask the owner to approve the spec (skill `spec-approve`). Do not write
    the code before the owner approves (000002).

## Protocol spec

- Keep the four sections `## Transport`, `## Schema`, `## Example`, `## Compatibility` (000027).
- A JSON format needs `<file>.schema.json` beside the spec, JSON Schema 2020-12 (000028).
- Each `json` block in `## Example` must match the schema (000029). Install `jsonschema` to run
  the check.
- A breaking change is a new spec with `version` plus one (000030).
- Add the full ID to `protocols` of each rule that uses the format (000032).

## Change an approved spec

- Change the text, set `status: draft` and a new `updated`. The owner approves again.
- If the old rule must stay readable, write a new spec. Set the old one to `status: replaced`
  with `replaced_by` (000010).
- Never use a number again. A dropped rule keeps its file with `status: removed`.
