"""Migrations of a project and of its copies to the format of this program (§000081).

Each migration names the commit of the kit that changed the format. A project or a copy whose
kit ref does not hold this commit gets the migration. A migration changes only what it finds in
the old format, so a second run changes nothing.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from specs_kit.migrations import m0001_specs_folder


@dataclass(frozen=True, slots=True)
class Migration:
    """One change of the format.

    Attributes:
        commit: The commit of the kit that changed the format.
        description: What the migration changes.
        project: The change of a project, from the root of the project.
        copy: The change of a copy, from the folder of the copy below `specs/.upstream/`.
    """

    commit: str
    description: str
    project: Callable[[Path], None]
    copy: Callable[[Path], None]


MIGRATIONS: tuple[Migration, ...] = (
    Migration(
        m0001_specs_folder.COMMIT,
        m0001_specs_folder.DESCRIPTION,
        m0001_specs_folder.project,
        m0001_specs_folder.copy,
    ),
)


def contains(history: Path, commit: str, ref: str) -> bool:
    """Return True when `ref` holds `commit` in a clone of the kit.

    Args:
        history: A clone of the kit with its history.
        commit: The commit.
        ref: The ref.

    Returns:
        True when `commit` is an ancestor of `ref` or the same commit. False when git does not
        know one of them.
    """
    return (
        subprocess.run(
            ("git", "-C", str(history), "merge-base", "--is-ancestor", commit, ref),
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )


def pending(history: Path, ref: str | None) -> tuple[Migration, ...]:
    """Return the migrations that a kit ref does not hold, oldest first.

    Args:
        history: A clone of the kit with its history.
        ref: The kit ref of the project or the copy, or None for the oldest format.

    Returns:
        The migrations.
    """
    return tuple(m for m in MIGRATIONS if ref is None or not contains(history, m.commit, ref))


def migrate_project(history: Path, root: Path, ref: str | None) -> tuple[str, ...]:
    """Run the pending migrations of a project.

    Args:
        history: A clone of the kit with its history.
        root: The root of the project.
        ref: The kit ref of the project.

    Returns:
        The descriptions of the migrations that ran.
    """
    todo = pending(history, ref)
    for migration in todo:
        migration.project(root)
    return tuple(m.description for m in todo)


def migrate_copy(history: Path, folder: Path, ref: str | None) -> tuple[str, ...]:
    """Run the pending migrations of a copy.

    Args:
        history: A clone of the kit with its history.
        folder: The folder of the copy.
        ref: The kit ref of the repository of the copy, or None when it has none.

    Returns:
        The descriptions of the migrations that ran.
    """
    todo = pending(history, ref)
    for migration in todo:
        migration.copy(folder)
    return tuple(m.description for m in todo)
