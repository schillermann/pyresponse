"""HTTP Method routing fork in Pure OOP."""

from typing import Any
from pyresponse.fork.empty_fork import EmptyFork
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.path import Path
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.request.request import Request


class Method(Fork):
    """Route fork matching HTTP request method."""

    def __init__(self, method: str, origin: Any = EmptyFork()) -> None:
        self._method = method.upper()
        self._origin = origin

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries for this HTTP method."""
        sub_routes = EndpointRoutes(self._origin).routes(prefix)
        return tuple(
            RouteEntry(self._method, r.path(), r.handler())
            for r in sub_routes
        )

    async def route(self, request: Request) -> Endpoint:
        """Route request by matching method."""
        req_method = await request.method()
        if req_method.upper() != self._method:
            return MissingEndpoint()

        return await SourceEndpoint(self._origin).route(request)

