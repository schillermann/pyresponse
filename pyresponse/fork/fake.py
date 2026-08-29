"""Fake Endpoint implementation for testing."""

from pyresponse.fork.fork import Endpoint
from pyresponse.request.request import Request
from pyresponse.response.no_content import NoContent
from pyresponse.response.response import Response


class Fake(Endpoint):
    """Fake Endpoint for testing."""

    def __init__(self, response: Response | None = None, matched: bool = True) -> None:
        self._response = response if response is not None else NoContent(status=200)
        self._matched = matched

    def is_matched(self) -> bool:
        return self._matched

    async def response(self, request: Request) -> Response:
        return self._response
