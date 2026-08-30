"""Fixed response endpoint."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Fixed(Endpoint):
    """Endpoint that always responds with a predetermined fixed response."""

    def __init__(self, response: Response) -> None:
        self._response = response

    def matched(self) -> bool:
        return True

    async def response(self, request: Request) -> Response:
        return self._response
