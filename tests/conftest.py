"""Fixtures for the tests of the specs command.

The tests run the command as a separate process in temporary git repositories. git reads the
kit and a second rules repository from local folders through `url.<base>.insteadOf`, so that no
test needs the network.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Generator, Mapping
from dataclasses import dataclass
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KIT_URL = "https://github.com/frederikbeimgraben/specs"
RULES_REPO = "example.com/team/rules"
RULES_URL = f"https://{RULES_REPO}"
FLAKE = "{ outputs = _: { }; }\n"
RULE = """---
id: "{number}"
title: {title}
kind: {kind}
status: approved
owner: someone
updated: 2026-11-27
implementation: null
scope:
  - src/
---

# {title}

{text}

Reason: A reason.
"""


@dataclass(frozen=True)
class Result:
    """The result of one run of the command.

    Attributes:
        code: The exit code.
        out: The text on stdout.
        err: The text on stderr.
    """

    code: int
    out: str
    err: str


def git(cwd: Path, *args: str, env: Mapping[str, str] | None = None) -> str:
    """Run git in a folder and return its output.

    Args:
        cwd: The folder.
        *args: The arguments of git.
        env: The environment, or None for the environment of the test.

    Returns:
        The output.
    """
    return subprocess.run(
        ("git", *args), cwd=cwd, env=env, capture_output=True, text=True, check=True
    ).stdout


def _commit_all(repo: Path, env: Mapping[str, str]) -> str:
    """Commit every file of a repository and return the commit.

    Args:
        repo: The repository.
        env: The environment with the git identity.

    Returns:
        The commit.
    """
    git(repo, "add", "-A", env=env)
    git(repo, "commit", "-q", "-m", "state", env=env)
    return git(repo, "rev-parse", "HEAD", env=env).strip()


def write_rule(
    root: Path, folder: str, number: str, name: str, title: str, kind: str, text: str
) -> Path:
    """Write one approved rule below `specs/`.

    Args:
        root: The root of the repository.
        folder: The folder below `specs/`, for example `agents/work/questions`.
        number: The number of six digits.
        name: The name of the file without number and suffix.
        title: The title.
        kind: The kind.
        text: The rule text.

    Returns:
        The file.
    """
    path = root / "specs" / folder / f"{number}_{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(RULE.format(number=number, title=title, kind=kind, text=text), encoding="utf-8")
    return path


@dataclass(frozen=True)
class Kit:
    """The local copy of the kit and of a second rules repository.

    Attributes:
        source: The folder of the kit.
        rev: The commit of the kit.
        rules: The folder of the rules repository.
        rules_rev: The first commit of the rules repository.
        env: The environment for the command.
    """

    source: Path
    rev: str
    rules: Path
    rules_rev: str
    env: Mapping[str, str]

    def run(self, cwd: Path, *args: str) -> Result:
        """Run the specs command with `--raw` where the command takes it.

        Args:
            cwd: The folder to run in.
            *args: The arguments.

        Returns:
            The result.
        """
        done = subprocess.run(
            (sys.executable, "-m", "specs_kit", *args),
            cwd=cwd,
            env=dict(self.env),
            capture_output=True,
            text=True,
            check=False,
        )
        return Result(done.returncode, done.stdout, done.stderr)

    def commit_rules(self) -> str:
        """Commit the current state of the rules repository.

        Returns:
            The commit.
        """
        return _commit_all(self.rules, self.env)


def _base_env(home: Path) -> dict[str, str]:
    """Return an environment with a git identity and without the user's git settings.

    Args:
        home: The home folder for the test.

    Returns:
        The environment.
    """
    keep = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "TERM", "NIX_PATH"}}
    return {
        **keep,
        "HOME": str(home),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "PYTHONPATH": str(ROOT / "src"),
    }


@pytest.fixture(scope="session")
def kit(tmp_path_factory: pytest.TempPathFactory) -> Kit:
    """Return a clean commit of the kit and a rules repository, both read through git.

    Args:
        tmp_path_factory: The factory of temporary folders.

    Returns:
        The kit.
    """
    base = tmp_path_factory.mktemp("repos")
    env = _base_env(base / "home")
    (base / "home").mkdir()
    source = base / "kit"
    files = git(ROOT, "ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    for name in files:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if (ROOT / name).is_symlink():
            target.symlink_to(os.readlink(ROOT / name))
        elif (ROOT / name).is_file():
            shutil.copy2(ROOT / name, target)
    git(source, "init", "-q", "-b", "main", env=env)
    rev = _commit_all(source, env)
    rules = base / "rules"
    write_rule(
        rules,
        "style/python/naming",
        "000001",
        "snake-case",
        "Names use snake case",
        "style",
        "A name must use snake case.",
    )
    write_rule(
        rules,
        "agents/work/tests",
        "000002",
        "run-tests",
        "An agent runs the tests",
        "agent",
        "An agent must run the tests before a commit.",
    )
    git(rules, "init", "-q", "-b", "main", env=env)
    rules_rev = _commit_all(rules, env)
    full = {
        **env,
        "SPECS_KIT_SOURCE": str(source),
        "SPECS_KIT_REV": rev,
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": f"url.{source}.insteadOf",
        "GIT_CONFIG_VALUE_0": f"{KIT_URL}.git",
        "GIT_CONFIG_KEY_1": f"url.{rules}.insteadOf",
        "GIT_CONFIG_VALUE_1": f"{RULES_URL}.git",
    }
    return Kit(source, rev, rules, rules_rev, full)


@pytest.fixture
def empty(tmp_path: Path, kit: Kit) -> Path:
    """Return a git repository with a `flake.nix`, so that init runs no nix command.

    Args:
        tmp_path: The temporary folder of the test.
        kit: The kit.

    Returns:
        The root of the repository.
    """
    root = tmp_path / "project"
    root.mkdir()
    git(root, "init", "-q", "-b", "main", env=kit.env)
    (root / "flake.nix").write_text(FLAKE, encoding="utf-8")
    return root


@pytest.fixture
def project(empty: Path, kit: Kit) -> Generator[Path]:
    """Return a git repository with the kit installed by `specs init`.

    Args:
        empty: The repository.
        kit: The kit.

    Yields:
        The root of the project.
    """
    result = kit.run(empty, "init", "--forge", "github", "--raw")
    assert result.code == 0, result.out + result.err
    yield empty
