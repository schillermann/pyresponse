"""CLI command contract and Null object in Pure OOP."""

from typing import Protocol

from pyresponse.cli.arguments import Arguments
from pyresponse.cli.exit_code import ExitCode, Failure
from pyresponse.cli.output import ConsoleOutput, Output


class CliCommand(Protocol):
    """Contract for an autonomous CLI command."""

    def name(self) -> str: ...

    def description(self) -> str: ...

    def matches(self, verb: str) -> bool: ...

    def execute(self, args: Arguments) -> ExitCode: ...


class CommandEnvelope(CliCommand):
    """Base class for CLI command decorators implementing the envelope pattern."""

    def __init__(self, origin: CliCommand) -> None:
        self._origin = origin

    def name(self) -> str:
        return self._origin.name()

    def description(self) -> str:
        return self._origin.description()

    def matches(self, verb: str) -> bool:
        return self._origin.matches(verb)

    def execute(self, args: Arguments) -> ExitCode:
        return self._origin.execute(args)


class UnknownCommand:
    """Null object fallback for unrecognized CLI verbs."""

    def __init__(self, verb: str, output: Output = ConsoleOutput()) -> None:
        self._verb = verb
        self._output = output

    def name(self) -> str:
        return self._verb

    def description(self) -> str:
        return ""

    def matches(self, verb: str) -> bool:
        return False

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        self._output.error(f"Unknown command: '{self._verb}'. Run 'pyresponse help' for available commands.")
        return Failure(1)
