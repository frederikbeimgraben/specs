"""The formatted output of the command `spezi` for a terminal (spec 000076)."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from spezi.changes import MIGRATED, REPO_LINE, Mark
from spezi.check import Count, summary
from spezi.project import Spec

STATUS_STYLE: Mapping[str, str] = {
    "approved": "green",
    "draft": "yellow",
    "replaced": "dim",
    "removed": "dim strike",
}

MARK_STYLE: Mapping[Mark, str] = {
    Mark.ADDED: "green",
    Mark.MODIFIED: "yellow",
    Mark.DELETED: "red",
}


def console() -> Console:
    """Return the console of stdout."""
    return Console(highlight=False)


def table(specs: Iterable[Spec]) -> Table:
    """Return a table of rules: kind letter, short form, status and title (spec 000072).

    Args:
        specs: The rules.

    Returns:
        The table.
    """
    grid = Table(box=None, header_style="bold", pad_edge=False)
    for name, style in (("Kind", "bold cyan"), ("ID", "bold"), ("Status", ""), ("Title", "")):
        grid.add_column(name, style=style, no_wrap=name != "Title")
    for spec in specs:
        grid.add_row(
            spec.prefix,
            spec.short,
            Text(spec.status, style=STATUS_STYLE.get(spec.status, "")),
            spec.title,
        )
    return grid


def spec_text(text: str) -> Group:
    """Return the front matter as YAML and the body as Markdown.

    Args:
        text: The text of a spec file.

    Returns:
        The two parts.
    """
    _, head, body = text.split("---\n", 2) if text.startswith("---\n") else ("", "", text)
    return Group(
        *((Panel(Syntax(head.rstrip(), "yaml", background_color="default")),) if head else ()),
        Markdown(body),
    )


def report(count: Count, errors: tuple[str, ...], warnings: tuple[str, ...]) -> Group:
    """Return the errors in red, the warnings in yellow and a summary (spec 000076).

    Args:
        count: The counts of the rules of the project and of the copies.
        errors: The errors.
        warnings: The warnings (spec 000093).

    Returns:
        The report. The summary is green without errors and warnings, yellow with only
        warnings, else red.
    """
    mark, style = _summary_mark(errors, warnings)
    return Group(
        *(Text.assemble(("✗ ", "bold red"), (e, "red")) for e in errors),
        *(Text.assemble(("! ", "bold yellow"), (w, "yellow")) for w in warnings),
        Text(f"{mark} {summary(count, errors, warnings)}", style=style),
    )


def _summary_mark(errors: tuple[str, ...], warnings: tuple[str, ...]) -> tuple[str, str]:
    """Return the mark and the style of the summary of the check (spec 000076).

    Args:
        errors: The errors.
        warnings: The warnings.

    Returns:
        Green without errors and warnings, yellow with only warnings, else red.
    """
    match errors, warnings:
        case (), ():
            return "✓", "bold green"
        case (), _:
            return "!", "bold yellow"
        case _:
            return "✗", "bold red"


def done(text: str) -> Text:
    """Return a message of success.

    Args:
        text: The message.

    Returns:
        The message with a green mark.
    """
    return Text.assemble(("✓ ", "bold green"), text)


def outcome(text: str, hints: tuple[str, ...]) -> Group:
    """Return the message of a command with a green mark and its hints below it.

    Each line of the message and each line of a repository gets a green mark (spec 000067,
    000083). A hint of a migration that ran gets a blue mark, as the lines of the changed
    files (spec 000081).

    Args:
        text: The message.
        hints: The hints.

    Returns:
        The message, the migrations, and the other hints.
    """
    return Group(
        *(done(line) for line in text.splitlines()),
        *(_hint(h) for h in hints),
    )


def _hint(hint: str) -> Text:
    """Return one hint: a migration with a blue mark, a repository with a green mark.

    Args:
        hint: The hint.

    Returns:
        The formatted hint.
    """
    match hint:
        case _ if hint.startswith(MIGRATED):
            return Text.assemble(("↻ ", "bold blue"), (hint.removeprefix(MIGRATED), "blue"))
        case _ if REPO_LINE.fullmatch(hint):
            return done(hint)
        case _:
            return Text(hint)


def file_list(changed: tuple[tuple[Mark, str], ...]) -> Group:
    """Return the changed files as in `git status --short`, with a color per mark (spec 000077).

    Args:
        changed: The mark and the path of each change.

    Returns:
        One line for each file.
    """
    return Group(
        *(Text.assemble((f"{m} ", f"bold {MARK_STYLE[m]}"), (p, MARK_STYLE[m])) for m, p in changed)
    )
