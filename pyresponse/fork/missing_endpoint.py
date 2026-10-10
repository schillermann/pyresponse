"""MissingEndpoint returning 404 or raising RouteNotFound in Pure OOP."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.route_not_found import RouteNotFound
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class MissingEndpoint(Endpoint):
    """Fallback endpoint when no fork matches."""

    def matched(self) -> bool:
        return False

    async def response(self, request: Request) -> Response:
        path = await request.path()
        method = await request.method()
        raise RouteNotFound(path, method)

