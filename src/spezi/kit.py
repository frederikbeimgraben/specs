"""Install the kit in a project, and update the copies of different repositories.

`init` replaces the old install script. `update` and `add` replace a copy below
`specs/.upstream/` with the `specs/` folder of its repository at one commit (§000048).
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import tempfile
import tomllib
from collections.abc import Callable, Generator, Mapping
from contextlib import ExitStack, contextmanager, suppress
from dataclasses import dataclass, field
from functools import cache
from importlib import resources
from pathlib import Path
from typing import cast

from spezi.ask import Ask, Cancelled, Proposals, Stop
from spezi.changes import remove_tree, replace_tree, write_text
from spezi.lock import LOCK_NAME, Locked, drop_locked, read_lock, set_locked, tree_hash
from spezi.migrations import History, contains, migrate_copy, migrate_project
from spezi.project import (
    CONFIG_NAME,
    FEATURES,
    FOLDER,
    KIT_REPO,
    OLD_KIT_REPO,
    REPO,
    TEMPLATES,
    Config,
    Project,
    config_file,
    kit_rev,
    kit_source,
    read_config,
)
from spezi.review import broken_references, change_lines, rule_changes, rules_in
from spezi.settings import (
    FORGES,
    SettingError,
    Value,
    drop_repo,
    set_keys,
    set_repo,
    write_settings,
)
from spezi.transitive import kept, offers, wanted


class KitError(Exception):
    """A command of the kit cannot finish."""


CI_FILES: Mapping[str, tuple[str, str]] = {
    "github": ("github-workflow.yml", ".github/workflows/spezi.yml"),
    "gitlab": ("gitlab-ci.yml", ".gitlab/ci/spezi.yml"),
    "codeberg": ("codeberg-workflow.yml", ".forgejo/workflows/spezi.yml"),
}
GITLAB_ROOT = ".gitlab-ci.yml"
MCP_NAME = "spezi"
GITLAB_INCLUDE = "  - local: .gitlab/ci/spezi.yml"
VERSION = re.compile(r"^v?[0-9]+(?:\.[0-9]+)*$")


def package_data(name: str) -> str:
    """Return the text of a file of the package data.

    Args:
        name: The file name below `spezi/data/`.

    Returns:
        The text.
    """
    return resources.files("spezi").joinpath("data", name).read_text(encoding="utf-8")


REMOTE_HOST = re.compile(r"^(?:[a-z][a-z0-9+.-]*://)?(?:[^@/]+@)?([^/:]+)")


def run_command(*args: str, cwd: Path | None = None) -> str:
    """Run a command and return its output.

    Args:
        *args: The command and its arguments.
        cwd: The folder to run the command in.

    Returns:
        The output.

    Raises:
        KitError: The command failed.
    """
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        raise KitError(
            f"{' '.join(args)} failed: {getattr(error, 'stderr', '') or error}"
        ) from error


@contextmanager
def kit_history() -> Generator[Path]:
    """Fetch the branches and tags of the kit, without file contents, into a temporary folder.

    Yields:
        The folder of the bare clone.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_command("git", "init", "-q", "--bare", tmp)
        run_command(
            "git",
            "-C",
            tmp,
            "fetch",
            "-q",
            "--filter=blob:none",
            "--end-of-options",
            f"https://{KIT_REPO}.git",
            "+refs/heads/*:refs/heads/*",
            "+refs/tags/*:refs/tags/*",
        )
        yield Path(tmp)


@contextmanager
def lazy_history() -> Generator[History]:
    """Give a function that fetches the history of the kit at its first call only.

    Yields:
        The function. It returns the folder of the clone.
    """
    with ExitStack() as stack:
        yield cache(lambda: stack.enter_context(kit_history()))


def upstream_kit_ref(source: Path) -> str | None:
    """Return the kit commit or ref of a checkout of a different repository.

    Args:
        source: The root of the checkout.

    A repository that a kit from before the new name installed has `specs.lock` and
    `specs.toml` with the old name of the kit.

    Returns:
        The commit of the kit in `spezi.lock`, else the kit ref in `spezi.toml`, else None.
    """
    lock = read_lock(source)
    locked = lock.get(KIT_REPO) or lock.get(OLD_KIT_REPO)
    path = config_file(source)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except tomllib.TOMLDecodeError:
        data = {}
    tables = data.get("upstream", {})
    table = tables.get(KIT_REPO) or tables.get(OLD_KIT_REPO) or {}
    match locked, table.get("ref"):
        case Locked(commit=commit), _:
            return commit
        case None, str() as ref:
            return ref
        case _:
            return None


def version(name: str) -> tuple[int, ...] | None:
    """Return the numbers of a version tag such as `1.2.3` or `v1.2.3`.

    Args:
        name: The name of the tag.

    Returns:
        The numbers, or None for a name without a version.
    """
    return tuple(int(p) for p in name.removeprefix("v").split(".")) if VERSION.match(name) else None


def version_tags(repo: str) -> tuple[str, ...]:
    """Return the version tags of a repository, the highest version first.

    Args:
        repo: The repository as `<host>/<group>/.../<repo>`.

    Returns:
        The names of the tags.
    """
    tags = run_command("git", "ls-remote", "--tags", "--refs", f"https://{repo}.git")
    names = (line.partition("refs/tags/")[2] for line in tags.splitlines())
    return tuple(
        sorted((n for n in names if VERSION.match(n)), key=lambda n: version(n) or (), reverse=True)
    )


def default_branch(repo: str) -> str | None:
    """Return the default branch of a repository.

    Args:
        repo: The repository as `<host>/<group>/.../<repo>`.

    Returns:
        The name of the branch, or None.
    """
    head = run_command("git", "ls-remote", "--symref", f"https://{repo}.git", "HEAD")
    return next(
        (
            line.split()[1].removeprefix("refs/heads/")
            for line in head.splitlines()
            if line.startswith("ref: ")
        ),
        None,
    )


def default_ref(repo: str) -> str:
    """Return the tag with the highest version of a repository, else its default branch.

    A tag has a version when it has the form `1.2.3` or `v1.2.3` with one or more numbers.

    Args:
        repo: The repository as `<host>/<group>/.../<repo>`.

    Returns:
        The tag or the name of the branch.

    Raises:
        KitError: git cannot read the repository, or it has no default branch.
    """
    match version_tags(repo), default_branch(repo):
        case (first, *_), _:
            return first
        case (), str() as branch:
            return branch
        case _:
            raise KitError(f"{repo} has no default branch")


OTHER = "other ref..."


def choose_ref(ask: Ask, repo: str, proposal: str) -> str:
    """Ask for the ref of a repository: one of the 10 highest tags, the branch or a typed ref.

    Args:
        ask: The questions.
        repo: The repository.
        proposal: The ref that the question proposes.

    Returns:
        The ref.
    """
    tags = version_tags(repo)[:10]
    branch = default_branch(repo)
    choices = (*tags, *((branch,) if branch and branch not in tags else ()), OTHER)
    picked = ask.select(f"Ref of {repo}?", choices, proposal)
    return (
        ask.text(f"Tag, branch or commit of {repo}?", "", lambda t: None if t else "type a ref")
        if picked == OTHER
        else picked
    )


def newer_tag(repo: str, ref: str) -> bool:
    """Return True when a repository has a tag with a higher version than `ref`.

    Args:
        repo: The repository.
        ref: The ref of `spezi.toml`.

    Returns:
        False for a ref without a version.
    """
    now = version(ref)
    return now is not None and any((version(t) or ()) > now for t in version_tags(repo))


@contextmanager
def checkout(repo: str, ref: str) -> Generator[Path]:
    """Check out a repository at one ref into a temporary folder.

    Args:
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag or the commit.

    Yields:
        The folder of the checkout.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_command("git", "init", "-q", tmp)
        run_command(
            "git",
            "-C",
            tmp,
            "fetch",
            "-q",
            "--depth",
            "1",
            "--end-of-options",
            f"https://{repo}.git",
            ref,
        )
        run_command("git", "-C", tmp, "checkout", "-q", "FETCH_HEAD")
        yield Path(tmp)


def normal_include(include: tuple[str, ...]) -> tuple[str, ...]:
    """Return the folders of `include` without a slash at the ends and without nested ones, sorted.

    Args:
        include: The folders, for example `style/python/`.

    Returns:
        The folders, for example `style/python`.

    Raises:
        KitError: A folder is not a path of kebab-case names.
    """
    stripped = {f.strip("/") for f in include}
    folders = tuple(sorted(f for f in stripped if not any(f.startswith(f"{g}/") for g in stripped)))
    bad = tuple(f for f in folders if not all(FOLDER.match(p) for p in f.split("/")))
    if bad:
        raise KitError(f"include {', '.join(map(repr, bad))} is not a path of kebab-case names")
    return folders


def own_folders(source: Path, include: tuple[str, ...]) -> tuple[str, ...]:
    """Return the folders of `own` of a repository that its copy leaves out (§000048).

    A folder of `own` that `include` names, or that holds a folder of `include`, is copied.

    Args:
        source: The root of a checkout of the repository.
        include: The folders below `specs/` to copy, or empty for all.

    Returns:
        The folders below `specs/`, without slashes at the ends.
    """
    named = tuple(i.strip("/") for i in include)
    return tuple(
        folder
        for folder in (o.strip("/") for o in read_config(source / CONFIG_NAME).own)
        if not any(n == folder or n.startswith(f"{folder}/") for n in named)
    )


def copy_rules(
    source: Path,
    project: Project,
    repo: str,
    include: tuple[str, ...] = (),
    *,
    direct: bool = True,
) -> None:
    """Replace the copy of one repository with its `specs/` folder or the folders of `include`.

    The copy holds `specs/README.md` only without `include` (§000048). The copy of a direct
    upstream also holds the `spezi.lock` of the repository (§000092).

    Args:
        source: The root of a checkout of the repository.
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        include: The folders below `specs/` to copy, or empty for all.
        direct: True for a direct upstream, False for a transitive upstream.

    Raises:
        KitError: The checkout has no `specs/` folder, or a folder of `include`.
    """
    missing = tuple(f for f in include if not (source / "specs" / f).is_dir())
    if not (source / "specs").is_dir():
        raise KitError(f"{repo} has no specs/ folder")
    if missing:
        raise KitError(f"{repo} has no folder specs/{', specs/'.join(missing)}")
    replace_tree(
        source / "specs", project.upstream_dir / repo, include, own_folders(source, include)
    )
    if direct and (source / LOCK_NAME).is_file():
        write_text(
            project.upstream_dir / repo / LOCK_NAME,
            (source / LOCK_NAME).read_text(encoding="utf-8"),
        )


def write_repo(
    project: Project,
    repo: str,
    ref: str,
    include: tuple[str, ...] | None = None,
    transitive: tuple[str, ...] | None = None,
) -> None:
    """Set `ref`, and `include` and `transitive` when given, of one repository in `spezi.toml`.

    The table is added when it is missing. The other lines of `spezi.toml` stay.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag, the branch or the commit.
        include: The folders of the copy, empty for all, or None to keep `include` as it is.
        transitive: The transitive upstreams to copy (§000092), or None to keep them.

    Raises:
        KitError: The new `spezi.toml` breaks a rule of 000078.
    """
    try:
        write_settings(project.root, lambda doc: set_repo(doc, repo, ref, include, transitive))
    except SettingError as error:
        raise KitError(str(error)) from error


def skills(source: Path) -> tuple[Path, ...]:
    """Return the skill folders of the kit.

    Args:
        source: The root of the kit.

    Returns:
        The folders `.claude/skills/spezi-*`.
    """
    folder = source / ".claude" / "skills"
    return tuple(sorted(p for p in folder.glob("spezi-*") if p.is_dir())) if folder.is_dir() else ()


def read_mcp(path: Path) -> dict[str, object]:
    """Read `.mcp.json`. A missing file gives an empty object.

    Args:
        path: The file `.mcp.json`.

    Returns:
        The object of the file.

    Raises:
        KitError: The file is no valid JSON, is not an object, or `mcpServers` is not an object.
    """
    try:
        data: object = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except json.JSONDecodeError as error:
        raise KitError(f".mcp.json: no valid JSON: {error}") from error
    match data:
        case dict() if isinstance(data.get("mcpServers", {}), dict):
            return cast("dict[str, object]", data)
        case dict():
            raise KitError(".mcp.json: mcpServers is not an object")
        case _:
            raise KitError(".mcp.json: the file is not a JSON object")


def write_mcp(project: Project, ref: str) -> None:
    """Write the server `spezi` into `.mcp.json`. Keep the other servers.

    Args:
        project: The project.
        ref: The commit of the kit.
    """
    path = project.root / ".mcp.json"
    data = read_mcp(path)
    servers = cast("dict[str, object]", data.get("mcpServers", {}))
    server = {
        "command": "nix",
        "args": ["run", f"github:{KIT_REPO.split('/', 1)[1]}/{ref}", "--", "mcp"],
    }
    write_text(
        path, json.dumps({**data, "mcpServers": {**servers, MCP_NAME: server}}, indent=2) + "\n"
    )


def gitlab_root_text(root: Path) -> str | None:
    """Return the new text of `.gitlab-ci.yml` with the include of the kit job.

    Args:
        root: The root of the project.

    Returns:
        The new text, or None when the file includes the job already.

    Raises:
        KitError: The file has an `include` that is not a block list.
    """
    path = root / GITLAB_ROOT
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    lines = text.splitlines()
    match (
        GITLAB_INCLUDE.strip("- ") in text,
        "include:" in lines,
        any(ln.startswith("include") for ln in lines),
    ):
        case (True, _, _):
            return None
        case (False, True, _):
            at = lines.index("include:") + 1
            return "\n".join((*lines[:at], GITLAB_INCLUDE, *lines[at:])) + "\n"
        case (False, False, True):
            raise KitError(f"{GITLAB_ROOT}: add {GITLAB_INCLUDE.strip()} to include by hand")
        case (False, False, False):
            return f"{text.rstrip()}\n\ninclude:\n{GITLAB_INCLUDE}\n".lstrip()


def check_forge(root: Path, forge: str, ci: bool) -> None:
    """Fail before a change when the kit cannot write its CI file for a forge.

    With the switch `ci` off, the kit does not read `.gitlab-ci.yml` (§000084).

    Args:
        root: The root of the project.
        forge: The forge.
        ci: The switch `ci` of `[features]`.

    Raises:
        KitError: The forge is unknown, or `.gitlab-ci.yml` cannot get the include.
    """
    if forge not in CI_FILES:
        raise KitError(f"spezi.toml: forge {forge!r} must be github, gitlab or codeberg")
    if forge == "gitlab" and ci:
        gitlab_root_text(root)


def templates(source: Path) -> Path:
    """Return the templates folder of a checkout of the kit, in the new or the old place.

    Args:
        source: The checkout of the kit.

    Returns:
        `specs/.templates/`, or `.specs/templates/` of a kit before the move.
    """
    new = source / "specs" / TEMPLATES
    return new if new.is_dir() else source / ".specs" / "templates"


def install_kit_files(source: Path, project: Project, ref: str) -> None:
    """Replace the templates, and the skills, the CI file and the MCP server that are on.

    The switches `skills`, `ci` and `mcp` of `[features]` choose the parts (§000084).

    Args:
        source: The root of the kit at `ref`.
        project: The project.
        ref: The commit of the kit.

    Raises:
        KitError: The forge in `spezi.toml` is unknown.
    """
    forge = project.config.forge
    check_forge(project.root, forge, project.config.on("ci"))
    data_name, target = CI_FILES[forge]
    config = project.config
    root_text = gitlab_root_text(project.root) if forge == "gitlab" and config.on("ci") else None
    replace_tree(templates(source), project.templates_dir)
    for skill in skills(source) if config.on("skills") else ():
        replace_tree(skill, project.root / ".claude" / "skills" / skill.name)
    branch = config.base_ref.removeprefix("origin/")
    if config.on("ci"):
        write_text(
            project.root / target,
            package_data(data_name).replace("{ref}", ref).replace("{branch}", branch),
        )
    if root_text is not None:
        write_text(project.root / GITLAB_ROOT, root_text)
    if config.on("mcp"):
        write_mcp(project, ref)


def detect_forge(root: Path) -> str:
    """Return the forge of the host of `git remote origin`.

    Args:
        root: The root of the project.

    Returns:
        `github`, `gitlab` or `codeberg`.

    Raises:
        KitError: The remote names neither GitHub, GitLab nor Codeberg.
    """
    try:
        url = run_command("git", "remote", "get-url", "origin", cwd=root)
    except KitError:
        url = ""
    host = next(iter(REMOTE_HOST.findall(url)), "").lower()
    match ("gitlab" in host, "github" in host, "codeberg" in host):
        case (True, _, _):
            return "gitlab"
        case (False, True, _):
            return "github"
        case (False, False, True):
            return "codeberg"
        case (False, False, False):
            raise KitError(
                "cannot find the forge from git remote origin; pass --forge github|gitlab|codeberg"
            )


def _check_repo(repo: str) -> None:
    """Fail for a repository name that is not `<host>/<group>/.../<repo>`.

    Args:
        repo: The repository name.

    Raises:
        KitError: The name has a different form.
    """
    if not re.fullmatch(REPO, repo):
        raise KitError(f"{repo!r} is not <host>/<group>/.../<repo>")


def own_ref(project: Project) -> str | None:
    """Return the kit commit of the project in `spezi.lock`, else the kit ref in `spezi.toml`.

    Args:
        project: The project.

    Before the migration of the name, the kit entry has the old name of the kit.

    Returns:
        The commit or the ref, or None when the project has no kit entry.
    """
    lock = read_lock(project.root)
    return next(
        (
            ref
            for name in (KIT_REPO, OLD_KIT_REPO)
            for ref in (
                (lock[name].commit if name in lock else None),
                project.config.upstream.get(name),
            )
            if ref
        ),
        None,
    )


def check_program(history: History, own: str | None) -> None:
    """Fail when this program is an older commit of the kit than the kit of the project.

    Args:
        history: Returns a clone of the kit with its history.
        own: The kit commit or ref of the project, or None.

    Raises:
        KitError: The commit of this program is an ancestor of `own` and not the same commit.
    """
    rev = kit_rev()
    if (
        rev
        and own
        and rev != own
        and contains(history(), rev, own)
        and not contains(history(), own, rev)
    ):
        raise KitError(
            f"this program is the kit at {rev}, older than the kit at {own} in spezi.lock;"
            " load the new program with nix develop first"
        )


@dataclass(frozen=True, slots=True)
class Plan:
    """What the questions before a copy chose (§000085).

    Attributes:
        include: The folders below `specs/` to copy, or empty for all.
        keep: The text of each changed template or skill that stays as it is.
        transitive: The transitive upstreams to copy (§000092), or None to keep the list.
    """

    include: tuple[str, ...]
    keep: Mapping[Path, str] = field(default_factory=dict)
    transitive: tuple[str, ...] | None = None


type Review = Callable[[Path, str], Plan]


def fetch_copy(
    project: Project,
    repo: str,
    ref: str,
    include: tuple[str, ...],
    history: History,
    own: str | None,
    *,
    kit_files: bool,
    review: Review | None = None,
    direct: bool = True,
) -> tuple[str, tuple[str, ...], Plan]:
    """Replace the copy of one repository with its rules at one ref, and migrate the copy.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag, the branch or the commit to fetch.
        include: The folders below `specs/` to copy, or empty for all.
        history: Returns a clone of the kit with its history.
        own: The kit commit or ref of the project, or None.
        kit_files: True to also replace the templates, the skills, the CI file and the MCP
            server entry from the kit.
        review: Asks the questions before the copy, with the checkout and its commit, or None.
        direct: True for a direct upstream, False for a transitive upstream (§000092).

    Returns:
        The commit of the copy, the descriptions of the migrations of the copy that ran, and
        the plan of the questions.

    Raises:
        KitError: The kit is too old, or the repository uses a newer kit than the project.
    """
    with checkout(repo, ref) as source:
        commit = run_command("git", "-C", str(source), "rev-parse", "HEAD").strip()
        if repo == KIT_REPO and not templates(source).is_dir():
            raise KitError(f"the kit at {commit} has no templates; it is too old")
        if repo == KIT_REPO:
            check_forge(project.root, project.config.forge, project.config.on("ci"))
        theirs = None if repo == KIT_REPO else upstream_kit_ref(source)
        if theirs and own and theirs != own and not contains(history(), theirs, own):
            raise KitError(
                f"{repo} at {commit} needs the kit at {theirs} or later; run spezi update first"
            )
        plan = review(source, commit) if review else Plan(include)
        copy_rules(source, project, repo, plan.include, direct=direct)
        ran = migrate_copy(
            history, project.upstream_dir / repo, commit if repo == KIT_REPO else theirs
        )
        if kit_files:
            install_kit_files(source, project, commit)
        for path, text in plan.keep.items():
            write_text(path, text)
    return commit, ran, plan


def _lock(project: Project, repo: str, ref: str, commit: str, include: tuple[str, ...]) -> None:
    """Write the entry of one repository to `spezi.lock` with the hash of its copy.

    Args:
        project: The project.
        repo: The repository.
        ref: The ref of `spezi.toml`.
        commit: The commit of the copy.
        include: The folders of the copy, without slashes.
    """
    set_locked(
        project.root, repo, Locked(ref, commit, include, tree_hash(project.upstream_dir / repo))
    )


def stale_copies(project: Project) -> tuple[str, ...]:
    """Return the repositories whose copy does not agree with `spezi.lock` and `spezi.toml`.

    Args:
        project: The project.

    Returns:
        The repositories, sorted.
    """
    lock = read_lock(project.root)
    return tuple(
        repo
        for repo, ref in sorted(project.config.upstream.items())
        if ref is not None
        and not (
            (entry := lock.get(repo)) is not None
            and entry.ref == ref
            and entry.include == normal_include(project.config.include.get(repo, ()))
            and entry.hash == tree_hash(project.upstream_dir / repo)
        )
    )


def sync_copies(project: Project, history: History) -> tuple[str, ...]:
    """Load each copy again that does not agree with `spezi.lock` and `spezi.toml` (§000083).

    A copy whose `ref` in `spezi.toml` did not change comes from its commit in `spezi.lock`.
    Else the command resolves `ref` again.

    Args:
        project: The project.
        history: Returns a clone of the kit with its history.

    Returns:
        The descriptions of the migrations of the copies that ran.
    """
    lock = read_lock(project.root)
    own = own_ref(project)
    ran: list[str] = []
    for repo in stale_copies(project):
        ref = project.config.upstream[repo] or ""
        include = normal_include(project.config.include.get(repo, ()))
        entry = lock.get(repo)
        fetch = entry.commit if entry is not None and entry.ref == ref else ref
        commit, done, _ = fetch_copy(project, repo, fetch, include, history, own, kit_files=False)
        _lock(project, repo, ref, commit, include)
        ran.extend(done)
    return tuple(dict.fromkeys(ran))


def _drop_copy(project: Project, repo: str) -> None:
    """Remove the copy of one repository and each empty folder above it.

    Args:
        project: The project.
        repo: The repository.
    """
    remove_tree(project.upstream_dir / repo)
    for parent in (project.upstream_dir / repo).parents:
        if parent == project.upstream_dir or not parent.is_dir() or any(parent.iterdir()):
            break
        parent.rmdir()


def sync_transitive(project: Project, history: History) -> tuple[str, ...]:
    """Load each copy of a transitive upstream again that does not agree with `spezi.lock`.

    The commit and the folders come from the `spezi.lock` in the copy of each direct upstream.
    A copy and an entry of `spezi.lock` that no table and no list `transitive` names go
    (§000083, §000092). A repository with a conflict keeps its copy; the check shows the error.

    Args:
        project: The project.
        history: Returns a clone of the kit with its history.

    Returns:
        The descriptions of the migrations of the copies that ran.
    """
    lock = read_lock(project.root)
    own = own_ref(project)
    stale = tuple(
        (name, want)
        for name, want in sorted(wanted(project).items())
        if not (
            (entry := lock.get(name)) is not None
            and (entry.commit, entry.include, entry.via) == (want.commit, want.include, want.via)
            and entry.hash == tree_hash(project.upstream_dir / name)
        )
    )
    ran = tuple(
        d
        for name, want in stale
        for d in _fetch_transitive(project, name, want.commit, want.include, want.via, history, own)
    )
    stay = kept(project)
    for repo in sorted(project.copies() - stay):
        _drop_copy(project, repo)
    drop_locked(project.root, stay)
    return tuple(dict.fromkeys(ran))


def _fetch_transitive(
    project: Project,
    repo: str,
    commit: str,
    include: tuple[str, ...],
    via: tuple[str, ...],
    history: History,
    own: str | None,
) -> tuple[str, ...]:
    """Replace the copy of one transitive upstream and write its entry to `spezi.lock`.

    Args:
        project: The project.
        repo: The repository.
        commit: The commit of the copy.
        include: The folders of the copy, empty for all.
        via: The direct upstreams that bring it.
        history: Returns a clone of the kit with its history.
        own: The kit commit or ref of the project, or None.

    Returns:
        The descriptions of the migrations of the copy that ran.
    """
    got, ran, _ = fetch_copy(
        project, repo, commit, include, history, own, kit_files=False, direct=False
    )
    set_locked(
        project.root,
        repo,
        Locked("", got, include, tree_hash(project.upstream_dir / repo), via),
    )
    return ran


def ask_transitive(
    ask: Ask, direct: str, offered: tuple[str, ...], recursive: bool
) -> tuple[str, ...]:
    """Ask which transitive upstreams of a direct upstream to copy (§000085).

    Args:
        ask: The questions.
        direct: The direct upstream.
        offered: The repositories that its copy can bring.
        recursive: True for `-r`: each one without a question.

    Returns:
        The chosen repositories, sorted. Without a terminal and without `-r`, none.
    """
    match recursive, bool(offered) and ask.interactive:
        case True, _:
            return tuple(sorted(offered))
        case False, True:
            return tuple(
                sorted(
                    ask.checkbox(
                        f"Transitive upstreams of {direct} to copy?",
                        tuple((r, False) for r in offered),
                    )
                )
            )
        case _:
            return ()


def tracked(root: Path) -> tuple[str, ...]:
    """Return the files that git tracks in a project.

    Args:
        root: The root of the project.

    Returns:
        The paths relative to the root, or nothing outside a git repository.
    """
    try:
        return tuple(run_command("git", "ls-files", cwd=root).splitlines())
    except KitError:
        return ()


def remote_base(root: Path) -> str:
    """Return the default branch of `origin`, as git knows it, else `origin/main`.

    Args:
        root: The root of the project.

    Returns:
        The branch, for example `origin/develop`.
    """
    try:
        found = run_command(
            "git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD", cwd=root
        ).strip()
    except KitError:
        found = ""
    return found or "origin/main"


def code_dir_choices(
    files: tuple[str, ...], suffixes: frozenset[str]
) -> tuple[tuple[str, bool], ...]:
    """Return the folders for `code_dirs`, checked when they hold a file of `suffixes`.

    Args:
        files: The tracked files.
        suffixes: The file types of the code.

    Returns:
        Each top folder that is not hidden and not `specs`, and True when it holds code.
    """
    tops = sorted({f.split("/")[0] for f in files if "/" in f} - {"specs"})
    return tuple(
        (
            top,
            any(f.startswith(f"{top}/") and Path(f).suffix in suffixes for f in files),
        )
        for top in tops
        if not top.startswith(".")
    )


def suffix_choices(
    files: tuple[str, ...], dirs: tuple[str, ...], default: frozenset[str]
) -> tuple[tuple[str, bool], ...]:
    """Return the file types for `code_suffixes`, checked when a file of `dirs` has them.

    Args:
        files: The tracked files.
        dirs: The folders with code.
        default: The default file types.

    Returns:
        The default file types and the types in `dirs`, each with True when `dirs` has it.
    """
    found = {
        Path(f).suffix for f in files if Path(f).suffix and any(f.startswith(f"{d}/") for d in dirs)
    }
    return tuple((s, s in found) for s in sorted(default | found))


def _features_answer(ask: Ask) -> tuple[str, ...]:
    """Ask for the parts of the kit until `claude` comes only with `agents` (§000084).

    Args:
        ask: The questions.

    Returns:
        The parts that are on.
    """
    picked = ask.checkbox("Parts of the kit?", tuple((f, True) for f in FEATURES))
    if "claude" in picked and "agents" not in picked:
        ask.show("claude needs agents: CLAUDE.md imports AGENTS.md")
        return _features_answer(ask)
    return picked


@dataclass(frozen=True, slots=True)
class Start:
    """The answers of the questions of `init` (§000085).

    Attributes:
        forge: The forge.
        base_ref: The base branch.
        code_dirs: The folders with code.
        code_suffixes: The file types of the code.
        features: The parts of the kit that are on.
        owner: The login to write to `git config --local <forge>.user`, or empty.
        repo: The full name of the project, or empty (§000092).
        transitive: The transitive upstreams of the kit to copy (§000092).
    """

    forge: str
    base_ref: str
    code_dirs: tuple[str, ...]
    code_suffixes: tuple[str, ...]
    features: tuple[str, ...]
    owner: str
    repo: str = ""
    transitive: tuple[str, ...] = ()


def _owner_known(root: Path, forge: str) -> bool:
    """Return True when git knows the login of the user on a forge.

    Args:
        root: The root of the project.
        forge: The forge.

    Returns:
        True when `git config <forge>.user` has a value.
    """
    try:
        return bool(run_command("git", "config", f"{forge}.user", cwd=root).strip())
    except KitError:
        return False


def remote_repo(root: Path) -> str:
    """Return the full name of the project from the URL of `git remote origin`.

    Args:
        root: The root of the project.

    Returns:
        `<host>/<group>/.../<repo>`, or empty when there is no such remote.
    """
    try:
        url = run_command("git", "remote", "get-url", "origin", cwd=root).strip()
    except KitError:
        return ""
    found = re.fullmatch(r"(?:[a-z+]+://)?(?:[^@/]+@)?([^/:]+)[:/](.+?)(?:\.git)?/?", url)
    name = f"{found.group(1)}/{found.group(2)}" if found else ""
    return name if re.fullmatch(REPO, name) else ""


def _repo_answer(text: str) -> str | None:
    """Return why a text is no full name of a repository, or None.

    Args:
        text: The answer.

    Returns:
        The error, or None for an empty text or a valid name.
    """
    return None if not text or re.fullmatch(REPO, text) else "type <host>/<group>/.../<repo>"


def ask_start(
    root: Path,
    forge: str | None,
    ask: Ask,
    kit_lock: Mapping[str, Locked] | None = None,
    recursive: bool = False,
) -> Start:
    """Ask the questions of `init`, or take their proposals (§000085).

    Args:
        root: The root of the project.
        forge: The forge of `--forge`, or None.
        ask: The questions.
        kit_lock: The entries of the `spezi.lock` of the kit, or None for none.
        recursive: True for `-r`: copy each transitive upstream of the kit without a question.

    Returns:
        The answers.

    Raises:
        KitError: The forge is unknown without a terminal.
        Cancelled: The user does not run the command.
    """
    try:
        detected = forge or detect_forge(root)
    except KitError:
        if not ask.interactive:
            raise
        detected = None
    found = forge or ask.select("Forge?", FORGES, detected)
    base = ask.text(
        "Base branch (base_ref)?", remote_base(root), lambda t: None if t else "type a branch"
    )
    files = tracked(root)
    default = Config().code_suffixes
    dir_choices = code_dir_choices(files, default)
    dirs = ask.checkbox("Folders with code (code_dirs)?", dir_choices) if dir_choices else ()
    suffixes = (
        ask.checkbox(
            "File types of the code (code_suffixes)?", suffix_choices(files, dirs, default)
        )
        if dirs
        else tuple(sorted(default))
    )
    repo = ask.text(
        "Full name of this project (repo, empty: none)?", remote_repo(root), _repo_answer
    ).strip()
    offered = tuple(sorted(r for r in (kit_lock or {}) if r not in (repo, KIT_REPO)))
    transitive = ask_transitive(ask, KIT_REPO, offered, recursive)
    owner = (
        ""
        if _owner_known(root, found)
        else ask.text(f"Your login on {found}, the owner of new specs (empty: none)?", "")
    )
    start = Start(
        found, base, dirs, suffixes, _features_answer(ask), owner.strip(), repo, transitive
    )
    ask.show(
        "\n".join(
            (
                f"forge = {start.forge}",
                f"base_ref = {start.base_ref}",
                f"code_dirs = {', '.join(start.code_dirs) or '-'}",
                f"code_suffixes = {', '.join(start.code_suffixes) or '-'}",
                f"repo = {start.repo or '-'}",
                f"transitive = {', '.join(start.transitive) or '-'}",
                f"features on = {', '.join(start.features) or '-'}",
                *((f"git config --local {found}.user {start.owner}",) if start.owner else ()),
            )
        )
    )
    if not ask.confirm("Run?", True):
        raise Cancelled("cancelled; no file changed")
    return start


def _write_start(root: Path, start: Start) -> None:
    """Write the answers of `init` to `spezi.toml` and to git.

    Args:
        root: The root of the project.
        start: The answers.
    """
    values: tuple[tuple[str, Value], ...] = (
        ("forge", start.forge),
        ("base_ref", start.base_ref),
        ("code_dirs", start.code_dirs),
        ("code_suffixes", start.code_suffixes),
        *((("repo", start.repo),) if start.repo else ()),
        *((f"features.{f}", f in start.features) for f in FEATURES),
    )
    write_settings(root, lambda doc: set_keys(doc, values))
    if start.owner:
        with suppress(KitError):
            run_command("git", "config", "--local", f"{start.forge}.user", start.owner, cwd=root)


def init(
    root: Path, forge: str | None, ask: Ask | None = None, recursive: bool = False
) -> tuple[Project, str]:
    """Ask the questions, write `spezi.toml` and copy the kit at its highest tag (§000066).

    The transitive upstreams of the kit come with the steps of `spezi install` (§000092).

    Args:
        root: The root of the project.
        forge: `github`, `gitlab`, `codeberg`, or None to ask or to read `git remote origin`.
        ask: The questions, or None to take the proposals.
        recursive: True for `-r`: copy each transitive upstream of the kit without a question.

    Returns:
        The project and the commit of the kit.

    Raises:
        KitError: The project has the kit already, or is the kit.
    """
    if root.resolve() == kit_source().resolve():
        raise KitError("the project must not be the kit itself")
    if config_file(root).exists():
        raise KitError(f"{config_file(root).name} exists; run spezi install or spezi update")
    ref = default_ref(KIT_REPO)
    with lazy_history() as history, checkout(KIT_REPO, ref) as source:
        commit = run_command("git", "-C", str(source), "rev-parse", "HEAD").strip()
        check_program(history, commit)
        if not templates(source).is_dir():
            raise KitError(f"the kit at {commit} has no templates; it is too old")
        start = ask_start(root, forge, ask or Proposals(), read_lock(source), recursive)
        check_forge(root, start.forge, "ci" in start.features)
        write_text(root / CONFIG_NAME, package_data(CONFIG_NAME).replace("{forge}", start.forge))
        _write_start(root, start)
        (root / "specs").mkdir(exist_ok=True)
        project = Project.open(root)
        copy_rules(source, project, KIT_REPO)
        write_repo(project, KIT_REPO, ref, None, start.transitive or None)
        install_kit_files(source, project, commit)
        _lock(project, KIT_REPO, ref, commit, ())
    return Project.open(root), commit


def offer_lines(root: Path, features: Mapping[str, bool], ask: Ask) -> None:
    """Offer to add the missing line to an `.envrc` and a `CLAUDE.md` that exist (§000085).

    Args:
        root: The root of the project.
        features: The switches of `[features]`.
        ask: The questions.
    """
    for name, line, switch in (
        (".envrc", "use flake", "envrc"),
        ("CLAUDE.md", "@AGENTS.md", "claude"),
    ):
        path = root / name
        text = path.read_text(encoding="utf-8") if path.is_file() else None
        if (
            features.get(switch, True)
            and text is not None
            and line not in text.splitlines()
            and ask.confirm(f"Add the line {line} to {name}?", False)
        ):
            write_text(path, f"{text.rstrip()}\n{line}\n" if text.strip() else f"{line}\n")


def _repo_name(repo: str) -> str:
    """Return the full name of a repository, with `kit` for the kit.

    Args:
        repo: The name, or `kit`.

    Returns:
        The full name.
    """
    return KIT_REPO if repo == "kit" else repo


def two_levels(folder: Path) -> tuple[str, ...]:
    """Return the kind folders of a `specs/` folder and their direct folders.

    Args:
        folder: The `specs/` folder of a checkout.

    Returns:
        The paths, for example `style` and `style/python`, sorted.
    """
    return tuple(
        sorted(
            p.relative_to(folder).as_posix()
            for p in (*folder.glob("*"), *folder.glob("*/*"))
            if p.is_dir() and not any(part.startswith(".") for part in p.relative_to(folder).parts)
        )
    )


def _covered(path: str, include: tuple[str, ...]) -> bool:
    """Return True when a folder of `include` holds `path` or is below it.

    Args:
        path: The folder below `specs/`.
        include: The folders of the copy.

    Returns:
        True when the copy holds the folder.
    """
    return any(path == f or path.startswith(f"{f}/") or f.startswith(f"{path}/") for f in include)


def _changed_kit_files(project: Project, source: Path, old: str) -> Mapping[Path, tuple[str, str]]:
    """Return each template and skill that a person changed, with its text and its new text.

    A file is changed when it is not the same as in the kit at `old` and not the same as in the
    new kit.

    Args:
        project: The project.
        source: The checkout of the new kit.
        old: The commit of the kit in `spezi.lock`.

    Returns:
        The local text and the text of the new kit of each changed file.
    """
    pairs = (
        *(
            (
                project.templates_dir / rel,
                templates(source) / rel,
                ("specs/.templates", ".specs/templates"),
                rel,
            )
            for rel in _rel_files(project.templates_dir)
        ),
        *(
            (
                project.root / ".claude" / "skills" / skill / rel,
                source / ".claude" / "skills" / skill / rel,
                (f".claude/skills/{skill}",),
                rel,
            )
            for skill in (
                s.name for s in sorted((project.root / ".claude" / "skills").glob("spezi-*"))
            )
            if project.config.on("skills")
            for rel in _rel_files(project.root / ".claude" / "skills" / skill)
        ),
    )
    differs = tuple(
        (local, new, bases, rel)
        for local, new, bases, rel in pairs
        if local.read_text(encoding="utf-8")
        != (new.read_text(encoding="utf-8") if new.is_file() else None)
    )
    if not differs:
        return {}
    with checkout(KIT_REPO, old) as before:
        return {
            local: (
                local.read_text(encoding="utf-8"),
                new.read_text(encoding="utf-8") if new.is_file() else "",
            )
            for local, new, bases, rel in differs
            if local.read_text(encoding="utf-8")
            not in tuple(
                (before / base / rel).read_text(encoding="utf-8")
                for base in bases
                if (before / base / rel).is_file()
            )
        }


def _rel_files(folder: Path) -> tuple[Path, ...]:
    """Return the files below a folder, relative to it.

    Args:
        folder: The folder.

    Returns:
        The paths, sorted; nothing when the folder does not exist.
    """
    return (
        tuple(sorted(p.relative_to(folder) for p in folder.rglob("*") if p.is_file()))
        if folder.is_dir()
        else ()
    )


def _keep_answers(
    project: Project, changed: Mapping[Path, tuple[str, str]], ask: Ask
) -> Mapping[Path, str]:
    """Ask for each changed template and skill: overwrite, keep or cancel (§000085).

    Args:
        project: The project.
        changed: The local text and the new text of each changed file.
        ask: The questions.

    Returns:
        The local text of each file that stays.

    Raises:
        Stop: A file changed, and nobody can answer.
        Cancelled: The user cancelled.
    """
    if changed and not ask.interactive:
        names = ", ".join(str(p.relative_to(project.root)) for p in changed)
        raise Stop(f"a person changed {names}; run spezi update on a terminal without --yes")
    keep: dict[Path, str] = {}
    for path, (local, new) in changed.items():
        rel = str(path.relative_to(project.root))
        ask.show(
            "".join(
                difflib.unified_diff(
                    local.splitlines(keepends=True),
                    new.splitlines(keepends=True),
                    f"{rel} (yours)",
                    f"{rel} (kit)",
                )
            )
        )
        match ask.select(f"{rel} changed. What to do?", ("overwrite", "keep", "cancel"), "keep"):
            case "keep":
                keep[path] = local
            case "cancel":
                raise Cancelled("cancelled; the files of the repositories before stay updated")
            case _:
                pass
    return keep


def _update_review(
    project: Project,
    repo: str,
    ref: str,
    include: tuple[str, ...],
    ask: Ask,
    recursive: bool = False,
) -> Review:
    """Return the questions of `update` for one repository (§000085).

    Args:
        project: The project.
        repo: The repository.
        ref: The new ref.
        include: The folders of the copy now.
        ask: The questions.
        recursive: True for `-r`: copy each new transitive upstream without a question.

    Returns:
        The function that asks before the copy.
    """

    def review(source: Path, commit: str) -> Plan:
        entry = read_lock(project.root).get(repo)
        chosen = include
        if include and ask.interactive and entry is not None:
            with checkout(repo, entry.commit) as before:
                old = set(two_levels(before / "specs"))
            fresh = tuple(
                f for f in two_levels(source / "specs") if f not in old and not _covered(f, include)
            )
            added = (
                ask.checkbox(
                    f"New folders of {repo} for include?", tuple((f, False) for f in fresh)
                )
                if fresh
                else ()
            )
            chosen = normal_include((*include, *added))
        named = read_lock(source)
        now = project.config.transitive.get(repo, ())
        fresh = tuple(r for r in offers(project, repo, named) if r not in now)
        picked = ask_transitive(ask, repo, fresh, recursive)
        transitive = tuple(sorted({*(r for r in now if r in named), *picked}))
        new = rules_in(source / "specs", repo, chosen)
        broken = broken_references(project, repo, new)
        if broken:
            ask.show("\n".join(broken))
        if broken and not ask.confirm(
            "Update anyway?",
            False,
            risk=f"the new version of {repo} replaces or removes rules that project rules name",
        ):
            raise Cancelled(f"cancelled; the copy of {repo} did not change")
        keep = (
            _keep_answers(project, _changed_kit_files(project, source, entry.commit), ask)
            if repo == KIT_REPO and entry is not None
            else {}
        )
        old_rules = rules_in(project.upstream_dir / repo, repo)
        ask.show(
            change_lines(
                repo, project.config.upstream.get(repo), ref, commit, rule_changes(old_rules, new)
            )
        )
        if not ask.confirm("Run?", True):
            raise Cancelled(f"cancelled; the copy of {repo} did not change")
        return Plan(chosen, keep, transitive if transitive != tuple(sorted(now)) else None)

    return review


def update(
    project: Project,
    repo: str | None,
    ref: str | None,
    ask: Ask | None = None,
    recursive: bool = False,
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    """Resolve the ref of one or of each repository again, and replace its copy (§000067).

    With `ref`, the command first sets `ref` in `spezi.toml`. The kit comes first, so that a
    different repository is measured against the new kit.

    Args:
        project: The project.
        repo: The repository, `kit`, or None for each repository of `spezi.toml`.
        ref: The new tag, branch or commit, or None to resolve the ref of `spezi.toml` again.
        ask: The questions, or None to take the proposals.
        recursive: True for `-r`: copy each new transitive upstream without a question.

    Returns:
        The repository and its new commit for each update, and the migrations that ran.

    Raises:
        KitError: The repository is not in `spezi.toml`, or git fails.
    """
    questions = ask or Proposals()
    name = None if repo is None else _repo_name(repo)
    if name is not None:
        _check_repo(name)
    if name is None and ref is not None:
        raise KitError("usage: spezi update [<repo> [<ref>]]")
    done: list[tuple[str, str]] = []
    ran: list[str] = []
    with lazy_history() as history:
        own = own_ref(project)
        check_program(history, own)
        if name in (None, KIT_REPO) and own is not None:
            ran.extend(migrate_project(history, project.root, own))
            ran.extend(
                d
                for other in sorted(Project.open(project.root).copies())
                for d in migrate_copy(history, project.upstream_dir / other, own)
            )
        upstream = Project.open(project.root).config.upstream
        if name is not None and name not in upstream:
            raise KitError(f"{name} is not in spezi.toml; run spezi add {name} <ref>")
        targets = sorted(
            (name,) if name is not None else tuple(upstream),
            key=lambda r: (r != KIT_REPO, r),
        )
        for target in targets:
            current = Project.open(project.root)
            now = current.config.upstream.get(target)
            wanted = (
                ref
                or (
                    choose_ref(questions, target, now)
                    if now and questions.interactive and newer_tag(target, now)
                    else None
                )
                or now
                or default_ref(target)
            )
            include = normal_include(current.config.include.get(target, ()))
            fresh = Project.open(project.root)
            commit, copied, plan = fetch_copy(
                fresh,
                target,
                wanted,
                include,
                history,
                own,
                kit_files=target == KIT_REPO,
                review=_update_review(fresh, target, wanted, include, questions, recursive),
            )
            chosen = plan.include
            write_repo(
                fresh, target, wanted, chosen if chosen != include else None, plan.transitive
            )
            _lock(fresh, target, wanted, commit, chosen)
            own = commit if target == KIT_REPO else own
            done.append((target, commit))
            ran.extend(copied)
    return tuple(done), tuple(dict.fromkeys(ran))


def repo_error(repo: str) -> str | None:
    """Return why a repository name cannot be added, or None.

    Args:
        repo: The name.

    Returns:
        The error, or None when git can read the repository.
    """
    if not re.fullmatch(REPO, repo):
        return "type <host>/<group>/.../<repo>"
    try:
        run_command("git", "ls-remote", "--heads", f"https://{repo}.git")
    except KitError:
        return f"git cannot read https://{repo}.git"
    return None


def _add_review(
    project: Project,
    repo: str,
    ref: str,
    include: tuple[str, ...],
    ask: Ask,
    recursive: bool = False,
) -> Review:
    """Return the questions of `add` (§000085).

    Args:
        project: The project.
        repo: The repository.
        ref: The ref.
        include: The folders of `--include`.
        ask: The questions.
        recursive: True for `-r`: copy each transitive upstream without a question.

    Returns:
        The function that asks before the copy.
    """

    def review(source: Path, commit: str) -> Plan:
        folders = two_levels(source / "specs")
        picked = (
            ask.checkbox(f"Folders of {repo} to copy?", tuple((f, True) for f in folders))
            if not include and folders
            else include
        )
        chosen = () if not include and set(picked) == set(folders) else normal_include(picked)
        transitive = ask_transitive(ask, repo, offers(project, repo, read_lock(source)), recursive)
        changes = rule_changes({}, rules_in(source / "specs", repo, chosen))
        ask.show(change_lines(repo, None, ref, commit, changes))
        if not ask.confirm("Run?", True):
            raise Cancelled("cancelled; no file changed")
        return Plan(chosen, transitive=transitive)

    return review


def add(
    project: Project,
    repo: str | None,
    ref: str | None,
    include: tuple[str, ...] = (),
    ask: Ask | None = None,
    recursive: bool = False,
) -> tuple[str, tuple[str, ...]]:
    """Add the copy of a new repository (§000068).

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`, or None to ask for it.
        ref: The tag, the branch or the commit, or None for the tag with the highest version,
            else the default branch.
        include: The folders below `specs/` to copy, or empty for all.
        ask: The questions, or None to take the proposals.
        recursive: True for `-r`: copy each transitive upstream without a question.

    Returns:
        The commit of the new copy and the migrations that ran.

    Raises:
        KitError: The repository is in `spezi.toml` already, or git fails.
    """
    questions = ask or Proposals()
    name = repo or questions.text("Repository (<host>/<group>/.../<repo>)?", "", repo_error)
    _check_repo(name)
    if name in project.config.upstream:
        raise KitError(f"{name} is in spezi.toml; run spezi update {name} <ref>")
    folders = normal_include(include)
    wanted = ref or (
        choose_ref(questions, name, default_ref(name))
        if questions.interactive
        else default_ref(name)
    )
    with lazy_history() as history:
        own = own_ref(project)
        check_program(history, own)
        commit, ran, plan = fetch_copy(
            project,
            name,
            wanted,
            folders,
            history,
            own,
            kit_files=False,
            review=_add_review(project, name, wanted, folders, questions, recursive),
        )
    write_repo(project, name, wanted, plan.include, plan.transitive)
    _lock(project, name, wanted, commit, plan.include)
    return commit, ran


def remove(project: Project, repo: str) -> str:
    """Remove the copy of a repository, its table in `spezi.toml` and its entry in `spezi.lock`.

    Args:
        project: The project.
        repo: The repository.

    Returns:
        The full name of the repository.

    Raises:
        KitError: The repository is the kit, or it is not in `spezi.toml`.
    """
    name = _repo_name(repo)
    if name == KIT_REPO:
        raise KitError("the kit cannot be removed; switch its parts off in [features]")
    if name not in project.config.upstream:
        raise KitError(f"{name} is not in spezi.toml")
    try:
        write_settings(project.root, lambda doc: drop_repo(doc, name))
    except SettingError as error:
        raise KitError(str(error)) from error
    _drop_copy(project, name)
    drop_locked(
        project.root,
        frozenset(project.config.upstream) - {name}
        | frozenset(r for r, e in read_lock(project.root).items() if e.via),
    )
    return name
