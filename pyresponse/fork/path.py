"""Exact path matching fork in Pure OOP."""

from typing import Any, Callable

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.request.request import Request


class Path(Fork):
    """Route fork matching exact request URI path."""

    def __init__(self, path: str, endpoint: Endpoint | Callable[[Request], Any]) -> None:
        self._path = path
        self._endpoint = endpoint

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries for this path."""
        combined = f"{prefix.rstrip('/')}/{self._path.lstrip('/')}"
        return EndpointRoutes(self._endpoint).routes(combined)

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        if path == self._path:
            return await SourceEndpoint(self._endpoint).route(request)
        return MissingEndpoint()
