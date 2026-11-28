"""Tests of the check of the rules of ASD-STE100 (spec 000093)."""

from __future__ import annotations

import json
from pathlib import Path

from conftest import Kit, write_rule
from lsprotocol import types

from spezi.lsp import diagnostics
from spezi.ste import findings

LONG = " ".join(["word"] * 26) + "."
SHORT = " ".join(["word"] * 25) + "."


def _rule(project: Path, text: str) -> Path:
    """Write one style rule with the given text to the project.

    Args:
        project: The root of the project.
        text: The rule text.

    Returns:
        The file.
    """
    (project / "src").mkdir(exist_ok=True)
    return write_rule(project, "style/code/names", "000100", "names", "Names", "style", text)


def _messages(body: str) -> tuple[str, ...]:
    """Return the messages of the warnings of a body.

    Args:
        body: The body.

    Returns:
        The messages.
    """
    return tuple(f.message for f in findings(body))


def test_ste_finds_a_long_sentence() -> None:
    """A sentence with more than 25 words is a warning at the line where it starts."""
    found = findings(f"# Title\n\nA name must be short.\n{SHORT}\n\n{LONG}\n")
    assert [f.line for f in found] == [6]
    assert found[0].message == "a sentence has 26 words, more than 25 (000093)"


def test_ste_counts_a_sentence_over_two_lines_once() -> None:
    """A sentence that a line break splits counts as one sentence."""
    half = " ".join(["word"] * 13)
    assert _messages(f"{half}\n{half}.\n") == ("a sentence has 26 words, more than 25 (000093)",)


def test_ste_reads_only_the_prose() -> None:
    """Code blocks, inline code, headings and link targets do not count."""
    code = " ".join(["`x`"] * 30)
    link = "[word](" + "/".join(["a b"] * 30) + ")"
    words = " ".join(["word"] * 24)
    body = f"# {LONG}\n\n```text\n{LONG}\n```\n\n{SHORT[:-1]} {code}.\n\n{words} {link}\n"
    assert findings(body) == ()


def test_ste_reads_each_list_item_and_cell_alone() -> None:
    """Each list item and each table cell is a separate text."""
    item = " ".join(["word"] * 15)
    body = f"- {item}\n- {item}\n\n| {item} | {item} |\n| --- | --- |\n| {item} | {item} |\n"
    assert findings(body) == ()
    assert _messages(f"- {LONG}\n")
    assert _messages(f"| a | {LONG} |\n")


def test_ste_keeps_an_abbreviation_in_the_sentence() -> None:
    """An abbreviation of the list does not end a sentence, e.g. only before a capital letter."""
    half = " ".join(["word"] * 13)
    assert _messages(f"{half} vs. {half}.\n")
    assert _messages(f"{half} e.g. {half}.\n")
    assert not _messages(f"{half} e.g. Word {half}.\n")


def test_ste_warns_on_passive_voice() -> None:
    """A form of be before a participle is a warning."""
    assert _messages("The file is written by the command.\n") == (
        "possible passive voice: 'is written' (000093)",
    )
    assert not _messages("The file is short.\n")


def test_ste_warns_on_two_verbs_of_one_group() -> None:
    """The second verb of a group of synonyms gets a warning at its first place."""
    found = findings("Check the file.\n\nThen verify the name.\n\nVerify it again.\n")
    assert [(f.line, f.message) for f in found] == [
        (3, "one word for one thing: 'verify' and 'Check' have one meaning (000093)")
    ]


def test_ste_warns_on_two_instructions() -> None:
    """Two signal words in one sentence are a warning. `must not` counts as one."""
    assert _messages("It must stop and must not write.\n") == (
        "a sentence has 2 instructions (000093)",
    )
    assert not _messages("It must not write.\n")


def test_check_shows_the_findings(kit: Kit, project: Path) -> None:
    """`spezi check` shows the warnings with their lines and counts them."""
    _rule(project, f"A name must be short. The name is used by the code.\n\n{LONG}")
    result = kit.run(project, "install", "--raw")
    rel = "specs/style/code/names/000100_names.md"
    lines = result.out.splitlines()
    assert result.code == 0, result.out
    assert lines.index(f"{rel}:15: warning: possible passive voice: 'is used' (000093)") < (
        lines.index(f"{rel}:17: warning: a sentence has 26 words, more than 25 (000093)")
    )
    assert lines[-1].endswith(", 0 errors, 2 warnings")


def test_check_passes_with_only_warnings(kit: Kit, project: Path) -> None:
    """A warning does not change the exit code."""
    _rule(project, "A name must be short. The name is used by the code.")
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out
    assert result.out.splitlines()[-1].endswith(", 0 errors, 1 warnings")


def test_check_without_ste(kit: Kit, project: Path) -> None:
    """With `ste = false`, the check does not check the rules of ASD-STE100."""
    config = project / "spezi.toml"
    config.write_text(
        config.read_text(encoding="utf-8").replace("ste = true", "ste = false"), encoding="utf-8"
    )
    _rule(project, f"A name must be short. The name is used by the code.\n\n{LONG}")
    result = kit.run(project, "install", "--raw")
    assert result.code == 0, result.out
    assert "(000093)" not in result.out


def test_check_gives_the_warnings_as_json(kit: Kit, project: Path) -> None:
    """The JSON of the check holds `warnings` with objects like the errors."""
    _rule(project, "A name must be short. The name is used by the code.")
    kit.run(project, "install", "--raw")
    data = json.loads(kit.run(project, "check", "--json").out)
    assert data["warnings"] == [
        {
            "file": "specs/style/code/names/000100_names.md",
            "line": 15,
            "message": "possible passive voice: 'is used'",
            "rule": "000093",
        }
    ]


def test_lsp_shows_a_warning_with_the_severity_warning(tmp_path: Path) -> None:
    """The language server gives a warning the severity warning."""
    (tmp_path / "a.md").write_text("one\ntwo\n", encoding="utf-8")
    found = diagnostics(tmp_path, ("a.md:2: warning: possible passive voice (000093)",))
    diagnostic = found[(tmp_path / "a.md").resolve()][0]
    assert diagnostic.severity == types.DiagnosticSeverity.Warning
    assert diagnostic.message == "possible passive voice (000093)"
    assert diagnostic.range.start.line == 1
