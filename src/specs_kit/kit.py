"""Install the kit in a project, and update the copies of different repositories.

`init` replaces the old install script. `update` and `add` replace a copy below
`.specs/upstream/` with the `specs/` folder of its repository at one commit (§000048).
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from typing import cast

from specs_kit.changes import replace_tree, write_text
from specs_kit.project import (
    CONFIG_NAME,
    FOLDER,
    KIT_REPO,
    REPO,
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


def latest_ref(repo: str) -> str:
    """Return the commit of the default branch of a repository.

    Args:
        repo: The repository as `<host>/<group>/.../<repo>`.

    Returns:
        The commit.

    Raises:
        KitError: git cannot read the repository.
    """
    out = run_command("git", "ls-remote", f"https://{repo}.git", "HEAD").split()
    if not out:
        raise KitError(f"{repo} has no default branch")
    return out[0]


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


def _skills(source: Path) -> tuple[Path, ...]:
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
    replace_tree(source / ".specs" / "templates", project.templates_dir)
    for skill in _skills(source):
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


def init(root: Path, forge: str | None) -> Project:
    """Install the kit in a project.

    Args:
        root: The root of the project.
        forge: `github`, `gitlab`, or None to read it from `git remote origin`.

    Returns:
        The project.

    Raises:
        KitError: The project has the kit already, is the kit, or the kit has no clean commit.
    """
    ref = kit_rev()
    source = kit_source()
    if ref is None:
        raise KitError("this program comes from a kit without a clean commit; run it from a ref")
    if root.resolve() == source.resolve():
        raise KitError("the project must not be the kit itself")
    if (root / CONFIG_NAME).exists():
        raise KitError(f"{CONFIG_NAME} exists; run specs update")
    found = forge or detect_forge(root)
    check_forge(root, found)
    write_text(root / CONFIG_NAME, package_data("specs.toml").replace("{forge}", found))
    (root / "specs").mkdir(exist_ok=True)
    project = Project.open(root)
    copy_rules(source, project, KIT_REPO)
    set_ref(project, KIT_REPO, ref)
    install_kit_files(source, project, ref)
    return Project.open(root)


def _check_repo(repo: str) -> None:
    """Fail for a repository name that is not `<host>/<group>/.../<repo>`.

    Args:
        repo: The repository name.

    Raises:
        KitError: The name has a different form.
    """
    if not re.fullmatch(REPO, repo):
        raise KitError(f"{repo!r} is not <host>/<group>/.../<repo>")


def update(project: Project, repo: str, ref: str | None) -> str:
    """Update the copy of one repository. For the kit, also update its files.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag or the commit, or None for the default branch.

    Returns:
        The commit of the new copy.

    Raises:
        KitError: The repository is not in `specs.toml`, or git fails.
    """
    _check_repo(repo)
    if repo not in project.config.upstream:
        raise KitError(f"{repo} is not in specs.toml; run specs add {repo} <ref>")
    return _install(project, repo, ref or latest_ref(repo), project.config.include.get(repo, ()))


def add(project: Project, repo: str, ref: str, include: tuple[str, ...] = ()) -> str:
    """Add the copy of a new repository.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag or the commit.
        include: The folders below `specs/` to copy, or empty for all.

    Returns:
        The commit of the new copy.

    Raises:
        KitError: The repository is in `specs.toml` already, or git fails.
    """
    _check_repo(repo)
    if repo in project.config.upstream:
        raise KitError(f"{repo} is in specs.toml; run specs update {repo} <ref>")
    folders = normal_include(include)
    commit = _install(project, repo, ref, folders)
    if folders:
        set_include(project, repo, folders)
    return commit


def _install(project: Project, repo: str, ref: str, include: tuple[str, ...]) -> str:
    """Replace the copy of one repository and set its ref.

    Args:
        project: The project.
        repo: The repository as `<host>/<group>/.../<repo>`.
        ref: The tag or the commit.
        include: The folders below `specs/` to copy, or empty for all.

    Returns:
        The commit of the new copy.
    """
    with checkout(repo, ref) as source:
        commit = run_command("git", "-C", str(source), "rev-parse", "HEAD").strip()
        if repo == KIT_REPO and not (source / ".specs" / "templates").is_dir():
            raise KitError(f"the kit at {commit} has no .specs/templates/; it is too old")
        if repo == KIT_REPO:
            check_forge(project.root, project.config.forge)
        copy_rules(source, project, repo, normal_include(include))
        set_ref(project, repo, commit)
        if repo == KIT_REPO:
            install_kit_files(source, Project.open(project.root), commit)
    return commit
