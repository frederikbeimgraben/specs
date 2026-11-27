"""Write the rules for agents to a block in `AGENTS.md` (§000079).

The block holds the A and W rules with the status `approved`. The text outside the block stays
as the person wrote it. `CLAUDE.md` imports `AGENTS.md` with the line `@AGENTS.md`.
"""

from __future__ import annotations

import re
from pathlib import Path

from specs_kit.changes import write_text
from specs_kit.index import row
from specs_kit.project import Spec

AGENTS = "AGENTS.md"
CLAUDE = "CLAUDE.md"
IMPORT = "@AGENTS.md"
BEGIN = "<!-- specs:begin (written by specs install, do not edit) -->"
OLD_BEGIN = "<!-- specs:begin (written by specs check --write, do not edit) -->"
END = "<!-- specs:end -->"
BLOCK = re.compile(
    rf"^(?:{re.escape(BEGIN)}|{re.escape(OLD_BEGIN)})\n.*?^{re.escape(END)}\n?",
    re.MULTILINE | re.DOTALL,
)
PREFIXES = frozenset({"A", "W"})
PREAMBLE = (
    "## Rules for agents",
    "",
    "The rules for agents (A) and the workflow rules (W) that apply to this project. Before a",
    "task, read each rule in this table that applies to the task. A rule wins over other text",
    "in this file. The ID links to the rule.",
)


def _rules(specs: tuple[Spec, ...]) -> tuple[Spec, ...]:
    """Return the approved A and W rules of a list of specs.

    Args:
        specs: The specs.

    Returns:
        The rules.
    """
    return tuple(s for s in specs if s.prefix in PREFIXES and s.status == "approved")


def block(specs: tuple[Spec, ...], upstream: tuple[Spec, ...]) -> str:
    """Return the block with the rules for agents, with its marker lines.

    Args:
        specs: The specs of the project.
        upstream: The specs of the copies that apply.

    Returns:
        The block.
    """
    rules = (
        *sorted(_rules(specs), key=lambda s: s.full_id),
        *sorted(_rules(upstream), key=lambda s: s.long),
    )
    return "\n".join(
        (
            BEGIN,
            *PREAMBLE,
            "",
            *(
                ("| ID | Title | Status |", "| --- | --- | --- |", *(row(s) for s in rules))
                if rules
                else ("No rules.",)
            ),
            END,
            "",
        )
    )


def merge(current: str | None, new: str) -> str:
    """Return the text of `AGENTS.md` with the new block.

    Args:
        current: The text of the file, or None when it does not exist.
        new: The block.

    Returns:
        The new text of the file.
    """
    match current:
        case None:
            return new
        case str() if BLOCK.search(current):
            return BLOCK.sub(lambda _: new, current, count=1)
        case _:
            return f"{current.rstrip()}\n\n{new}" if current.strip() else new


def claude_import(root: Path) -> tuple[str, ...]:
    """Create `CLAUDE.md` with the import of `AGENTS.md` when it does not exist.

    Args:
        root: The root of the project.

    Returns:
        The hints: the line to add when `CLAUDE.md` exists without the import.
    """
    path = root / CLAUDE
    match path.exists():
        case False:
            write_text(path, f"{IMPORT}\n")
            return ()
        case True if IMPORT in path.read_text(encoding="utf-8").splitlines() or (
            (root / AGENTS).exists() and (root / AGENTS).resolve() == path.resolve()
        ):
            return ()
        case True:
            return (f"hint: add the line {IMPORT} to {CLAUDE} to load the rules for agents",)
