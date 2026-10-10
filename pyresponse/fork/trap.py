"""Exception-trapping fork decorator for declarative error handling in Pure OOP."""

from collections.abc import Callable as TypingCallable
from types import MappingProxyType
from typing import Any, Mapping

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.fork_envelope import ForkEnvelope
from pyresponse.fork.trap_endpoint import Rethrow, TrapEndpoint
from pyresponse.request.request import Request


class Trap(ForkEnvelope):
    """Fork decorator that catches exceptions and routes them to handler callbacks."""

    def __init__(
        self,
        origin: Fork,
        traps: Mapping[type[Exception], TypingCallable[[Exception, Request], Any]] = MappingProxyType({}),
        fallback: TypingCallable[[Exception, Request], Any] = Rethrow(),
    ) -> None:
        super().__init__(origin)
        self._traps = traps
        self._fallback = fallback

    async def route(self, request: Request) -> Endpoint:
        endpoint = await self._origin.route(request)
        return TrapEndpoint(endpoint, self._traps, self._fallback)
