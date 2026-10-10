"""CORS routing fork with automatic preflight OPTIONS handling in Pure OOP."""

from collections.abc import Callable as TypingCallable
from typing import Any, Sequence

from pyresponse.fork.constant_endpoint import ConstantEndpoint
from pyresponse.fork.cors_endpoint import CorsEndpoint
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.request.request import Request
from pyresponse.response.cors import Cors as CorsResponse
from pyresponse.response.no_content import NoContent


class Cors(Fork):
    """Routing fork wrapping routes with CORS headers and preflight OPTIONS handling."""

    def __init__(
        self,
        origin: Endpoint | Fork | TypingCallable[[Request], Any],
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
        return True

    async def route(self, request: Request) -> Endpoint:
        req_method = await request.method()
        if req_method.upper() == "OPTIONS":
            preflight = CorsResponse(
                origin=NoContent(status=204),
                allow_origin=self._allow_origin,
                allow_methods=self._allow_methods,
                allow_headers=self._allow_headers,
                allow_credentials=self._allow_credentials,
                max_age=self._max_age,
            )
            return ConstantEndpoint(preflight)

        endpoint = await SourceEndpoint(self._origin).route(request)

        if endpoint.matched():
            return CorsEndpoint(
                endpoint,
                self._allow_origin,
                self._allow_methods,
                self._allow_headers,
                self._allow_credentials,
                self._max_age,
            )

        return endpoint
