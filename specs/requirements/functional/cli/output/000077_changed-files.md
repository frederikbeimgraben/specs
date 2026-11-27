---
id: "000077"
title: specs lists the files that a command changes
kind: functional
status: draft
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_output.py:test_the_report_comes_after_the_files
  - tests/test_output.py:test_changed_files_are_sorted_and_relative
  - tests/test_output.py:test_a_write_with_the_same_content_is_no_change
implementation:
  - src/specs_kit/changes.py
  - src/specs_kit/cli.py
  - src/specs_kit/view.py
  - src/specs_kit/mcp_server.py
scope:
  - src/specs_kit/
---

# specs lists the files that a command changes

Each command of `specs` that changes files (`init`, `install`, `update`, `add`, `configure`,
`remove` and `new`) must list each file that it created, changed or deleted, one file on each
line, as in `git status --short`. The list must come after the message and the hints, and
before the report of `specs check`, so that the report is at the end. A command without a check
must end with the list:

| Mark | Change | Color on a terminal |
| --- | --- | --- |
| `A` | The command created the file. | Green |
| `M` | The command changed the content of the file. | Yellow |
| `D` | The command deleted the file. | Red |

The path must be relative to the root of the project. The list must be sorted by path. Each
place in the code that writes a file must record it. A file that a different program writes
for the command, for example `flake.lock` from `nix flake lock`, must be in the list too. A
write with the same content is no change. For a copied folder, for example
`specs/.upstream/`, the list must hold only the files that are new, changed or deleted. The
MCP tools `install`, `new`, `configure` and `remove` must return the same list as plain text,
in the same place.

Reason: The person sees what a command did without `git status`, and a script can read the
list.

Test: `tests/test_output.py`.
