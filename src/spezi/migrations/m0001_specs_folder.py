"""Migration 1: move the files of `.specs/` below `specs/` (§000051).

`.specs/upstream/` becomes `specs/.upstream/` and `.specs/templates/` becomes
`specs/.templates/`. The index `.specs/index.md` goes away, because `specs/README.md` is the
index now.
"""

from __future__ import annotations

from pathlib import Path

from spezi.changes import delete_file, move_tree

COMMIT = "9f62adf517e7076b57593d5355729493cfb55a73"
DESCRIPTION = "move .specs/ below specs/"


def project(root: Path) -> None:
    """Move `.specs/upstream/` and `.specs/templates/`, and delete `.specs/index.md`.

    Args:
        root: The root of the project.
    """
    old = root / ".specs"
    move_tree(old / "upstream", root / "specs" / ".upstream")
    move_tree(old / "templates", root / "specs" / ".templates")
    delete_file(old / "index.md")
    if old.is_dir() and not any(old.iterdir()):
        old.rmdir()


def copy(folder: Path) -> None:
    """Change nothing: a copy holds only the `specs/` folder, which keeps its form.

    Args:
        folder: The folder of the copy.
    """
    del folder
