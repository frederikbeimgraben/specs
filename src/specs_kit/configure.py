"""`specs configure`: change the settings of `specs.toml` in a menu, or one key at a time (§000086).

The menu shows each key with its value, and each repository of `[upstream]`. A change stays in
memory until `save`. `save` writes `specs.toml` with its comments, and the command then runs
`specs install`. `discard` and Ctrl+C change no file.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import cast

import tomlkit
from tomlkit.items import Table

from specs_kit.ask import Ask, Cancelled
from specs_kit.changes import write_text
from specs_kit.kit import (
    KitError,
    checkout,
    choose_ref,
    code_dir_choices,
    default_ref,
    normal_include,
    repo_error,
    suffix_choices,
    tracked,
    two_levels,
)
from specs_kit.project import KIT_REPO, Config, Project, read_config
from specs_kit.settings import (
    FORGES,
    SIMPLE,
    SettingError,
    Value,
    current,
    drop_repo,
    edit_text,
    parse_value,
    plain,
    set_key,
)

SAVE = "save"
DISCARD = "discard"
ADD = "add a repository"


def set_value(project: Project, key: str, text: str) -> str:
    """Set one key of `specs.toml` from its plain form, without questions.

    Args:
        project: The project.
        key: The key, for example `features.mcp`.
        text: The plain form of the value, for example `false` or `src,lib`.

    Returns:
        The message, for example `features.mcp = false`.

    Raises:
        KitError: The key or the value is not valid.
    """
    try:
        value = parse_value(key, text)
        new = edit_text(
            project.config_path.read_text(encoding="utf-8"), lambda d: set_key(d, key, value)
        )
    except SettingError as error:
        raise KitError(str(error)) from error
    write_text(project.config_path, new)
    return f"{key} = {plain(value)}"


def _config_of(text: str) -> Config:
    """Return the settings of a text of `specs.toml`, or the defaults when it is not valid.

    Args:
        text: The text.

    Returns:
        The settings.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "specs.toml"
        path.write_text(text, encoding="utf-8")
        try:
            return read_config(path)
        except Exception:
            return Config()


def _repos(document: tomlkit.TOMLDocument) -> dict[str, Table]:
    """Return the table of each repository of `[upstream]`.

    Args:
        document: The document of `specs.toml`.

    Returns:
        The tables.
    """
    upstream = document.get("upstream")
    return (
        {k: v for k, v in upstream.items() if isinstance(v, Table)}
        if isinstance(upstream, Table)
        else {}
    )


def _set_repo(
    document: tomlkit.TOMLDocument, repo: str, ref: str, include: tuple[str, ...]
) -> None:
    """Set `ref` and `include` of one repository. Add its table when it is missing.

    Args:
        document: The document of `specs.toml`.
        repo: The repository.
        ref: The ref.
        include: The folders of the copy, or empty for all.
    """
    if not isinstance(document.get("upstream"), Table):
        document["upstream"] = tomlkit.table(is_super_table=True)
    upstream = cast("Table", document["upstream"])
    table = cast("Table", upstream[repo]) if repo in upstream else tomlkit.table()
    table["ref"] = ref
    if include:
        table["include"] = [f"{f}/" for f in include]
    elif "include" in table:
        del table["include"]
    if repo not in upstream:
        upstream[repo] = table


def _repo_line(repo: str, table: Table) -> str:
    """Return the menu line of one repository.

    Args:
        repo: The repository.
        table: Its table.

    Returns:
        The line.
    """
    include = cast("list[str]", table.get("include", []))
    return f"upstream {repo}: ref = {table.get('ref', '')}" + (
        f", include = {','.join(include)}" if include else ""
    )


def _ask_value(root: Path, key: str, now: Value, config: Config, ask: Ask) -> Value:
    """Ask for the new value of one key.

    Args:
        root: The root of the project.
        key: The key.
        now: The value now.
        config: The settings now.
        ask: The questions.

    Returns:
        The new value.
    """
    files = tracked(root)
    match SIMPLE[key], key:
        case "switch", _:
            return not now
        case _, "forge":
            return ask.select("Forge?", FORGES, str(now))
        case _, "code_dirs":
            tops = dict(code_dir_choices(files, config.code_suffixes))
            names = sorted({*tops, *config.code_dirs})
            return ask.checkbox(
                "Folders with code?", tuple((n, n in config.code_dirs) for n in names)
            )
        case _, "code_suffixes":
            found = dict(suffix_choices(files, config.code_dirs, config.code_suffixes))
            return ask.checkbox(
                "File types of the code?", tuple((s, s in config.code_suffixes) for s in found)
            )
        case _:
            return parse_value(key, ask.text(f"{key}?", plain(now), lambda t: _error(key, t)))


def _error(key: str, text: str) -> str | None:
    """Return why a text is no value of a key, or None.

    Args:
        key: The key.
        text: The text.

    Returns:
        The error, or None.
    """
    try:
        parse_value(key, text)
    except SettingError as error:
        return str(error)
    return None


def _ask_include(repo: str, ref: str, now: tuple[str, ...], ask: Ask) -> tuple[str, ...]:
    """Ask for the folders of a copy, as `specs add` does.

    Args:
        repo: The repository.
        ref: The ref.
        now: The folders now, or empty for all.
        ask: The questions.

    Returns:
        The folders, or empty for all.
    """
    with checkout(repo, ref) as source:
        folders = two_levels(source / "specs")
    picked = ask.checkbox(
        f"Folders of {repo} to copy?",
        tuple((f, not now or any(f == n or f.startswith(f"{n}/") for n in now)) for f in folders),
    )
    return () if set(picked) == set(folders) else normal_include(picked)


def _edit_repo(document: tomlkit.TOMLDocument, repo: str, ask: Ask) -> None:
    """Ask what to change for one repository: the ref, the folders, or remove it.

    Args:
        document: The document of `specs.toml`.
        repo: The repository.
        ask: The questions.
    """
    table = _repos(document)[repo]
    ref = str(table.get("ref", ""))
    include = tuple(f.strip("/") for f in cast("list[str]", table.get("include", [])))
    actions = ("ref", "include", *(("remove",) if repo != KIT_REPO else ()), "back")
    match ask.select(f"{repo}: what to change?", actions, "back"):
        case "ref":
            _set_repo(document, repo, choose_ref(ask, repo, ref), include)
        case "include":
            _set_repo(document, repo, ref, _ask_include(repo, ref, include, ask))
        case "remove":
            drop_repo(document, repo)
        case _:
            pass


def _add_repo(document: tomlkit.TOMLDocument, ask: Ask) -> None:
    """Ask for a new repository with the questions of `specs add`.

    Args:
        document: The document of `specs.toml`.
        ask: The questions.
    """
    repo = ask.text("Repository (<host>/<group>/.../<repo>)?", "", repo_error)
    if repo in _repos(document):
        ask.show(f"{repo} is in specs.toml already")
        return
    ref = choose_ref(ask, repo, default_ref(repo))
    _set_repo(document, repo, ref, _ask_include(repo, ref, (), ask))


def configure(project: Project, ask: Ask) -> bool:
    """Show the menu of `specs configure` until `save` or `discard` (§000086).

    Args:
        project: The project.
        ask: The questions.

    Returns:
        True when the command wrote `specs.toml`.

    Raises:
        Cancelled: The user discarded the changes.
    """
    original = project.config_path.read_text(encoding="utf-8")
    document = tomlkit.parse(original)
    while True:
        text = tomlkit.dumps(document)
        config = _config_of(text)
        keys = {f"{k} = {plain(current(config, k))}": k for k in SIMPLE}
        repos = {_repo_line(r, t): r for r, t in _repos(document).items()}
        picked = ask.select(
            "specs.toml: what to change?", (*keys, *repos, ADD, SAVE, DISCARD), SAVE
        )
        match picked:
            case "save":
                try:
                    new = edit_text(text, lambda _: None)
                except SettingError as error:
                    ask.show(str(error))
                    continue
                if new != original:
                    write_text(project.config_path, new)
                return new != original
            case "discard":
                if text == original or ask.confirm("Discard the changes?", True):
                    raise Cancelled("discarded; no file changed")
            case "add a repository":
                _add_repo(document, ask)
            case line if line in repos:
                _edit_repo(document, repos[line], ask)
            case line:
                key = keys[line]
                set_key(
                    document, key, _ask_value(project.root, key, current(config, key), config, ask)
                )
