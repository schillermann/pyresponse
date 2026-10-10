"""Standard CLI Application composition in Pure OOP."""

from pyresponse.cli.app_commands import AppCommands
from pyresponse.cli.arguments import Arguments
from pyresponse.cli.command import CliCommand
from pyresponse.cli.exit_code import ExitCode
from pyresponse.cli.fork import ForkCli
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.output import ConsoleOutput, Output


class CliApp:
    """Composite CLI application runner in Pure OOP."""

    def __init__(
        self,
        *commands: CliCommand,
        app_target: str = "main:app",
        output: Output = ConsoleOutput(),
    ) -> None:
        self._commands = commands
        self._app_target = app_target
        self._output = output

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        all_cmds = AppCommands(self._commands, self._app_target, self._output).commands()
        help_cmd = HelpCommand(all_cmds, output=self._output)
        return ForkCli(all_cmds, fallback=help_cmd, output=self._output).execute(args)
