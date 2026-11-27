"""Migration 2: write `specs.lock` from the commits in `specs.toml` (§000082).

Before this migration, `ref` in `specs.toml` was the commit of each copy, and `specs.lock` did not
exist. The migration writes an entry for each repository whose `ref` is a commit and whose copy
exists, with the hash of the copy as it is.
"""

from __future__ import annotations

import re
from pathlib import Path

from specs_kit.lock import LOCK_NAME, Locked, tree_hash, write_lock
from specs_kit.project import UPSTREAM, read_config

COMMIT = "a7f306dd3e7a5b99ba02d69337f0439583691ba7"
DESCRIPTION = "write specs.lock from the commits in specs.toml"


def project(root: Path) -> None:
    """Write `specs.lock` when it does not exist and `specs.toml` names a commit for a copy.

    Args:
        root: The root of the project.
    """
    config = read_config(root / "specs.toml")
    copies = root / "specs" / UPSTREAM
    entries = {
        repo: Locked(
            ref,
            ref,
            tuple(f.strip("/") for f in config.include.get(repo, ())),
            tree_hash(copies / repo),
        )
        for repo, ref in config.upstream.items()
        if ref and re.fullmatch(r"[0-9a-f]{40}", ref) and (copies / repo).is_dir()
    }
    if entries and not (root / LOCK_NAME).exists():
        write_lock(root, entries)


def copy(folder: Path) -> None:
    """Change nothing: a copy holds only the `specs/` folder, without `specs.toml`.

    Args:
        folder: The folder of the copy.
    """
    del folder
