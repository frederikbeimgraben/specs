---
id: "000079"
title: specs writes the rules for agents to AGENTS.md
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_settings.py:test_init_writes_agents_and_claude
  - tests/test_settings.py:test_init_keeps_an_existing_claude
  - tests/test_settings.py:test_the_block_keeps_the_text_around_it
  - tests/test_settings.py:test_a_file_without_block_gets_it_at_the_end
implementation:
  - src/specs_kit/agents.py
  - src/specs_kit/check.py
  - src/specs_kit/cli.py
  - src/specs_kit/migrations/m0003_agents_marker.py
scope:
  - src/specs_kit/
  - AGENTS.md
  - CLAUDE.md
---

# specs writes the rules for agents to AGENTS.md

`specs install` must write one block to `AGENTS.md` in the root of the project. The block
must start with the line `<!-- specs:begin (written by specs install, do not edit) -->`
and end with the line `<!-- specs:end -->`. Between these lines, the block must hold a short
text that tells an agent how to use the rules, and the table of `specs/README.md` (000007) with
only the A and W rules that have the status `approved`, first the rules of the project and then
the rules of the copies (000049).

| State of `AGENTS.md` | `specs install` |
| --- | --- |
| The file does not exist. | It creates the file with the block. |
| The file has no block. | It adds the block at the end. |
| The file has the block. | It replaces only the block. |

The text before and after the block must not change. `specs check` must show an error when
the block is not current. `specs init` must create `CLAUDE.md` with the line
`@AGENTS.md` when it does not exist. When `CLAUDE.md` exists without that line, `specs init`
must not change it and must print the line to add. A block that starts with the older line
`<!-- specs:begin (written by specs check --write, do not edit) -->` gets the new line through
the migrations of 000081.

Reason: An agent finds every rule that applies in the file that it reads first, and the file
stays current with the specs. Claude Code reads `AGENTS.md` through the import in `CLAUDE.md`.

Test: `specs check` fails when the block in `AGENTS.md` is not current.
