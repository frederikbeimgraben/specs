"""The file `spezi.lock`: the commit, the folders and the hash of each copy (§000082).

`spezi.toml` names a tag, a branch or a commit as `ref`. `spezi.lock` holds the commit that
`ref` named at the last `spezi update` or `spezi add`, and the hash of the copy below
`specs/.upstream/`. `spezi install` loads a copy again only when it does not agree with
`spezi.lock`, and `spezi check` finds a copy that a person changed.
"""

from __future__ import annotations

import base64
import hashlib
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from spezi.changes import write_text

LOCK_NAME = "spezi.lock"
OLD_LOCK_NAME = "specs.lock"
HEAD = "# Written by spezi install, spezi update and spezi add (000082). Do not edit.\n"


@dataclass(frozen=True, slots=True)
class Locked:
    """The entry of one repository in `spezi.lock`.

    Attributes:
        ref: The `ref` of `spezi.toml` that gave the commit; empty for a transitive upstream.
        commit: The commit of the copy.
        include: The folders of the copy below `specs/`, without slashes; empty for all.
        hash: The hash of the copy (`tree_hash`).
        via: The direct upstreams that bring a transitive upstream, sorted; empty for a direct
            upstream (§000092).
    """

    ref: str
    commit: str
    include: tuple[str, ...]
    hash: str
    via: tuple[str, ...] = ()


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
    """Return one entry of `spezi.lock`, or None when a key is missing or has a wrong type.

    Args:
        table: The table of the repository.

    Returns:
        The entry or None.
    """
    match (
        table.get("ref", ""),
        table.get("commit"),
        table.get("include", []),
        table.get("hash"),
        table.get("via", []),
    ):
        case str() as ref, str() as commit, list() as include, str() as digest, list() as via if (
            all(isinstance(f, str) for f in (*cast("list[object]", include), *via))
            and bool(ref) != bool(via)
        ):
            return Locked(
                ref,
                commit,
                tuple(f.strip("/") for f in cast("list[str]", include)),
                digest,
                tuple(sorted(cast("list[str]", via))),
            )
        case _:
            return None


def read_lock(root: Path) -> Mapping[str, Locked]:
    """Read `spezi.lock`. A missing or broken file or entry gives no entry.

    Before the migration of the name, the file is `specs.lock`.

    Args:
        root: The root of the project.

    Returns:
        The entry of each repository.
    """
    path = next(
        (root / n for n in (LOCK_NAME, OLD_LOCK_NAME) if (root / n).is_file()), root / LOCK_NAME
    )
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
    """Return the text of `spezi.lock`.

    Args:
        entries: The entry of each repository.

    Returns:
        The text, with the repositories sorted.
    """
    return HEAD + "".join(
        f'\n[upstream."{repo}"]\n'
        + (f"via = [{', '.join(f'"{v}"' for v in e.via)}]\n" if e.via else f'ref = "{e.ref}"\n')
        + f'commit = "{e.commit}"\n'
        f"include = [{', '.join(f'"{f}/"' for f in e.include)}]\n"
        f'hash = "{e.hash}"\n'
        for repo, e in sorted(entries.items())
    )


def write_lock(root: Path, entries: Mapping[str, Locked]) -> None:
    """Write `spezi.lock`.

    Args:
        root: The root of the project.
        entries: The entry of each repository.
    """
    write_text(root / LOCK_NAME, lock_text(entries))


def set_locked(root: Path, repo: str, entry: Locked) -> None:
    """Set the entry of one repository in `spezi.lock`. Keep the other entries.

    Args:
        root: The root of the project.
        repo: The repository.
        entry: The new entry.
    """
    write_lock(root, {**read_lock(root), repo: entry})


def drop_locked(root: Path, repos: frozenset[str]) -> None:
    """Remove the entries of repositories that `spezi.toml` does not name any more.

    Args:
        root: The root of the project.
        repos: The repositories of `spezi.toml` and the transitive upstreams that stay.
    """
    current = read_lock(root)
    if set(current) - repos:
        write_lock(root, {r: e for r, e in current.items() if r in repos})
