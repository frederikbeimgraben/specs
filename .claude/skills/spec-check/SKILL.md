---
name: spec-check
description: Check the specs in specs/ and the code against them. Run the checker, fix errors, and review what the checker cannot see. Use before a pull request, in a review, or when code and a spec may not agree.
---

# Check the specs

## Run the checker

```sh
python3 scripts/check_specs.py          # check, exit 1 on an error
python3 scripts/check_specs.py --write  # also write the tree and the index
pip install jsonschema                  # needed only for JSON protocol specs
```

Each error names the file and the rule number. Read that rule in `specs/style/specs/` and fix
the spec. Do not change a rule of `specs/style/specs/` to make the check pass.

`specs/config.toml` sets `base_ref`, `code_dirs`, `code_suffixes` and `max_elements`.

## Review what the checker cannot see

For each changed spec:

- One rule, one thing (000019). A test can decide (000020).
- ASD-STE100: active voice, short sentences, one word for one thing (000025).
- No history, no ticket, no pull request number (000024).
- `Reason:` keeps the cause (000022).
- `implementation` and `tests` name the real code (000009, 000023).
- A structure spec shows the code as it is (000038).

## Check the code against the specs

1. Find the rules of a file: search `scope` and `implementation` for its path, and `§` in it.

   ```sh
   grep -rln "<path>" specs
   grep -rn "§" <path>
   ```

2. Read each rule. If the code and a rule do not agree, tell the owner (000001). Do not change
   the code or the spec silently.
3. A pull request with code names the approved spec that it implements (000002).
