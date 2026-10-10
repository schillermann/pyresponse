"""SourceEndpoint decorator converting callables, responses, or branches into standard Endpoints."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any, cast

from pyresponse.fork.constant_endpoint import ConstantEndpoint
from pyresponse.fork.endpoint import Branch, Endpoint
from pyresponse.fork.function_endpoint import FunctionEndpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class SourceEndpoint(Endpoint):
    """Decorator converting raw callables, responses, or branches into standard Endpoints."""

    def __init__(self, origin: Endpoint | Branch | Response | TypingCallable[[Request], Any] | Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        if isinstance(self._origin, Endpoint):
            return self._origin.matched()
        return True

    def value(self) -> Endpoint:
        """Resolve origin into an Endpoint instance."""
        if isinstance(self._origin, Endpoint):
            return self._origin
        if callable(self._origin):
            return FunctionEndpoint(self._origin)
        return cast(Endpoint, self._origin)

    async def route(self, request: Request) -> Endpoint:
        if isinstance(self._origin, Branch):
            return await self._origin.route(request)
        return self.value()

    async def response(self, request: Request) -> Response:
        res = self.value().response(request)
        if inspect.isawaitable(res):
            res = await res
        return cast(Response, res)

