"""The layout of a project with specs: paths, settings, rule IDs and the parsed specs.

`specs/` holds the rules of the project in its kind folders, the index `specs/README.md`, the
copies of different repositories in `specs/.upstream/` and the templates in `specs/.templates/`
(spec 000004). The settings are in `spezi.toml` in the
root of the project (spec 000013).
"""

from __future__ import annotations

import os
import re
import tomllib
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import cast

import yaml

KIT_REPO = "github.com/frederikbeimgraben/spezi"
OLD_KIT_REPO = "github.com/frederikbeimgraben/specs"
CONFIG_NAME = "spezi.toml"
OLD_CONFIG_NAME = "specs.toml"

KINDS: Mapping[str, tuple[str, str]] = {
    "requirements/functional": ("F", "functional"),
    "requirements/non-functional": ("NF", "non-functional"),
    "protocols": ("P", "protocol"),
    "structures": ("U", "structure"),
    "style": ("S", "style"),
    "conventions": ("C", "convention"),
    "workflow": ("W", "workflow"),
    "agents": ("A", "agent"),
    "decisions": ("D", "decision"),
}
KINDS_BY_PREFIX: Mapping[str, str] = dict(KINDS.values())
FOLDER_BY_KIND: Mapping[str, str] = {kind: folder for folder, (_, kind) in KINDS.items()}
PREFIXES = "|".join(prefix for prefix, _ in KINDS.values())
STATUSES = frozenset({"draft", "approved", "replaced", "removed"})
IN_FORCE = frozenset({"draft", "approved"})
FORGES = ("github", "gitlab", "codeberg")
TOP_KEYS = frozenset(
    {
        "repo",
        "forge",
        "base_ref",
        "code_dirs",
        "code_suffixes",
        "max_elements",
        "features",
        "upstream",
        "own",
    }
)
REPO_KEYS = frozenset({"ref", "include", "transitive"})
ATTRIBUTES_NAME = ".gitattributes"
UPSTREAM_ATTRIBUTE = "specs/.upstream/** -text"
FEATURES = ("mcp", "agents", "claude", "ci", "skills", "flake", "envrc")
UPSTREAM = ".upstream"
TEMPLATES = ".templates"

FOLDER = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FILE_NAME = re.compile(r"^[0-9]{6}_[a-z0-9]+(-[a-z0-9]+)*\.md$")
REPO = r"[a-z0-9.-]+\.[a-z]+(?:/[A-Za-z0-9_.-]+){2,}"
TOP_FOLDERS = frozenset(folder.split("/")[0] for folder in KINDS)
NUMBER = r"[0-9]{6}"
LONG_LOCAL = rf"(?:{PREFIXES})/[a-z0-9-]+/[a-z0-9-]+/{NUMBER}"
SHORT = re.compile(rf"^(?:({REPO}):)?({NUMBER})$")
LONG = re.compile(rf"^(?:({REPO}):)?({LONG_LOCAL})$")

type Meta = Mapping[str, str | tuple[str, ...]]

_TEXTS: ContextVar[Mapping[Path, str]] = ContextVar("texts", default=MappingProxyType({}))


@contextmanager
def editing(texts: Mapping[Path, str]) -> Generator[None]:
    """Read the texts of an editor in place of the files on the disk in the block (spec 000088).

    Args:
        texts: The text of each file by absolute path.

    Yields:
        Nothing.
    """
    token = _TEXTS.set(MappingProxyType({p.resolve(): t for p, t in texts.items()}))
    try:
        yield
    finally:
        _TEXTS.reset(token)


def source(path: Path, errors: str = "strict") -> str:
    """Return the text of a file, or the text of the editor in a block of `editing`.

    Args:
        path: The file.
        errors: How to decode bytes that are no UTF-8.

    Returns:
        The text.
    """
    texts = _TEXTS.get()
    return (
        texts[path.resolve()]
        if path.resolve() in texts
        else path.read_text(encoding="utf-8", errors=errors)
    )


@dataclass(frozen=True, slots=True)
class Config:
    """The settings of `spezi.toml`.

    Attributes:
        base_ref: The base branch for the check of the numbers (spec 000013).
        forge: `github`, `gitlab` or `codeberg`.
        code_dirs: The folders with code that refers to rules (spec 000017).
        code_suffixes: The file types of the code.
        max_elements: The highest count of elements in one structure diagram.
        upstream: The `ref` of each repository with a copy below `specs/.upstream/` (spec 000048).
        include: The folders of each repository that the copy holds; empty for all (spec 000048).
        transitive: The transitive upstreams that the copy of each repository brings (spec 000092).
        repo: The full name of the project, or empty (spec 000092).
        features: The switch of each optional part of the kit (spec 000084).
        own: The folders below `specs/` that hold the rules of this repository only. A copy
            of the repository leaves them out (spec 000048).
    """

    base_ref: str = "origin/main"
    forge: str = "github"
    code_dirs: tuple[str, ...] = ()
    code_suffixes: frozenset[str] = frozenset(
        {".py", ".ts", ".js", ".go", ".rs", ".java", ".kt", ".nix", ".sh"}
    )
    max_elements: int = 25
    upstream: Mapping[str, str | None] = MappingProxyType({})
    include: Mapping[str, tuple[str, ...]] = MappingProxyType({})
    transitive: Mapping[str, tuple[str, ...]] = MappingProxyType({})
    repo: str = ""
    features: Mapping[str, bool] = MappingProxyType(dict.fromkeys(FEATURES, True))
    own: tuple[str, ...] = ()

    def on(self, feature: str) -> bool:
        """Return True when the part of the kit is switched on.

        Args:
            feature: The name of the switch in `[features]`.

        Returns:
            The switch. A missing switch is on.
        """
        return self.features.get(feature, True)


def hidden(rel: Path) -> bool:
    """Return True for a path below a folder whose name starts with a dot.

    Args:
        rel: The path relative to `specs/`.

    Returns:
        True for a path in `specs/.upstream/`, `specs/.templates/` or a different hidden folder.
    """
    return any(part.startswith(".") for part in rel.parts[:-1])


@dataclass(frozen=True, slots=True)
class Spec:
    """One parsed spec file.

    Attributes:
        path: The path of the file.
        base: The folder that holds the kind folders.
        full_id: The local part of the long form, for example `C/specs/format/000012`.
        meta: The keys of the front matter.
        keys: The keys of the front matter in their order.
        body: The Markdown text after the front matter.
        repo: Empty for a rule of the project, else `<host>/<group>/.../<repo>`.
    """

    path: Path
    base: Path
    full_id: str
    meta: Meta
    keys: tuple[str, ...]
    body: str
    repo: str = ""

    @property
    def rel(self) -> Path:
        """Return the path below the folder of the kind folders."""
        return self.path.relative_to(self.base)

    @property
    def number(self) -> str:
        """Return the six-digit number of the rule."""
        return self.path.name[:6]

    @property
    def prefix(self) -> str:
        """Return the kind letter of the rule ID."""
        return self.full_id.split("/", 1)[0]

    @property
    def short(self) -> str:
        """Return the short form of the ID (spec 000047)."""
        return f"{self.repo}:{self.number}" if self.repo else self.number

    @property
    def long(self) -> str:
        """Return the long form of the ID (spec 000047)."""
        return f"{self.repo}:{self.full_id}" if self.repo else self.full_id

    @property
    def status(self) -> str:
        """Return the status, or an empty string."""
        return str(self.meta.get("status", ""))

    @property
    def title(self) -> str:
        """Return the title, or an empty string."""
        return str(self.meta.get("title", ""))

    def entries(self, key: str) -> tuple[str, ...] | None:
        """Return the entries of a list key, an empty tuple for a key with one value, or None.

        Args:
            key: The key of the front matter.

        Returns:
            The entries, `()` when the key holds a single value, or None without the key.
        """
        value = self.meta.get(key)
        return value if isinstance(value, tuple) or value is None else ()


class FrontMatterError(Exception):
    """The front matter is no valid YAML of the form of 000009."""


def _value(node: yaml.Node) -> str | tuple[str, ...]:
    """Return the value of one key of the front matter.

    Args:
        node: The YAML node of the value.

    Returns:
        The text, or the entries of a list. A key without a value gets an empty tuple.

    Raises:
        FrontMatterError: The value is no text and no list of texts.
    """
    match node:
        case yaml.ScalarNode(value="", style=None):
            return ()
        case yaml.ScalarNode(value=str(text)):
            return text
        case yaml.SequenceNode(value=list(items)) if all(
            isinstance(i, yaml.ScalarNode) for i in items
        ):
            return tuple(str(cast("yaml.ScalarNode", i).value) for i in items)
        case _:
            raise FrontMatterError("a value must be a text or a list of texts")


def _pairs(block: str) -> tuple[tuple[str, str | tuple[str, ...]], ...]:
    """Return the keys and values of a front matter block, read as YAML (spec 000009).

    Args:
        block: The text between the two `---` lines.

    Returns:
        One pair of key and value per key, in the order of the block.

    Raises:
        FrontMatterError: The block is no valid YAML, or no mapping of texts and lists.
    """
    try:
        root = yaml.compose(block, Loader=yaml.BaseLoader)
    except yaml.YAMLError as error:
        raise FrontMatterError(f"no valid YAML: {' '.join(str(error).split())}") from error
    match root:
        case None:
            return ()
        case yaml.MappingNode(value=list(entries)):
            pairs = tuple(
                (str(cast("yaml.ScalarNode", k).value), _value(v))
                for k, v in cast("list[tuple[yaml.Node, yaml.Node]]", entries)
            )
            match len({k for k, _ in pairs}) == len(pairs):
                case True:
                    return pairs
                case False:
                    raise FrontMatterError("a key is there more than one time")
        case _:
            raise FrontMatterError("the block must be a mapping")


def parse_front_matter(text: str) -> tuple[Meta, tuple[str, ...], str] | None:
    """Return the keys, their order and the body of a spec text.

    Args:
        text: The whole text of a spec file.

    Returns:
        The keys and values, the order of the keys and the body, or None without front matter.

    Raises:
        FrontMatterError: The front matter is no valid YAML of the form of 000009.
    """
    end = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    pairs = _pairs(text[4:end]) if end >= 0 else ()
    return (dict(pairs), tuple(k for k, _ in pairs), text[end + 5 :]) if end >= 0 else None


def kind_of(rel: Path) -> tuple[str, str, Path] | None:
    """Return the ID prefix, the kind and the path below the kind folder.

    Args:
        rel: A path below the folder of the kind folders.

    Returns:
        The prefix, the kind and the rest of the path, or None outside every kind folder.
    """
    return next(
        (
            (prefix, kind, Path(*rel.parts[len(Path(folder).parts) :]))
            for folder, (prefix, kind) in KINDS.items()
            if rel.parts[: len(Path(folder).parts)] == Path(folder).parts
        ),
        None,
    )


def parse_spec(path: Path, base: Path, repo: str) -> tuple[Spec | None, tuple[str, ...]]:
    """Return the spec of one file below `base`, and the errors of its layout.

    Args:
        path: The spec file.
        base: The folder of the kind folders.
        repo: Empty for the project, else `<host>/<group>/.../<repo>`.

    Returns:
        The spec or None, and the errors of the file layout.
    """
    kind = kind_of(path.relative_to(base))
    if kind is None:
        return None, ("not below a kind folder (000051)",)
    prefix, _, below = kind
    if len(below.parts) != 3:
        return None, ("must be <area>/<topic>/<file> below the kind folder (000004)",)
    errors = (
        *(() if FILE_NAME.match(path.name) else ("file name breaks 000016",)),
        *(f"folder {f!r} breaks 000005" for f in below.parts[:2] if not FOLDER.match(f)),
    )
    try:
        parsed = parse_front_matter(source(path))
    except FrontMatterError as error:
        return None, (*errors, f"front matter: {error} (000009)")
    if parsed is None:
        return None, (*errors, "no front matter (000009)")
    meta, keys, body = parsed
    full_id = f"{prefix}/{below.parts[0]}/{below.parts[1]}/{path.name[:6]}"
    return Spec(path, base, full_id, meta, keys, body, repo), errors


def config_file(root: Path) -> Path:
    """Return `spezi.toml` of a project, or `specs.toml` before the migration of the name.

    Args:
        root: The root of the project.

    Returns:
        The file that exists, else `spezi.toml`.
    """
    return next(
        (root / n for n in (CONFIG_NAME, OLD_CONFIG_NAME) if (root / n).is_file()),
        root / CONFIG_NAME,
    )


def find_root(start: Path) -> Path:
    """Return the nearest folder from `start` upward that holds `spezi.toml`, else `start`.

    A folder with only `specs.toml` from before the migration of the name also counts.

    Args:
        start: The folder to start the search in.

    Returns:
        The root of the project.
    """
    here = start.resolve()
    return next((f for f in (here, *here.parents) if config_file(f).is_file()), here)


class ConfigError(Exception):
    """`spezi.toml` is no valid TOML, or a key has a wrong type."""


def _text(data: Mapping[str, object], key: str, default: str) -> str:
    """Return a string key of `spezi.toml`.

    Args:
        data: The table.
        key: The key.
        default: The value without the key.

    Returns:
        The value.

    Raises:
        ConfigError: The value is no string.
    """
    value = data.get(key, default)
    if not isinstance(value, str):
        raise ConfigError(f"spezi.toml: {key} must be a string")
    return value


def _forge(data: Mapping[str, object], default: str) -> str:
    """Return the key `forge` of `spezi.toml` (spec 000078).

    Args:
        data: The table.
        default: The value without the key.

    Returns:
        `github`, `gitlab` or `codeberg`.

    Raises:
        ConfigError: The value is not one of the forges.
    """
    match _text(data, "forge", default):
        case str(forge) if forge in FORGES:
            return forge
        case _:
            raise ConfigError(f"spezi.toml: forge must be {', '.join(FORGES)}")


def _texts(data: Mapping[str, object], key: str, default: tuple[str, ...]) -> tuple[str, ...]:
    """Return a key of `spezi.toml` that holds a list of strings.

    Args:
        data: The table.
        key: The key.
        default: The value without the key.

    Returns:
        The strings.

    Raises:
        ConfigError: The value is no list of strings.
    """
    value = data.get(key, list(default))
    items = cast("list[object]", value) if isinstance(value, list) else None
    if items is None or not all(isinstance(i, str) for i in items):
        raise ConfigError(f"spezi.toml: {key} must be a list of strings")
    return tuple(cast("list[str]", items))


def _number(data: Mapping[str, object], key: str, default: int) -> int:
    """Return a whole-number key of `spezi.toml`.

    Args:
        data: The table.
        key: The key.
        default: The value without the key.

    Returns:
        The number.

    Raises:
        ConfigError: The value is no whole number from 1.
    """
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigError(f"spezi.toml: {key} must be a whole number from 1")
    return value


def _upstream(data: Mapping[str, object]) -> Mapping[str, Mapping[str, object]]:
    """Return the tables below `upstream` of `spezi.toml`.

    Args:
        data: The whole file.

    Returns:
        The table of each repository.

    Raises:
        ConfigError: `upstream` or a repository entry is no table.
    """
    value = data.get("upstream", {})
    tables = cast("Mapping[str, object]", value) if isinstance(value, dict) else None
    if tables is None or not all(isinstance(t, dict) for t in tables.values()):
        raise ConfigError('spezi.toml: upstream must hold one table [upstream."<repo>"] each')
    found = cast("Mapping[str, Mapping[str, object]]", tables)
    match next(
        ((repo, key) for repo, table in found.items() for key in table if key not in REPO_KEYS),
        None,
    ):
        case (repo, key):
            raise ConfigError(f'spezi.toml: unknown key {key} in [upstream."{repo}"]')
        case None:
            return found


def _known(data: Mapping[str, object]) -> Mapping[str, object]:
    """Return the table of `spezi.toml` when each key of its top level is known (spec 000078).

    Args:
        data: The whole file.

    Returns:
        The same table.

    Raises:
        ConfigError: A key is unknown.
    """
    match next((key for key in data if key not in TOP_KEYS), None):
        case str(key):
            raise ConfigError(f"spezi.toml: unknown key {key}")
        case None:
            return data


def _features(data: Mapping[str, object]) -> Mapping[str, bool]:
    """Return the switches of `[features]` of `spezi.toml` (spec 000084).

    Args:
        data: The whole file.

    Returns:
        The switch of each part. A missing switch is on.

    Raises:
        ConfigError: `features` is no table, a key is unknown or no boolean, or `claude` is on
            and `agents` is off.
    """
    value = data.get("features", {})
    table = cast("Mapping[str, object]", value) if isinstance(value, dict) else None
    if table is None:
        raise ConfigError("spezi.toml: features must be a table [features]")
    unknown = sorted(set(table) - set(FEATURES))
    if unknown:
        raise ConfigError(
            f"spezi.toml: features has no switch {', '.join(unknown)};"
            f" the switches are {', '.join(FEATURES)}"
        )
    if not all(isinstance(v, bool) for v in table.values()):
        raise ConfigError("spezi.toml: each switch of features must be true or false")
    found = {name: cast("bool", table.get(name, True)) for name in FEATURES}
    if found["claude"] and not found["agents"]:
        raise ConfigError("spezi.toml: features.claude needs features.agents")
    return found


def _load_toml(path: Path) -> Mapping[str, object]:
    """Return the content of `spezi.toml`, or an empty table without the file.

    Args:
        path: The path of `spezi.toml`.

    Returns:
        The table.

    Raises:
        ConfigError: The file is no valid TOML.
    """
    try:
        return tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"spezi.toml: no valid TOML: {error}") from error


def read_config(path: Path) -> Config:
    """Read `spezi.toml`. A missing file or key gets the default.

    Args:
        path: The path of `spezi.toml`.

    Returns:
        The settings.
    """
    data = _known(_load_toml(path))
    default = Config()
    upstream = _upstream(data)
    return Config(
        base_ref=_text(data, "base_ref", default.base_ref),
        forge=_forge(data, default.forge),
        code_dirs=_texts(data, "code_dirs", default.code_dirs),
        code_suffixes=frozenset(
            _texts(data, "code_suffixes", tuple(sorted(default.code_suffixes)))
        ),
        max_elements=_number(data, "max_elements", default.max_elements),
        upstream={repo: _text(table, "ref", "") or None for repo, table in upstream.items()},
        include={repo: _texts(table, "include", ()) for repo, table in upstream.items()},
        transitive={repo: _texts(table, "transitive", ()) for repo, table in upstream.items()},
        repo=_text(data, "repo", default.repo),
        features=_features(data),
        own=_texts(data, "own", default.own),
    )


@dataclass(frozen=True, slots=True)
class Project:
    """A project with a `specs/` folder.

    Attributes:
        root: The root folder of the project.
        config: The settings of `spezi.toml`.
    """

    root: Path
    config: Config

    @classmethod
    def open(cls, root: Path | None = None) -> Project:
        """Read the project at `root`, or at the nearest folder above the current folder.

        Args:
            root: The root of the project, or None to search from the current folder.

        Returns:
            The project.
        """
        found = root.resolve() if root else find_root(Path.cwd())
        return cls(found, read_config(config_file(found)))

    @property
    def specs_dir(self) -> Path:
        """Return `specs/`."""
        return self.root / "specs"

    @property
    def upstream_dir(self) -> Path:
        """Return `specs/.upstream/`."""
        return self.specs_dir / UPSTREAM

    @property
    def templates_dir(self) -> Path:
        """Return `specs/.templates/`."""
        return self.specs_dir / TEMPLATES

    @property
    def index_path(self) -> Path:
        """Return `specs/README.md`, the index."""
        return self.specs_dir / "README.md"

    @property
    def config_path(self) -> Path:
        """Return `spezi.toml`, or `specs.toml` before the migration of the name."""
        return config_file(self.root)

    def copies(self) -> frozenset[str]:
        """Return the repositories that have a copy below `specs/.upstream/`.

        A copy is a folder whose path has the form of a repository and that holds a kind folder
        or `README.md`. A folder inside a copy is no copy.
        """
        roots = tuple(
            p.relative_to(self.upstream_dir).as_posix()
            for p in (sorted(self.upstream_dir.rglob("*")) if self.upstream_dir.is_dir() else ())
            if p.is_dir()
            and re.fullmatch(REPO, p.relative_to(self.upstream_dir).as_posix())
            and any(c.name in TOP_FOLDERS or c.name == "README.md" for c in p.iterdir())
        )
        return frozenset(r for r in roots if not any(r.startswith(f"{o}/") for o in roots))

    def needs_attribute(self) -> bool:
        """Return True when a copy exists and `.gitattributes` lacks the line of (spec 000048)."""
        path = self.root / ATTRIBUTES_NAME
        lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else ()
        return bool(self.copies()) and UPSTREAM_ATTRIBUTE not in (s.strip() for s in lines)

    def load(self) -> tuple[tuple[Spec, ...], tuple[str, ...]]:
        """Parse every rule of the project.

        Returns:
            The specs and the errors of the file layout.
        """
        if not self.specs_dir.is_dir():
            return (), ("specs/: the folder does not exist (000004)",)
        files = tuple(
            p
            for p in sorted(self.specs_dir.rglob("*"))
            if p.is_file() and not hidden(p.relative_to(self.specs_dir))
        )
        top = tuple(
            f"specs/{p.name}: specs/ holds only rules and README.md (000051)"
            for p in files
            if p.parent == self.specs_dir and p.name != "README.md"
        )
        parsed = tuple(
            (p, parse_spec(p, self.specs_dir, ""))
            for p in files
            if p.parent != self.specs_dir and p.suffix == ".md"
        )
        loose = tuple(
            f"specs/{p.relative_to(self.specs_dir).as_posix()}: not below a kind folder (000051)"
            for p in files
            if p.parent != self.specs_dir
            and p.suffix != ".md"
            and kind_of(p.relative_to(self.specs_dir)) is None
        )
        return (
            tuple(spec for _, (spec, _) in parsed if spec),
            (
                *top,
                *loose,
                *(
                    f"specs/{p.relative_to(self.specs_dir)}: {e}"
                    for p, (_, errors) in parsed
                    for e in errors
                ),
            ),
        )

    def load_upstream(self) -> tuple[Spec, ...]:
        """Parse every rule of the copies below `specs/.upstream/`. Skip a file that is no rule.

        `copy_errors` gives the errors of the skipped files.

        Returns:
            The specs of the copies.
        """
        return tuple(spec for _, (spec, errors) in self._parse_upstream() if spec and not errors)

    def copy_errors(self) -> tuple[str, ...]:
        """Return the errors of each rule of the copies that the program cannot read (spec 000065).

        Returns:
            One error per problem, as `<path>: <message>`.
        """
        return tuple(
            f"{path.relative_to(self.root).as_posix()}: {e}"
            for path, (_, errors) in self._parse_upstream()
            for e in errors
        )

    def _parse_upstream(self) -> tuple[tuple[Path, tuple[Spec | None, tuple[str, ...]]], ...]:
        """Parse each Markdown file below a folder of each copy.

        Returns:
            The path, the spec or None, and the errors of each file.
        """
        return tuple(
            (path, parse_spec(path, self.upstream_dir / repo, repo))
            for repo in sorted(self.copies())
            for path in sorted((self.upstream_dir / repo).rglob("*.md"))
            if path.relative_to(self.upstream_dir / repo).parent != Path()
        )

    def all_specs(self) -> tuple[Spec, ...]:
        """Return the rules of the project, then the rules of the copies."""
        return (*self.load()[0], *self.load_upstream())

    def find(self, ref: str) -> Spec | None:
        """Return the spec of a short or a long ID (spec 000047).

        Args:
            ref: The ID, for example `000012` or `github.com/o/r:C/specs/format/000012`.

        Returns:
            The spec, or None when no rule has this ID.
        """
        match = SHORT.match(ref) or LONG.match(ref)
        if match is None:
            return None
        repo, rest = match.group(1) or "", match.group(2)
        pool = self.load_upstream() if repo else self.load()[0]
        return next((s for s in pool if s.repo == repo and rest in (s.number, s.full_id)), None)


def kit_source() -> Path:
    """Return the folder of the kit that this program comes from."""
    env = os.environ.get("SPEZI_KIT_SOURCE")
    return Path(env) if env else Path(__file__).resolve().parents[2]


def kit_rev() -> str | None:
    """Return the commit of the kit that this program comes from, or None if it is not clean."""
    rev = os.environ.get("SPEZI_KIT_REV", "")
    return rev if re.fullmatch(r"[0-9a-f]{40}", rev) else None
