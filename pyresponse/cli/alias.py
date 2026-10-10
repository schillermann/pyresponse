"""CLI command decorator adding alternative execution verb aliases in Pure OOP."""

from pyresponse.cli.command import CliCommand, CommandEnvelope


class AliasCommand(CommandEnvelope):
    """Decorator extending an autonomous CliCommand with alternative verb aliases."""

    def __init__(self, origin: CliCommand, *aliases: str) -> None:
        super().__init__(origin)
        self._aliases = aliases

    def matches(self, verb: str) -> bool:
        return self._origin.matches(verb) or verb in self._aliases
