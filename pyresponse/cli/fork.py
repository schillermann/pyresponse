"""CLI command router in Pure OOP."""

from collections.abc import Sequence

from pyresponse.cli.arguments import Arguments
from pyresponse.cli.command import CliCommand, UnknownCommand
from pyresponse.cli.exit_code import ExitCode
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.output import ConsoleOutput, Output


class ForkCli:
    """Dispatches CLI verbs to matching commands without procedural branching."""

    def __init__(
        self,
        commands: Sequence[CliCommand],
        fallback: CliCommand = HelpCommand(),
        output: Output = ConsoleOutput(),
    ) -> None:
        self._commands = commands
        self._fallback = fallback
        self._output = output

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        if args.empty():
            return self._fallback.execute(args)
        verb = args.first()
        rest = args.sub(1)
        for command in self._commands:
            if command.matches(verb):
                return command.execute(rest)
        return UnknownCommand(verb, self._output).execute(rest)
