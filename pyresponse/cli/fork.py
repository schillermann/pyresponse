"""CLI command router in Pure OOP."""

from typing import Sequence
from pyresponse.cli.command import CliCommand, UnknownCommand
from pyresponse.cli.help import HelpCommand


class ForkCli:
    """Dispatches CLI verbs to matching commands without procedural branching."""

    def __init__(
        self,
        commands: Sequence[CliCommand],
        fallback: CliCommand = HelpCommand(),
    ) -> None:
        self._commands = commands
        self._fallback = fallback

    def execute(self, args: list[str]) -> int:
        if not args:
            return self._fallback.execute(args)
        verb = args[0]
        rest = args[1:]
        for command in self._commands:
            if command.matches(verb):
                return command.execute(rest)
        return UnknownCommand(verb).execute(rest)
