---
id: "000088"
title: spezi lsp runs the language server
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-27
tests:
  - tests/test_lsp.py:test_the_server_shows_the_errors_of_the_project
  - tests/test_lsp.py:test_the_server_checks_the_text_while_it_changes
  - tests/test_lsp.py:test_the_hover_shows_the_rule
  - tests/test_lsp.py:test_the_definition_opens_the_spec
  - tests/test_lsp.py:test_the_link_marks_the_reference_in_the_code
  - tests/test_lsp.py:test_the_server_writes_no_file
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# spezi lsp runs the language server

`spezi lsp` must run a language server on stdin and stdout. The server must use the root of
the workspace as the root of the project. It must serve the specs below `specs/` and the files
of `code_dirs` with the suffixes of `code_suffixes` (000078).

The server must show each error of `spezi check` (000065) as a diagnostic with the severity
error, at the line of the error. An error without a line must go to line 1 of its file. An
error of a folder or of a missing file must go to line 1 of `spezi.toml`, with its path in the
text. The server must check the project:

1. When the client starts it: the whole project, from the files on the disk.
2. 300 ms after the last change of an open file: only this file, with the text in the editor.
3. When the client saves a file: the whole project, from the files on the disk. The server
   must remove each diagnostic of a file that has no error now.

On a reference to a rule, the server must give a hover and a definition. In a spec, a reference
is a rule ID in the short or the long form (000047), also in the front matter. In the code, a
reference is a `§` reference (000017). The hover must show the long form, the title, the status
and the text of the rule after the front matter. The definition must give the first line of the
file of the rule. The hover and the definition must mark only the reference, in the code with
the `§`, and not the whole line. The server must not write a file.

Reason: The editor shows the errors of the check at their line while a person writes, and the
text of a rule without a change of file.

Test: `tests/test_lsp.py`.
