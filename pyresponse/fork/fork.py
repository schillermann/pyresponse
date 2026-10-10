"""Composite route fork branch evaluator in Pure OOP."""

from typing import Any
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


class Fork:
    """Composite route evaluator executing child forks or endpoints in sequence."""

    def __init__(self, *branches: Any) -> None:
        self._branches = branches

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically collect route entries from all branches."""
        entries: list[RouteEntry] = []
        for branch in self._branches:
            entries.extend(EndpointRoutes(branch).routes(prefix))
        return tuple(entries)

    async def route(self, request: Request) -> Endpoint:
        """Evaluate branches in sequence and return the matching Endpoint."""
        for branch in self._branches:
            matched_endpoint = await SourceEndpoint(branch).route(request)
            if matched_endpoint.matched():
                return matched_endpoint
        return MissingEndpoint()

    async def response(self, request: Request) -> Response:
        """Act as an Endpoint by evaluating routes and rendering the response."""
        res = await self.route(request)
        if res.matched():
            return await res.response(request)
        return NotFound(Text("Not Found"))
