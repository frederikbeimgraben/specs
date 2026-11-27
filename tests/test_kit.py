"""Tests of `specs init`, `specs update` and `specs add` (§000066, §000067, §000068)."""

from __future__ import annotations

import tomllib
from pathlib import Path

from conftest import RULES_REPO, Kit, git, write_rule

KIT = "specs/.upstream/github.com/frederikbeimgraben/specs"


def _config(project: Path) -> dict[str, object]:
    """Return the parsed `specs.toml` of a project.

    Args:
        project: The root of the project.

    Returns:
        The settings.
    """
    return tomllib.loads((project / "specs.toml").read_text(encoding="utf-8"))


def _upstream(project: Path) -> dict[str, dict[str, object]]:
    """Return the upstream tables of `specs.toml`.

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
    assert _upstream(project)["github.com/frederikbeimgraben/specs"]["ref"] == kit.rev
    for name in (
        f"{KIT}/workflow/specs/process/000001_precedence.md",
        "specs/.templates/TEMPLATE.md",
        ".claude/skills/spec-write/SKILL.md",
        ".github/workflows/specs.yml",
        ".mcp.json",
        ".envrc",
        "specs/README.md",
    ):
        assert (project / name).is_file(), name


def test_init_ci_runs_on_the_base_branch(kit: Kit, project: Path) -> None:
    """The CI job runs for a push to the branch of `base_ref`."""
    assert "branches: [main]" in (project / ".github/workflows/specs.yml").read_text(
        encoding="utf-8"
    )


def test_init_keeps_an_existing_flake(kit: Kit, empty: Path) -> None:
    """`specs init` changes no `flake.nix` that exists and prints the lines to add."""
    before = (empty / "flake.nix").read_text(encoding="utf-8")
    result = kit.run(empty, "init", "--forge", "github", "--raw")
    assert result.code == 0, result.out + result.err
    assert (empty / "flake.nix").read_text(encoding="utf-8") == before
    assert f'inputs.specs.url = "github:frederikbeimgraben/specs/{kit.rev}";' in result.out


def test_init_takes_the_forge_from_the_remote(kit: Kit, empty: Path) -> None:
    """Without `--forge`, init reads the forge from `git remote origin`."""
    git(empty, "remote", "add", "origin", "https://codeberg.org/me/app.git", env=kit.env)
    result = kit.run(empty, "init", "--raw")
    assert result.code == 0, result.out + result.err
    assert _config(empty)["forge"] == "codeberg"
    assert (empty / ".forgejo/workflows/specs.yml").is_file()


def test_init_stops_when_the_kit_is_there(kit: Kit, project: Path) -> None:
    """`specs init` stops with an error when `specs.toml` exists."""
    result = kit.run(project, "init", "--forge", "github", "--raw")
    assert result.code == 1
    assert "specs.toml exists" in result.err


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


def test_add_stops_for_a_repository_in_the_settings(kit: Kit, project: Path) -> None:
    """`specs add` stops with an error when the repository is in `specs.toml` already."""
    assert kit.run(project, "add", RULES_REPO, kit.rules_rev, "--raw").code == 0
    result = kit.run(project, "add", RULES_REPO, kit.rules_rev, "--raw")
    assert result.code == 1
    assert "is in specs.toml" in result.err


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
    """`specs update` stops with an error when the repository is not in `specs.toml`."""
    result = kit.run(project, "update", RULES_REPO, kit.rules_rev, "--raw")
    assert result.code == 1
    assert "is not in specs.toml" in result.err


def test_update_of_the_kit_runs_the_check(kit: Kit, project: Path) -> None:
    """`specs update` of the kit replaces the kit files and prints the report of the check."""
    result = kit.run(project, "update", kit.rev, "--raw")
    assert result.code == 0, result.out + result.err
    assert f"updated to {kit.rev}" in result.out
    assert "0 specs, 0 errors" in result.out
