"""Trap endpoint decorator executing exception handlers in Pure OOP."""

import inspect
from collections.abc import Callable as TypingCallable
from types import MappingProxyType
from typing import Any, Mapping

from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Rethrow:
    """Fallback exception handler re-raising caught exceptions."""

    def __call__(self, exc: Exception, _request: Request) -> Any:
        raise exc


class TrapEndpoint(Envelope):
    """Endpoint decorator catching domain exceptions and delegating to registered handlers."""

    def __init__(
        self,
        origin: Endpoint,
        traps: Mapping[type[Exception], TypingCallable[[Exception, Request], Any]] = MappingProxyType({}),
        fallback: TypingCallable[[Exception, Request], Any] = Rethrow(),
    ) -> None:
        super().__init__(origin)
        self._traps = traps
        self._fallback = fallback

    async def response(self, request: Request) -> Response:
        try:
            return await self._origin.response(request)
        except Exception as exc:
            for exc_type, handler in self._traps.items():
                if isinstance(exc, exc_type):
                    result = handler(exc, request)
                    if inspect.isawaitable(result):
                        result = await result
                    return result
            result = self._fallback(exc, request)
            if inspect.isawaitable(result):
                result = await result
            return result


