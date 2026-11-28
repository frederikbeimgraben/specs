"""Record the files that a command creates, changes or deletes (spec 000077).

Each place that writes a file reports it here. A command that runs in `recording()` gets the
list at its end. A write with the same content is no change.
"""

from __future__ import annotations

import shutil
import stat
from collections.abc import Callable, Generator, Iterable, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from enum import StrEnum
from pathlib import Path

MIGRATED = "migrated: "
"""The start of the hint line of a migration that ran (spec 000081)."""


class Mark(StrEnum):
    """The mark of a change, as in `git status --short`."""

    ADDED = "A"
    MODIFIED = "M"
    DELETED = "D"


_LOG: ContextVar[dict[Path, Mark] | None] = ContextVar("changes", default=None)


@contextmanager
def recording() -> Generator[Mapping[Path, Mark]]:
    """Record the changes of the code in the block.

    Yields:
        The changes by absolute path. The mapping fills while the block runs.
    """
    log: dict[Path, Mark] = {}
    token = _LOG.set(log)
    try:
        yield log
    finally:
        _LOG.reset(token)


def _merge(before: Mark | None, after: Mark) -> Mark | None:
    """Return the mark of two changes of one file in sequence.

    Args:
        before: The first mark, or None.
        after: The second mark.

    Returns:
        The total mark, or None when the file is as before.
    """
    match (before, after):
        case (Mark.ADDED, Mark.MODIFIED):
            return Mark.ADDED
        case (Mark.ADDED, Mark.DELETED):
            return None
        case (Mark.DELETED, Mark.ADDED):
            return Mark.MODIFIED
        case _:
            return after


def note(path: Path, mark: Mark) -> None:
    """Record one change.

    Args:
        path: The file.
        mark: The change.
    """
    log = _LOG.get()
    if log is None:
        return
    key = path.resolve()
    match _merge(log.get(key), mark):
        case None:
            log.pop(key, None)
        case total:
            log[key] = total


def _content(path: Path) -> bytes | None:
    """Return the bytes of a file, or None without a file.

    Args:
        path: The file.

    Returns:
        The bytes or None.
    """
    return path.read_bytes() if path.is_file() else None


def _compare(path: Path, old: bytes | None) -> None:
    """Record the change of a file from its old content.

    Args:
        path: The file.
        old: The old bytes, or None when the file was not there.
    """
    _compare_bytes(path, old, _content(path))


def write_text(path: Path, text: str) -> None:
    """Write a text file, with its folders, and record the change.

    Args:
        path: The file.
        text: The new text.
    """
    old = _content(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    _compare(path, old)


@contextmanager
def watching(*paths: Path) -> Generator[None]:
    """Record the changes that a different program makes to some files.

    Args:
        *paths: The files.

    Yields:
        Nothing.
    """
    old = {p: _content(p) for p in paths}
    yield
    for path, before in old.items():
        _compare(path, before)


def _files(root: Path) -> Mapping[Path, bytes]:
    """Return the bytes of each file below a folder, by relative path.

    Args:
        root: The folder.

    Returns:
        The bytes by relative path.
    """
    return (
        {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        if root.is_dir()
        else {}
    )


def unlock(folder: Path) -> None:
    """Give the owner write access to a folder and to all its files and folders.

    A copy from the Nix store is read-only, so that a later move or delete would fail.

    Args:
        folder: The folder. Nothing happens when it does not exist.
    """
    for path in (
        p for p in ((folder, *folder.rglob("*")) if folder.is_dir() else ()) if not p.is_symlink()
    ):
        path.chmod(path.stat().st_mode | stat.S_IWUSR)


def _rmtree(folder: Path) -> None:
    """Delete a folder with its read-only parts, when it exists.

    Args:
        folder: The folder.
    """
    unlock(folder)
    shutil.rmtree(folder, ignore_errors=True)


def _ignore(source: Path, left_out: frozenset[str]) -> Callable[[str, list[str]], set[str]]:
    """Return the names that a copy of a `specs/` folder leaves out (spec 000048).

    Args:
        source: The folder to copy.
        left_out: The folders below `source` to leave out, without slashes at the ends.

    Returns:
        The function for `shutil.copytree`: each hidden name, `upstream` at the top, and each
        folder of `left_out`.
    """
    top = str(source)
    return lambda folder, names: {
        n
        for n in names
        if n.startswith(".")
        or (folder == top and n == "upstream")
        or (Path(folder) / n).relative_to(source).as_posix() in left_out
    }


def replace_tree(
    source: Path, target: Path, folders: Iterable[str] = (), left_out: Iterable[str] = ()
) -> None:
    """Replace the folder `target` with a copy of `source`, and record each changed file.

    Without `folders`, the copy holds all of `source` except each hidden file or folder, for
    example `.upstream/` and `.templates/`, and the folder `upstream/` at the top of `source`,
    where the copies of a kit before `.upstream/` were (spec 000048).

    Args:
        source: The folder to copy.
        target: The folder to replace.
        folders: The folders of `source` to copy, or empty for all of `source`.
        left_out: The folders below `source` that the copy leaves out, also inside `folders`.
    """
    skip = frozenset(f.strip("/") for f in left_out)
    old = _files(target)
    _rmtree(target)
    match tuple(folders):
        case ():
            shutil.copytree(source, target, ignore=_ignore(source, skip))
        case chosen:
            for folder in chosen:
                shutil.copytree(
                    source / folder,
                    target / folder,
                    ignore=lambda at, names: {
                        n for n in names if (Path(at) / n).relative_to(source).as_posix() in skip
                    },
                )
    unlock(target)
    new = _files(target)
    for rel in sorted({*old, *new}):
        _compare_bytes(target / rel, old.get(rel), new.get(rel))


def delete_file(path: Path) -> None:
    """Delete a file when it exists, and record the change.

    Args:
        path: The file.
    """
    old = _content(path)
    path.unlink(missing_ok=True)
    _compare_bytes(path, old, None)


def move_tree(source: Path, target: Path) -> None:
    """Move a folder to a new place that replaces any folder there, and record each change.

    Args:
        source: The folder to move. Nothing happens when it does not exist.
        target: The new place.
    """
    if not source.is_dir():
        return
    old = _files(source)
    replace_tree_all(source, target)
    unlock(source)
    shutil.rmtree(source)
    for rel in sorted(old):
        _compare_bytes(source / rel, old[rel], None)


def replace_tree_all(source: Path, target: Path) -> None:
    """Replace the folder `target` with a full copy of `source`, and record each changed file.

    Args:
        source: The folder to copy.
        target: The folder to replace.
    """
    old = _files(target)
    _rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    unlock(target)
    new = _files(target)
    for rel in sorted({*old, *new}):
        _compare_bytes(target / rel, old.get(rel), new.get(rel))


def _compare_bytes(path: Path, old: bytes | None, new: bytes | None) -> None:
    """Record the change of a file from its old and its new bytes.

    Args:
        path: The file.
        old: The old bytes, or None.
        new: The new bytes, or None.
    """
    match (old, new):
        case (None, None):
            return
        case (None, _):
            note(path, Mark.ADDED)
        case (_, None):
            note(path, Mark.DELETED)
        case (before, after) if before != after:
            note(path, Mark.MODIFIED)
        case _:
            return


def lines(log: Mapping[Path, Mark], root: Path) -> tuple[tuple[Mark, str], ...]:
    """Return the changes sorted by path, with paths relative to the root of the project.

    Args:
        log: The changes by absolute path.
        root: The root of the project.

    Returns:
        The mark and the path of each change.
    """
    base = root.resolve()
    return tuple(
        (mark, path.relative_to(base).as_posix() if path.is_relative_to(base) else str(path))
        for path, mark in sorted(log.items())
    )


def remove_tree(folder: Path) -> None:
    """Delete a folder when it exists, and record each deleted file.

    Args:
        folder: The folder.
    """
    old = _files(folder)
    _rmtree(folder)
    for rel in sorted(old):
        _compare_bytes(folder / rel, old[rel], None)
