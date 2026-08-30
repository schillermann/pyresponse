"""Unmatched branch domain entity."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.route_not_found import RouteNotFoundError
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Unmatched(Endpoint):
    """Domain entity representing an unmatched branch that fails fast when invoked."""

    def matched(self) -> bool:
        return False

    async def route(self, request: Request) -> Endpoint:
        return self

    async def response(self, request: Request) -> Response:
        path = await request.path()
        method = await request.method()
        raise RouteNotFoundError(path, method)


UnmatchedEndpoint = Unmatched
UnmatchedResource = Unmatched
