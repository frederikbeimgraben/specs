"""Migration 3: name `specs install` in the first line of the block in `AGENTS.md` (§000079).

`specs check --write` wrote the block before `specs install` took its place.
"""

from __future__ import annotations

from pathlib import Path

from specs_kit.agents import AGENTS, BEGIN, OLD_BEGIN
from specs_kit.changes import write_text
from specs_kit.migrations.m0002_lock_file import COMMIT as LOCK_COMMIT

COMMIT = LOCK_COMMIT
DESCRIPTION = "name specs install in the block of AGENTS.md"


def project(root: Path) -> None:
    """Replace the old first line of the block in `AGENTS.md`.

    Args:
        root: The root of the project.
    """
    path = root / AGENTS
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if OLD_BEGIN in text.splitlines():
        write_text(path, text.replace(OLD_BEGIN, BEGIN, 1))


def copy(folder: Path) -> None:
    """Change nothing: a copy holds no `AGENTS.md`.

    Args:
        folder: The folder of the copy.
    """
    del folder
