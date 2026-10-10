"""PyResponse CLI package."""

from pyresponse.cli.arguments import ArgumentNotFound, Arguments, ArgumentsFrom, SysArguments
from pyresponse.cli.command import CliCommand, CommandEnvelope, UnknownCommand
from pyresponse.cli.alias import AliasCommand
from pyresponse.cli.exit_code import ExitCode, Failure, Success
from pyresponse.cli.fork import ForkCli
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.serve import ServeCommand
from pyresponse.cli.routes import (
    RoutesCommand,
    SourceRoutes,
    RoutesTable,
    TableRow,
    RouteEntry,
    Routes,
    CliRoutes,
    FixedRoutes,
)
from pyresponse.cli.output import (
    Output,
    Envelope as OutputEnvelope,
    ConsoleOutput,
    MemoryOutput,
    PrefixedOutput,
    SilentOutput,
    ColorOutput,
)

from pyresponse.cli.discovered import DiscoveredCommands
from pyresponse.cli.app_commands import AppCommands
from pyresponse.cli.app import CliApp

__all__ = [
    "Arguments",
    "ArgumentsFrom",
    "SysArguments",
    "ArgumentNotFound",
    "ExitCode",
    "Success",
    "Failure",
    "CliCommand",
    "CommandEnvelope",
    "AliasCommand",
    "UnknownCommand",
    "ForkCli",
    "HelpCommand",
    "ServeCommand",
    "RoutesCommand",
    "SourceRoutes",
    "RoutesTable",
    "TableRow",
    "RouteEntry",
    "Routes",
    "CliRoutes",
    "FixedRoutes",
    "Output",
    "OutputEnvelope",
    "ConsoleOutput",
    "MemoryOutput",
    "PrefixedOutput",
    "SilentOutput",
    "ColorOutput",
    "DiscoveredCommands",
    "AppCommands",
    "CliApp",
]
