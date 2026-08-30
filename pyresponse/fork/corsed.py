"""CORS-decorated endpoint."""

from typing import Sequence

from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.response.cors import Cors as CorsResponse
from pyresponse.response.response import Response


class Corsed(Endpoint):
    """Endpoint decorator wrapping the response with CORS headers."""

    def __init__(
        self,
        origin: Endpoint,
        allow_origin: str = "*",
        allow_methods: Sequence[str] = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"),
        allow_headers: Sequence[str] = ("*",),
        allow_credentials: bool = False,
        max_age: int = 86400,
    ) -> None:
        self._origin = origin
        self._allow_origin = allow_origin
        self._allow_methods = allow_methods
        self._allow_headers = allow_headers
        self._allow_credentials = allow_credentials
        self._max_age = max_age

    def matched(self) -> bool:
        return self._origin.matched()

    async def response(self, request: Request) -> Response:
        res = await self._origin.response(request)
        return CorsResponse(
            origin=res,
            allow_origin=self._allow_origin,
            allow_methods=self._allow_methods,
            allow_headers=self._allow_headers,
            allow_credentials=self._allow_credentials,
            max_age=self._max_age,
        )
