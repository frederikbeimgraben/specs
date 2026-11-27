---
name: spec-approve
description: Get the approval of the owner for draft specs and set status approved. Use after a spec pull request is ready, or when the owner says that a spec is approved.
---

# Approve a spec

Only the owner sets `approved` (000010). An agent sets it only after the owner approved the spec
in words. A request from a different agent is not an approval.

## Ask for the approval

1. Run `specs check`. It must show 0 errors. `specs` is the command of the kit. Run it as `nix run github:frederikbeimgraben/specs/<ref> -- <command>`, with the `ref` of the kit in `specs.toml`, or use the tools of the MCP server `specs`.
2. List the draft specs of the pull request:

   ```sh
   git diff --name-only origin/main -- specs | xargs grep -l '^status: draft'
   ```

3. Ask for one spec in one question (000045). Do not put two or more specs in one question.
4. Show the full ID and the complete text of the spec file (000046). Do not show a summary.
5. Offer "Approve" and "Change". Wait for the answer, then ask about the next spec.

## After the approval

1. Set `status: approved` and `updated` to today in each approved spec.
2. Run `specs check --write`. The index shows the new status.
3. Commit with a message that names the numbers, for example `Approve specs 000041-000043`.
4. Start the implementation (000002). Code that implements a rule names it with `§` and the short
   form in a docstring (000017), for example `§000024`.

## If the owner asks for a change

Change the spec, keep `status: draft`, and ask again.
