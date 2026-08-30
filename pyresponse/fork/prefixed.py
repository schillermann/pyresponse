"""Prefixed endpoint decorator."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.sub_path import SubPath
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Prefixed(Endpoint):
    """Endpoint decorator ensuring request sub-path is preserved when generating a response."""

    def __init__(self, origin: Endpoint, sub_path: str) -> None:
        self._origin = origin
        self._sub_path = sub_path

    def matched(self) -> bool:
        return self._origin.matched()

    async def response(self, request: Request) -> Response:
        return await self._origin.response(SubPath(request, self._sub_path))


PrefixedEndpoint = Prefixed
