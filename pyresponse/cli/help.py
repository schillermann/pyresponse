"""Help command for pyresponse CLI in Pure OOP."""

from collections.abc import Sequence

from pyresponse.cli.arguments import Arguments
from pyresponse.cli.command import CliCommand
from pyresponse.cli.exit_code import ExitCode, Success
from pyresponse.cli.output import ConsoleOutput, Output


class HelpCommand:
    """Displays available CLI commands."""

    def __init__(
        self,
        commands: Sequence[CliCommand] = (),
        output: Output = ConsoleOutput(),
    ) -> None:
        self._commands = commands
        self._output = output

    def name(self) -> str:
        return "help"

    def description(self) -> str:
        return "Show available commands and usage."

    def matches(self, verb: str) -> bool:
        return verb in ("help", "--help", "-h", "")

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        self._output.print("\nPyResponse Developer Console (Pure OOP)")
        self._output.print("───────────────────────────────────────")
        self._output.print("Available commands:\n")
        max_len = max([len(cmd.name()) for cmd in self._commands], default=8)
        for cmd in self._commands:
            self._output.print(f"  {cmd.name().ljust(max_len + 4)}{cmd.description()}")
        self._output.print("")
        return Success()
