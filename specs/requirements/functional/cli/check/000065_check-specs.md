---
id: "000065"
title: spezi check checks the specs
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_check.py:test_check_passes_after_init
  - tests/test_check.py:test_check_changes_no_file
  - tests/test_check.py:test_install_writes_the_index
  - tests/test_check.py:test_check_finds_a_rule_without_must
  - tests/test_check.py:test_check_finds_a_bad_file_name
  - tests/test_check.py:test_check_finds_a_missing_key
  - tests/test_check.py:test_check_finds_a_stale_index
  - tests/test_check.py:test_check_gives_the_line
implementation:
  - src/spezi/agents.py
  - src/spezi/check.py
  - src/spezi/index.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi check checks the specs

`spezi check` must run every check of the conventions on the specs of the project. It must also
check that `spezi.toml`, `spezi.lock` and the copies agree (spec 000048, 000082). It must check
each reference to a rule in the files of `code_dirs` and in each Markdown file that git tracks
(spec 000017). It must print one line for each error, then the count of specs and errors. An
error line must start with `<path>:<line>: `. The line must be the line of the front matter key,
of the entry or of the reference that the error names, else 1. An error of a folder or of a
missing file must have only `<path>: `. The command must exit with 1 when it finds an error,
else with 0. The command must not change a file and must not use the network. `spezi install`
writes the index `specs/README.md` (spec 000007) and the block in `AGENTS.md`
(spec 000079, 000083).

Reason: CI and an agent run the same check with one command.

Test: `tests/test_check.py`.
