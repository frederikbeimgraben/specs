---
name: spec-write
description: Write a new spec or change a spec in specs/ (functional, non-functional, protocol, style, convention, workflow, agent or decision). Use for every change request before code, and when a rule must change.
---

# Write a spec

The rules are in `specs/conventions/specs/` and `specs/workflow/specs/`, in a project below
`specs/.upstream/github.com/frederikbeimgraben/specs/`. A spec wins over this skill (000001).

`specs` is the command of the kit. Run it as `nix run github:frederikbeimgraben/specs/<ref> -- <command>`, with the `ref` of the kit in `specs.toml`, or use the tools of the MCP server `specs`.

## Steps

1. Find the kind with the list in 000004, then the kind folder and the topic folder `<area>/<topic>/`. If there is no topic
   folder, make it. Use lower case and `-` (000005).
2. Search `specs/` for a rule that already covers the change. Change that rule instead of a new
   one (000006).
3. Make the file with `specs new <kind> <area>/<topic> <short-name> "<title>" --scope <path>` (000008). It
   copies the template, takes the highest number of `specs/` and the base branch plus one, and
   sets `owner` from `--owner` or `git config <forge>.user`. Run `git fetch origin` first. If an
   open pull request has the same number, give the spec a new number (000013). For a UML
   diagram, use the skill `spec-structure`.
4. The file is `<number>_<short-name>.md` (000016) with `status: draft` and the date of today.
5. Write the rule text:
   - One rule, one thing (000019). Use `must` and `must not` (000021).
   - Use numbers, names, states and paths, so that a test can decide (000020).
   - Add `Reason:` with the cause (000022) and `Test:` with the check (000023).
   - Write ASD-STE100: active voice, at most 20 words for each instruction (000025).
   - No history, no ticket numbers, no introduction (000018, 000024).
   - Refer to a rule by its number, and to a rule of a different repository as
     `<host>/<group>/.../<repo>:<number>` (000047). `specs resolve` and `specs show` find the rule.
6. Set `implementation: null` until code exists. Set `scope` to the paths that the rule
   controls. Each path must exist (000009).
7. Run `specs check --write`. Fix each error.
8. Open a pull request. Ask the owner to approve the spec (skill `spec-approve`). Do not write
    the code before the owner approves (000002).

## Protocol spec

- Keep the four sections `## Transport`, `## Schema`, `## Example`, `## Compatibility` (000027).
- A JSON format needs `<file>.schema.json` beside the spec, JSON Schema 2020-12 (000028).
- Each `json` block in `## Example` must match the schema (000029).
- A breaking change is a new spec with `version` plus one (000030).
- Add the number to `protocols` of each rule that uses the format (000032).

## Change an approved spec

- Change the text, set `status: draft` and a new `updated`. The owner approves again.
- If the old rule must stay readable, write a new spec. Set the old one to `status: replaced`
  and name it in `replaces` of the new spec. Name the new spec in `replaced_by` of the old one
  (000010).
- Never use a number again. A dropped rule keeps its file with `status: removed`.
