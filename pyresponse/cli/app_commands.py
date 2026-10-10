"""Application CLI commands composition in Pure OOP."""

from collections.abc import Sequence

from pyresponse.cli.command import CliCommand
from pyresponse.cli.discovered import DiscoveredCommands
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.output import ConsoleOutput, Output
from pyresponse.cli.routes import RoutesCommand
from pyresponse.cli.serve import ServeCommand


class AppCommands:
    """Composes application commands with discovered and framework CLI commands."""

    def __init__(
        self,
        commands: Sequence[CliCommand] = (),
        app_target: str = "main:app",
        output: Output = ConsoleOutput(),
    ) -> None:
        self._commands = commands
        self._app_target = app_target
        self._output = output

    def commands(self) -> tuple[CliCommand, ...]:
        """Assemble and return all available CLI commands without imperative mutation."""
        active = tuple(self._commands) + tuple(DiscoveredCommands().commands())
        framework = (
            RoutesCommand(output=self._output),
            ServeCommand(self._app_target, output=self._output),
        )
        missing = tuple(
            cmd for cmd in framework
            if not any(c.matches(cmd.name()) for c in active)
        )
        combined = active + missing
        help_cmd = HelpCommand(combined, output=self._output)
        if not any(c.matches(help_cmd.name()) for c in combined):
            return combined + (help_cmd,)
        return combined
