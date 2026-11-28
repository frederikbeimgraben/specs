"""Migration 6: remove the comments of the template from `spezi.toml` (spec 000078).

Before this migration, the template of `spezi.toml` had a comment for each key. The migration
removes each line that is a comment of an earlier template, and then the empty lines at the
start and the second of two empty lines. A comment of a person stays.
"""

from __future__ import annotations

import re
from pathlib import Path

from spezi.changes import write_text
from spezi.project import CONFIG_NAME

COMMIT = "710d7ff8f429d8feb1aa93e4e683531403d236b1"
DESCRIPTION = "remove the comments of the template from spezi.toml"
TEMPLATE_COMMENTS = frozenset(
    (
        '# "C/specs/content/000025" = "The specs of this project are in German."',
        "# .envrc with use flake.",
        "# CLAUDE.md with the line @AGENTS.md. It needs agents = true.",
        "# Settings of scripts/check_specs.py. Each key is optional.",
        "# Settings of the specs command (000013). Each key is optional.",
        "# Settings of the specs command (000078). Each key is optional.",
        "# Settings of the spezi command (000078). Each key is optional.",
        "# The CI job, for example .github/workflows/specs.yml.",
        "# The CI job, for example .github/workflows/spezi.yml.",
        "# The MCP server specs in .mcp.json.",
        "# The MCP server spezi in .mcp.json.",
        "# The base branch. A spec number that this branch took after your"
        " branch left it is an error.",
        "# The block with the rules for agents in AGENTS.md (000079).",
        "# The file types of the code in code_dirs.",
        "# The folders that hold code. The check finds a § reference to a rule"
        " that does not exist.",
        "# The folders that hold code. The check finds a reference to a rule that does not exist.",
        "# The full name of this project, <host>/<group>/.../<repo>. A"
        " transitive upstream of this name",
        "# The highest count of elements in one structure diagram (000037).",
        "# The optional parts of the kit (000084). true: specs install writes"
        " the part and keeps it.",
        "# The optional parts of the kit (000084). true: spezi install writes"
        " the part and keeps it.",
        "# The rules of a different repository, copied to"
        " .specs/upstream/<host>/<group>/.../<repo>/ (000048).",
        "# The rules of a different repository, copied to"
        " .specs/upstream/<host>/<owner>/<repo>/ (000048).",
        "# The rules of a different repository, copied to"
        " specs/.upstream/<host>/<group>/.../<repo>/ (000048).",
        "# The rules of a different repository, copied to"
        " specs/upstream/<host>/<owner>/<repo>/ (000048).",
        "# The skills .claude/skills/spec-*.",
        "# The skills .claude/skills/spezi-*.",
        "# Without include, the copy holds all rules. specs add --include sets it.",
        "# Without include, the copy holds all rules. spezi add --include sets it.",
        '# [upstream."github.com/frederikbeimgraben/specs".exclude]',
        '# [upstream."github.com/frederikbeimgraben/specs"]',
        "# commit of its spezi.lock (000092). spezi init, spezi add and spezi"
        " update ask for it, and -r",
        "# false: specs install removes it. specs init and specs update also"
        " follow these switches.",
        "# false: spezi install removes it. spezi init and spezi update also"
        " follow these switches.",
        "# flake.nix with a devShell with the command specs.",
        "# flake.nix with a devShell with the command spezi.",
        "# gets no copy (000092). spezi init asks for it.",
        "# github or gitlab.",
        "# github, gitlab or codeberg.",
        "# include is optional: the folders below specs/ that the copy holds,"
        ' for example ["style/python/"].',
        '# ref = "<commit>"',
        "# ref is a tag, a branch or a commit. specs.lock holds the commit of the copy (000082).",
        "# ref is a tag, a branch or a commit. spezi.lock holds the commit of the copy (000082).",
        "# ref is the commit of the copy. Change it with specs update or specs add.",
        "# ref is the tag or the commit of the copy. A project rule drops a rule of the copy with",
        "# ref is the tag or the commit of the copy. exclude maps a rule ID to"
        " the reason (000049).",
        "# replaces in its front matter (000049).",
        '# repo = "github.com/<owner>/<repo>"',
        "# specs update resolves ref again, specs add adds a repository, specs"
        " install changes no ref.",
        "# spezi update resolves ref again, spezi add adds a repository, spezi"
        " install changes no ref.",
        "# takes each one.",
        "# transitive is optional: the upstreams of this repository that the"
        " project also copies, at the",
    )
)


def clean(text: str) -> str:
    """Return a text of `spezi.toml` without the comments of the templates.

    Args:
        text: The text.

    Returns:
        The text without the lines of `TEMPLATE_COMMENTS`, also with `(spec <ref>)` in place of
        `(<ref>)`, without empty lines at the start and with one empty line at most between two
        lines.
    """
    return re.sub(
        r"\n{3,}",
        "\n\n",
        "".join(
            line
            for line in text.splitlines(keepends=True)
            if line.rstrip().replace("(spec ", "(") not in TEMPLATE_COMMENTS
        ).lstrip("\n"),
    )


def project(root: Path) -> None:
    """Remove the comments of the templates from `spezi.toml` of a project.

    Args:
        root: The root of the project.
    """
    path = root / CONFIG_NAME
    if path.is_file():
        write_text(path, clean(path.read_text(encoding="utf-8")))


def copy(folder: Path) -> None:
    """Change nothing: a copy holds only the `specs/` folder, without `spezi.toml`.

    Args:
        folder: The folder of the copy.
    """
    del folder
