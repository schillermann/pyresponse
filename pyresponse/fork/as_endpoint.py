"""Adapter converting callables or forks into standard Endpoints."""

import inspect
from typing import Any
from collections.abc import Callable as TypingCallable

from pyresponse.fork.callable import Callable as CallableEndpoint
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.request.request import Request


class AsEndpoint(Endpoint):
    """Decorator converting raw callables or forks into standard Endpoints."""

    def __init__(self, origin: Endpoint | Fork | TypingCallable[[Request], Any] | Any) -> None:
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
            return CallableEndpoint(self._origin)
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
