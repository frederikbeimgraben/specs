---
name: spezi-write
description: Write a new spec or change a spec in specs/ (functional, non-functional, protocol, style, convention, workflow, agent or decision). Use for every change request before code, and when a rule must change.
---

# Write a spec

The rules are in `specs/conventions/specs/` and `specs/workflow/specs/`, in a project below
`specs/.upstream/github.com/frederikbeimgraben/spezi/`. A spec wins over this skill (spec 000001).

`spezi` is the command of the kit. Run it as `nix run github:frederikbeimgraben/spezi/<commit> -- <command>`, with the commit of the kit in `spezi.lock`, or use the tools of the MCP server `spezi`.

## Steps

1. Find the kind with the list in (spec 000004), then the kind folder and the topic folder `<area>/<topic>/`. If there is no topic
   folder, make it. Use lower case and `-` (spec 000005).
2. Search `specs/` for a rule that already covers the change. Change that rule instead of a new
   one (spec 000006).
3. Make the file with `spezi new <kind> <area>/<topic> <short-name> "<title>" --scope <path>` (spec 000008). It
   copies the template, takes the highest number of `specs/` and the base branch plus one, and
   sets `owner` from `--owner` or `git config <forge>.user`. Run `git fetch origin` first. If an
   open pull request has the same number, give the spec a new number (spec 000013). For a UML
   diagram, use the skill `spezi-structure`.
4. The file is `<number>_<short-name>.md` (spec 000016) with `status: draft` and the date of today.
5. Write the rule text:
   - One rule, one thing (spec 000019). Use `must` and `must not` (spec 000021).
   - Use numbers, names, states and paths, so that a test can decide (spec 000020).
   - Add `Reason:` with the cause (spec 000022) and `Test:` with the check (spec 000023).
   - Write ASD-STE100: active voice, at most 20 words for each instruction (spec 000025).
   - No history, no ticket numbers, no introduction (spec 000018, 000024).
   - Refer to a rule by its number, and to a rule of a different repository as
     `<host>/<group>/.../<repo>:<number>` (spec 000047). `spezi resolve` and `spezi show` find the rule.
6. Set `implementation: null` until code exists. Set `scope` to the paths that the rule
   controls. Each path must exist (spec 000009).
7. Run `spezi install`. Fix each error.
8. Open a pull request. Ask the owner to approve the spec (skill `spezi-approve`). Do not write
    the code before the owner approves (spec 000002).

## Protocol spec

- Keep the four sections `## Transport`, `## Schema`, `## Example`, `## Compatibility` (spec 000027).
- A JSON format needs `<file>.schema.json` beside the spec, JSON Schema 2020-12 (spec 000028).
- Each `json` block in `## Example` must match the schema (spec 000029).
- A breaking change is a new spec with `version` plus one (spec 000030).
- Add the number to `protocols` of each rule that uses the format (spec 000032).

## Change an approved spec

- Change the text, set `status: draft` and a new `updated`. The owner approves again.
- If the old rule must stay readable, write a new spec. Set the old one to `status: replaced`
  and name it in `replaces` of the new spec. Name the new spec in `replaced_by` of the old one
  (spec 000010).
- Never use a number again. A dropped rule keeps its file with `status: removed`.
