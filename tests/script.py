"""A scripted user for the tests of the questions (§000085, §000086)."""

from __future__ import annotations

import os
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from specs_kit.ask import Check

PROPOSAL = object()


@dataclass
class Script:
    """Answer each question with the next answer of a list.

    Attributes:
        answers: The answers in their order. `PROPOSAL` takes the proposal of a question.
        asked: The questions in their order.
        shown: The texts that the command showed.
    """

    answers: list[object]
    asked: list[str] = field(default_factory=list)
    shown: list[str] = field(default_factory=list)

    @property
    def interactive(self) -> bool:
        """Return True."""
        return True

    def _next(self, message: str, proposal: object) -> object:
        """Return the next answer.

        Args:
            message: The question.
            proposal: The proposal of the question.

        Returns:
            The answer.
        """
        self.asked.append(message)
        assert self.answers, f"no answer for {message!r}"
        answer = self.answers.pop(0)
        return proposal if answer is PROPOSAL else answer

    def show(self, text: str) -> None:
        """Record a text.

        Args:
            text: The text.
        """
        self.shown.append(text)

    def select(self, message: str, choices: tuple[str, ...], default: str | None) -> str:
        """Return the next answer.

        Args:
            message: The question.
            choices: The choices.
            default: The proposal.

        Returns:
            The answer.
        """
        answer = self._next(message, default)
        assert answer in choices, (answer, choices)
        return str(answer)

    def checkbox(self, message: str, choices: tuple[tuple[str, bool], ...]) -> tuple[str, ...]:
        """Return the next answer.

        Args:
            message: The question.
            choices: The choices.

        Returns:
            The answer.
        """
        answer = self._next(message, tuple(name for name, on in choices if on))
        assert isinstance(answer, tuple)
        return tuple(str(a) for a in answer)

    def confirm(self, message: str, default: bool, risk: str | None = None) -> bool:
        """Return the next answer.

        Args:
            message: The question.
            default: The proposal.
            risk: The risk.

        Returns:
            The answer.
        """
        del risk
        return bool(self._next(message, default))

    def text(self, message: str, default: str, check: Check | None = None) -> str:
        """Return the next answer.

        Args:
            message: The question.
            default: The proposal.
            check: The check.

        Returns:
            The answer.
        """
        answer = str(self._next(message, default))
        assert check is None or check(answer) is None, check and check(answer)
        return answer


@contextmanager
def inside(env: Mapping[str, str], folder: Path) -> Generator[None]:
    """Run code in a folder with the environment of the kit.

    Args:
        env: The environment.
        folder: The folder.

    Yields:
        Nothing.
    """
    old_env, old_dir = dict(os.environ), Path.cwd()
    os.environ.update(env)
    os.chdir(folder)
    try:
        yield
    finally:
        os.chdir(old_dir)
        os.environ.clear()
        os.environ.update(old_env)
