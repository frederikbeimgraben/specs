---
id: "000322"
title: The language server shows each finding of the check
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_lsp.py:test_the_server_shows_the_errors_of_the_project
  - tests/test_ste.py:test_lsp_shows_a_warning_with_the_severity_warning
implementation:
  - src/spezi/lsp.py
  - src/spezi/check.py
  - src/spezi/cli.py
scope:
  - src/spezi/
---

# The language server shows each finding of the check

The language server (spec 000088) must show each error of `spezi check` (spec 000065) as a
diagnostic with the severity error, at the line of the error. It must show each warning
(spec 000093) in the same way, with the severity warning.

Reason: The editor shows the errors and the warnings with their own color.

Test: `tests/test_lsp.py`.
