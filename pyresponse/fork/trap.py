"""Exception-trapping fork decorator for declarative error handling in Pure OOP."""

from collections.abc import Callable as TypingCallable
from types import MappingProxyType
from typing import Any, Mapping

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.trap_endpoint import Rethrow, TrapEndpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Trap(Fork):
    """Fork decorator that catches exceptions and routes them to handler callbacks."""

    def __init__(
        self,
        origin: Endpoint | Fork,
        traps: Mapping[type[Exception], TypingCallable[[Exception, Request], Any]] = MappingProxyType({}),
        fallback: TypingCallable[[Exception, Request], Any] = Rethrow(),
    ) -> None:
        self._origin = origin
        self._traps = traps
        self._fallback = fallback

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        endpoint = await SourceEndpoint(self._origin).route(request)
        return TrapEndpoint(endpoint, self._traps, self._fallback)

    async def response(self, request: Request) -> Response:
        endpoint = await self.route(request)
        return await endpoint.response(request)
