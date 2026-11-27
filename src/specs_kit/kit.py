"""Install the kit in a project, and update the copies of different repositories.

`init` replaces the old install script. `update` and `add` replace a copy below
`specs/.upstream/` with the `specs/` folder of its repository at one commit (§000048).
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import tomllib
from collections.abc import Generator, Mapping
from contextlib import ExitStack, contextmanager
from functools import cache
from importlib import resources
from pathlib import Path
from typing import cast

from specs_kit.changes import replace_tree, write_text
from specs_kit.lock import Locked, read_lock, set_locked, tree_hash
from specs_kit.migrations import History, contains, migrate_copy, migrate_project
from specs_kit.project import (
    CONFIG_NAME,
    FOLDER,
    KIT_REPO,
    REPO,
    TEMPLATES,
    Project,
    kit_rev,
    kit_source,
)


class KitError(Exception):
    """A command of the kit cannot finish."""


CI_FILES: Mapping[str, tuple[str, str]] = {
    "github": ("github-workflow.yml", ".github/workflows/specs.yml"),
    "gitlab": ("gitlab-ci.yml", ".gitlab/ci/specs.yml"),
    "codeberg": ("codeberg-workflow.yml", ".forgejo/workflows/specs.yml"),
}
GITLAB_ROOT = ".gitlab-ci.yml"
GITLAB_INCLUDE = "  - local: .gitlab/ci/specs.yml"
VERSION = re.compile(r"^v?[0-9]+(?:\.[0-9]+)*$")


def package_data(name: str) -> str:
    """Return the text of a file of the package data.

    Args:
        name: The file name below `specs_kit/data/`.

    Returns:
        The text.
    """
    return resources.files("specs_kit").joinpath("data", name).read_text(encoding="utf-8")


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

    Returns:
        The commit of the kit in `specs.lock`, else the kit ref in `specs.toml`, else None.
    """
    locked = read_lock(source).get(KIT_REPO)
    path = source / CONFIG_NAME
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except tomllib.TOMLDecodeError:
        data = {}
    match locked, data.get("upstream", {}).get(KIT_REPO, {}).get("ref"):
        case Locked(commit=commit), _:
            return commit
        case None, str() as ref:
            return ref
        case _:
            return None


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
    url = f"https://{repo}.git"
    tags = run_command("git", "ls-remote", "--tags", "--refs", "--sort=-v:refname", url)
    versions = tuple(
        name
        for line in tags.splitlines()
        for name in (line.partition("refs/tags/")[2],)
        if VERSION.match(name)
    )
    head = run_command("git", "ls-remote", "--symref", url, "HEAD")
    branch = next(
        (
            line.split()[1].removeprefix("refs/heads/")
            for line in head.splitlines()
            if line.startswith("ref: ")
        ),
        None,
    )
    match versions, branch:
        case (first, *_), _:
            return first
        case (), str():
            return branch
        case _:
            raise KitError(f"{repo} has no default branch")


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
    """Return the folders of `include` without a slash at the start or the end, sorted.

    Args:
        include: The folders, for example `style/python/`.

    Returns:
        The folders, for example `style/python`.

    Raises:
        KitError: A folder is not a path of kebab-case names.
    """
    folders = tuple(sorted({f.strip("/") for f in include}))
    bad = tuple(f for f in folders if not all(FOLDER.match(p) for p in f.split("/")))
    if bad:
        raise KitError(f"include {', '.join(map(repr, bad))} is not a path of kebab-case names")
    return folders


def copy_rules(source: Path, project: Project, repo: str, include: tuple[str, ...] = ()) -> None:
    """Replace the copy of one repository with its `specs/` folder or the folders of `include`.

    The copy holds `specs/README.md` only without `include` (§000048).

    Args:
        source: The root of a checkout of the repository.
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        include: The folders below `specs/` to copy, or empty for all.

    Raises:
        KitError: The checkout has no `specs/` folder, or a folder of `include`.
    """
    missing = tuple(f for f in include if not (source / "specs" / f).is_dir())
    if not (source / "specs").is_dir():
        raise KitError(f"{repo} has no specs/ folder")
    if missing:
        raise KitError(f"{repo} has no folder specs/{', specs/'.join(missing)}")
    replace_tree(source / "specs", project.upstream_dir / repo, include)


def set_ref(project: Project, repo: str, ref: str) -> None:
    """Set `ref` of one repository in `specs.toml`. Add the table when it is missing.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The commit.
    """
    text = project.config_path.read_text(encoding="utf-8") if project.config_path.is_file() else ""
    header = f'[upstream."{repo}"]'
    pattern = re.compile(rf"^{re.escape(header)}\n(?:(?!\[).*\n)*?ref = .*$", re.MULTILINE)
    updated = (
        pattern.sub(lambda m: re.sub(r"ref = .*$", f'ref = "{ref}"', m.group(0)), text)
        if pattern.search(text)
        else f'{text.rstrip()}\n\n{header}\nref = "{ref}"\n'.lstrip()
    )
    write_text(project.config_path, updated if updated.endswith("\n") else f"{updated}\n")


def set_include(project: Project, repo: str, include: tuple[str, ...]) -> None:
    """Add `include` below the table of one repository in `specs.toml`.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        include: The folders of the copy.
    """
    text = project.config_path.read_text(encoding="utf-8")
    header = f'[upstream."{repo}"]'
    entry = "include = [" + ", ".join(f'"{f}/"' for f in include) + "]"
    write_text(
        project.config_path,
        re.sub(
            rf"^({re.escape(header)}\n(?:(?!\[).*\n)*?ref = .*)$",
            lambda m: f"{m.group(1)}\n{entry}",
            text,
            count=1,
            flags=re.MULTILINE,
        ),
    )


def skills(source: Path) -> tuple[Path, ...]:
    """Return the skill folders of the kit.

    Args:
        source: The root of the kit.

    Returns:
        The folders `.claude/skills/spec-*`.
    """
    folder = source / ".claude" / "skills"
    return tuple(sorted(p for p in folder.glob("spec-*") if p.is_dir())) if folder.is_dir() else ()


def write_mcp(project: Project, ref: str) -> None:
    """Write the server `specs` into `.mcp.json`. Keep the other servers.

    Args:
        project: The project.
        ref: The commit of the kit.
    """
    path = project.root / ".mcp.json"
    data = (
        cast("dict[str, object]", json.loads(path.read_text(encoding="utf-8")))
        if path.is_file()
        else {}
    )
    servers = cast("dict[str, object]", data.get("mcpServers", {}))
    server = {
        "command": "nix",
        "args": ["run", f"github:{KIT_REPO.split('/', 1)[1]}/{ref}", "--", "mcp"],
    }
    write_text(
        path, json.dumps({**data, "mcpServers": {**servers, "specs": server}}, indent=2) + "\n"
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


def check_forge(root: Path, forge: str) -> None:
    """Fail before a change when the kit cannot write its CI file for a forge.

    Args:
        root: The root of the project.
        forge: The forge.

    Raises:
        KitError: The forge is unknown, or `.gitlab-ci.yml` cannot get the include.
    """
    if forge not in CI_FILES:
        raise KitError(f"specs.toml: forge {forge!r} must be github, gitlab or codeberg")
    if forge == "gitlab":
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
    """Replace the templates, the skills, the CI file and the MCP server of the kit.

    Args:
        source: The root of the kit at `ref`.
        project: The project.
        ref: The commit of the kit.

    Raises:
        KitError: The forge in `specs.toml` is unknown.
    """
    forge = project.config.forge
    check_forge(project.root, forge)
    data_name, target = CI_FILES[forge]
    root_text = gitlab_root_text(project.root) if forge == "gitlab" else None
    replace_tree(templates(source), project.templates_dir)
    for skill in skills(source):
        replace_tree(skill, project.root / ".claude" / "skills" / skill.name)
    branch = project.config.base_ref.removeprefix("origin/")
    write_text(
        project.root / target,
        package_data(data_name).replace("{ref}", ref).replace("{branch}", branch),
    )
    if root_text is not None:
        write_text(project.root / GITLAB_ROOT, root_text)
    write_mcp(project, ref)


def detect_forge(root: Path) -> str:
    """Return the forge of `git remote origin`.

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
    match ("gitlab" in url, "github" in url, "codeberg" in url):
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
    """Return the kit commit of the project in `specs.lock`, else the kit ref in `specs.toml`.

    Args:
        project: The project.

    Returns:
        The commit or the ref, or None when the project has no kit entry.
    """
    locked = read_lock(project.root).get(KIT_REPO)
    return locked.commit if locked else project.config.upstream.get(KIT_REPO)


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
            f"this program is the kit at {rev}, older than the kit at {own} in specs.lock;"
            " load the new program with nix develop first"
        )


def fetch_copy(
    project: Project,
    repo: str,
    ref: str,
    include: tuple[str, ...],
    history: History,
    own: str | None,
    *,
    kit_files: bool,
) -> tuple[str, tuple[str, ...]]:
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

    Returns:
        The commit of the copy and the descriptions of the migrations of the copy that ran.

    Raises:
        KitError: The kit is too old, or the repository uses a newer kit than the project.
    """
    with checkout(repo, ref) as source:
        commit = run_command("git", "-C", str(source), "rev-parse", "HEAD").strip()
        if repo == KIT_REPO and not templates(source).is_dir():
            raise KitError(f"the kit at {commit} has no templates; it is too old")
        if repo == KIT_REPO:
            check_forge(project.root, project.config.forge)
        theirs = None if repo == KIT_REPO else upstream_kit_ref(source)
        if theirs and own and theirs != own and not contains(history(), theirs, own):
            raise KitError(
                f"{repo} at {commit} needs the kit at {theirs} or later; run specs update first"
            )
        copy_rules(source, project, repo, include)
        ran = migrate_copy(history, project.upstream_dir / repo, theirs)
        if kit_files:
            install_kit_files(source, project, commit)
    return commit, ran


def _lock(project: Project, repo: str, ref: str, commit: str, include: tuple[str, ...]) -> None:
    """Write the entry of one repository to `specs.lock` with the hash of its copy.

    Args:
        project: The project.
        repo: The repository.
        ref: The ref of `specs.toml`.
        commit: The commit of the copy.
        include: The folders of the copy, without slashes.
    """
    set_locked(
        project.root, repo, Locked(ref, commit, include, tree_hash(project.upstream_dir / repo))
    )


def stale_copies(project: Project) -> tuple[str, ...]:
    """Return the repositories whose copy does not agree with `specs.lock` and `specs.toml`.

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
    """Load each copy again that does not agree with `specs.lock` and `specs.toml` (§000083).

    A copy whose `ref` in `specs.toml` did not change comes from its commit in `specs.lock`.
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
        commit, done = fetch_copy(project, repo, fetch, include, history, own, kit_files=False)
        _lock(project, repo, ref, commit, include)
        ran.extend(done)
    return tuple(dict.fromkeys(ran))


def init(root: Path, forge: str | None) -> tuple[Project, str]:
    """Write `specs.toml` and copy the kit at its tag with the highest version (§000066).

    Args:
        root: The root of the project.
        forge: `github`, `gitlab`, `codeberg`, or None to read it from `git remote origin`.

    Returns:
        The project and the commit of the kit.

    Raises:
        KitError: The project has the kit already, or is the kit.
    """
    if root.resolve() == kit_source().resolve():
        raise KitError("the project must not be the kit itself")
    if (root / CONFIG_NAME).exists():
        raise KitError(f"{CONFIG_NAME} exists; run specs install or specs update")
    found = forge or detect_forge(root)
    check_forge(root, found)
    ref = default_ref(KIT_REPO)
    with lazy_history() as history, checkout(KIT_REPO, ref) as source:
        commit = run_command("git", "-C", str(source), "rev-parse", "HEAD").strip()
        check_program(history, commit)
        if not templates(source).is_dir():
            raise KitError(f"the kit at {commit} has no templates; it is too old")
        write_text(root / CONFIG_NAME, package_data("specs.toml").replace("{forge}", found))
        (root / "specs").mkdir(exist_ok=True)
        project = Project.open(root)
        copy_rules(source, project, KIT_REPO)
        set_ref(project, KIT_REPO, ref)
        install_kit_files(source, project, commit)
        _lock(project, KIT_REPO, ref, commit, ())
    return Project.open(root), commit


def _repo_name(repo: str) -> str:
    """Return the full name of a repository, with `kit` for the kit.

    Args:
        repo: The name, or `kit`.

    Returns:
        The full name.
    """
    return KIT_REPO if repo == "kit" else repo


def update(
    project: Project, repo: str | None, ref: str | None
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    """Resolve the ref of one or of each repository again, and replace its copy (§000067).

    With `ref`, the command first sets `ref` in `specs.toml`. The kit comes first, so that a
    different repository is measured against the new kit.

    Args:
        project: The project.
        repo: The repository, `kit`, or None for each repository of `specs.toml`.
        ref: The new tag, branch or commit, or None to resolve the ref of `specs.toml` again.

    Returns:
        The repository and its new commit for each update, and the migrations that ran.

    Raises:
        KitError: The repository is not in `specs.toml`, or git fails.
    """
    name = None if repo is None else _repo_name(repo)
    if name is not None:
        _check_repo(name)
    if name is not None and name not in project.config.upstream:
        raise KitError(f"{name} is not in specs.toml; run specs add {name} <ref>")
    if name is None and ref is not None:
        raise KitError("usage: specs update [<repo> [<ref>]]")
    targets = sorted(
        (name,) if name is not None else tuple(project.config.upstream),
        key=lambda r: (r != KIT_REPO, r),
    )
    done: list[tuple[str, str]] = []
    ran: list[str] = []
    with lazy_history() as history:
        own = own_ref(project)
        check_program(history, own)
        for target in targets:
            current = Project.open(project.root)
            wanted = ref or current.config.upstream.get(target) or default_ref(target)
            include = normal_include(current.config.include.get(target, ()))
            if target == KIT_REPO:
                ran.extend(migrate_project(history, project.root, own))
                ran.extend(
                    d
                    for other in sorted(Project.open(project.root).copies())
                    for d in migrate_copy(history, project.upstream_dir / other, own)
                )
            fresh = Project.open(project.root)
            commit, copied = fetch_copy(
                fresh, target, wanted, include, history, own, kit_files=target == KIT_REPO
            )
            set_ref(fresh, target, wanted)
            _lock(fresh, target, wanted, commit, include)
            own = commit if target == KIT_REPO else own
            done.append((target, commit))
            ran.extend(copied)
    return tuple(done), tuple(dict.fromkeys(ran))


def add(
    project: Project, repo: str, ref: str | None, include: tuple[str, ...] = ()
) -> tuple[str, tuple[str, ...]]:
    """Add the copy of a new repository (§000068).

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag, the branch or the commit, or None for the tag with the highest version,
            else the default branch.
        include: The folders below `specs/` to copy, or empty for all.

    Returns:
        The commit of the new copy and the migrations that ran.

    Raises:
        KitError: The repository is in `specs.toml` already, or git fails.
    """
    _check_repo(repo)
    if repo in project.config.upstream:
        raise KitError(f"{repo} is in specs.toml; run specs update {repo} <ref>")
    folders = normal_include(include)
    wanted = ref or default_ref(repo)
    with lazy_history() as history:
        own = own_ref(project)
        check_program(history, own)
        commit, ran = fetch_copy(project, repo, wanted, folders, history, own, kit_files=False)
    set_ref(project, repo, wanted)
    if folders:
        set_include(project, repo, folders)
    _lock(project, repo, wanted, commit, folders)
    return commit, ran
