"""Endpoint decorator attaching extracted parameters."""

from typing import Mapping

from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.request.with_params import WithParams as RequestWithParams
from pyresponse.response.response import Response


class WithParams(Endpoint):
    """Endpoint decorator enriching the request with extracted path parameters."""

    def __init__(self, origin: Endpoint, params: Mapping[str, str]) -> None:
        self._origin = origin
        self._params = params

    def matched(self) -> bool:
        return self._origin.matched()

    async def response(self, request: Request) -> Response:
        return await self._origin.response(RequestWithParams(request, dict(self._params)))

