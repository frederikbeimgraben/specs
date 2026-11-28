"""What every check of one spec can read."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from spezi.project import Project, Spec

type Errors = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Context:
    """What every check of one spec can read.

    Attributes:
        project: The project.
        local: The specs of the project by number.
        foreign: The status of each rule of the copies by short form. A rule that a spec in
            force replaces has the status `replaced` (§000049).
    """

    project: Project
    local: Mapping[str, Spec]
    foreign: Mapping[str, str]


def where(project: Project, spec: Spec) -> str:
    """Return the path of a spec from the root of the project.

    Args:
        project: The project.
        spec: The spec.

    Returns:
        The path as text.
    """
    return spec.path.relative_to(project.root).as_posix()
