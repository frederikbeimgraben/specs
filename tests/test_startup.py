"""Tests of the libraries that a command loads (spec 000095)."""

from __future__ import annotations

import subprocess
import sys

import pytest
from conftest import ROOT, Kit

PROBE = """
import runpy
import sys

sys.argv = ["spezi", *sys.argv[1:]]
try:
    runpy.run_module("spezi", run_name="__main__")
except SystemExit:
    pass
print(sorted({name.split(".")[0] for name in sys.modules} & {"mcp", "lsprotocol", "pygls"}))
"""


@pytest.mark.parametrize("args", [("--help",), ("check", "--raw"), ("list", "--raw")])
def test_a_command_loads_no_server_library(kit: Kit, args: tuple[str, ...]) -> None:
    """A command other than `spezi mcp` and `spezi lsp` loads no server library."""
    done = subprocess.run(
        (sys.executable, "-c", PROBE, *args),
        cwd=ROOT,
        env=dict(kit.env),
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.stdout.splitlines()[-1] == "[]", done.stdout + done.stderr
