"""Fake Endpoint and Fork implementation for testing."""

from pyresponse.fork.fork import Endpoint, Fork
from pyresponse.request.request import Request
from pyresponse.response.no_content import NoContent
from pyresponse.response.response import Response


class Fake(Endpoint, Fork):
    """Fake Endpoint and Fork for testing."""

    def __init__(self, response: Response = NoContent(status=200), matched: bool = True) -> None:
        self._response = response
        self._matched = matched

    def matched(self) -> bool:
        return self._matched

    async def route(self, request: Request) -> Endpoint:
        return self

    async def response(self, request: Request) -> Response:
        return self._response
