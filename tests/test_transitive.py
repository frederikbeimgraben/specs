"""Tests of the transitive upstreams (§000092, §000082, §000083, §000068, §000067)."""

from __future__ import annotations

import dataclasses
import tomllib
from pathlib import Path

from conftest import Kit, git, write_rule

from spezi.lock import Locked, lock_text, read_lock
from spezi.transitive import union

MID = "example.com/team/mid"
OTHER = "example.com/team/other"
BASE = "example.com/team/base"


def _repo(kit: Kit, folder: Path, number: str, lock: str | None = None) -> str:
    """Make a rules repository with one rule and an optional `spezi.lock`, and commit it.

    Args:
        kit: The kit, for the git environment.
        folder: The folder of the repository.
        number: The number of the rule.
        lock: The text of `spezi.lock`, or None for none.

    Returns:
        The commit.
    """
    write_rule(folder, "style/shared/x", number, "rule", f"Rule {number}", "style", "A must B.")
    if lock is not None:
        (folder / "spezi.lock").write_text(lock, encoding="utf-8")
    if not (folder / ".git").is_dir():
        git(folder, "init", "-q", "-b", "main", env=kit.env)
    git(folder, "add", "-A", env=kit.env)
    git(folder, "commit", "-q", "-m", number, env=kit.env)
    return git(folder, "rev-parse", "HEAD", env=kit.env).strip()


def _pin(repo: str, commit: str) -> str:
    """Return the text of a `spezi.lock` that pins one repository.

    Args:
        repo: The repository.
        commit: The commit.

    Returns:
        The text.
    """
    return lock_text({repo: Locked("main", commit, (), "sha256-x")})


def _env(kit: Kit, folders: dict[str, Path]) -> Kit:
    """Return the kit with git reading more repositories from local folders.

    Args:
        kit: The kit.
        folders: The local folder of each repository.

    Returns:
        The kit with the new environment.
    """
    count = int(kit.env["GIT_CONFIG_COUNT"])
    extra = {
        key: value
        for i, (repo, folder) in enumerate(sorted(folders.items()), start=count)
        for key, value in (
            (f"GIT_CONFIG_KEY_{i}", f"url.{folder}.insteadOf"),
            (f"GIT_CONFIG_VALUE_{i}", f"https://{repo}.git"),
        )
    }
    return dataclasses.replace(
        kit, env={**kit.env, **extra, "GIT_CONFIG_COUNT": str(count + len(folders))}
    )


def _settings(project: Path) -> dict[str, object]:
    """Return the parsed `spezi.toml`.

    Args:
        project: The root of the project.

    Returns:
        The settings.
    """
    return tomllib.loads((project / "spezi.toml").read_text(encoding="utf-8"))


def _repos(kit: Kit, tmp_path: Path) -> tuple[Kit, str, str]:
    """Make BASE with two commits, MID that pins the second and OTHER that pins the first.

    Args:
        kit: The kit.
        tmp_path: The temporary folder of the test.

    Returns:
        The kit for the three repositories, and the first and the second commit of BASE.
    """
    first = _repo(kit, tmp_path / "base", "000030")
    second = _repo(kit, tmp_path / "base", "000031")
    _repo(kit, tmp_path / "mid", "000020", _pin(BASE, second))
    _repo(kit, tmp_path / "other", "000040", _pin(BASE, first))
    folders = {BASE: tmp_path / "base", MID: tmp_path / "mid", OTHER: tmp_path / "other"}
    return _env(kit, folders), first, second


def test_add_with_recursive_copies_the_transitive_upstream(
    kit: Kit, project: Path, tmp_path: Path
) -> None:
    """`spezi add -r` copies the upstream of the upstream at the commit of its lock."""
    more, _, second = _repos(kit, tmp_path)
    result = more.run(project, "add", MID, "main", "-r", "--raw")
    assert result.code == 0, result.out + result.err
    table = _settings(project)["upstream"][MID]  # type: ignore[index]
    assert table["transitive"] == [BASE]
    entry = read_lock(project)[BASE]
    assert (entry.ref, entry.commit, entry.via) == ("", second, (MID,))
    assert (project / "specs/.upstream" / MID / "spezi.lock").is_file()
    assert (project / "specs/.upstream" / BASE / "style/shared/x/000031_rule.md").is_file()
    assert not (project / "specs/.upstream" / BASE / "spezi.lock").exists()


def test_add_without_recursive_copies_no_transitive_upstream(
    kit: Kit, project: Path, tmp_path: Path
) -> None:
    """Without `-r` and without a terminal, `spezi add` copies no transitive upstream."""
    more, _, _ = _repos(kit, tmp_path)
    result = more.run(project, "add", MID, "main", "--raw")
    assert result.code == 0, result.out + result.err
    assert "transitive" not in _settings(project)["upstream"][MID]  # type: ignore[index]
    assert not (project / "specs/.upstream" / BASE).exists()


def test_the_project_itself_gets_no_copy(kit: Kit, project: Path, tmp_path: Path) -> None:
    """A transitive upstream with the name of `repo` gets no copy."""
    more, _, _ = _repos(kit, tmp_path)
    settings = project / "spezi.toml"
    settings.write_text(f'repo = "{BASE}"\n' + settings.read_text(encoding="utf-8"), "utf-8")
    result = more.run(project, "add", MID, "main", "-r", "--raw")
    assert result.code == 0, result.out + result.err
    assert not (project / "specs/.upstream" / BASE).exists()
    assert BASE not in read_lock(project)


def test_two_commits_of_one_upstream_are_an_error(kit: Kit, project: Path, tmp_path: Path) -> None:
    """Two direct upstreams that pin different commits give an error until a table decides."""
    more, first, _ = _repos(kit, tmp_path)
    assert more.run(project, "add", MID, "main", "-r", "--raw").code == 0
    result = more.run(project, "add", OTHER, "main", "-r", "--raw")
    assert result.code == 1
    assert "has different commits" in result.out + result.err
    fixed = more.run(project, "add", BASE, first, "--raw")
    assert fixed.code == 0, fixed.out + fixed.err
    assert read_lock(project)[BASE].via == ()


def test_install_restores_a_transitive_copy(kit: Kit, project: Path, tmp_path: Path) -> None:
    """`spezi install` loads a changed transitive copy again from the commit of the lock."""
    more, _, _ = _repos(kit, tmp_path)
    assert more.run(project, "add", MID, "main", "-r", "--raw").code == 0
    rule = project / "specs/.upstream" / BASE / "style/shared/x/000031_rule.md"
    rule.write_text("changed\n", encoding="utf-8")
    assert more.run(project, "check", "--raw").code == 1
    result = more.run(project, "install", "--raw")
    assert result.code == 0, result.out + result.err
    assert rule.read_text(encoding="utf-8") != "changed\n"


def test_the_lock_keeps_via_and_no_ref() -> None:
    """A transitive entry of `spezi.lock` has `via` and no `ref`, and reads back the same."""
    entry = Locked("", "abc", ("style",), "sha256-x", (MID, OTHER))
    text = lock_text({BASE: entry})
    assert "ref =" not in text
    assert f'via = ["{MID}", "{OTHER}"]' in text
    table = tomllib.loads(text)["upstream"][BASE]
    assert table["via"] == [MID, OTHER]


def test_union_of_folders() -> None:
    """The union of two include lists drops nested folders; an empty list is all rules."""
    assert union((("style/python",), ("style",))) == ("style",)
    assert union((("agents",), ("style",))) == ("agents", "style")
    assert union((("agents",), ())) == ()


def test_update_with_recursive_adds_a_new_transitive_upstream(
    kit: Kit, project: Path, tmp_path: Path
) -> None:
    """`spezi update -r` copies a transitive upstream that `transitive` does not hold yet."""
    more, _, _ = _repos(kit, tmp_path)
    assert more.run(project, "add", MID, "main", "--raw").code == 0
    result = more.run(project, "update", MID, "-r", "--raw")
    assert result.code == 0, result.out + result.err
    assert _settings(project)["upstream"][MID]["transitive"] == [BASE]  # type: ignore[index]
    assert (project / "specs/.upstream" / BASE).is_dir()
