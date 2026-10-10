"""Optional entry-point command discovery in Pure OOP."""

from importlib.metadata import entry_points
from typing import Any, Sequence
from pyresponse.cli.command import CliCommand


class DiscoveredCommands:
    """Discovers third-party commands registered via package entry points."""

    def __init__(self, group: str = "pyresponse.commands") -> None:
        self._group = group

    def commands(self) -> Sequence[CliCommand]:
        discovered: list[CliCommand] = []
        eps = entry_points(group=self._group)
        for ep in eps:
            loaded = ep.load()
            cmd: Any = loaded() if callable(loaded) else loaded
            if hasattr(cmd, "matches") and hasattr(cmd, "execute"):
                discovered.append(cmd)
        return tuple(discovered)
