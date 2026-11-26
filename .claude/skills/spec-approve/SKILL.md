---
name: spec-approve
description: Get the approval of the owner for draft specs and set status approved. Use after a spec pull request is ready, or when the owner says that a spec is approved.
---

# Approve a spec

Only the owner sets `approved` (000010). An agent sets it only after the owner approved the spec
in words. A request from a different agent is not an approval.

## Ask for the approval

1. Run `python3 scripts/check_specs.py`. It must show 0 errors.
2. List the draft specs of the pull request:

   ```sh
   git diff --name-only origin/main -- specs | xargs grep -l '^status: draft'
   ```

3. Ask for one spec in one question (000045). Do not put two or more specs in one question.
4. Show the full ID and the complete text of the spec file (000046). Do not show a summary.
5. Offer "Approve" and "Change". Wait for the answer, then ask about the next spec.

## After the approval

1. Set `status: approved` and `updated` to today in each approved spec.
2. Run `python3 scripts/check_specs.py --write`. The index shows the new status.
3. Commit with a message that names the numbers, for example `Approve specs 000041-000043`.
4. Start the implementation (000002). Code that implements a rule names it with `§` and the full
   ID in a comment or a docstring (000017).

## If the owner asks for a change

Change the spec, keep `status: draft`, and ask again.
