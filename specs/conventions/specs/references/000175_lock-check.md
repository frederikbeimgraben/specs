---
id: "000175"
title: spezi check finds a lock that does not agree
kind: convention
status: approved
owner: frederikbeimgraben
updated: 2026-11-28
implementation:
  - src/spezi/lock.py
  - src/spezi/check.py
  - src/spezi/kit.py
scope:
  - src/spezi/lock.py
  - spezi.toml
---

# spezi check finds a lock that does not agree

`spezi check` must show an error in these cases:

- `spezi.lock` does not name each repository of `spezi.toml` and each copy (spec 000092), or it
  names a different repository.
- `ref` or `include` of the entry of a direct upstream is not the same as in `spezi.toml`.
- `commit`, `include` or `via` of the entry of a transitive upstream does not agree with the
  rules of the transitive upstreams (spec 000092).
- The hash of a copy is not the hash of its entry.

Reason: A lock that does not agree with the settings or the copies gives a different copy on
the next `spezi install`.

Test: `tests/test_transitive.py`.
