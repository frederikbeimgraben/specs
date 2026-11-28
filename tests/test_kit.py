"""Tests of `specs init`, `specs update` and `specs add` (§000066, §000067, §000068)."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from conftest import RULES_REPO, Kit, git, write_rule

from spezi.kit import copy_rules, write_repo
from spezi.project import Project

KIT = "specs/.upstream/github.com/frederikbeimgraben/spezi"


def _config(project: Path) -> dict[str, object]:
    """Return the parsed `spezi.toml` of a project.

    Args:
        project: The root of the project.

    Returns:
        The settings.
    """
    return tomllib.loads((project / "spezi.toml").read_text(encoding="utf-8"))


def _lock(project: Path) -> dict[str, dict[str, object]]:
    """Return the upstream tables of `spezi.lock`.

    Args:
        project: The root of the project.

    Returns:
        The tables by repository.
    """
    value = tomllib.loads((project / "spezi.lock").read_text(encoding="utf-8"))["upstream"]
    assert isinstance(value, dict)
    return value


def _upstream(project: Path) -> dict[str, dict[str, object]]:
    """Return the upstream tables of `spezi.toml`.

    Args:
        project: The root of the project.

    Returns:
        The tables by repository.
    """
    value = _config(project)["upstream"]
    assert isinstance(value, dict)
    return value


def test_init_writes_the_kit_files(kit: Kit, project: Path) -> None:
    """`specs init` writes the settings, the kit copy, templates, skills, CI and MCP files."""
    assert _config(project)["forge"] == "github"
    assert _upstream(project)["github.com/frederikbeimgraben/spezi"]["ref"] == "main"
    assert _lock(project)["github.com/frederikbeimgraben/spezi"]["commit"] == kit.rev
    for name in (
        f"{KIT}/workflow/specs/process/000001_precedence.md",
        "specs/.templates/TEMPLATE.md",
        ".claude/skills/spezi-write/SKILL.md",
        ".github/workflows/spezi.yml",
        ".mcp.json",
        ".envrc",
        "specs/README.md",
        "spezi.lock",
    ):
        assert (project / name).is_file(), name


def test_init_ci_runs_on_the_base_branch(kit: Kit, project: Path) -> None:
    """The CI job runs for a push to the branch of `base_ref`."""
    assert "branches: [main]" in (project / ".github/workflows/spezi.yml").read_text(
        encoding="utf-8"
    )


def test_init_keeps_an_existing_flake(kit: Kit, empty: Path) -> None:
    """`specs init` changes no `flake.nix` that exists and prints the lines to add."""
    before = (empty / "flake.nix").read_text(encoding="utf-8")
    result = kit.run(empty, "init", "--forge", "github", "--raw")
    assert result.code == 0, result.out + result.err
    assert (empty / "flake.nix").read_text(encoding="utf-8") == before
    assert f'inputs.spezi.url = "github:frederikbeimgraben/spezi/{kit.rev}";' in result.out


def test_init_takes_the_forge_from_the_remote(kit: Kit, empty: Path) -> None:
    """Without `--forge`, init reads the forge from `git remote origin`."""
    git(empty, "remote", "add", "origin", "https://codeberg.org/me/app.git", env=kit.env)
    result = kit.run(empty, "init", "--raw")
    assert result.code == 0, result.out + result.err
    assert _config(empty)["forge"] == "codeberg"
    assert (empty / ".forgejo/workflows/spezi.yml").is_file()


def test_init_reads_the_forge_from_the_host_only(kit: Kit, empty: Path) -> None:
    """The forge comes from the host of the remote, not from the path of the repository."""
    git(empty, "remote", "add", "origin", "git@github.com:me/gitlab-tools.git", env=kit.env)
    result = kit.run(empty, "init", "--raw")
    assert result.code == 0, result.out + result.err
    assert _config(empty)["forge"] == "github"


def test_init_stops_when_the_kit_is_there(kit: Kit, project: Path) -> None:
    """`specs init` stops with an error when `spezi.toml` exists."""
    result = kit.run(project, "init", "--forge", "github", "--raw")
    assert result.code == 1
    assert "spezi.toml exists" in result.err


def test_add_copies_the_rules(kit: Kit, project: Path) -> None:
    """`specs add` copies the rules and writes the commit as `ref`."""
    result = kit.run(project, "add", RULES_REPO, kit.rules_rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert _upstream(project)[RULES_REPO]["ref"] == kit.rules_rev
    copy = project / "specs/.upstream" / RULES_REPO
    assert (copy / "style/python/naming/000001_snake-case.md").is_file()
    assert "example.com/team/rules:S/python/naming/000001" in (
        project / "specs/README.md"
    ).read_text(encoding="utf-8")


def test_add_with_include_copies_only_the_folders(kit: Kit, project: Path) -> None:
    """`specs add` with `--include` copies only these folders and writes `include`."""
    result = kit.run(project, "add", RULES_REPO, kit.rules_rev, "--include", "agents/", "--raw")
    assert result.code == 0, result.out + result.err
    copy = project / "specs/.upstream" / RULES_REPO
    assert (copy / "agents/work/tests/000002_run-tests.md").is_file()
    assert not (copy / "style").exists()
    assert _upstream(project)[RULES_REPO]["include"] == ["agents/"]


def test_init_leaves_out_the_own_folders_of_the_kit(kit: Kit, project: Path) -> None:
    """The copy of the kit holds no folder of `own` in the `spezi.toml` of the kit."""
    assert (project / KIT / "conventions").is_dir()
    assert not (project / KIT / "requirements").exists()
    assert not (project / KIT / "workflow/kit").exists()
    assert (project / KIT / "workflow/specs").is_dir()


def test_add_copies_an_own_folder_that_include_names(kit: Kit, project: Path) -> None:
    """A copy leaves out each folder of `own`, except a folder that `include` names."""
    (kit.rules / "spezi.toml").write_text('own = ["style/"]\n', encoding="utf-8")
    rev = kit.commit_rules()
    copy = project / "specs/.upstream" / RULES_REPO
    try:
        assert kit.run(project, "add", RULES_REPO, rev, "--raw").code == 0
        assert (copy / "agents/work/tests/000002_run-tests.md").is_file()
        assert not (copy / "style").exists()
        assert kit.run(project, "remove", RULES_REPO, "--raw").code == 0
        result = kit.run(project, "add", RULES_REPO, rev, "--include", "style/python/", "--raw")
        assert result.code == 0, result.out + result.err
        assert (copy / "style/python/naming/000001_snake-case.md").is_file()
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)


def test_add_stops_for_a_repository_in_the_settings(kit: Kit, project: Path) -> None:
    """`specs add` stops with an error when the repository is in `spezi.toml` already."""
    assert kit.run(project, "add", RULES_REPO, kit.rules_rev, "--raw").code == 0
    result = kit.run(project, "add", RULES_REPO, kit.rules_rev, "--raw")
    assert result.code == 1
    assert "is in spezi.toml" in result.err


def test_update_replaces_the_copy_and_keeps_include(kit: Kit, project: Path) -> None:
    """`specs update` replaces the copy, sets the new commit and keeps `include`."""
    assert kit.run(project, "add", RULES_REPO, kit.rules_rev, "--include", "agents/").code == 0
    write_rule(
        kit.rules,
        "agents/work/tests",
        "000003",
        "small-commits",
        "An agent makes small commits",
        "agent",
        "An agent must make small commits.",
    )
    rev = kit.commit_rules()
    try:
        result = kit.run(project, "update", RULES_REPO, rev, "--raw")
        assert result.code == 0, result.out + result.err
        assert _upstream(project)[RULES_REPO] == {"ref": rev, "include": ["agents/"]}
        assert (
            project / "specs/.upstream" / RULES_REPO / "agents/work/tests/000003_small-commits.md"
        ).is_file()
        assert f"M {'specs/.upstream/' + RULES_REPO}" not in result.out
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)


def test_update_stops_for_an_unknown_repository(kit: Kit, project: Path) -> None:
    """`specs update` stops with an error when the repository is not in `spezi.toml`."""
    result = kit.run(project, "update", RULES_REPO, kit.rules_rev, "--raw")
    assert result.code == 1
    assert "is not in spezi.toml" in result.err


def test_update_of_the_kit_runs_the_check(kit: Kit, project: Path) -> None:
    """`specs update` of the kit replaces the kit files and prints the report of the check."""
    result = kit.run(project, "update", "kit", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert f"github.com/frederikbeimgraben/spezi is up to date at {kit.rev}" in result.out
    assert re.search(r"0 specs, [1-9][0-9]* upstream, 0 errors", result.out)


def test_add_without_ref_takes_the_default_branch(kit: Kit, project: Path) -> None:
    """`specs add` without a ref writes the default branch as `ref` and its commit to the lock."""
    result = kit.run(project, "add", RULES_REPO, "--raw")
    assert result.code == 0, result.out + result.err
    assert _upstream(project)[RULES_REPO]["ref"] == "main"
    assert _lock(project)[RULES_REPO]["commit"] == kit.rules_rev


def test_update_without_arguments_updates_each_repository(kit: Kit, project: Path) -> None:
    """`specs update` resolves the ref of each repository again and keeps the refs."""
    assert kit.run(project, "add", RULES_REPO, "main").code == 0
    write_rule(
        kit.rules,
        "agents/work/tests",
        "000003",
        "small-commits",
        "An agent makes small commits",
        "agent",
        "An agent must make small commits.",
    )
    rev = kit.commit_rules()
    try:
        result = kit.run(project, "update", "--raw")
        assert result.code == 0, result.out + result.err
        assert _upstream(project)[RULES_REPO]["ref"] == "main"
        assert _lock(project)[RULES_REPO]["commit"] == rev
        assert f"updated {RULES_REPO} to {rev}" in result.out
        assert f"github.com/frederikbeimgraben/spezi is up to date at {kit.rev}" in result.out
    finally:
        git(kit.rules, "reset", "-q", "--hard", kit.rules_rev, env=kit.env)


def test_update_reads_a_ref_without_spaces(kit: Kit, project: Path) -> None:
    """`specs update` sets the ref of a table that writes `ref="..."` without spaces."""
    assert kit.run(project, "add", RULES_REPO, kit.rules_rev).code == 0
    path = project / "spezi.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(f'ref = "{kit.rules_rev}"', f'ref="{kit.rules_rev}"'))
    result = kit.run(project, "update", RULES_REPO, "main", "--raw")
    assert result.code == 0, result.out + result.err
    assert _upstream(project)[RULES_REPO]["ref"] == "main"


def test_update_writes_include_once(tmp_path: Path) -> None:
    """A new `include` replaces the `include` of the table and does not add a second key."""
    (tmp_path / "spezi.toml").write_text(
        f'[upstream."{RULES_REPO}"]\nref = "v1"\ninclude = ["style/"]\n', encoding="utf-8"
    )
    write_repo(Project.open(tmp_path), RULES_REPO, "v2", ("agents", "style"))
    assert _upstream(tmp_path)[RULES_REPO] == {"ref": "v2", "include": ["agents/", "style/"]}
    write_repo(Project.open(tmp_path), RULES_REPO, "v3")
    assert _upstream(tmp_path)[RULES_REPO] == {"ref": "v3", "include": ["agents/", "style/"]}


def test_a_copy_keeps_a_folder_named_upstream(tmp_path: Path) -> None:
    """A copy holds an area or a topic `upstream`, but no hidden folder and no top `upstream/`."""
    source = tmp_path / "source" / "specs"
    for name in (
        "workflow/upstream/process/000001_one.md",
        "upstream/github.com/o/r/README.md",
        ".templates/TEMPLATE.md",
    ):
        (source / name).parent.mkdir(parents=True, exist_ok=True)
        (source / name).write_text("text\n", encoding="utf-8")
    copy_rules(source.parent, Project.open(tmp_path), RULES_REPO)
    copy = tmp_path / "specs/.upstream" / RULES_REPO
    assert sorted(p.relative_to(copy).as_posix() for p in copy.rglob("*") if p.is_file()) == [
        "workflow/upstream/process/000001_one.md"
    ]
