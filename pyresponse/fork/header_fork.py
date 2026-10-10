"""HTTP Header routing fork in Pure OOP."""

from typing import Any, Callable

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.request.header import Header as RequestHeader
from pyresponse.request.request import Request


class HeaderFork(Fork):
    """Route fork matching a specific HTTP header and value (e.g. for API versioning)."""

    def __init__(
        self,
        name: str,
        value: str,
        origin: Endpoint | Fork | Callable[[Request], Any],
    ) -> None:
        self._header_name = name
        self._expected_value = value
        self._origin = origin

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        return EndpointRoutes(self._origin).routes(prefix)

    async def route(self, request: Request) -> Endpoint:
        header = RequestHeader(request, self._header_name)
        if not await header.has():
            return MissingEndpoint()
        if await header.value() == self._expected_value:
            return await SourceEndpoint(self._origin).route(request)
        return MissingEndpoint()
