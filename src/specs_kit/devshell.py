"""Keep the input `specs` of the flake of a project at the ref of the kit (§000066, §000067).

The kit never changes a `flake.nix` or an `.envrc` that exists. For a missing part it returns a
hint with the lines to add.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from specs_kit.changes import watching, write_text
from specs_kit.kit import KitError, package_data, run_command

FLAKE = "flake.nix"
LOCK = "flake.lock"
ENVRC = ".envrc"
INPUT = re.compile(r'"github:frederikbeimgraben/specs(?:/[^"?]*)?"')
INPUT_LINES = (
    "  # The specs command of the kit. The ref must be the commit in specs.lock.\n"
    '  inputs.specs.url = "github:frederikbeimgraben/specs/{ref}";'
)
PACKAGE = "specs.packages.${system}.default"


def _git_repo(root: Path) -> bool:
    """Return True when the root is in a git work tree.

    Args:
        root: The root of the project.

    Returns:
        True in a git work tree.
    """
    try:
        return run_command("git", "rev-parse", "--is-inside-work-tree", cwd=root).strip() == "true"
    except KitError:
        return False


def envrc(root: Path) -> tuple[str, ...]:
    """Write `.envrc` with `use flake` when it is missing.

    Args:
        root: The root of the project.

    Returns:
        The hints.
    """
    path = root / ENVRC
    match (path.is_file(), path.is_file() and "use flake" in path.read_text(encoding="utf-8")):
        case (False, _):
            write_text(path, "use flake\n")
            return ("hint: run direnv allow to load the devShell with direnv",)
        case (True, False):
            return (f"hint: add the line use flake to {ENVRC} to load the devShell with direnv",)
        case (True, True):
            return ()


def init_flake(root: Path, ref: str) -> tuple[str, ...]:
    """Give the project a devShell with the program `specs` at the ref of the kit.

    Without `flake.nix`, write a new flake with the input `specs` and a devShell, lock it, and
    add it to git. With `flake.nix`, change nothing and return a hint for each missing part.

    Args:
        root: The root of the project.
        ref: The commit of the kit.

    Returns:
        The hints.
    """
    path = root / FLAKE
    match path.is_file():
        case False:
            write_text(path, package_data(FLAKE).replace("{ref}", ref))
            hints = envrc(root)
            if _git_repo(root):
                run_command("git", "add", "--", FLAKE, ENVRC, cwd=root)
            with watching(root / LOCK):
                run_command("nix", "flake", "lock", cwd=root)
            if _git_repo(root):
                run_command("git", "add", "--", LOCK, cwd=root)
            return hints
        case True:
            text = path.read_text(encoding="utf-8")
            return (
                *(
                    ()
                    if INPUT.search(text)
                    else (f"hint: add to {FLAKE}:\n{INPUT_LINES.replace('{ref}', ref)}",)
                ),
                *(
                    ()
                    if "specs.packages" in text
                    else (f"hint: add {PACKAGE} to the packages of your devShell",)
                ),
                *envrc(root),
            )


def update_flake(root: Path, ref: str) -> tuple[str, ...]:
    """Set the ref of the input `specs` in `flake.nix` and lock the input again.

    Without `flake.nix` or without the input `specs`, change nothing.

    Args:
        root: The root of the project.
        ref: The commit of the kit.

    Returns:
        The hints: in a devShell without direnv, how to load the new program.
    """
    path = root / FLAKE
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    match bool(INPUT.search(text)):
        case False:
            return ()
        case True:
            write_text(path, INPUT.sub(f'"github:frederikbeimgraben/specs/{ref}"', text))
            with watching(root / LOCK):
                run_command("nix", "flake", "update", "specs", cwd=root)
            return (
                ("hint: exit this shell and run nix develop to use the new specs",)
                if os.environ.get("IN_NIX_SHELL") and not os.environ.get("DIRENV_DIR")
                else ()
            )
