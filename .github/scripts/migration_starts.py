"""Print the start commits of the migration CI as a JSON list (W 000090).

A start commit is the parent of the commit of each migration, once for each commit.
"""

from __future__ import annotations

import json
import subprocess

from specs_kit.migrations import MIGRATIONS


def parent(commit: str) -> str:
    """Return the parent of a commit of the kit.

    Args:
        commit: The commit.

    Returns:
        The full hash of the first parent.
    """
    return subprocess.run(
        ("git", "rev-parse", f"{commit}^"), capture_output=True, text=True, check=True
    ).stdout.strip()


if __name__ == "__main__":
    print(json.dumps([parent(c) for c in dict.fromkeys(m.commit for m in MIGRATIONS)]))
