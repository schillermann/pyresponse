"""Prefix endpoint decorator in Pure OOP."""

from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.fork.sub_path import SubPath
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class PrefixEndpoint(Envelope):
    """Endpoint decorator ensuring request sub-path is preserved when generating a response."""

    def __init__(self, origin: Endpoint, sub_path: str) -> None:
        super().__init__(origin)
        self._sub_path = sub_path

    async def response(self, request: Request) -> Response:
        return await self._origin.response(SubPath(request, self._sub_path))


