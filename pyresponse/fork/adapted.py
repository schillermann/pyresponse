"""Adapter converting callables, responses, or forks into standard Endpoints."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.callable import Callable
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fixed import Fixed
from pyresponse.fork.fork import Fork
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Adapted(Endpoint):
    """Decorator converting raw callables, responses, or forks into standard Endpoints."""

    def __init__(self, origin: Endpoint | Fork | Response | TypingCallable[[Request], Any] | Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        if isinstance(self._origin, Endpoint):
            return self._origin.matched()
        return True

    def value(self) -> Endpoint:
        """Resolve origin into an Endpoint instance."""
        if isinstance(self._origin, Endpoint):
            return self._origin
        if isinstance(self._origin, Response):
            return Fixed(self._origin)
        if callable(self._origin):
            return Callable(self._origin)
        return self._origin

    async def route(self, request: Request) -> Endpoint:
        if isinstance(self._origin, Fork):
            return await self._origin.route(request)
        return self.value()

    async def response(self, request: Request) -> Any:
        res = self.value().response(request)
        if inspect.isawaitable(res):
            res = await res
        return res
