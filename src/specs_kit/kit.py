"""Install the kit in a project, and update the copies of different repositories.

`init` replaces the old install script. `update` and `add` replace a copy below
`.specs/upstream/` with the `specs/` folder of its repository at one commit (§000048).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from typing import cast

from specs_kit.project import CONFIG_NAME, KIT_REPO, REPO, Project, kit_rev, kit_source


class KitError(Exception):
    """A command of the kit cannot finish."""


CI_FILES: Mapping[str, tuple[str, str]] = {
    "github": ("github-workflow.yml", ".github/workflows/specs.yml"),
    "gitlab": ("gitlab-ci.yml", ".gitlab-ci.yml"),
}


def _data(name: str) -> str:
    """Return the text of a file of the package data.

    Args:
        name: The file name below `specs_kit/data/`.

    Returns:
        The text.
    """
    return resources.files("specs_kit").joinpath("data", name).read_text(encoding="utf-8")


def _run(*args: str, cwd: Path | None = None) -> str:
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
        repo: The repository as `<host>/<owner>/<repo>`.

    Returns:
        The commit.

    Raises:
        KitError: git cannot read the repository.
    """
    out = _run("git", "ls-remote", f"https://{repo}.git", "HEAD").split()
    if not out:
        raise KitError(f"{repo} has no default branch")
    return out[0]


@contextmanager
def checkout(repo: str, ref: str) -> Generator[Path]:
    """Check out a repository at one ref into a temporary folder.

    Args:
        repo: The repository as `<host>/<owner>/<repo>`.
        ref: The tag or the commit.

    Yields:
        The folder of the checkout.
    """
    with tempfile.TemporaryDirectory() as tmp:
        _run("git", "init", "-q", tmp)
        _run("git", "-C", tmp, "fetch", "-q", "--depth", "1", f"https://{repo}.git", ref)
        _run("git", "-C", tmp, "checkout", "-q", "FETCH_HEAD")
        yield Path(tmp)


def _replace_tree(source: Path, target: Path) -> None:
    """Replace the folder `target` with a copy of `source`, without an `upstream/` folder.

    Args:
        source: The folder to copy.
        target: The folder to replace.
    """
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("upstream"))


def copy_rules(source: Path, project: Project, repo: str) -> None:
    """Replace the copy of one repository with its `specs/` folder (§000048).

    Args:
        source: The root of a checkout of the repository.
        project: The project.
        repo: The repository as `<host>/<owner>/<repo>`.

    Raises:
        KitError: The checkout has no `specs/` folder.
    """
    if not (source / "specs").is_dir():
        raise KitError(f"{repo} has no specs/ folder")
    _replace_tree(source / "specs", project.upstream_dir / repo)


def set_ref(project: Project, repo: str, ref: str) -> None:
    """Set `ref` of one repository in `specs.toml`. Add the table when it is missing.

    Args:
        project: The project.
        repo: The repository as `<host>/<owner>/<repo>`.
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
    project.config_path.write_text(
        updated if updated.endswith("\n") else f"{updated}\n", encoding="utf-8"
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
    path.write_text(
        json.dumps({**data, "mcpServers": {**servers, "specs": server}}, indent=2) + "\n",
        encoding="utf-8",
    )


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
    if forge not in CI_FILES:
        raise KitError(f"specs.toml: forge {forge!r} must be github or gitlab")
    data_name, target = CI_FILES[forge]
    _replace_tree(source / ".specs" / "templates", project.templates_dir)
    for skill in _skills(source):
        _replace_tree(skill, project.root / ".claude" / "skills" / skill.name)
    (project.root / target).parent.mkdir(parents=True, exist_ok=True)
    (project.root / target).write_text(_data(data_name).replace("{ref}", ref), encoding="utf-8")
    write_mcp(project, ref)


def detect_forge(root: Path) -> str:
    """Return the forge of `git remote origin`.

    Args:
        root: The root of the project.

    Returns:
        `github` or `gitlab`.

    Raises:
        KitError: The remote names neither GitHub nor GitLab.
    """
    try:
        url = _run("git", "remote", "get-url", "origin", cwd=root)
    except KitError:
        url = ""
    match ("gitlab" in url, "github" in url):
        case (True, _):
            return "gitlab"
        case (False, True):
            return "github"
        case (False, False):
            raise KitError(
                "cannot find the forge from git remote origin; pass --forge github|gitlab"
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
    (root / CONFIG_NAME).write_text(_data("specs.toml").replace("{forge}", found), encoding="utf-8")
    (root / "specs").mkdir(exist_ok=True)
    project = Project.open(root)
    copy_rules(source, project, KIT_REPO)
    set_ref(project, KIT_REPO, ref)
    install_kit_files(source, project, ref)
    return Project.open(root)


def _check_repo(repo: str) -> None:
    """Fail for a repository name that is not `<host>/<owner>/<repo>`.

    Args:
        repo: The repository name.

    Raises:
        KitError: The name has a different form.
    """
    if not re.fullmatch(REPO, repo):
        raise KitError(f"{repo!r} is not <host>/<owner>/<repo>")


def update(project: Project, repo: str, ref: str | None) -> str:
    """Update the copy of one repository. For the kit, also update its files.

    Args:
        project: The project.
        repo: The repository as `<host>/<owner>/<repo>`.
        ref: The tag or the commit, or None for the default branch.

    Returns:
        The commit of the new copy.

    Raises:
        KitError: The repository is not in `specs.toml`, or git fails.
    """
    _check_repo(repo)
    if repo not in project.config.upstream:
        raise KitError(f"{repo} is not in specs.toml; run specs add {repo} <ref>")
    return _install(project, repo, ref or latest_ref(repo))


def add(project: Project, repo: str, ref: str) -> str:
    """Add the copy of a new repository.

    Args:
        project: The project.
        repo: The repository as `<host>/<owner>/<repo>`.
        ref: The tag or the commit.

    Returns:
        The commit of the new copy.

    Raises:
        KitError: The repository is in `specs.toml` already, or git fails.
    """
    _check_repo(repo)
    if repo in project.config.upstream:
        raise KitError(f"{repo} is in specs.toml; run specs update {repo} <ref>")
    return _install(project, repo, ref)


def _install(project: Project, repo: str, ref: str) -> str:
    """Replace the copy of one repository and set its ref.

    Args:
        project: The project.
        repo: The repository as `<host>/<owner>/<repo>`.
        ref: The tag or the commit.

    Returns:
        The commit of the new copy.
    """
    with checkout(repo, ref) as source:
        commit = _run("git", "-C", str(source), "rev-parse", "HEAD").strip()
        if repo == KIT_REPO and not (source / ".specs" / "templates").is_dir():
            raise KitError(f"the kit at {commit} has no .specs/templates/; it is too old")
        copy_rules(source, project, repo)
        set_ref(project, repo, commit)
        if repo == KIT_REPO:
            install_kit_files(source, Project.open(project.root), commit)
    return commit
