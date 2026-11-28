"""Migration 6: write each reference to a rule as `(spec <ref>)` (spec 000017).

The old kit wrote a reference in the code with a section sign before the short form, and a
reference in a Markdown file as the bare rule number. The migration writes each of them as
`(spec <ref>)`. A list of references in one pair of parentheses becomes one list, and a range
`<a> to <b>` becomes the list of each number from `a` to `b`. In a Markdown file, the migration
does not change the front matter, a code block, text in backticks or a table that `spezi`
writes.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from functools import reduce
from pathlib import Path

from spezi.changes import write_text
from spezi.project import CONFIG_NAME, NUMBER, PREFIXES, REPO, hidden, read_config
from spezi.refs import SPEC_REF, markdown_files, prose

COMMIT = "6bbce6f83d3451c3d3b34ecb35296eb43aeaea1a"
DESCRIPTION = "write each reference to a rule as (spec <ref>)"

RULE = rf"(?:{REPO}:)?(?:(?:{PREFIXES})/[a-z0-9/-]+/)?{NUMBER}"
OLD = rf"§ ?{RULE}(?![0-9])"
BARE = rf"(?<![\w/.:§-]){RULE}(?![\w-])"
JOIN = r"(?:, | to )"
OLD_GROUP = re.compile(rf"\(({OLD}(?:{JOIN}{OLD})*)\)")
OLD_SINGLE = re.compile(rf"§ ?({RULE})(?![0-9])")
BARE_GROUP = re.compile(rf"\(({BARE}(?:{JOIN}{BARE})*)\)")
BARE_SINGLE = re.compile(rf"({BARE})")
type Change = Callable[[re.Match[str]], str]

RANGE = re.compile(rf"({RULE}) to ({RULE})")


def _expand(match: re.Match[str]) -> str:
    """Return the list of each number of a range.

    Args:
        match: A range `<a> to <b>`.

    Returns:
        The numbers from `a` to `b`, with `, ` between them, with the repository of `a`.
    """
    first, last = match[1], match[2]
    repo, _, number = first.rpartition(":")
    return ", ".join(
        f"{repo}:{n:06d}" if repo else f"{n:06d}"
        for n in range(int(number[-6:]), int(last[-6:]) + 1)
    )


def _list(inner: str) -> str:
    """Return the items of an old list as the text of a `(spec ...)` reference.

    Args:
        inner: The text between the parentheses.

    Returns:
        The reference.
    """
    return f"(spec {RANGE.sub(_expand, inner.replace('§ ', '').replace('§', ''))})"


def _code(text: str) -> str:
    """Write each old reference of a code file as `(spec <ref>)`.

    Args:
        text: The text of the file.

    Returns:
        The new text.
    """
    return OLD_SINGLE.sub(lambda m: f"(spec {m[1]})", OLD_GROUP.sub(lambda m: _list(m[1]), text))


def _step(text: str, rel: str, pattern: re.Pattern[str], change: Change) -> str:
    """Change each match of a pattern that lies in the prose and in no reference.

    Args:
        text: The text of the file.
        rel: The path of the file below the root of the project.
        pattern: The old form.
        change: The new text of a match.

    Returns:
        The new text.
    """
    mask = prose(text, rel)
    spans = tuple((m.start(), m.end()) for m in SPEC_REF.finditer(text))
    return pattern.sub(
        lambda m: (
            change(m)
            if mask[m.start() : m.end()] == m[0] and not any(s <= m.start() < e for s, e in spans)
            else m[0]
        ),
        text,
    )


def _markdown(text: str, rel: str) -> str:
    """Write each old reference of a Markdown file as `(spec <ref>)`.

    Args:
        text: The text of the file.
        rel: The path of the file below the root of the project.

    Returns:
        The new text.
    """
    steps: tuple[tuple[re.Pattern[str], Change], ...] = (
        (OLD_GROUP, lambda m: _list(m[1])),
        (OLD_SINGLE, lambda m: f"(spec {m[1]})"),
        (BARE_GROUP, lambda m: _list(m[1])),
        (BARE_SINGLE, lambda m: f"(spec {m[1]})"),
    )
    return reduce(lambda done, step: _step(done, rel, *step), steps, text)


def _rewrite(path: Path, change: Callable[[str], str]) -> None:
    """Change a text file when the change gives a different text.

    Args:
        path: The file.
        change: The change of the text.
    """
    text = path.read_text(encoding="utf-8")
    new = change(text)
    if new != text:
        write_text(path, new)


def project(root: Path) -> None:
    """Write the references in the code and in the Markdown files of the project.

    Args:
        root: The root of the project.
    """
    config = read_config(root / CONFIG_NAME)
    code = (
        p
        for folder in config.code_dirs
        for p in sorted((root / folder).rglob("*"))
        if p.is_file() and p.suffix in config.code_suffixes and "node_modules" not in p.parts
    )
    specs = root / "specs"
    rules = (
        p.relative_to(root).as_posix()
        for p in sorted(specs.rglob("*.md"))
        if p.is_file() and not hidden(p.relative_to(specs))
    )
    texts = tuple(
        dict.fromkeys(
            (
                *rules,
                *(
                    rel
                    for rel in markdown_files(root)
                    if not rel.startswith("specs/") or not hidden(Path(rel).relative_to("specs"))
                ),
            )
        )
    )
    for path in code:
        _rewrite(path, _code)
    for rel in texts:
        _rewrite(root / rel, lambda text, rel=rel: _markdown(text, rel))


def copy(folder: Path) -> None:
    """Write the references in the rules of a copy.

    Args:
        folder: The folder of the copy.
    """
    for path in sorted(p for p in folder.rglob("*.md") if p.is_file()):
        rel = "specs/README.md" if path == folder / "README.md" else ""
        _rewrite(path, lambda text, rel=rel: _markdown(text, rel))
