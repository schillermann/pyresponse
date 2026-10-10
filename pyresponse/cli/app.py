"""Standard CLI Application composition in Pure OOP."""

from typing import Sequence
from pyresponse.cli.command import CliCommand
from pyresponse.cli.fork import ForkCli
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.serve import ServeCommand
from pyresponse.cli.routes import RoutesCommand
from pyresponse.cli.discovered import DiscoveredCommands


class CliApp:
    """Standard composite CLI runner."""

    def __init__(
        self,
        *commands: CliCommand,
        app_target: str = "main:app",
    ) -> None:
        self._commands = commands
        self._app_target = app_target

    def execute(self, args: list[str]) -> int:
        discovered = DiscoveredCommands().commands()
        all_commands: list[CliCommand] = list(self._commands)
        all_commands.extend(discovered)

        # Built-in fallback commands
        if not any(c.matches("routes") for c in all_commands):
            all_commands.append(RoutesCommand())

        if not any(c.matches("serve") for c in all_commands):
            all_commands.append(ServeCommand(self._app_target))

        help_cmd = HelpCommand(all_commands)
        if not any(c.matches("help") for c in all_commands):
            all_commands.append(help_cmd)

        return ForkCli(all_commands, fallback=help_cmd).execute(args)
