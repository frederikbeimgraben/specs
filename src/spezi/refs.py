"""References to rules in a text: `(spec <ref>)` (spec 000017).

A reference holds a list of short forms, with `, ` between two items. In a Markdown file, a
rule number must not stand outside a reference, except in the front matter, in the tables that
`spezi` writes, and in backticks or in a code block.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from spezi.agents import BLOCK
from spezi.project import LONG_LOCAL, NUMBER, PREFIXES, REPO

SPEC_REF = re.compile(r"\(spec ([^()\n]*)\)")
ITEM = re.compile(rf"(?:{REPO}:)?{NUMBER}")
LOOSE_ITEM = re.compile(rf"(?:{REPO}:)?(?:{LONG_LOCAL}|{NUMBER})")
OLD_REF = re.compile(rf"§ ?((?:{REPO}:)?(?:(?:{PREFIXES})/[a-z0-9/-]+/)?{NUMBER})(?![0-9])")
BARE_REF = re.compile(rf"(?<![\w/.:§-])((?:{REPO}:)?{NUMBER})(?![\w-])")
FRONT_MATTER = re.compile(r"\A---\n.*?^---$", re.MULTILINE | re.DOTALL)
FENCE = re.compile(r"^ *(```|~~~)[^\n]*\n.*?^ *\1[^\n]*$", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
TABLE_ROW = re.compile(r"^\|.*$", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class Item:
    """One item of a `(spec ...)` reference.

    Attributes:
        text: The text of the item.
        start: The offset of the first character in the text.
        end: The offset after the last character in the text.
    """

    text: str
    start: int
    end: int


def _blank(text: str, pattern: re.Pattern[str]) -> str:
    """Replace each match with spaces, but keep the line breaks.

    Args:
        text: The text.
        pattern: The parts to remove.

    Returns:
        The text with the same length and the same lines.
    """
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m[0]), text)


def prose(text: str, rel: str = "") -> str:
    """Return the text of a Markdown file without the parts that the rule does not cover.

    Args:
        text: The text of the file.
        rel: The path of the file below the root of the project.

    Returns:
        The text with spaces in place of the front matter, the code blocks, the text in
        backticks and the tables that `spezi` writes.
    """
    plain = _blank(_blank(_blank(text, FRONT_MATTER), FENCE), INLINE_CODE)
    match rel:
        case "specs/README.md":
            return _blank(plain, TABLE_ROW)
        case "AGENTS.md":
            return _blank(plain, BLOCK)
        case _:
            return plain


def items(text: str) -> Iterator[Item]:
    """Return the items of each `(spec ...)` reference in a text.

    Args:
        text: The text.

    Returns:
        The items, in the order of the text.
    """
    return (
        Item(part, start, start + len(part))
        for m in SPEC_REF.finditer(text)
        for part, start in _parts(m[1], m.start(1))
    )


def _parts(inner: str, offset: int) -> Iterator[tuple[str, int]]:
    """Return each part of a list with its offset.

    Args:
        inner: The text between `(spec ` and `)`.
        offset: The offset of the text.

    Returns:
        The parts and their offsets.
    """
    starts = (0, *(m.end() for m in re.finditer(", ", inner)))
    ends = (*(m.start() for m in re.finditer(", ", inner)), len(inner))
    return ((inner[s:e], offset + s) for s, e in zip(starts, ends, strict=True))


def bad_references(text: str) -> Iterator[str]:
    """Return each `(spec ...)` reference with a rule number and more than short forms.

    A reference without a rule number, for example `(spec <number>)`, is a placeholder.

    Args:
        text: The text.

    Returns:
        The whole references.
    """
    return (
        m[0]
        for m in SPEC_REF.finditer(text)
        if re.search(r"[0-9]{6}", m[1])
        and not all(ITEM.fullmatch(part) for part, _ in _parts(m[1], 0))
    )


def references(text: str) -> Iterator[str]:
    """Return the short form of each item that is a short form.

    Args:
        text: The text.

    Returns:
        The short forms.
    """
    return (i.text for i in items(text) if ITEM.fullmatch(i.text))


def old_references(text: str) -> Iterator[str]:
    """Return each rule ID after a `§`.

    Args:
        text: The text.

    Returns:
        The rule IDs.
    """
    return (m[1] for m in OLD_REF.finditer(text))


def bare_numbers(text: str) -> Iterator[str]:
    """Return each rule number outside a `(spec ...)` reference.

    Args:
        text: The prose of a Markdown file (see `prose`).

    Returns:
        The rule numbers and the foreign short forms.
    """
    return (m[1] for m in BARE_REF.finditer(_blank(text, SPEC_REF)))


def markdown_files(root: Path, *, new: bool = False) -> tuple[str, ...]:
    """Return the Markdown files that git tracks in a project.

    Args:
        root: The root of the project.
        new: True to add the new files that git does not ignore.

    Returns:
        The paths below the root, or nothing outside a git repository.
    """
    try:
        listed = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                *(("--others", "--cached", "--exclude-standard") if new else ()),
                "--",
                "*.md",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return ()
    return tuple(p for p in listed.split("\0") if p and (root / p).is_file())
