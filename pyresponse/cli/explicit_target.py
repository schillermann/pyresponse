"""Explicit target implementation in Pure OOP."""

import importlib
from typing import Any, Sequence

from pyresponse.cli.coordinate import Coordinate
from pyresponse.error import Error
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry


class TargetNotFound(Error):
    """Raised when an application target cannot be found or loaded."""

    pass


class ExplicitTarget:
    """Explicitly specified module:attribute target."""

    def __init__(self, coordinate: Coordinate) -> None:
        self._coordinate = coordinate

    def name(self) -> str:
        return str(self._coordinate)

    def load(self) -> Any:
        mod_name = self._coordinate.module_name()
        attr_name = self._coordinate.attribute_name()

        try:
            module = importlib.import_module(mod_name)
        except ImportError as exc:
            raise TargetNotFound(f"Cannot import module '{mod_name}': {exc}") from exc

        if not hasattr(module, attr_name):
            raise TargetNotFound(f"Module '{mod_name}' has no attribute '{attr_name}'")

        return getattr(module, attr_name)

    def routes(self) -> Sequence[RouteEntry]:
        return EndpointRoutes(self.load()).routes()
