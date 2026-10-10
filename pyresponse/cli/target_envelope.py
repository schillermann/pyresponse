"""Target envelope decorator in Pure OOP."""

from typing import Any, Sequence

from pyresponse.fork.route_entry import RouteEntry


class TargetEnvelope:
    """Base decorator for Target protocol implementations."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def name(self) -> str:
        return self._origin.name()

    def load(self) -> Any:
        return self._origin.load()

    def routes(self) -> Sequence[RouteEntry]:
        return self._origin.routes()
