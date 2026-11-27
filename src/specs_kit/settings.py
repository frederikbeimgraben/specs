"""Change the values of `specs.toml` and keep its comments and its order (§000086).

`specs configure` and the questions of `init` and `add` change `specs.toml` with tomlkit, so
that only the values change.
"""

from __future__ import annotations

import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import cast

import tomlkit
from tomlkit.items import Table

from specs_kit.changes import write_text
from specs_kit.project import FEATURES, Config, ConfigError, read_config

type Value = str | int | bool | tuple[str, ...]

SIMPLE: Mapping[str, str] = {
    "forge": "text",
    "base_ref": "text",
    "code_dirs": "list",
    "code_suffixes": "list",
    "max_elements": "number",
    **{f"features.{name}": "switch" for name in FEATURES},
}
FORGES = ("github", "gitlab", "codeberg")


class SettingError(Exception):
    """A key or a value for `specs.toml` is not valid."""


def parse_value(key: str, text: str) -> Value:
    """Return the value of a key from its plain form, for example `false` or `src,lib`.

    Args:
        key: The key, for example `features.mcp`.
        text: The plain form of the value.

    Returns:
        The value with the type of the key.

    Raises:
        SettingError: The key is unknown, or the text has the wrong form.
    """
    match SIMPLE.get(key), text.strip():
        case None, _:
            raise SettingError(
                f"specs configure has no key {key!r}; the keys are {', '.join(SIMPLE)}"
            )
        case "switch", "true" | "false" as word:
            return word == "true"
        case "switch", _:
            raise SettingError(f"{key} must be true or false")
        case "number", word if word.isdigit() and int(word) >= 1:
            return int(word)
        case "number", _:
            raise SettingError(f"{key} must be a whole number from 1")
        case "list", word:
            return tuple(part.strip() for part in word.split(",") if part.strip())
        case "text", "":
            raise SettingError(f"{key} must not be empty")
        case "text", word if key == "forge" and word not in FORGES:
            raise SettingError(f"forge must be {', '.join(FORGES)}")
        case _, word:
            return word


def plain(value: Value) -> str:
    """Return the plain form of a value.

    Args:
        value: The value.

    Returns:
        The text, with commas between the entries of a list.
    """
    match value:
        case bool():
            return "true" if value else "false"
        case tuple():
            return ",".join(value)
        case _:
            return str(value)


def current(config: Config, key: str) -> Value:
    """Return the value of a key in the settings.

    Args:
        config: The settings.
        key: The key.

    Returns:
        The value.
    """
    match key.partition("."):
        case "features", ".", name:
            return config.on(name)
        case "code_suffixes", _, _:
            return tuple(sorted(config.code_suffixes))
        case "code_dirs", _, _:
            return config.code_dirs
        case "max_elements", _, _:
            return config.max_elements
        case "forge", _, _:
            return config.forge
        case _:
            return config.base_ref


def edit_text(text: str, change: Callable[[tomlkit.TOMLDocument], None]) -> str:
    """Return the text of `specs.toml` after a change, with its comments and order.

    Args:
        text: The text of `specs.toml`.
        change: Changes the document in place.

    Returns:
        The new text.

    Raises:
        SettingError: The new text breaks a rule of `specs.toml`.
    """
    document = tomlkit.parse(text)
    change(document)
    new = tomlkit.dumps(document)
    with_trailing = new if new.endswith("\n") else f"{new}\n"
    _validate(with_trailing)
    return with_trailing


def _validate(text: str) -> None:
    """Fail when a text of `specs.toml` breaks a rule of `specs.toml`.

    Args:
        text: The text.

    Raises:
        SettingError: The text breaks a rule.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "specs.toml"
        path.write_text(text, encoding="utf-8")
        try:
            read_config(path)
        except ConfigError as error:
            raise SettingError(str(error)) from error


def set_key(document: tomlkit.TOMLDocument, key: str, value: Value) -> None:
    """Set one key in a document of `specs.toml`.

    Args:
        document: The document.
        key: The key, for example `features.mcp`.
        value: The value.
    """
    stored = list(value) if isinstance(value, tuple) else value
    match key.partition("."):
        case table, ".", name:
            existing = document.get(table)
            target = existing if isinstance(existing, Table) else tomlkit.table()
            target[name] = stored
            if not isinstance(existing, Table):
                document[table] = target
        case _:
            document[key] = stored


def set_keys(document: tomlkit.TOMLDocument, values: tuple[tuple[str, Value], ...]) -> None:
    """Set several keys in a document of `specs.toml`.

    Args:
        document: The document.
        values: Each key and its value.
    """
    for key, value in values:
        set_key(document, key, value)


def drop_repo(document: tomlkit.TOMLDocument, repo: str) -> None:
    """Remove the table of one repository from a document of `specs.toml`.

    Args:
        document: The document.
        repo: The repository.
    """
    upstream = cast("Table | None", document.get("upstream"))
    if upstream is not None and repo in upstream:
        del upstream[repo]


def write_settings(root: Path, change: Callable[[tomlkit.TOMLDocument], None]) -> None:
    """Change `specs.toml` of a project in place.

    Args:
        root: The root of the project.
        change: Changes the document in place.
    """
    path = root / "specs.toml"
    write_text(path, edit_text(path.read_text(encoding="utf-8"), change))
