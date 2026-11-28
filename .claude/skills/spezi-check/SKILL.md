---
name: spezi-check
description: Check the specs in specs/ and the code against them. Run the checker, fix errors, and review what the checker cannot see. Use before a pull request, in a review, or when code and a spec may not agree.
---

# Check the specs

## Run the checker

`spezi` is the command of the kit. Run it as `nix run github:frederikbeimgraben/spezi/<commit> -- <command>`, with the commit of the kit in `spezi.lock`, or use the tools of the MCP server `spezi`.

```sh
spezi check          # check, exit 1 on an error
spezi install        # load the copies, write missing files, the index and AGENTS.md
```

Each error names the file and the rule number. Read that rule with `spezi show <number>` and fix
the spec. Do not change a rule of the kit to make the check pass.

`spezi.toml` sets `forge`, `base_ref`, `code_dirs`, `code_suffixes`, `max_elements` and
`upstream` with `ref` and `include` (spec 000078).

## Review what the checker cannot see

For each changed spec:

- One rule, one thing (spec 000019). A test can decide (spec 000020).
- ASD-STE100: active voice, short sentences, one word for one thing (spec 000025).
- No history, no ticket, no pull request number (spec 000024).
- `Reason:` keeps the cause (spec 000022).
- `implementation` and `tests` name the real code (spec 000009, 000023).
- A structure spec shows the code as it is (spec 000038).

## Check the code against the specs

1. Find the rules of a file: search `scope` and `implementation` for its path, and `(spec ` in it.

   ```sh
   grep -rln "<path>" specs
   grep -rn "(spec " <path>
   ```

2. Read each rule. If the code and a rule do not agree, tell the owner (spec 000001). Do not change
   the code or the spec silently.
3. A pull request with code names the approved spec that it implements (spec 000002).
