"""Help command for pyresponse CLI."""

from typing import Sequence
from pyresponse.cli.command import CliCommand


class HelpCommand:
    """Displays available CLI commands."""

    def __init__(self, commands: Sequence[CliCommand] = ()) -> None:
        self._commands = commands

    def name(self) -> str:
        return "help"

    def description(self) -> str:
        return "Show available commands and usage."

    def matches(self, verb: str) -> bool:
        return verb in ("help", "--help", "-h", "")

    def execute(self, args: list[str]) -> int:
        print("\nPyResponse Developer Console (Pure OOP)")
        print("───────────────────────────────────────")
        print("Available commands:\n")
        max_len = max([len(cmd.name()) for cmd in self._commands], default=8)
        for cmd in self._commands:
            print(f"  {cmd.name().ljust(max_len + 4)}{cmd.description()}")
        print()
        return 0
