"""Unmatched endpoint returning 404 or raising RouteNotFound."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.route_not_found import RouteNotFound
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Unmatched(Endpoint):
    """Fallback endpoint when no fork matches."""

    def __init__(self, path: str = "", method: str = "") -> None:
        self._path = path
        self._method = method

    def matched(self) -> bool:
        return False

    async def response(self, req: Request) -> Response:
        path = await req.path() if hasattr(req, "path") else self._path
        method = await req.method() if hasattr(req, "method") else self._method
        raise RouteNotFound(path, method)
