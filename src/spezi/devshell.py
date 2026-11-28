"""Keep the input `spezi` of the flake of a project at the ref of the kit (§000066, §000067).

The kit never changes a `flake.nix` or an `.envrc` that exists. For a missing part it returns a
hint with the lines to add.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from pathlib import Path

from spezi.changes import watching, write_text
from spezi.kit import KitError, package_data, run_command

FLAKE = "flake.nix"
LOCK = "flake.lock"
ENVRC = ".envrc"
INPUT = re.compile(r'"github:frederikbeimgraben/(?:spezi|specs)(?:/[^"?]*)?"')
INPUT_NAME = re.compile(r'([\w-]+)\.url\s*=\s*"github:frederikbeimgraben/(?:spezi|specs)[/"]')
INPUT_LINES = (
    "  # The spezi command of the kit. The ref must be the commit in spezi.lock.\n"
    '  inputs.spezi.url = "github:frederikbeimgraben/spezi/{ref}";'
)
PACKAGE = "spezi.packages.${system}.default"


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


def init_flake(root: Path, ref: str, features: Mapping[str, bool]) -> tuple[str, ...]:
    """Give the project a devShell with the program `spezi` at the ref of the kit.

    Without `flake.nix`, write a new flake with the input `spezi` and a devShell, lock it, and
    add it to git. With `flake.nix`, change nothing and return a hint for each missing part.
    The switches `flake` and `envrc` of `[features]` choose the parts (§000084).

    Args:
        root: The root of the project.
        ref: The commit of the kit.
        features: The switches of `[features]`.

    Returns:
        The hints.
    """
    path = root / FLAKE
    hints = envrc(root) if features.get("envrc", True) else ()
    match features.get("flake", True), path.is_file():
        case False, _:
            return hints
        case True, False:
            write_text(path, package_data(FLAKE).replace("{ref}", ref))
            added = tuple(f for f in (FLAKE, ENVRC) if (root / f).is_file())
            if _git_repo(root):
                run_command("git", "add", "--", *added, cwd=root)
            with watching(root / LOCK):
                run_command("nix", "flake", "lock", cwd=root)
            if _git_repo(root):
                run_command("git", "add", "--", LOCK, cwd=root)
            return hints
        case True, True:
            text = path.read_text(encoding="utf-8")
            return (
                *(
                    ()
                    if INPUT.search(text)
                    else (f"hint: add to {FLAKE}:\n{INPUT_LINES.replace('{ref}', ref)}",)
                ),
                *(
                    ()
                    if re.search(r"\b(?:spezi|specs)\.packages", text)
                    else (f"hint: add {PACKAGE} to the packages of your devShell",)
                ),
                *hints,
            )


def flake_template(ref: str) -> str:
    """Return the text of a new `flake.nix` at a commit of the kit.

    Args:
        ref: The commit of the kit.

    Returns:
        The text.
    """
    return package_data(FLAKE).replace("{ref}", ref)


def update_flake(root: Path, ref: str) -> tuple[str, ...]:
    """Set the ref of the input of the kit in `flake.nix` and lock the input again.

    The input has the URL of the kit, with the new or the old name of the kit. Without
    `flake.nix` or without this input, change nothing.

    Args:
        root: The root of the project.
        ref: The commit of the kit.

    Returns:
        The hints: in a devShell without direnv, how to load the new program.
    """
    path = root / FLAKE
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    match INPUT_NAME.search(text):
        case None:
            return ()
        case found:
            write_text(path, INPUT.sub(f'"github:frederikbeimgraben/spezi/{ref}"', text))
            with watching(root / LOCK):
                run_command("nix", "flake", "update", found.group(1), cwd=root)
            return (
                ("hint: exit this shell and run nix develop to use the new spezi",)
                if os.environ.get("IN_NIX_SHELL") and not os.environ.get("DIRENV_DIR")
                else ()
            )
