"""The file `specs.lock`: the commit, the folders and the hash of each copy (§000082).

`specs.toml` names a tag, a branch or a commit as `ref`. `specs.lock` holds the commit that
`ref` named at the last `specs update` or `specs add`, and the hash of the copy below
`specs/.upstream/`. `specs install` loads a copy again only when it does not agree with
`specs.lock`, and `specs check` finds a copy that a person changed.
"""

from __future__ import annotations

import base64
import hashlib
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from specs_kit.changes import write_text

LOCK_NAME = "specs.lock"
HEAD = "# Written by specs install, specs update and specs add (000082). Do not edit.\n"


@dataclass(frozen=True, slots=True)
class Locked:
    """The entry of one repository in `specs.lock`.

    Attributes:
        ref: The `ref` of `specs.toml` that gave the commit.
        commit: The commit of the copy.
        include: The folders of the copy below `specs/`, without slashes; empty for all.
        hash: The hash of the copy (`tree_hash`).
    """

    ref: str
    commit: str
    include: tuple[str, ...]
    hash: str


def tree_hash(folder: Path) -> str:
    """Return the SHA-256 hash of the paths and the contents of the files below a folder.

    Each file adds its path relative to `folder`, a null byte, the length of its content, a null
    byte and its content, in the order of the sorted paths.

    Args:
        folder: The folder.

    Returns:
        `sha256-<base64>`. A missing folder gives the hash of no files.
    """
    files = sorted(
        (p.relative_to(folder).as_posix(), p)
        for p in (folder.rglob("*") if folder.is_dir() else ())
        if p.is_file()
    )
    digest = hashlib.sha256()
    for rel, path in files:
        content = path.read_bytes()
        digest.update(f"{rel}\0{len(content)}\0".encode())
        digest.update(content)
    return f"sha256-{base64.b64encode(digest.digest()).decode()}"


def _entry(table: Mapping[str, object]) -> Locked | None:
    """Return one entry of `specs.lock`, or None when a key is missing or has a wrong type.

    Args:
        table: The table of the repository.

    Returns:
        The entry or None.
    """
    match table.get("ref"), table.get("commit"), table.get("include", []), table.get("hash"):
        case str() as ref, str() as commit, list() as include, str() as digest if all(
            isinstance(f, str) for f in cast("list[object]", include)
        ):
            return Locked(
                ref, commit, tuple(f.strip("/") for f in cast("list[str]", include)), digest
            )
        case _:
            return None


def read_lock(root: Path) -> Mapping[str, Locked]:
    """Read `specs.lock`. A missing or broken file or entry gives no entry.

    Args:
        root: The root of the project.

    Returns:
        The entry of each repository.
    """
    path = root / LOCK_NAME
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except tomllib.TOMLDecodeError:
        return {}
    tables = data.get("upstream", {})
    found = (
        {
            repo: _entry(cast("Mapping[str, object]", table))
            for repo, table in cast("Mapping[str, object]", tables).items()
            if isinstance(table, dict)
        }
        if isinstance(tables, dict)
        else {}
    )
    return {repo: entry for repo, entry in found.items() if entry is not None}


def lock_text(entries: Mapping[str, Locked]) -> str:
    """Return the text of `specs.lock`.

    Args:
        entries: The entry of each repository.

    Returns:
        The text, with the repositories sorted.
    """
    return HEAD + "".join(
        f'\n[upstream."{repo}"]\n'
        f'ref = "{e.ref}"\n'
        f'commit = "{e.commit}"\n'
        f"include = [{', '.join(f'"{f}/"' for f in e.include)}]\n"
        f'hash = "{e.hash}"\n'
        for repo, e in sorted(entries.items())
    )


def write_lock(root: Path, entries: Mapping[str, Locked]) -> None:
    """Write `specs.lock`.

    Args:
        root: The root of the project.
        entries: The entry of each repository.
    """
    write_text(root / LOCK_NAME, lock_text(entries))


def set_locked(root: Path, repo: str, entry: Locked) -> None:
    """Set the entry of one repository in `specs.lock`. Keep the other entries.

    Args:
        root: The root of the project.
        repo: The repository.
        entry: The new entry.
    """
    write_lock(root, {**read_lock(root), repo: entry})


def drop_locked(root: Path, repos: frozenset[str]) -> None:
    """Remove the entries of repositories that `specs.toml` does not name any more.

    Args:
        root: The root of the project.
        repos: The repositories of `specs.toml`.
    """
    current = read_lock(root)
    if set(current) - repos:
        write_lock(root, {r: e for r, e in current.items() if r in repos})
