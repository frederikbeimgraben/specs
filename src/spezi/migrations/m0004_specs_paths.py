"""Migration 4: change the paths below `.specs/` in the specs of the project (spec 000051).

Migration 1 moved the files of `.specs/` below `specs/`, but a spec of the project can still
name an old path, for example in `implementation` or in the element table of a structure.
"""

from __future__ import annotations

import re
from pathlib import Path

from spezi.changes import write_text
from spezi.migrations.m0001_specs_folder import COMMIT as FOLDER_COMMIT

COMMIT = FOLDER_COMMIT
DESCRIPTION = "change the paths below .specs/ in the specs of the project"
OLD_PATH = re.compile(r"(?<![\w./-])\.specs/(templates/|upstream/|index\.md)?")
NEW_PATHS = {
    "templates/": "specs/.templates/",
    "upstream/": "specs/.upstream/",
    "index.md": "specs/README.md",
}


def new_path(found: re.Match[str]) -> str:
    """Return the new path of an old path below `.specs/`.

    Args:
        found: The match of `OLD_PATH`.

    Returns:
        The path below `specs/`.
    """
    return NEW_PATHS.get(found[1] or "", "specs/")


def project(root: Path) -> None:
    """Change each old path in the specs of the project, but not in the copies.

    Args:
        root: The root of the project.
    """
    specs = root / "specs"
    for path in sorted(
        p
        for p in specs.rglob("*.md")
        if not p.relative_to(specs).parts[0].startswith(".") and p.is_file()
    ):
        text = path.read_text(encoding="utf-8")
        changed = OLD_PATH.sub(new_path, text)
        if changed != text:
            write_text(path, changed)


def copy(folder: Path) -> None:
    """Change nothing: the paths in a copy are paths of the other repository.

    Args:
        folder: The folder of the copy.
    """
    del folder
