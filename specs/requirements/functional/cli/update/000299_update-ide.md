---
id: "000299"
title: spezi update writes the editor folders again
kind: functional
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
tests:
  - tests/test_setup_ide.py:test_update_writes_the_folder_again
implementation:
  - src/spezi/ide.py
  - src/spezi/kit.py
scope:
  - src/spezi/
---

# spezi update writes the editor folders again

For the kit, `spezi update` must write each editor folder (spec 000089) again that is in the
project. The folder of VS Code stays as it is when the program has no `spezi.vsix`.

Reason: The extension starts the language server of the new kit.

Test: `tests/test_setup_ide.py`.
