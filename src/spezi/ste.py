"""Check the rules of ASD-STE100 in the text of a spec (spec 000093).

The check reads the prose of the body: paragraphs, list items and table cells. It finds sentences
with more than 25 words (an error), and possible passive voice, two verbs of one group of
synonyms and more than one instruction in a sentence (warnings).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache, reduce
from importlib import resources

MAX_WORDS = 25
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#")
TABLE_RULE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|[0-9]{1,9}[.)])\s+")
INLINE_CODE = re.compile(r"`+[^`]*`+")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
HTML = re.compile(r"<!--.*?-->|<[A-Za-z][A-Za-z0-9+.-]*:[^<>\s]*>")
TOKEN = re.compile(r"\S+")
WORD_CHAR = re.compile(r"[^\W_]")
SENTENCE_END = re.compile(r"[.!?][\"'”’)\]*_]*$")
OPENERS = "\"'“‘([*_"
DOTTED = re.compile(r"(?:[a-z]\.){2,}", re.IGNORECASE)
SIGNAL = re.compile(r"\b(?:must(?:\s+not)?|do\s+not|never|shall)\b", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class Finding:
    """One result of the check.

    Attributes:
        line: The line in the body where the sentence starts, from 1.
        message: The text, with the rule number at the end.
        warning: True for a warning, False for an error.
    """

    line: int
    message: str
    warning: bool


@dataclass(frozen=True, slots=True)
class Piece:
    """One line of a text, with its line in the body.

    Attributes:
        line: The line in the body, from 1.
        text: The prose of the line, with code and link targets masked.
    """

    line: int
    text: str


@dataclass(frozen=True, slots=True)
class Sentence:
    """One sentence and the line where it starts.

    Attributes:
        line: The line in the body, from 1.
        text: The text of the sentence.
    """

    line: int
    text: str


@dataclass(frozen=True, slots=True)
class State:
    """The state of the reader of the body.

    Attributes:
        texts: The finished texts.
        current: The lines of the open text.
        fence: The open code fence, or an empty string.
    """

    texts: tuple[tuple[Piece, ...], ...] = ()
    current: tuple[Piece, ...] = ()
    fence: str = ""


@cache
def _words(name: str) -> tuple[str, ...]:
    """Return the words of one list of `src/spezi/data/ste/`.

    Args:
        name: The file name.

    Returns:
        The words of the file, in their order.
    """
    return tuple(resources.files("spezi").joinpath("data", "ste", name).read_text("utf-8").split())


@cache
def _groups() -> tuple[tuple[str, ...], ...]:
    """Return the groups of verbs with one meaning, one group for each line of `verbs.txt`."""
    return tuple(
        tuple(line.split())
        for line in resources.files("spezi")
        .joinpath("data", "ste", "verbs.txt")
        .read_text("utf-8")
        .splitlines()
        if line.strip()
    )


@cache
def _passive() -> re.Pattern[str]:
    """Return the pattern of a possible passive voice, as in the reference linter."""
    return re.compile(
        r"\b(?:is|are|was|were|been|being)\s+(?:\w+ed|"
        + "|".join(_words("participles.txt"))
        + r")\b(?!\s+(?:to|for|by)\s+\w+ing)",
        re.IGNORECASE,
    )


def _mask(text: str) -> str:
    """Return a line with inline code, link targets and inline HTML replaced by spaces.

    Args:
        text: The line.

    Returns:
        The line with the same length.
    """
    return reduce(
        lambda acc, pattern: pattern.sub(lambda m: " " * len(m.group(0)), acc),
        (INLINE_CODE, LINK_TARGET, HTML),
        text,
    )


def _close(state: State) -> State:
    """Return the state with the open text added to the finished texts.

    Args:
        state: The state.

    Returns:
        The new state.
    """
    return State((*state.texts, state.current) if state.current else state.texts, (), state.fence)


def _cells(line: int, text: str) -> tuple[tuple[Piece, ...], ...]:
    """Return each cell of a table row as a separate text.

    Args:
        line: The line in the body.
        text: The row.

    Returns:
        One text for each cell that is not empty.
    """
    return tuple(
        (Piece(line, cell),) for cell in _mask(text).strip().strip("|").split("|") if cell.strip()
    )


def _step(state: State, numbered: tuple[int, str]) -> State:
    """Read one line of the body.

    Args:
        state: The state before the line.
        numbered: The line number and the line.

    Returns:
        The state after the line.
    """
    line, text = numbered
    fence = FENCE.match(text)
    match state.fence, fence, text:
        case "", None, _ if not text.strip() or HEADING.match(text):
            return _close(state)
        case "", None, _ if TABLE_RULE.match(text) and "-" in text:
            return _close(state)
        case "", None, _ if text.lstrip().startswith("|"):
            closed = _close(state)
            return State((*closed.texts, *_cells(line, text)), (), "")
        case "", None, _ if LIST_ITEM.match(text):
            closed = _close(state)
            return State(closed.texts, (Piece(line, _mask(LIST_ITEM.sub("", text, 1))),), "")
        case "", None, _:
            return State(state.texts, (*state.current, Piece(line, _mask(text))), "")
        case "", _, _:
            return State(_close(state).texts, (), fence.group(1)[0] * 3 if fence else "")
        case open_fence, _, _ if text.strip().startswith(open_fence):
            return State(state.texts, (), "")
        case _:
            return state


def texts(body: str) -> tuple[tuple[Piece, ...], ...]:
    """Return the prose texts of a body: paragraphs, list items and table cells (spec 000093).

    Args:
        body: The Markdown body.

    Returns:
        Each text as its lines.
    """
    return _close(reduce(_step, enumerate(body.splitlines(), 1), State())).texts


def _ends(token: str, following: str) -> bool:
    """Tell if a token ends a sentence.

    Args:
        token: The token.
        following: The next token.

    Returns:
        True when the token ends in `.`, `!` or `?` and is no abbreviation of the list.
    """
    end = SENTENCE_END.search(token)
    core = token[: end.start() + 1].lstrip(OPENERS) if end else ""
    return bool(
        end
        and core.lower() not in _words("abbreviations.txt")
        and not (DOTTED.fullmatch(core) and not following.lstrip(OPENERS)[:1].isupper())
    )


def sentences(text: tuple[Piece, ...]) -> tuple[Sentence, ...]:
    """Return the sentences of one text, each with the line where it starts.

    Args:
        text: The lines of the text.

    Returns:
        The sentences.
    """
    tokens = tuple((piece.line, m.group(0)) for piece in text for m in TOKEN.finditer(piece.text))
    starts = (
        0,
        *(
            i + 1
            for i, ((_, token), (_, following)) in enumerate(zip(tokens, tokens[1:], strict=False))
            if _ends(token, following)
        ),
    )
    return tuple(
        Sentence(tokens[start][0], " ".join(token for _, token in tokens[start:end]))
        for start, end in zip(starts, (*starts[1:], len(tokens)), strict=True)
        if start < len(tokens)
    )


def _count(text: str) -> int:
    """Return the count of words of a text: tokens with a letter or a digit.

    Args:
        text: The text.

    Returns:
        The count.
    """
    return sum(1 for token in text.split() if WORD_CHAR.search(token))


def _sentence_findings(sentence: Sentence) -> Iterable[Finding]:
    """Return the findings of one sentence.

    Args:
        sentence: The sentence.

    Returns:
        The error for its length and the warnings for passive voice and instructions.
    """
    count = _count(sentence.text)
    signals = len(SIGNAL.findall(sentence.text))
    return (
        *(
            (Finding(sentence.line, f"a sentence has {count} words, more than 25 (000093)", False),)
            if count > MAX_WORDS
            else ()
        ),
        *(
            Finding(sentence.line, f"possible passive voice: '{m.group(0)}' (000093)", True)
            for m in _passive().finditer(sentence.text)
        ),
        *(
            (Finding(sentence.line, f"a sentence has {signals} instructions (000093)", True),)
            if signals > 1
            else ()
        ),
    )


def _first(all_sentences: tuple[Sentence, ...], verb: str) -> tuple[int, int, str] | None:
    """Return the first place of a verb of a group of synonyms.

    Args:
        all_sentences: The sentences of the spec, in their order.
        verb: The base form of the verb.

    Returns:
        The index of the sentence, the line and the verb as written, or None.
    """
    pattern = re.compile(rf"\b{verb}(?:s|es|ed|d|ing)?\b", re.IGNORECASE)
    return next(
        (
            (i, s.line, m.group(0))
            for i, s in enumerate(all_sentences)
            for m in (pattern.search(s.text),)
            if m
        ),
        None,
    )


def _synonym_findings(all_sentences: tuple[Sentence, ...]) -> Iterable[Finding]:
    """Return a warning for each verb of a group after the first verb of the group in the spec.

    Args:
        all_sentences: The sentences of the spec, in their order.

    Returns:
        The warnings.
    """
    return (
        Finding(
            line,
            f"one word for one thing: '{written}' and '{places[0][2]}' have one meaning (000093)",
            True,
        )
        for group in _groups()
        for places in (sorted(p for p in (_first(all_sentences, v) for v in group) if p),)
        for _, line, written in places[1:]
    )


def findings(body: str) -> tuple[Finding, ...]:
    """Return the errors and the warnings of the rules of ASD-STE100 for one body (spec 000093).

    Args:
        body: The Markdown body of a spec.

    Returns:
        The findings, the errors first, each group in the order of the lines.
    """
    all_sentences = tuple(s for text in texts(body) for s in sentences(text))
    found = (
        *(f for s in all_sentences for f in _sentence_findings(s)),
        *_synonym_findings(all_sentences),
    )
    return tuple(sorted(found, key=lambda f: (f.warning, f.line)))
