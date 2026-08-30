"""HTTP Method routing fork."""

from typing import Any, Callable

from pyresponse.fork.as_endpoint import AsEndpoint
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.unmatched import UnmatchedEndpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


class Method(Fork):
    """Route fork matching HTTP request method (and optional path)."""

    def __init__(
        self,
        method_or_endpoint: str | Endpoint | Fork | Callable[..., Any],
        endpoint: Endpoint | Fork | Callable[..., Any] | None = None,
    ) -> None:
        self._method_or_endpoint = method_or_endpoint
        self._endpoint = endpoint

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        req_method = await request.method()

        target_method = getattr(self, "METHOD", None)
        if target_method is not None:
            if req_method.upper() != target_method.upper():
                return UnmatchedEndpoint()
            if self._endpoint is None:
                return await AsEndpoint(self._method_or_endpoint).route(request)
            req_path = await request.path()
            if req_path != self._method_or_endpoint:
                return UnmatchedEndpoint()
            return await AsEndpoint(self._endpoint).route(request)

        if isinstance(self._method_or_endpoint, str):
            if req_method.upper() != self._method_or_endpoint.upper():
                return UnmatchedEndpoint()
            if self._endpoint is not None:
                return await AsEndpoint(self._endpoint).route(request)
            return UnmatchedEndpoint()

        return await AsEndpoint(self._method_or_endpoint).route(request)

    async def response(self, request: Request) -> Response:
        matched = await self.route(request)
        if matched.matched():
            return await matched.response(request)
        return NotFound(Text("Not Found"))
