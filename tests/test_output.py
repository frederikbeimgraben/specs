"""Tests of the output of the command (§000076, §000077) and of the MCP tools (§000074)."""

from __future__ import annotations

import os
import pty
import re
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import Kit

ANSI = re.compile(r"\x1b\[")


def _on_terminal(kit: Kit, cwd: Path, *args: str) -> str:
    """Run the command with stdout on a terminal and return its output.

    Args:
        kit: The kit.
        cwd: The folder to run in.
        *args: The arguments.

    Returns:
        The output.
    """
    main, side = pty.openpty()
    with subprocess.Popen(
        (sys.executable, "-m", "specs_kit", *args),
        cwd=cwd,
        env={**kit.env, "COLUMNS": "200", "TERM": "xterm-256color"},
        stdout=side,
        stderr=side,
    ) as process:
        os.close(side)
        chunks: list[bytes] = []
        while True:
            try:
                chunk = os.read(main, 4096)
            except OSError:
                break
            if not chunk:
                break
            chunks.append(chunk)
        process.wait()
    os.close(main)
    return b"".join(chunks).decode("utf-8", "replace")


def test_terminal_output_has_color(kit: Kit, project: Path) -> None:
    """On a terminal, the output is formatted."""
    assert ANSI.search(_on_terminal(kit, project, "check"))


def test_raw_output_has_no_color(kit: Kit, project: Path) -> None:
    """With `--raw`, the output is plain text also on a terminal."""
    assert not ANSI.search(_on_terminal(kit, project, "list", "--raw"))


def test_changed_files_are_sorted_and_relative(kit: Kit, empty: Path) -> None:
    """A command lists each changed file once, sorted, relative, as in `git status --short`."""
    lines = [
        line
        for line in kit.run(empty, "init", "--forge", "github", "--raw").out.splitlines()
        if re.match(r"^[AMD] ", line)
    ]
    paths = [line[2:] for line in lines]
    assert paths == sorted(paths, key=lambda p: Path(p).parts)
    assert "A specs.toml" in lines
    assert all(not p.startswith("/") for p in paths)


def test_a_write_with_the_same_content_is_no_change(kit: Kit, project: Path) -> None:
    """`check --write` on a current project lists no file."""
    out = kit.run(project, "check", "--write", "--raw").out
    assert not [line for line in out.splitlines() if re.match(r"^[AMD] ", line)]


def test_mcp_tools_give_the_plain_results(
    kit: Kit, project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The MCP tools give the same results as the commands, and `check` writes no index."""
    for key, value in kit.env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.chdir(project)
    from specs_kit import mcp_server

    (project / "specs" / "README.md").write_text("changed\n", encoding="utf-8")
    assert "not an exact copy" in mcp_server.check()
    assert (project / "specs" / "README.md").read_text(encoding="utf-8") == "changed\n"
    assert mcp_server.list_specs() == kit.run(project, "list", "--raw").out
    (project / "src").mkdir()
    result = mcp_server.new("F", "app/login", "sign-in", "Sign in", ["src"], "someone")
    assert "A specs/requirements/functional/app/login/000001_sign-in.md" in result
