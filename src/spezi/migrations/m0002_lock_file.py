"""Migration 2: write `specs.lock` from the commits in `specs.toml` (§000082).

Before this migration, `ref` in `specs.toml` was the commit of each copy, and `specs.lock` did not
exist. The migration writes an entry for each repository whose `ref` is a commit and whose copy
exists, with the hash of the copy as it is.
"""

from __future__ import annotations

import re
from pathlib import Path

from spezi.changes import write_text
from spezi.lock import OLD_LOCK_NAME, Locked, lock_text, tree_hash
from spezi.project import OLD_CONFIG_NAME, UPSTREAM, read_config

COMMIT = "a7f306dd3e7a5b99ba02d69337f0439583691ba7"
DESCRIPTION = "write specs.lock from the commits in specs.toml"


def project(root: Path) -> None:
    """Write `specs.lock` when it does not exist and `specs.toml` names a commit for a copy.

    Args:
        root: The root of the project.
    """
    config = read_config(root / OLD_CONFIG_NAME)
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
    if entries and not (root / OLD_LOCK_NAME).exists():
        write_text(root / OLD_LOCK_NAME, lock_text(entries))


def copy(folder: Path) -> None:
    """Change nothing: a copy holds only the `specs/` folder, without `specs.toml`.

    Args:
        folder: The folder of the copy.
    """
    del folder
