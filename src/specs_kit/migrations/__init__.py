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

from specs_kit.migrations import (
    m0001_specs_folder,
    m0002_lock_file,
    m0003_agents_marker,
    m0004_specs_paths,
)
from specs_kit.project import kit_rev

type History = Callable[[], Path]


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
    Migration(
        m0002_lock_file.COMMIT,
        m0002_lock_file.DESCRIPTION,
        m0002_lock_file.project,
        m0002_lock_file.copy,
    ),
    Migration(
        m0003_agents_marker.COMMIT,
        m0003_agents_marker.DESCRIPTION,
        m0003_agents_marker.project,
        m0003_agents_marker.copy,
    ),
    Migration(
        m0004_specs_paths.COMMIT,
        m0004_specs_paths.DESCRIPTION,
        m0004_specs_paths.project,
        m0004_specs_paths.copy,
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


def pending(history: History, ref: str | None) -> tuple[Migration, ...]:
    """Return the migrations that a kit ref does not hold, oldest first.

    The commit of this program holds each of its migrations, so this ref needs no history.

    Args:
        history: Returns a clone of the kit with its history. It runs only when it is needed.
        ref: The kit ref of the project or the copy, or None for the oldest format.

    Returns:
        The migrations.
    """
    match ref:
        case None:
            return MIGRATIONS
        case str() if ref == kit_rev():
            return ()
        case str():
            return tuple(m for m in MIGRATIONS if not contains(history(), m.commit, ref))


def migrate_project(history: History, root: Path, ref: str | None) -> tuple[str, ...]:
    """Run the pending migrations of a project.

    Args:
        history: Returns a clone of the kit with its history.
        root: The root of the project.
        ref: The kit ref of the project.

    Returns:
        The descriptions of the migrations that ran.
    """
    todo = pending(history, ref)
    for migration in todo:
        migration.project(root)
    return tuple(m.description for m in todo)


def migrate_copy(history: History, folder: Path, ref: str | None) -> tuple[str, ...]:
    """Run the pending migrations of a copy.

    Args:
        history: Returns a clone of the kit with its history.
        folder: The folder of the copy.
        ref: The kit ref of the repository of the copy, or None when it has none.

    Returns:
        The descriptions of the migrations that ran.
    """
    todo = pending(history, ref)
    for migration in todo:
        migration.copy(folder)
    return tuple(m.description for m in todo)
