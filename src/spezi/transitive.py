"""The transitive upstreams: the upstreams that the copy of a direct upstream brings (§000092).

The copy of each direct upstream holds the `spezi.lock` of its repository. The list
`transitive` in the table of the direct upstream names the repositories of that file that the
project copies. A repository gets its commit and its `include` from that file. The project
itself and a repository with its own table get no copy from `transitive`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from spezi.lock import Locked, read_lock
from spezi.project import Project


@dataclass(frozen=True, slots=True)
class Wanted:
    """The copy of one transitive upstream that the direct upstreams ask for.

    Attributes:
        commit: The commit of the copy.
        include: The union of the folders of the copy, without slashes; empty for all.
        via: The direct upstreams that name the repository in `transitive`, sorted.
    """

    commit: str
    include: tuple[str, ...]
    via: tuple[str, ...]


def upstream_lock(project: Project, direct: str) -> Mapping[str, Locked]:
    """Return the entries of the `spezi.lock` in the copy of a direct upstream.

    Args:
        project: The project.
        direct: The direct upstream.

    Returns:
        The entry of each repository; empty when the copy has no `spezi.lock`.
    """
    return read_lock(project.upstream_dir / direct)


def offers(
    project: Project, direct: str, entries: Mapping[str, Locked], own: str | None = None
) -> tuple[str, ...]:
    """Return the repositories that a direct upstream can bring.

    Args:
        project: The project.
        direct: The direct upstream.
        entries: The entries of the `spezi.lock` of the direct upstream.
        own: The full name of the project, or None for `repo` of `spezi.toml`.

    Returns:
        The repositories of `entries` without the project, without the direct upstream and
        without a repository of `spezi.toml`, sorted.
    """
    name = project.config.repo if own is None else own
    return tuple(
        sorted(r for r in entries if r not in (name, direct) and r not in project.config.upstream)
    )


def claims(project: Project) -> tuple[tuple[str, str, Locked | None], ...]:
    """Return each repository of a list `transitive` that gets a copy, with its direct upstream.

    Args:
        project: The project.

    Returns:
        The repository, the direct upstream and the entry in the `spezi.lock` of the direct
        upstream, or None when that file does not name it.
    """
    config = project.config
    return tuple(
        (name, direct, upstream_lock(project, direct).get(name))
        for direct, names in sorted(config.transitive.items())
        if direct in config.upstream
        for name in sorted(set(names))
        if name != config.repo and name not in config.upstream
    )


def conflicts(project: Project) -> Mapping[str, tuple[str, ...]]:
    """Return each transitive upstream that two direct upstreams name with different commits.

    Args:
        project: The project.

    Returns:
        The direct upstreams of each such repository, sorted.
    """
    found = claims(project)
    return {
        name: tuple(sorted(d for n, d, e in found if n == name and e is not None))
        for name in sorted({n for n, _, _ in found})
        if len({e.commit for n, _, e in found if n == name and e is not None}) > 1
    }


def missing(project: Project) -> tuple[tuple[str, str], ...]:
    """Return each repository of a list `transitive` that the copied `spezi.lock` does not name.

    Args:
        project: The project.

    Returns:
        The repository and its direct upstream.
    """
    return tuple((name, direct) for name, direct, entry in claims(project) if entry is None)


def union(includes: tuple[tuple[str, ...], ...]) -> tuple[str, ...]:
    """Return the union of folder lists. An empty list is all rules.

    Args:
        includes: The folder lists, without slashes.

    Returns:
        The folders without a folder below a different one, sorted; empty for all.
    """
    folders = {f for include in includes for f in include}
    return (
        ()
        if any(not include for include in includes)
        else tuple(sorted(f for f in folders if not any(f.startswith(f"{g}/") for g in folders)))
    )


def wanted(project: Project) -> Mapping[str, Wanted]:
    """Return the copy that each transitive upstream must be, without a conflict.

    Args:
        project: The project.

    Returns:
        The wanted copy of each repository that has no conflict and an entry in the copied
        `spezi.lock` of each of its direct upstreams.
    """
    found = claims(project)
    bad = {*conflicts(project), *(n for n, _ in missing(project))}
    entries = {
        name: tuple((d, e) for n, d, e in found if n == name and e is not None)
        for name in sorted({n for n, _, _ in found} - bad)
    }
    return {
        name: Wanted(
            pairs[0][1].commit,
            union(tuple(e.include for _, e in pairs)),
            tuple(sorted(d for d, _ in pairs)),
        )
        for name, pairs in entries.items()
        if pairs
    }


def kept(project: Project) -> frozenset[str]:
    """Return every repository whose copy and entry in `spezi.lock` stay.

    Args:
        project: The project.

    Returns:
        The repositories of `spezi.toml`, the wanted transitive upstreams and the transitive
        upstreams with a conflict.
    """
    return frozenset({*project.config.upstream, *wanted(project), *conflicts(project)})
