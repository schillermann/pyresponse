"""CLI command contract and Null object in Pure OOP."""

from typing import Protocol


class CliCommand(Protocol):
    """Contract for an autonomous CLI command."""

    def name(self) -> str: ...

    def description(self) -> str: ...

    def matches(self, verb: str) -> bool: ...

    def execute(self, args: list[str]) -> int: ...


class UnknownCommand:
    """Null object fallback for unrecognized CLI verbs."""

    def __init__(self, verb: str) -> None:
        self._verb = verb

    def name(self) -> str:
        return self._verb

    def description(self) -> str:
        return ""

    def matches(self, verb: str) -> bool:
        return False

    def execute(self, args: list[str]) -> int:
        print(f"Unknown command: '{self._verb}'. Run 'pyresponse help' for available commands.")
        return 1
