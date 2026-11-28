"""The questions of `init`, `add`, `update` and `configure` (spec 000085).

On a terminal the commands ask with questionary. Without a terminal, with `--yes` or with
`--json`, each question takes its proposal, and a question with a risk stops the command.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import questionary

from spezi.view import console


class Cancelled(Exception):
    """The user ended a command without a change."""


class Stop(Exception):
    """A question with a risk has no answer without a terminal."""


type Check = Callable[[str], str | None]


class Ask(Protocol):
    """Ask the user, or take the proposals."""

    @property
    def interactive(self) -> bool:
        """Return True when the user answers the questions."""
        ...

    def show(self, text: str) -> None:
        """Show a text, for example a summary or a diff.

        Args:
            text: The text.
        """
        ...

    def select(self, message: str, choices: tuple[str, ...], default: str | None) -> str:
        """Return one of the choices.

        Args:
            message: The question.
            choices: The choices.
            default: The proposal, or None when there is none.
        """
        ...

    def checkbox(self, message: str, choices: tuple[tuple[str, bool], ...]) -> tuple[str, ...]:
        """Return the checked choices.

        Args:
            message: The question.
            choices: Each choice and True when it is checked at the start.
        """
        ...

    def confirm(self, message: str, default: bool, risk: str | None = None) -> bool:
        """Return the answer to a yes-or-no question.

        Args:
            message: The question.
            default: The proposal.
            risk: Why the question has a risk, or None. Without a terminal it stops the command.
        """
        ...

    def text(self, message: str, default: str, check: Check | None = None) -> str:
        """Return a text.

        Args:
            message: The question.
            default: The proposal.
            check: Returns an error for a bad text, else None.
        """
        ...


def _answer[T](value: T | None) -> T:
    """Return the answer of questionary, or stop after Ctrl+C.

    Args:
        value: The answer, or None after Ctrl+C.

    Returns:
        The answer.

    Raises:
        Cancelled: The user pressed Ctrl+C.
    """
    if value is None:
        raise Cancelled("cancelled; no file changed")
    return value


@dataclass(frozen=True, slots=True)
class Questions:
    """Ask the user on the terminal with questionary."""

    @property
    def interactive(self) -> bool:
        """Return True."""
        return True

    def show(self, text: str) -> None:
        """Print a text.

        Args:
            text: The text.
        """
        console().print(text, markup=False, highlight=False)

    def select(self, message: str, choices: tuple[str, ...], default: str | None) -> str:
        """Ask for one of the choices.

        Args:
            message: The question.
            choices: The choices.
            default: The proposal, or None.

        Returns:
            The choice.
        """
        return _answer(
            questionary.select(
                message, choices=list(choices), default=default if default in choices else None
            ).ask()
        )

    def checkbox(self, message: str, choices: tuple[tuple[str, bool], ...]) -> tuple[str, ...]:
        """Ask for the checked choices.

        Args:
            message: The question.
            choices: Each choice and True when it is checked at the start.

        Returns:
            The checked choices.
        """
        return tuple(
            _answer(
                questionary.checkbox(
                    message,
                    choices=[questionary.Choice(name, checked=on) for name, on in choices],
                ).ask()
            )
        )

    def confirm(self, message: str, default: bool, risk: str | None = None) -> bool:
        """Ask a yes-or-no question.

        Args:
            message: The question.
            default: The proposal.
            risk: Why the question has a risk, or None.

        Returns:
            The answer.
        """
        del risk
        return _answer(questionary.confirm(message, default=default).ask())

    def text(self, message: str, default: str, check: Check | None = None) -> str:
        """Ask for a text.

        Args:
            message: The question.
            default: The proposal.
            check: Returns an error for a bad text, else None.

        Returns:
            The text.
        """
        return _answer(
            questionary.text(
                message,
                default=default,
                validate=(lambda t: check(t) or True) if check else None,
            ).ask()
        )


@dataclass(frozen=True, slots=True)
class Proposals:
    """Take the proposal of each question, and stop at a question with a risk."""

    @property
    def interactive(self) -> bool:
        """Return False."""
        return False

    def show(self, text: str) -> None:
        """Show nothing.

        Args:
            text: The text.
        """
        del text

    def select(self, message: str, choices: tuple[str, ...], default: str | None) -> str:
        """Return the proposal.

        Args:
            message: The question.
            choices: The choices.
            default: The proposal, or None.

        Returns:
            The proposal.

        Raises:
            Stop: The question has no proposal.
        """
        if default is None:
            raise Stop(f"{message.rstrip('?')}: no proposal; give the value as an argument")
        return default

    def checkbox(self, message: str, choices: tuple[tuple[str, bool], ...]) -> tuple[str, ...]:
        """Return the choices that are checked at the start.

        Args:
            message: The question.
            choices: Each choice and True when it is checked at the start.

        Returns:
            The checked choices.
        """
        del message
        return tuple(name for name, on in choices if on)

    def confirm(self, message: str, default: bool, risk: str | None = None) -> bool:
        """Return the proposal, or stop for a question with a risk.

        Args:
            message: The question.
            default: The proposal.
            risk: Why the question has a risk, or None.

        Returns:
            The proposal.

        Raises:
            Stop: The question has a risk.
        """
        del message
        if risk is not None:
            raise Stop(f"{risk}; run the command on a terminal without --yes")
        return default

    def text(self, message: str, default: str, check: Check | None = None) -> str:
        """Return the proposal.

        Args:
            message: The question.
            default: The proposal.
            check: Returns an error for a bad text, else None.

        Returns:
            The proposal.

        Raises:
            Stop: The proposal is not valid.
        """
        error = check(default) if check else None
        if error is not None:
            raise Stop(f"{message.rstrip('?')}: {error}")
        return default


def asker(*, yes: bool, json: bool) -> Ask:
    """Return the questions on a terminal, else the proposals.

    Args:
        yes: True for `--yes`.
        json: True for `--json`.

    Returns:
        The questions when stdin and stdout are a terminal and neither flag is given.
    """
    terminal = sys.stdin.isatty() and sys.stdout.isatty()
    return Questions() if terminal and not yes and not json else Proposals()
