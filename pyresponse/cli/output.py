"""Output abstraction for CLI commands in Pure OOP."""

import sys
from typing import Protocol


class Output(Protocol):
    """Protocol for command text output."""

    def print(self, message: str) -> None:
        """Output a regular message."""
        ...

    def error(self, message: str) -> None:
        """Output an error message."""
        ...


class ConsoleOutput:
    """Standard console output using sys.stdout and sys.stderr."""

    def print(self, message: str) -> None:
        print(message)

    def error(self, message: str) -> None:
        print(message, file=sys.stderr)


class MemoryOutput:
    """In-memory output collector for testing without global side effects."""

    def __init__(self) -> None:
        self._messages: list[str] = []
        self._errors: list[str] = []

    def print(self, message: str) -> None:
        self._messages.append(message)

    def error(self, message: str) -> None:
        self._errors.append(message)

    def stdout(self) -> str:
        return "\n".join(self._messages)

    def stderr(self) -> str:
        return "\n".join(self._errors)


class Envelope(Output):
    """Base class for Output decorators implementing the envelope pattern."""

    def __init__(self, origin: Output) -> None:
        self._origin = origin

    def print(self, message: str) -> None:
        self._origin.print(message)

    def error(self, message: str) -> None:
        self._origin.error(message)


class PrefixedOutput(Envelope):
    """Output decorator prepending a prefix to all messages and errors."""

    def __init__(self, origin: Output, prefix: str) -> None:
        self._origin = origin
        self._prefix = prefix

    def print(self, message: str) -> None:
        self._origin.print(f"{self._prefix}{message}")

    def error(self, message: str) -> None:
        self._origin.error(f"{self._prefix}{message}")


class SilentOutput:
    """Null-object output suppressing all print and error calls."""

    def print(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass


class ColorOutput(Envelope):
    """Output decorator applying ANSI color escape codes (green for print, red for error)."""

    def print(self, message: str) -> None:
        self._origin.print(f"\033[32m{message}\033[0m")

    def error(self, message: str) -> None:
        self._origin.error(f"\033[31m{message}\033[0m")


