"""HTTP Routes inspection and table formatting for pyresponse CLI in Pure OOP."""

from typing import Any, Protocol, Sequence, runtime_checkable
from pyresponse.cli.arguments import Arguments
from pyresponse.cli.exit_code import ExitCode, Failure, Success
from pyresponse.cli.output import ConsoleOutput, Output
from pyresponse.cli.target import AppTarget, TargetNotFound
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry

__all__ = [
    "RouteEntry",
    "Routes",
    "CliRoutes",
    "FixedRoutes",
    "SourceRoutes",
    "TableRow",
    "RoutesTable",
    "RoutesCommand",
]


@runtime_checkable
class Routes(Protocol):
    """Protocol representing a collection of route entries."""

    def entries(self, target_name: str = "") -> Sequence[RouteEntry]:
        """Sequence of route entries."""
        ...


class CliRoutes(Routes):
    """Routes discovered from a target name or environment/filesystem default."""

    def __init__(self, target_name: str = "") -> None:
        self._target_name = target_name

    def for_target(self, target_name: str) -> "CliRoutes":
        return CliRoutes(target_name if target_name else self._target_name)

    def entries(self, target_name: str = "") -> Sequence[RouteEntry]:
        target = target_name if target_name else self._target_name
        return AppTarget(target).routes()


class FixedRoutes(Routes):
    """Routes encapsulated within a fixed fork, endpoint, or factory."""

    def __init__(self, origin: Any, prefix: str = "") -> None:
        self._origin = origin
        self._prefix = prefix

    def entries(self, target_name: str = "") -> Sequence[RouteEntry]:
        root = self._origin() if callable(self._origin) else self._origin
        return EndpointRoutes(root).routes(self._prefix)


class SourceRoutes(Routes):
    """Polymorphic adapter resolving an arbitrary source into Routes."""

    def __init__(self, origin: Any, prefix: str = "") -> None:
        self._origin = origin
        self._prefix = prefix

    def entries(self, target_name: str = "") -> Sequence[RouteEntry]:
        try:
            return self._origin.entries(target_name)
        except AttributeError:
            return FixedRoutes(self._origin, self._prefix).entries(target_name)


class TableRow:
    """Formats a RouteEntry into a columnar table row."""

    def __init__(self, entry: RouteEntry, method_width: int, path_width: int) -> None:
        self._entry = entry
        self._method_width = method_width
        self._path_width = path_width

    def text(self) -> str:
        return (
            f"{self._entry.method().ljust(self._method_width + 2)}"
            f"{self._entry.path().ljust(self._path_width + 4)}"
            f"{self._entry.handler()}"
        )

    def __str__(self) -> str:
        return self.text()


class RoutesTable:
    """Renders route entries as a clean terminal table."""

    def __init__(self, entries: Sequence[RouteEntry]) -> None:
        self._entries = entries

    def text(self) -> str:
        if not self._entries:
            return "No routes registered.\n"

        max_method = max([len(e.method()) for e in self._entries] + [6])
        max_path = max([len(e.path()) for e in self._entries] + [4])

        lines = [
            f"\n{'METHOD'.ljust(max_method + 2)}{'PATH'.ljust(max_path + 4)}HANDLER",
            "─" * (max_method + max_path + 30),
        ]
        for e in self._entries:
            lines.append(TableRow(e, max_method, max_path).text())
        lines.append(f"\nTotal: {len(self._entries)} routes\n")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.text()


class RoutesCommand:
    """CLI command displaying registered HTTP routes."""

    def __init__(
        self,
        routes: Any = CliRoutes(),
        output: Output = ConsoleOutput(),
    ) -> None:
        self._routes = routes
        self._output = output

    def name(self) -> str:
        return "routes"

    def description(self) -> str:
        return "Inspect and list all registered HTTP routes."

    def matches(self, verb: str) -> bool:
        return verb in ("routes", "route:list")

    def execute(self, args: Arguments = Arguments()) -> ExitCode:
        has_target = not args.empty()
        target_name = args.first() if has_target else ""
        try:
            entries = (
                SourceRoutes(self._routes).entries(target_name)
                if has_target
                else SourceRoutes(self._routes).entries()
            )
            self._output.print(str(RoutesTable(entries)))
            return Success()
        except TargetNotFound as exc:
            self._output.error(f"❌ {exc}")
            self._output.error("   Specify target as argument (e.g. 'pyr routes app:app') or set PYRESPONSE_APP.")
            return Failure(1)
        except (ImportError, AttributeError) as exc:
            target_display = target_name or AppTarget(target_name).name()
            self._output.error(f"❌ Could not load application target '{target_display}': {exc}")
            self._output.error("   Specify target as argument (e.g. 'pyr routes app:app') or set PYRESPONSE_APP.")
            return Failure(1)
