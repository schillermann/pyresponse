"""HTTP Method routing fork."""

from typing import Any, Callable

from pyresponse.fork.adapted import Adapted
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.unmatched import Unmatched
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
        method_name = getattr(self, "METHOD", self._method_or_endpoint if isinstance(self._method_or_endpoint, str) and self._endpoint is not None else "")
        target_endpoint = self._endpoint if self._endpoint is not None else self._method_or_endpoint
        path_filter = self._method_or_endpoint if self._endpoint is not None and getattr(self, "METHOD", None) is not None else ""

        if method_name and req_method.upper() != method_name.upper():
            return Unmatched()

        if path_filter:
            req_path = await request.path()
            if req_path != path_filter:
                return Unmatched()

        return await Adapted(target_endpoint).route(request)




    async def response(self, request: Request) -> Response:
        matched = await self.route(request)
        if matched.matched():
            return await matched.response(request)
        return NotFound(Text("Not Found"))
