"""Tests of the references to rules and of migration 6 (spec 000017, 000081)."""

from __future__ import annotations

from spezi.migrations.m0006_spec_references import _code, _markdown
from spezi.refs import bad_references, bare_numbers, items, old_references, prose, references


def test_a_list_gives_each_item() -> None:
    """Each item of a list is one reference, with its place in the text."""
    text = "See (spec 000088, github.com/o/r:000012)."
    assert [(i.text, text[i.start : i.end]) for i in items(text)] == [
        ("000088", "000088"),
        ("github.com/o/r:000012", "github.com/o/r:000012"),
    ]
    assert list(references(text)) == ["000088", "github.com/o/r:000012"]


def test_a_range_and_a_long_form_are_bad() -> None:
    """A range and a long form are no short forms; a placeholder is no reference."""
    text = "(spec 000070 to 000073) (spec C/specs/format/000012) (spec <number>)"
    assert list(bad_references(text)) == ["(spec 000070 to 000073)", "(spec C/specs/format/000012)"]


def test_the_prose_has_no_code_and_no_front_matter() -> None:
    """A bare number in the front matter, in backticks or in a code block is no error."""
    text = '---\nid: "000017"\n---\n\nSee `000018`.\n\n```\n000019\n```\n\nSee 000020.\n'
    assert list(bare_numbers(prose(text))) == ["000020"]
    assert list(old_references("See §000021.")) == ["000021"]


def test_the_migration_writes_the_code() -> None:
    """A section sign, a list and a range in the code become `(spec ...)`."""
    assert _code("# See §000017.") == "# See (spec 000017)."
    assert _code("(§000088, §000089)") == "(spec 000088, 000089)"
    assert _code("(§000070 to §000072)") == "(spec 000070, 000071, 000072)"


def test_the_migration_writes_the_markdown() -> None:
    """A bare number and a list become `(spec ...)`; the heading, code and front matter stay."""
    text = (
        '---\nid: "000100"\n---\n\n# Rule 000100\n\n'
        "The kind folders of 000004 (000048, 000082). See `000017`.\n"
    )
    assert _markdown(text, "specs/a/b/000100_x.md") == (
        '---\nid: "000100"\n---\n\n# Rule 000100\n\n'
        "The kind folders of (spec 000004) (spec 000048, 000082). See `000017`.\n"
    )


def test_the_migration_changes_nothing_twice() -> None:
    """A second run of the migration changes nothing."""
    text = "See 000004 and (000048).\n"
    once = _markdown(text, "README.md")
    assert _markdown(once, "README.md") == once
    assert _code(_code("# §000017")) == "# (spec 000017)"
