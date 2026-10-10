"""Base fork envelope decorator in Pure OOP."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class ForkEnvelope(Fork):
    """Base class for Fork decorators implementing the envelope pattern."""

    def __init__(self, origin: Fork) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return self._origin.matched()

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        return EndpointRoutes(self._origin).routes(prefix)

    async def route(self, request: Request) -> Endpoint:
        return await self._origin.route(request)

    async def response(self, request: Request) -> Response:
        res = await self.route(request)
        if res.matched():
            return await res.response(request)
        return await self._origin.response(request)
